import pandas as pd

REQUIRED_COLUMNS = {"date", "description", "amount", "balance", "category"}

def load_transactions(file) -> pd.DataFrame:
    """Load and validate transaction data from a CSV file."""
    df = pd.read_csv(file)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce")

    df = df.dropna(subset=["date", "amount", "balance"])
    df = df.sort_values("date").reset_index(drop=True)

    return df

def calculate_cashflow_metrics(df: pd.DataFrame) -> dict:
    """Calculate credit-relevant cash-flow metrics from transaction data."""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df.groupby("month").agg(
        inflows=("amount", lambda x: x[x > 0].sum()),
        outflows=("amount", lambda x: abs(x[x < 0].sum())),
        net_cashflow=("amount", "sum"),
        avg_balance=("balance", "mean"),
    ).reset_index()

    avg_monthly_revenue = monthly["inflows"].mean()
    avg_monthly_outflows = monthly["outflows"].mean()
    avg_balance = df["balance"].mean()
    negative_balance_days = df.loc[df["balance"] < 0, "date"].dt.date.nunique()
    total_days = df["date"].dt.date.nunique()

    revenue_stability = 1 - min(monthly["inflows"].std() / avg_monthly_revenue, 1) if avg_monthly_revenue > 0 else 0
    cashflow_volatility = min(monthly["net_cashflow"].std() / max(abs(monthly["net_cashflow"].mean()), 1), 2)
    liquidity_buffer_months = avg_balance / avg_monthly_outflows if avg_monthly_outflows > 0 else 0
    negative_balance_ratio = negative_balance_days / total_days if total_days > 0 else 0

    if len(monthly) >= 2 and monthly["inflows"].iloc[0] > 0:
        growth_trend = (monthly["inflows"].iloc[-1] - monthly["inflows"].iloc[0]) / monthly["inflows"].iloc[0]
    else:
        growth_trend = 0

    return {
        "monthly": monthly,
        "avg_monthly_revenue": round(avg_monthly_revenue, 2),
        "avg_monthly_outflows": round(avg_monthly_outflows, 2),
        "avg_balance": round(avg_balance, 2),
        "negative_balance_days": int(negative_balance_days),
        "revenue_stability": round(float(revenue_stability), 3),
        "cashflow_volatility": round(float(cashflow_volatility), 3),
        "liquidity_buffer_months": round(float(liquidity_buffer_months), 3),
        "negative_balance_ratio": round(float(negative_balance_ratio), 3),
        "growth_trend": round(float(growth_trend), 3),
    }
