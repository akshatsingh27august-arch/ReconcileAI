import csv
import random
from datetime import datetime, timedelta

random.seed(42)

number_of_transactions = 100

exception_types = [
    "Amount Mismatch",
    "Missing Settlement",
    "Duplicate Transaction",
    "Fee Mismatch",
    "Date Mismatch"
]

start_date = datetime(2026, 8, 1)

with open("transactions.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "transaction_id",
        "order_amount",
        "settlement_amount",
        "fee",
        "transaction_date",
        "settlement_date",
        "status",
        "exception_type"
    ])

    for i in range(1, number_of_transactions + 1):

        order_amount = random.choice([
            500, 750, 1000, 1500, 2000,
            2500, 3000, 5000, 7500, 10000
        ])

        transaction_date = start_date + timedelta(
            days=random.randint(0, 29)
        )

        settlement_date = transaction_date + timedelta(
            days=random.randint(1, 3)
        )

        fee = round(order_amount * 0.02, 2)

        # 80% normal transactions
        if random.random() < 0.80:

            settlement_amount = order_amount - fee
            status = "Matched"
            exception_type = "None"

        # 20% transactions contain an exception
        else:

            exception_type = random.choice(exception_types)

            if exception_type == "Amount Mismatch":
                settlement_amount = order_amount - fee - random.choice(
                    [50, 100, 150, 200, 300]
                )
                status = "Exception"

            elif exception_type == "Missing Settlement":
                settlement_amount = 0
                status = "Exception"

            elif exception_type == "Duplicate Transaction":
                settlement_amount = order_amount - fee
                status = "Exception"

            elif exception_type == "Fee Mismatch":
                settlement_amount = order_amount - random.choice(
                    [50, 75, 100, 125]
                )
                status = "Exception"

            elif exception_type == "Date Mismatch":
                settlement_amount = order_amount - fee
                settlement_date = transaction_date + timedelta(days=10)
                status = "Exception"

        transaction_id = f"TXN{i:03d}"

        writer.writerow([
            transaction_id,
            order_amount,
            settlement_amount,
            fee,
            transaction_date.strftime("%Y-%m-%d"),
            settlement_date.strftime("%Y-%m-%d"),
            status,
            exception_type
        ])

print("Successfully generated 100 realistic transactions!")
print("Exception types included:")
print("- Amount Mismatch")
print("- Missing Settlement")
print("- Duplicate Transaction")
print("- Fee Mismatch")
print("- Date Mismatch")