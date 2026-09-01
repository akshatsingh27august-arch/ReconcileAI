import streamlit as st
import csv


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ReconcileAI",
    page_icon="💰",
    layout="wide"
)


# ==========================================
# LOAD DATA
# ==========================================

with open("transactions.csv", "r") as file:
    transactions = list(csv.DictReader(file))

with open("prioritized_exceptions.csv", "r") as file:
    exceptions = list(csv.DictReader(file))


# ==========================================
# CALCULATE MAIN METRICS
# ==========================================

total_transactions = len(transactions)
total_exceptions = len(exceptions)
matched_transactions = total_transactions - total_exceptions

if total_transactions > 0:
    match_rate = matched_transactions / total_transactions * 100
else:
    match_rate = 0


# ==========================================
# PRIORITY COUNTS
# ==========================================

high = 0
medium = 0
low = 0
amount_at_risk = 0

for exception in exceptions:

    priority = exception["priority"]

    difference = abs(float(exception["difference"]))

    amount_at_risk += difference

    if priority == "HIGH":
        high += 1

    elif priority == "MEDIUM":
        medium += 1

    elif priority == "LOW":
        low += 1


# ==========================================
# HEADER
# ==========================================

st.title("💰 ReconcileAI")
st.subheader("AI Finance Controller")

st.write(
    "Automated transaction reconciliation, "
    "exception detection and financial risk prioritization."
)

st.divider()


# ==========================================
# MAIN METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "Matched",
        matched_transactions
    )

with col3:
    st.metric(
        "Exceptions",
        total_exceptions
    )

with col4:
    st.metric(
        "Match Rate",
        f"{match_rate:.1f}%"
    )


st.divider()


# ==========================================
# RISK SUMMARY
# ==========================================

st.subheader("⚠️ Exception Risk Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔴 High Priority", high)

with col2:
    st.metric("🟡 Medium Priority", medium)

with col3:
    st.metric("🟢 Low Priority", low)

with col4:
    st.metric(
        "💰 Amount at Risk",
        f"₹ {amount_at_risk:,.2f}"
    )


# ==========================================
# PRIORITY CHART
# ==========================================

st.subheader("📊 Exception Distribution")

chart_data = {
    "Priority": [
        "HIGH",
        "MEDIUM",
        "LOW"
    ],
    "Exceptions": [
        high,
        medium,
        low
    ]
}

st.bar_chart(
    chart_data,
    x="Priority",
    y="Exceptions"
)


st.divider()


# ==========================================
# FILTER SECTION
# ==========================================

st.subheader("🔎 Investigate Exceptions")

col1, col2 = st.columns(2)

with col1:

    search = st.text_input(
        "Search Transaction ID",
        placeholder="Example: TXN023"
    )

with col2:

    priority_filter = st.selectbox(
        "Filter by Priority",
        [
            "ALL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ]
    )


# ==========================================
# FILTER DATA
# ==========================================

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
        priority_filter == "ALL"
        or priority == priority_filter
    )

    if matches_search and matches_priority:
        filtered_exceptions.append(exception)


st.write(
    f"Showing **{len(filtered_exceptions)}** exception(s)"
)


# ==========================================
# EXCEPTION TABLE
# ==========================================

if filtered_exceptions:

    table_data = []

    for exception in filtered_exceptions:

        table_data.append({
            "Transaction": exception["transaction_id"],
            "Issue": exception["type"],
            "Difference": f"₹ {float(exception['difference']):,.2f}",
            "Priority": exception["priority"],
            "Recommended Action":
                exception["recommended_action"]
        })

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No exceptions match your filters.")


# ==========================================
# EXCEPTION DETAIL
# ==========================================

st.divider()

st.subheader("🔍 Exception Details")

if filtered_exceptions:

    transaction_options = [
        item["transaction_id"]
        for item in filtered_exceptions
    ]

    selected_transaction = st.selectbox(
        "Select a transaction to investigate",
        transaction_options
    )

    selected = None

    for exception in filtered_exceptions:

        if exception["transaction_id"] == selected_transaction:
            selected = exception
            break

    if selected:

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Transaction")

            st.write(
                f"**Transaction ID:** "
                f"{selected['transaction_id']}"
            )

            st.write(
                f"**Issue:** {selected['type']}"
            )

            st.write(
                f"**Difference:** "
                f"₹ {float(selected['difference']):,.2f}"
            )

        with col2:

            st.write("### Risk Assessment")

            st.write(
                f"**Priority:** "
                f"{selected['priority']}"
            )

            st.write(
                f"**Recommended Action:** "
                f"{selected['recommended_action']}"
            )

                # ==========================================
        # INVESTIGATION RESULT
        # ==========================================

        st.write("### 🤖 Investigation Result")

        issue = selected["type"]
        difference = abs(float(selected["difference"]))
        priority = selected["priority"]

        if issue == "Amount Mismatch":

            explanation = (
                f"The transaction has an amount discrepancy "
                f"of ₹{difference:,.2f}. The recorded transaction "
                f"amount does not match the expected settlement."
            )

            action = (
                "Verify the order amount and settlement amount "
                "against the original payment record."
            )

        elif issue == "Fee Mismatch":

            explanation = (
                f"A fee discrepancy of ₹{difference:,.2f} "
                f"was detected. The expected processing fee "
                f"does not match the recorded fee."
            )

            action = (
                "Verify the applicable payment fee and compare "
                "it with the settlement record."
            )

        elif issue == "Date Mismatch":

            explanation = (
                "The transaction and settlement dates do not "
                "match the expected reconciliation window."
            )

            action = (
                "Check settlement timing, transaction timestamps "
                "and the applicable settlement cycle."
            )

        elif issue == "Duplicate Transaction":

            explanation = (
                "A possible duplicate transaction was detected. "
                "The transaction should be verified before any "
                "additional settlement action."
            )

            action = (
                "Compare transaction IDs, order records and "
                "payment timestamps before processing."
            )

        elif issue == "Missing Settlement":

            explanation = (
                "The transaction appears to have no corresponding "
                "settlement record."
            )

            action = (
                "Immediately verify the settlement status and "
                "escalate if the payment was successfully captured."
            )

        else:

            explanation = (
                "An exception was detected that requires "
                "additional financial review."
            )

            action = (
                "Review the transaction evidence before taking action."
            )


        st.write("**What happened?**")

        st.write(explanation)

        st.write("**Recommended action**")

        st.write(action)

        st.write("**Risk level**")

        if priority == "HIGH":
            st.error("🔴 HIGH — Human review recommended")

        elif priority == "MEDIUM":
            st.warning("🟡 MEDIUM — Finance review recommended")

        else:
            st.success("🟢 LOW — Batch review recommended")

        st.caption(
            "Investigation is based on the available transaction "
            "evidence. Final financial decisions require human approval."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "ReconcileAI | Financial reconciliation "
    "and AI-assisted exception management"
)