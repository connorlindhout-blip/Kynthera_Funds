def calculate_credit_score(metrics: dict) -> dict:
    """Generate an explainable rule-based credit score from cash-flow metrics."""
    score = 50
    drivers = []

    if metrics["revenue_stability"] >= 0.75:
        score += 15
        drivers.append(("Revenue stability", "positive", "Monthly revenue is relatively stable."))
    elif metrics["revenue_stability"] >= 0.50:
        score += 8
        drivers.append(("Revenue stability", "neutral", "Monthly revenue is moderately stable."))
    else:
        score -= 8
        drivers.append(("Revenue stability", "negative", "Monthly revenue is unstable."))

    if metrics["liquidity_buffer_months"] >= 1.5:
        score += 15
        drivers.append(("Liquidity buffer", "positive", "Average balance covers more than 1.5 months of outflows."))
    elif metrics["liquidity_buffer_months"] >= 0.75:
        score += 7
        drivers.append(("Liquidity buffer", "neutral", "Liquidity buffer is acceptable but not strong."))
    else:
        score -= 10
        drivers.append(("Liquidity buffer", "negative", "Liquidity buffer is weak."))

    if metrics["negative_balance_ratio"] == 0:
        score += 10
        drivers.append(("Negative balance days", "positive", "No negative balance days were observed."))
    elif metrics["negative_balance_ratio"] <= 0.05:
        score += 3
        drivers.append(("Negative balance days", "neutral", "Only a few negative balance days were observed."))
    else:
        score -= 12
        drivers.append(("Negative balance days", "negative", "Frequent negative balance days increase liquidity risk."))

    if metrics["cashflow_volatility"] <= 0.8:
        score += 10
        drivers.append(("Cash-flow volatility", "positive", "Net cash flow is relatively predictable."))
    elif metrics["cashflow_volatility"] <= 1.3:
        score += 2
        drivers.append(("Cash-flow volatility", "neutral", "Net cash flow shows moderate volatility."))
    else:
        score -= 10
        drivers.append(("Cash-flow volatility", "negative", "Net cash flow is highly volatile."))

    if metrics["growth_trend"] >= 0.10:
        score += 10
        drivers.append(("Growth trend", "positive", "Revenue increased over the observed period."))
    elif metrics["growth_trend"] >= -0.10:
        score += 3
        drivers.append(("Growth trend", "neutral", "Revenue trend is broadly stable."))
    else:
        score -= 8
        drivers.append(("Growth trend", "negative", "Revenue declined over the observed period."))

    score = max(0, min(100, round(score)))

    if score >= 75:
        recommendation = "Approve"
    elif score >= 55:
        recommendation = "Manual review"
    else:
        recommendation = "Reject"

    suggested_max_loan = max(0, round(metrics["avg_monthly_revenue"] * (score / 100) * 2, -2))

    return {
        "score": score,
        "recommendation": recommendation,
        "suggested_max_loan": suggested_max_loan,
        "drivers": drivers,
    }
