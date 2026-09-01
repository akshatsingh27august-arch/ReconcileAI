# ReconcileAI

## AI Finance Controller

ReconcileAI is a financial reconciliation and exception-management system.

## What it does

- Processes transaction data
- Identifies reconciliation exceptions
- Classifies exceptions by priority
- Provides recommended actions
- Displays financial metrics
- Provides an interactive investigation dashboard
- Keeps human approval in the loop

## Current Workflow

Transactions
→ Reconciliation
→ Exception Detection
→ Investigation
→ Priority Classification
→ Finance Dashboard
→ Human Review

## Technologies

- Python
- Streamlit
- CSV
- Rule-based financial validation

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run dashboard.py

Then open:

http://localhost:8501

## Project Structure

- generate_data.py — generates transaction data
- reconciliation.py — performs reconciliation
- investigator.py — investigates exceptions
- finance_summary.py — generates financial metrics
- priority.py — assigns exception priorities
- dashboard.py — Streamlit dashboard

## Important

Financial decisions remain subject to human approval.