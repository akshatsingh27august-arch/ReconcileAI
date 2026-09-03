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
# HEADER
# ============================================================

st.title("💰 ReconcileAI")

st.subheader("AI Finance Controller")

st.write(
    "Automated transaction reconciliation, "
    "exception detection, risk prioritization "
    "and AI-assisted investigation."
)

st.divider()


# ============================================================
# MAIN METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Physical Records",
        physical_records
    )


with col2:
    st.metric(
        "Unique Transactions",
        unique_transactions
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


# ============================================================
# RECONCILIATION SUMMARY
# ============================================================

st.subheader("📊 Reconciliation Summary")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "✅ Matched",
        matched_transactions
    )


with col2:

    st.metric(
        "⚠️ Exceptions",
        total_exceptions
    )


with col3:

    st.metric(
        "💰 Amount at Risk",
        f"₹ {amount_at_risk:,.2f}"
    )


st.divider()


# ============================================================
# PRIORITY SUMMARY
# ============================================================

st.subheader("⚠️ Exception Risk Summary")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔴 High Priority",
        high
    )


with col2:

    st.metric(
        "🟡 Medium Priority",
        medium
    )


with col3:

    st.metric(
        "🟢 Low Priority",
        low
    )


st.subheader("📈 Exception Distribution")


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


# ============================================================
# EXCEPTION SEARCH
# ============================================================

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


filtered_exceptions = []


for exception in exceptions:

    transaction_id = exception["transaction_id"]

    priority = exception["priority"]


    matches_search = (

        search.strip().upper()
        in transaction_id.upper()

        if search.strip()

        else True
    )


    matches_priority = (

        priority_filter == "ALL"

        or priority == priority_filter
    )


    if matches_search and matches_priority:

        filtered_exceptions.append(
            exception
        )


st.write(
    f"Showing **{len(filtered_exceptions)}** exception(s)"
)


# ============================================================
# EXCEPTION TABLE
# ============================================================

if filtered_exceptions:

    table_data = []


    for exception in filtered_exceptions:

        table_data.append({

            "Transaction":
                exception["transaction_id"],

            "Issue":
                exception["type"],

            "Difference":
                f"₹ {float(exception['difference']):,.2f}",

            "Priority":
                exception["priority"],

            "Recommended Action":
                exception["recommended_action"]

        })


    st.dataframe(
        table_data,
        width="stretch",
        hide_index=True
    )


else:

    st.info(
        "No exceptions match your filters."
    )


st.divider()


# ============================================================
# EXCEPTION DETAILS
# ============================================================

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

        if (
            exception["transaction_id"]
            == selected_transaction
        ):

            selected = exception

            break


    if selected:

        selected_transaction_data = [
            transaction
            for transaction in transactions
            if transaction["transaction_id"] == selected["transaction_id"]
        ]


        col1, col2 = st.columns(2)


        with col1:

            st.write("### Transaction")

            st.write(
                f"**Transaction ID:** "
                f"{selected['transaction_id']}"
            )

            st.write(
                f"**Issue:** "
                f"{selected['type']}"
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


        # ====================================================
        # AI INVESTIGATION
        # ====================================================

        st.write("### 🤖 AI Investigation")


        if selected_transaction_data:

            transaction = selected_transaction_data[0]


            order_amount = float(
                transaction["order_amount"]
            )

            fee = float(
                transaction["fee"]
            )

            settlement_amount = float(
                transaction["settlement_amount"]
            )


            expected_settlement = (
                order_amount - fee
            )


            difference = abs(
                expected_settlement
                - settlement_amount
            )


            duplicate_count = len(selected_transaction_data)

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

                with st.spinner(
                    "Gemini is investigating the exception..."
                ):

                    try:

                        result = investigate_exception(
                            exception_data
                        )


                        st.success(
                            "AI investigation completed."
                        )

                        st.markdown(result)


                    except Exception as e:

                        error_text = str(e)

                        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                            st.warning(
                                "⚠️ Gemini AI quota is temporarily exhausted."
                            )
                            st.info(
                                "The rule-based reconciliation and exception "
                                "prioritization remain fully available."
                            )
                        else:
                            st.error(
                                "Gemini investigation could not be completed."
                            )
                            st.info(
                                "The existing rule-based investigation remains available."
                            )


        else:

            st.error(
                "Transaction details could not be found "
                "in transactions.csv."
            )


        st.caption(
            "AI investigation is based on available "
            "transaction evidence. Final financial "
            "decisions require human approval."
        )


st.divider()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "ReconcileAI | Financial reconciliation "
    "and AI-assisted exception management"
)