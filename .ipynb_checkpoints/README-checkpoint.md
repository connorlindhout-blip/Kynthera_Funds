# Kynthera Funds MVP

Kynthera Funds is a prototype cash-flow intelligence tool for SME lending.

The MVP allows a lender to upload bank transaction data, calculate cash-flow indicators, generate an explainable credit confidence score, and view a lending recommendation.

## Features

- CSV upload for SME transaction data
- Data validation and cleaning
- Cash-flow metrics
- Rule-based explainable credit score
- Lending recommendation: approve, manual review, or reject
- Driver breakdown explaining the score
- Simple Streamlit dashboard

## Required CSV Format

The uploaded CSV should contain:

```text
date, description, amount, balance, category
```

A sample file is included in `data/sample_transactions.csv`.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## MVP Scope

The current MVP uses CSV uploads to simulate transaction data access. In production, this input would be replaced with PSD2/open banking API connections.

The scoring model is intentionally rule-based for transparency. In later versions, it could be validated and improved using real repayment and default outcome data.

## Limitations

- No live PSD2 API integration yet
- No real customer authentication
- No production-grade encryption or access control
- Rule-based scoring is not yet validated on real loan outcomes
- Not intended for real lending decisions
