import csv


total_transactions = 0
matched_transactions = 0
exception_transactions = 0

total_order_value = 0
total_expected_settlement = 0
total_actual_settlement = 0
total_exception_amount = 0


with open("transactions.csv", "r") as file:

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

        if transaction["exception_type"] == "None":

            matched_transactions += 1

        else:

            exception_transactions += 1

            difference = abs(
                expected_settlement - settlement_amount
            )

            total_exception_amount += difference


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


print("\n======================================")
print("          FINANCE SUMMARY")
print("======================================")

print(
    "Total transactions       :",
    total_transactions
)

print(
    "Total order value        : ₹",
    round(total_order_value, 2)
)

print(
    "Expected settlement      : ₹",
    round(total_expected_settlement, 2)
)

print(
    "Actual settlement        : ₹",
    round(total_actual_settlement, 2)
)

print(
    "Amount affected by issues: ₹",
    round(total_exception_amount, 2)
)

print(
    "Matched transactions     :",
    matched_transactions
)

print(
    "Exceptions               :",
    exception_transactions
)

print(
    "Match rate               :",
    round(match_rate, 2),
    "%"
)

print(
    "Exception rate           :",
    round(exception_rate, 2),
    "%"
)

print("======================================")