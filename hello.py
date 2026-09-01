import csv

total_transactions = 0
matched_transactions = 0
exception_transactions = 0

with open("transactions.csv", "r") as file:
    transactions = csv.DictReader(file)

    for transaction in transactions:
        total_transactions += 1

        order_amount = float(transaction["order_amount"])
        settlement_amount = float(transaction["settlement_amount"])

        if order_amount == settlement_amount:
            matched_transactions += 1
            print(transaction["transaction_id"], "→ MATCHED")
        else:
            exception_transactions += 1
            difference = order_amount - settlement_amount

            print(
                transaction["transaction_id"],
                "→ EXCEPTION | Difference: ₹",
                difference
            )

if total_transactions > 0:
    match_rate = (matched_transactions / total_transactions) * 100
else:
    match_rate = 0

print("\n----------------------------")
print("RECONCILIATION SUMMARY")
print("----------------------------")
print("Total transactions:", total_transactions)
print("Matched:", matched_transactions)
print("Exceptions:", exception_transactions)
print("Match rate:", round(match_rate, 2), "%")