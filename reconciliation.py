import csv


def reconcile_transactions(filename):
    total = 0
    matched = 0
    exceptions = []

    with open(filename, "r") as file:
        transactions = csv.DictReader(file)

        for transaction in transactions:
            total += 1

            transaction_id = transaction["transaction_id"]

            order_amount = float(transaction["order_amount"])
            settlement_amount = float(transaction["settlement_amount"])
            fee = float(transaction["fee"])

            expected_settlement = order_amount - fee

            exception_type = transaction["exception_type"]

            if exception_type == "None":
                if abs(settlement_amount - expected_settlement) < 0.01:
                    matched += 1
                else:
                    exceptions.append({
                        "transaction_id": transaction_id,
                        "type": "Unexpected Amount Difference",
                        "order_amount": order_amount,
                        "settlement_amount": settlement_amount,
                        "expected_settlement": expected_settlement,
                        "difference": round(
                            expected_settlement - settlement_amount, 2
                        )
                    })

            else:
                exceptions.append({
                    "transaction_id": transaction_id,
                    "type": exception_type,
                    "order_amount": order_amount,
                    "settlement_amount": settlement_amount,
                    "expected_settlement": expected_settlement,
                    "difference": round(
                        expected_settlement - settlement_amount, 2
                    )
                })

    match_rate = (matched / total * 100) if total else 0

    return total, matched, exceptions, match_rate


# Run reconciliation
total, matched, exceptions, match_rate = reconcile_transactions(
    "transactions.csv"
)


# Save exceptions to a separate CSV file
with open("exceptions.csv", "w", newline="") as file:

    fieldnames = [
        "transaction_id",
        "type",
        "order_amount",
        "settlement_amount",
        "expected_settlement",
        "difference"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for exception in exceptions:
        writer.writerow(exception)


# Display report
print("\n================================")
print("       RECONCILIATION REPORT")
print("================================")

print("Total transactions :", total)
print("Matched             :", matched)
print("Exceptions          :", len(exceptions))
print("Match rate          :", round(match_rate, 2), "%")

print("\nException file created: exceptions.csv")

print("\n---------- EXCEPTIONS ----------")

for exception in exceptions:
    print(
        exception["transaction_id"],
        "|",
        exception["type"],
        "| Difference: ₹",
        exception["difference"]
    )