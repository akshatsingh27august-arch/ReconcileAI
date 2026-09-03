import csv
import streamlit as st
from ai_investigator import investigate_exception


st.set_page_config(
    page_title="ReconcileAI",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

with open("transactions.csv", "r") as file:
    transactions = list(csv.DictReader(file))

with open("prioritized_exceptions.csv", "r") as file:
    exceptions = list(csv.DictReader(file))


# ============================================================
# TRANSACTION METRICS
# ============================================================

physical_records = len(transactions)

unique_transaction_ids = set(
    transaction["transaction_id"]
    for transaction in transactions
)

unique_transactions = len(unique_transaction_ids)

total_exceptions = len(exceptions)

matched_transactions = unique_transactions - total_exceptions

if unique_transactions > 0:
    match_rate = (
        matched_transactions / unique_transactions
    ) * 100
else:
    match_rate = 0


# ============================================================
# PRIORITY METRICS
# ============================================================

high = 0
medium = 0
low = 0

amount_at_risk = 0

for exception in exceptions:

    priority = exception["priority"]

    difference = abs(
        float(exception["difference"])
    )

    amount_at_risk += difference

    if priority == "HIGH":
        high += 1

    elif priority == "MEDIUM":
        medium += 1

    elif priority == "LOW":
        low += 1



# ============================================================
# PRESENTATION UI
# ============================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .hero {
        padding: 1.4rem 1.6rem;
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 18px;
        margin-bottom: 1.2rem;
        background: linear-gradient(135deg, rgba(70,130,180,.12), rgba(120,80,180,.08));
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: .78;
        margin-top: .25rem;
    }

    .status {
        display: inline-block;
        margin-top: .9rem;
        padding: .35rem .75rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: .85rem;
        border: 1px solid rgba(46,160,67,.35);
        background: rgba(46,160,67,.10);
    }

    .section-note {
        opacity: .72;
        margin-top: -.35rem;
        margin-bottom: .8rem;
    }

    .risk-card {
        padding: 1rem;
        border: 1px solid rgba(128,128,128,.20);
        border-radius: 14px;
        text-align: center;
    }

    .risk-label {
        font-size: .82rem;
        opacity: .7;
    }

    .risk-value {
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: .2rem;
    }

    .pill {
        display: inline-block;
        padding: .2rem .55rem;
        border-radius: 999px;
        font-size: .78rem;
        font-weight: 700;
    }

    .pill-high { background: rgba(220,53,69,.14); color: #b42333; }
    .pill-medium { background: rgba(230,160,20,.16); color: #9a6700; }
    .pill-low { background: rgba(25,135,84,.14); color: #146c43; }

    .evidence-box {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(128,128,128,.20);
        border-radius: 14px;
        background: rgba(128,128,128,.035);
        margin-bottom: .8rem;
    }

    .footer {
        text-align: center;
        opacity: .6;
        padding: 1rem 0 .2rem;
        font-size: .82rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">💰 ReconcileAI</div>
    <div class="hero-subtitle">AI Finance Controller — reconciliation, exception detection, risk prioritization and investigation</div>
    <div class="status">🟢 Reconciliation Complete</div>
</div>
""", unsafe_allow_html=True)

# KPI row
st.subheader("Executive Overview")
st.markdown(
    "A finance-operations view of the current reconciliation batch.",
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric("Physical Records", f"{physical_records:,}")
with k2:
    st.metric("Unique Transactions", f"{unique_transactions:,}")
with k3:
    st.metric("Matched", f"{matched_transactions:,}")
with k4:
    st.metric("Match Rate", f"{match_rate:.1f}%")
with k5:
    st.metric("Exceptions", f"{total_exceptions:,}")

st.divider()

# Financial impact + risk distribution
st.subheader("💰 Financial Impact & Risk")
st.markdown(
    "Exceptions are prioritized so finance teams can focus on the highest-impact items first.",
    unsafe_allow_html=True
)

a1, a2, a3, a4 = st.columns(4)
with a1:
    st.metric("Amount at Risk", f"₹ {amount_at_risk:,.2f}")
with a2:
    st.metric("High Priority", high)
with a3:
    st.metric("Medium Priority", medium)
with a4:
    st.metric("Low Priority", low)

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("**Matched vs Exceptions**")
    st.bar_chart(
        {"Transactions": [matched_transactions, total_exceptions]},
        x=None,
        y="Transactions",
        height=260
    )

with chart2:
    st.markdown("**Exception Priority Distribution**")
    priority_chart = {
        "Priority": ["HIGH", "MEDIUM", "LOW"],
        "Exceptions": [high, medium, low]
    }
    st.bar_chart(priority_chart, x="Priority", y="Exceptions", height=260)

st.divider()

# Exception type distribution
st.subheader("📊 Exception Types")

type_counts = {}
for exception in exceptions:
    issue_type = exception["type"]
    type_counts[issue_type] = type_counts.get(issue_type, 0) + 1

type_rows = [
    {"Exception Type": issue_type, "Count": count}
    for issue_type, count in sorted(
        type_counts.items(), key=lambda item: item[1], reverse=True
    )
]

if type_rows:
    st.bar_chart(type_rows, x="Exception Type", y="Count", height=280)

st.divider()

# Search / filters
st.subheader("🔎 Exception Management")
st.markdown(
    "Search by transaction ID or filter by risk priority.",
    unsafe_allow_html=True
)

f1, f2 = st.columns([2, 1])

with f1:
    search = st.text_input(
        "Search Transaction ID",
        placeholder="Example: TXN023",
        label_visibility="collapsed"
    )

with f2:
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["ALL", "HIGH", "MEDIUM", "LOW"],
        label_visibility="collapsed"
    )

filtered_exceptions = []

for exception in exceptions:
    transaction_id = exception["transaction_id"]
    priority = exception["priority"]

    matches_search = (
        search.strip().upper() in transaction_id.upper()
        if search.strip()
        else True
    )

    matches_priority = (
        priority_filter == "ALL" or priority == priority_filter
    )

    if matches_search and matches_priority:
        filtered_exceptions.append(exception)

st.caption(f"Showing {len(filtered_exceptions)} of {total_exceptions} exceptions")

if filtered_exceptions:
    table_data = []

    for exception in filtered_exceptions:
        priority = exception["priority"]
        table_data.append({
            "Transaction": exception["transaction_id"],
            "Issue": exception["type"],
            "Difference": f"₹ {float(exception['difference']):,.2f}",
            "Priority": priority,
            "Recommended Action": exception["recommended_action"]
        })

    st.dataframe(
        table_data,
        width="stretch",
        hide_index=True,
        column_config={
            "Transaction": st.column_config.TextColumn("Transaction"),
            "Issue": st.column_config.TextColumn("Issue"),
            "Difference": st.column_config.TextColumn("Difference"),
            "Priority": st.column_config.TextColumn("Priority"),
            "Recommended Action": st.column_config.TextColumn(
                "Recommended Action",
                width="large"
            )
        }
    )
else:
    st.info("No exceptions match your filters.")

st.divider()

# Detailed investigation
st.subheader("🔍 Exception Investigation")
st.markdown(
    "Select an exception to review its transaction evidence and optionally run AI-assisted investigation.",
    unsafe_allow_html=True
)

if filtered_exceptions:
    transaction_options = [
        item["transaction_id"] for item in filtered_exceptions
    ]

    selected_transaction = st.selectbox(
        "Select a transaction",
        transaction_options
    )

    selected = next(
        (
            exception
            for exception in filtered_exceptions
            if exception["transaction_id"] == selected_transaction
        ),
        None
    )

    if selected:
        selected_transaction_data = [
            transaction
            for transaction in transactions
            if transaction["transaction_id"] == selected["transaction_id"]
        ]

        d1, d2 = st.columns(2)

        with d1:
            st.markdown("**Transaction Evidence**")
            st.markdown(
                f"""
                <div class="evidence-box">
                <b>Transaction ID:</b> {selected['transaction_id']}<br>
                <b>Issue:</b> {selected['type']}<br>
                <b>Difference:</b> ₹ {float(selected['difference']):,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

        with d2:
            st.markdown("**Risk Assessment**")
            priority = selected["priority"]
            pill_class = {
                "HIGH": "pill-high",
                "MEDIUM": "pill-medium",
                "LOW": "pill-low"
            }.get(priority, "pill-low")

            st.markdown(
                f"""
                <div class="evidence-box">
                <span class="pill {pill_class}">{priority}</span><br><br>
                <b>Recommended Action:</b><br>
                {selected['recommended_action']}
                </div>
                """,
                unsafe_allow_html=True
            )

        if selected_transaction_data:
            transaction = selected_transaction_data[0]

            order_amount = float(transaction["order_amount"])
            fee = float(transaction["fee"])
            settlement_amount = float(transaction["settlement_amount"])
            expected_settlement = order_amount - fee
            difference = abs(expected_settlement - settlement_amount)

            duplicate_count = len(selected_transaction_data)

            st.markdown("**Reconciliation Evidence**")
            e1, e2, e3, e4 = st.columns(4)

            with e1:
                st.metric("Order Amount", f"₹ {order_amount:,.2f}")
            with e2:
                st.metric("Expected Settlement", f"₹ {expected_settlement:,.2f}")
            with e3:
                st.metric("Actual Settlement", f"₹ {settlement_amount:,.2f}")
            with e4:
                st.metric("Records Sharing ID", duplicate_count)

            st.caption(
                f"Transaction date: {transaction['transaction_date']}  •  "
                f"Settlement date: {transaction['settlement_date']}  •  "
                f"Status: {transaction['status']}"
            )

            # AI investigation — same evidence pipeline as the working version
            st.markdown("### 🤖 AI Investigation")

            duplicate_records_text = ""
            for index, record in enumerate(selected_transaction_data, start=1):
                duplicate_records_text += f"""
Record {index}:
- Transaction ID: {record["transaction_id"]}
- Order Amount: ₹{float(record["order_amount"]):,.2f}
- Processing Fee: ₹{float(record["fee"]):,.2f}
- Settlement Amount: ₹{float(record["settlement_amount"]):,.2f}
- Transaction Date: {record["transaction_date"]}
- Settlement Date: {record["settlement_date"]}
- Status: {record["status"]}
- Exception Type: {record["exception_type"]}
"""

            exception_data = f"""
Transaction ID: {selected["transaction_id"]}
Issue: {selected["type"]}
Number of records with this Transaction ID: {duplicate_count}
Duplicate evidence: {"YES - multiple records with the same Transaction ID" if duplicate_count > 1 else "NO - only one record found"}

Primary transaction evidence:
Order Amount: ₹{order_amount:,.2f}
Processing Fee: ₹{fee:,.2f}
Expected Settlement: ₹{expected_settlement:,.2f}
Actual Settlement: ₹{settlement_amount:,.2f}
Transaction Date: {transaction["transaction_date"]}
Settlement Date: {transaction["settlement_date"]}
Transaction Status: {transaction["status"]}
Exception Type: {transaction["exception_type"]}
Reconciliation Difference: ₹{difference:,.2f}
Priority: {selected["priority"]}
Recommended Action: {selected["recommended_action"]}

All records sharing this Transaction ID:
{duplicate_records_text}
"""

            if st.button(
                "🤖 Investigate with Gemini",
                key=f"investigate_{selected['transaction_id']}"
            ):
                with st.spinner("Gemini is investigating the exception..."):
                    try:
                        result = investigate_exception(exception_data)
                        st.success("AI investigation completed.")
                        st.markdown(result)
                    except Exception as e:
                        error_text = str(e)

                        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                            st.warning("⚠️ Gemini AI quota is temporarily exhausted.")
                            st.info(
                                "The core reconciliation, exception detection and "
                                "risk prioritization remain fully available."
                            )
                        else:
                            st.error("Gemini investigation could not be completed.")
                            st.info(
                                "The existing rule-based investigation remains available."
                            )

            st.caption(
                "AI investigation is evidence-based and advisory. "
                "Final financial decisions require human approval."
            )
        else:
            st.error("Transaction details could not be found in transactions.csv.")

st.divider()

# Explainability section
st.subheader("⚙️ How ReconcileAI Works")

steps = st.columns(6)
workflow = [
    ("1", "Load", "Transaction batch"),
    ("2", "Reconcile", "Expected vs actual"),
    ("3", "Detect", "Exceptions"),
    ("4", "Prioritize", "Risk level"),
    ("5", "Investigate", "Evidence + AI"),
    ("6", "Review", "Human approval"),
]

for col, (number, title, detail) in zip(steps, workflow):
    with col:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-label">{number}</div>
                <div class="risk-value">{title}</div>
                <div class="risk-label">{detail}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()

with st.expander("📌 Methodology & Limitations"):
    st.markdown("""
    - Reconciliation compares transaction evidence against expected settlement values.
    - Exceptions are surfaced for amount, fee, date, missing-settlement and duplicate issues.
    - Priority is rule-based and intended to focus human attention on higher-risk items.
    - AI investigation is optional and uses the available transaction evidence as context.
    - AI output is advisory; it does not approve, post, or make final financial decisions.
    - The demonstration uses synthetic transaction data.
    """)

st.markdown(
    '<div class="footer">ReconcileAI · Financial reconciliation & AI-assisted exception management</div>',
    unsafe_allow_html=True
)
