import csv


def generate_finance_summary(filename):

    total_transactions = 0
    matched_transactions = 0
    exception_transactions = 0

    total_order_value = 0
    total_expected_settlement = 0
    total_actual_settlement = 0
    total_exception_amount = 0

    with open(filename, "r") as file:

        transactions = csv.DictReader(file)

        for transaction in transactions:

            total_transactions += 1

            order_amount = float(transaction["order_amount"])
            settlement_amount = float(transaction["settlement_amount"])
            fee = float(transaction["fee"])

            expected_settlement = order_amount - fee

            total_order_value += order_amount
            total_expected_settlement += expected_settlement
            total_actual_settlement += settlement_amount

            difference = round(
                expected_settlement - settlement_amount,
                2
            )

            # Use actual settlement reconciliation
            # rather than relying only on exception labels.
            amount_matches = abs(difference) < 0.01

            if amount_matches and transaction["exception_type"] == "None":

                matched_transactions += 1

            else:

                exception_transactions += 1

                total_exception_amount += abs(difference)

    if total_transactions > 0:

        match_rate = (
            matched_transactions / total_transactions
        ) * 100

        exception_rate = (
            exception_transactions / total_transactions
        ) * 100

    else:

        match_rate = 0
        exception_rate = 0

    return {
        "total_transactions": total_transactions,
        "matched_transactions": matched_transactions,
        "exception_transactions": exception_transactions,
        "total_order_value": total_order_value,
        "total_expected_settlement": total_expected_settlement,
        "total_actual_settlement": total_actual_settlement,
        "total_exception_amount": total_exception_amount,
        "match_rate": match_rate,
        "exception_rate": exception_rate
    }


# Generate finance summary

summary = generate_finance_summary("transactions.csv")


# Display report

print("\n======================================")
print("          FINANCE SUMMARY")
print("======================================")

print(
    "Total transactions       :",
    summary["total_transactions"]
)

print(
    "Total order value        : ₹",
    round(summary["total_order_value"], 2)
)

print(
    "Expected settlement      : ₹",
    round(summary["total_expected_settlement"], 2)
)

print(
    "Actual settlement        : ₹",
    round(summary["total_actual_settlement"], 2)
)

print(
    "Amount affected by issues: ₹",
    round(summary["total_exception_amount"], 2)
)

print(
    "Matched transactions     :",
    summary["matched_transactions"]
)

print(
    "Exceptions               :",
    summary["exception_transactions"]
)

print(
    "Match rate               :",
    round(summary["match_rate"], 2),
    "%"
)

print(
    "Exception rate           :",
    round(summary["exception_rate"], 2),
    "%"
)

print("======================================")