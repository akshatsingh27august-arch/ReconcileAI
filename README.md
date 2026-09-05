# ReconcileAI — AI Finance Controller 💰🤖

ReconcileAI is an AI-assisted finance operations system that automates the first layer of transaction reconciliation.

It processes synthetic transaction batches, measures reconciliation performance, identifies unresolved exceptions, prioritizes them by risk, and provides optional AI-assisted investigation support.

---

## 🎯 Razorpay Buildathon — Track 04: AI Finance Controller

### Problem

Finance operations teams often need to reconcile large batches of payment transactions and identify which transactions match expected settlements and which require investigation.

Manual reconciliation can make it difficult to quickly identify:

- Amount mismatches
- Missing settlements
- Duplicate transactions
- Fee mismatches
- Settlement date mismatches

More importantly, finance teams need an honest view of both successful matches and unresolved exceptions.

### Solution

ReconcileAI automates the first layer of this workflow by:

1. Processing transaction batches
2. Calculating expected settlement amounts
3. Identifying successful matches
4. Detecting unresolved exceptions
5. Detecting duplicate transaction records
6. Prioritizing exceptions by risk
7. Reporting the reconciliation match rate
8. Providing optional Gemini AI-assisted investigation
9. Keeping humans responsible for final financial decisions

---

# 📊 Current Results

ReconcileAI was tested on a synthetic dataset containing more than the required 50 records.

| Metric | Result |
|---|---:|
| Physical records processed | **104** |
| Unique transactions | **100** |
| Matched transactions | **74** |
| Match rate | **74.0%** |
| Unresolved exceptions | **26** |
| HIGH priority | **11** |
| MEDIUM priority | **11** |
| LOW priority | **4** |

The system reports unresolved exceptions honestly instead of forcing uncertain transactions into successful matches.

---

# 🔎 Exception Types

The synthetic dataset contains multiple finance-operation exception categories:

- **Amount Mismatch**
- **Missing Settlement**
- **Duplicate Transaction**
- **Fee Mismatch**
- **Date Mismatch**

Each exception is assigned a priority and recommended action.

---

# 🧠 AI Investigation

ReconcileAI uses **Gemini** as an optional investigation assistant.

The AI receives transaction evidence and provides:

- Root cause assessment
- Supporting evidence
- Recommended investigation action
- Risk level
- Human review requirement
- Confidence level

### Responsible AI Design

The AI is instructed to:

- Use only the provided transaction evidence
- Avoid inventing transaction information
- Clearly distinguish facts from inference
- Avoid making unsupported financial claims
- Recommend investigation steps rather than final financial decisions
- Escalate uncertain cases for human review

The AI is an **investigation assistant**, not the authority for financial decisions.

If the AI service is unavailable because of API quota or service limitations, the core reconciliation and prioritization pipeline continues to work.

---

# 🏗️ Architecture

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
