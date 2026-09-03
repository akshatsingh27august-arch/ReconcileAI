import csv


def reconcile_transactions(filename):

    transactions = []

    # Read all transaction records
    with open(filename, "r") as file:

        reader = csv.DictReader(file)

        for transaction in reader:
            transactions.append(transaction)

    total_records = len(transactions)

    # Find duplicate transaction IDs
    transaction_counts = {}

    for transaction in transactions:

        transaction_id = transaction["transaction_id"]

        transaction_counts[transaction_id] = (
            transaction_counts.get(transaction_id, 0) + 1
        )

    duplicate_ids = set()

    for transaction_id, count in transaction_counts.items():

        if count > 1:
            duplicate_ids.add(transaction_id)

    matched = 0
    exceptions = []

    processed_duplicate_ids = set()

    for transaction in transactions:

        transaction_id = transaction["transaction_id"]

        order_amount = float(transaction["order_amount"])
        settlement_amount = float(transaction["settlement_amount"])
        fee = float(transaction["fee"])

        expected_settlement = order_amount - fee

        difference = round(
            expected_settlement - settlement_amount,
            2
        )

        exception_type = transaction["exception_type"]

        # Handle duplicates separately
        if transaction_id in duplicate_ids:

            # Create only one exception for each duplicate ID
            if transaction_id not in processed_duplicate_ids:

                exceptions.append({
                    "transaction_id": transaction_id,
                    "type": "Duplicate Transaction",
                    "order_amount": order_amount,
                    "settlement_amount": settlement_amount,
                    "expected_settlement": expected_settlement,
                    "difference": difference,
                    "transaction_date": transaction["transaction_date"],
                    "settlement_date": transaction["settlement_date"]
                })

                processed_duplicate_ids.add(transaction_id)

            continue

        # Normal reconciliation
        amount_matches = abs(difference) < 0.01

        if amount_matches and exception_type == "None":

            matched += 1

        else:

            if exception_type == "None":
                detected_type = "Unexpected Amount Difference"
            else:
                detected_type = exception_type

            exceptions.append({
                "transaction_id": transaction_id,
                "type": detected_type,
                "order_amount": order_amount,
                "settlement_amount": settlement_amount,
                "expected_settlement": expected_settlement,
                "difference": difference,
                "transaction_date": transaction["transaction_date"],
                "settlement_date": transaction["settlement_date"]
            })

    # Calculate unique transaction count
    unique_transaction_count = len(transaction_counts)

    match_rate = (
        matched / unique_transaction_count * 100
        if unique_transaction_count > 0
        else 0
    )

    return (
        total_records,
        unique_transaction_count,
        matched,
        exceptions,
        match_rate
    )


# Run reconciliation

(
    total_records,
    unique_transactions,
    matched,
    exceptions,
    match_rate
) = reconcile_transactions("transactions.csv")


# Save exceptions

with open("exceptions.csv", "w", newline="") as file:

    fieldnames = [
        "transaction_id",
        "type",
        "order_amount",
        "settlement_amount",
        "expected_settlement",
        "difference",
        "transaction_date",
        "settlement_date"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for exception in exceptions:
        writer.writerow(exception)


# Display report

print("\n================================")
print("       RECONCILIATION REPORT")
print("================================")

print(
    "Physical records     :",
    total_records
)

print(
    "Unique transactions  :",
    unique_transactions
)

print(
    "Matched transactions :",
    matched
)

print(
    "Exceptions           :",
    len(exceptions)
)

print(
    "Match rate           :",
    round(match_rate, 2),
    "%"
)

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