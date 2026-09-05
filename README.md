# ReconcileAI — AI Finance Controller 💰🤖

ReconcileAI is an AI-assisted finance operations system built for the **Razorpay Buildathon — Track 04: AI Finance Controller**.

It automates the first layer of transaction reconciliation across a synthetic transaction batch, measures reconciliation performance, identifies unresolved exceptions, prioritizes exceptions by risk, validates batch coverage, and provides optional AI-assisted investigation.

> **Design principle:** Rules authorize what can be measured. AI investigates what needs explanation. Humans remain responsible for financial decisions.

---

# 🎯 Razorpay Buildathon — Track 04

## Problem

Finance operations teams need to reconcile large batches of payment transactions and determine which transactions match expected settlements and which require investigation.

Manual reconciliation can make it difficult to quickly identify:

- Amount mismatches
- Missing settlements
- Duplicate transactions
- Fee-related discrepancies
- Settlement date mismatches

A finance controller should not only report successful matches. It should also provide an honest list of transactions that could not be confidently resolved.

---

# 💡 Solution

ReconcileAI automates the first layer of this workflow:

1. Load a transaction batch
2. Calculate expected settlement amounts
3. Reconcile transactions
4. Detect duplicate transaction IDs
5. Identify settlement-date issues
6. Surface unresolved exceptions
7. Prioritize exceptions by risk
8. Validate that the entire batch is accounted for
9. Present results through a Streamlit dashboard
10. Optionally investigate exceptions using Gemini AI
11. Keep humans responsible for final financial decisions

---

# 📊 Measured Batch Results

The current synthetic test batch contains **104 physical records representing 100 unique transactions**.

| Metric | Result |
|---|---:|
| Physical records processed | **104** |
| Unique transactions | **100** |
| Matched transactions | **74** |
| Match rate | **74.0%** |
| Exceptions | **26** |
| Batch coverage | **100.0%** |
| Unaccounted transactions | **0** |
| Duplicate IDs detected | **4** |
| Validation status | **PASS** |

### Exception Priority

| Priority | Count |
|---|---:|
| HIGH | **11** |
| MEDIUM | **11** |
| LOW | **4** |

### Financial Impact

The dashboard currently reports:

**Amount at risk: ₹31,205**

The amount-at-risk figure represents the aggregate financial difference associated with the reported exceptions.

---

# 🔎 Exception Types

The synthetic dataset contains multiple finance-operation exception categories:

- **Amount Mismatch**
- **Missing Settlement**
- **Duplicate Transaction**
- **Fee Mismatch**
- **Date Mismatch**

Each exception is surfaced for investigation and assigned a priority.

---

# 🧠 Detection & Explainability

ReconcileAI distinguishes between different ways an exception can enter the investigation pipeline.

### Rule-based detection

Some conditions can be independently established from transaction evidence.

Examples:

- **Duplicate ID Detection** — repeated transaction IDs
- **Settlement Date Rule** — settlement date inconsistent with the expected transaction timing

### Classification-based exceptions

Some synthetic exception categories are supplied by the synthetic dataset and are surfaced by the controller for investigation rather than being presented as independently proven root causes.

This distinction is intentional.

ReconcileAI does **not** claim that every synthetic label is independently discoverable from the available transaction fields.

This makes the system's reporting more transparent and avoids overstating detection accuracy.

---

# 🛡️ Batch Validation

The controller validates that every unique transaction is accounted for.

For the current batch:

```text
74 matched
+
26 exceptions
=
100 unique transactions
