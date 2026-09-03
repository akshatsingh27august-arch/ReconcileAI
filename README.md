# ReconcileAI — AI Finance Controller

ReconcileAI is an AI-assisted finance operations system that automates transaction reconciliation, detects exceptions, prioritizes financial risks, and provides evidence-based AI investigation support.

## 🎯 Razorpay Buildathon — AI Finance Controller

### Problem

Finance teams often reconcile large batches of payment transactions manually. This can make it difficult to quickly identify:

- Amount mismatches
- Missing settlements
- Duplicate transactions
- Fee mismatches
- Settlement date mismatches

ReconcileAI automates the first layer of this finance-operations workflow.

## 🚀 What ReconcileAI Does

ReconcileAI processes a synthetic batch of **100 unique transactions / 104 physical records** and:

1. Reconciles transaction amounts.
2. Detects duplicate transaction records.
3. Identifies unresolved exceptions.
4. Calculates the reconciliation match rate.
5. Prioritizes exceptions by financial risk.
6. Provides optional Gemini AI-assisted investigation.
7. Keeps human review in the loop for financial decisions.

## 📊 Current Results

| Metric | Result |
|---|---:|
| Physical records processed | 104 |
| Unique transactions | 100 |
| Matched transactions | 74 |
| Match rate | **74.0%** |
| Exceptions | 26 |
| HIGH priority | 11 |
| MEDIUM priority | 11 |
| LOW priority | 4 |

The system reports unresolved exceptions honestly instead of forcing uncertain transactions into a match.

## 🔎 Exception Types

The synthetic dataset contains:

- Amount Mismatch
- Missing Settlement
- Duplicate Transaction
- Fee Mismatch
- Date Mismatch

## 🧠 AI Investigation

Gemini is used as an **investigation assistant**, not as the authority for financial decisions.

The AI receives transaction evidence and returns:

- Root cause assessment
- Supporting evidence
- Recommended investigation action
- Risk level
- Human review requirement
- Confidence level

The system instructs the AI not to invent transaction information or make final financial decisions.

If AI investigation is unavailable because of API quota or service limitations, the core reconciliation and prioritization pipeline continues to work.

## 🏗️ Architecture

```text
Synthetic Transaction Data
          ↓
     Reconciliation
          ↓
   Match / Exception
          ↓
 Exception Prioritization
          ↓
   Finance Dashboard
          ↓
 AI Investigation (Optional)
          ↓
 Evidence + Recommendation
          ↓
     Human Review
