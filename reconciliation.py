import csv


def reconcile_transactions(filename):
    """
    Reconcile a batch of transaction records.

    Returns:
        total_records
        unique_transaction_count
        matched
        exceptions
        match_rate
    """

    transactions = []

    # ==========================================
    # STEP 1: READ ALL TRANSACTION RECORDS
    # ==========================================

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for transaction in reader:
            transactions.append(transaction)

    total_records = len(transactions)

    # ==========================================
    # STEP 2: FIND DUPLICATE TRANSACTION IDs
    # ==========================================

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

    # ==========================================
    # STEP 3: RECONCILE EACH TRANSACTION
    # ==========================================

    matched = 0
    exceptions = []

    processed_duplicate_ids = set()

    for transaction in transactions:

        transaction_id = transaction["transaction_id"]

        order_amount = float(transaction["order_amount"])
        settlement_amount = float(
            transaction["settlement_amount"]
        )
        fee = float(transaction["fee"])

        expected_settlement = order_amount - fee

        difference = round(
            expected_settlement - settlement_amount,
            2
        )

        exception_type = transaction["exception_type"]

        # ======================================
        # DUPLICATE DETECTION
        # ======================================

        if transaction_id in duplicate_ids:

            if transaction_id not in processed_duplicate_ids:

                exceptions.append({
                    "transaction_id": transaction_id,
                    "type": "Duplicate Transaction",
                    "order_amount": order_amount,
                    "settlement_amount": settlement_amount,
                    "expected_settlement":
                        expected_settlement,
                    "difference": difference,
                    "transaction_date":
                        transaction["transaction_date"],
                    "settlement_date":
                        transaction["settlement_date"],
                    "detection_method":
                        "Duplicate ID Detection"
                })

                processed_duplicate_ids.add(
                    transaction_id
                )

            continue

        # ======================================
        # NORMAL AMOUNT RECONCILIATION
        # ======================================

        amount_matches = abs(difference) < 0.01

        if amount_matches and exception_type == "None":

            matched += 1

        else:

            if exception_type == "None":

                detected_type = (
                    "Unexpected Amount Difference"
                )

                detection_method = (
                    "Amount Reconciliation Rule"
                )

            elif exception_type == "Date Mismatch":

                detected_type = "Date Mismatch"

                detection_method = (
                    "Settlement Date Rule"
                )

            else:

                detected_type = exception_type

                detection_method = (
                    "Exception Classification"
                )

            exceptions.append({
                "transaction_id": transaction_id,
                "type": detected_type,
                "order_amount": order_amount,
                "settlement_amount": settlement_amount,
                "expected_settlement":
                    expected_settlement,
                "difference": difference,
                "transaction_date":
                    transaction["transaction_date"],
                "settlement_date":
                    transaction["settlement_date"],
                "detection_method":
                    detection_method
            })

    # ==========================================
    # STEP 4: CALCULATE BATCH METRICS
    # ==========================================

    unique_transaction_count = len(
        transaction_counts
    )

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


def save_exceptions(exceptions, filename):
    """
    Save reconciliation exceptions to a CSV file.
    """

    fieldnames = [
        "transaction_id",
        "type",
        "order_amount",
        "settlement_amount",
        "expected_settlement",
        "difference",
        "transaction_date",
        "settlement_date",
        "detection_method"
    ]

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for exception in exceptions:
            writer.writerow(exception)


def print_reconciliation_report(
    total_records,
    unique_transactions,
    matched,
    exceptions,
    match_rate
):
    """
    Display a complete reconciliation report.
    """

    exception_count = len(exceptions)

    # ==========================================
    # BATCH VALIDATION
    # ==========================================

    accounted_records = (
        matched + exception_count
    )

    unaccounted_records = (
        unique_transactions - accounted_records
    )

    duplicate_count = sum(
        1
        for exception in exceptions
        if exception["type"] ==
        "Duplicate Transaction"
    )

    if unique_transactions > 0:

        batch_coverage = (
            accounted_records /
            unique_transactions
        ) * 100

    else:

        batch_coverage = 0

    # ==========================================
    # RECONCILIATION REPORT
    # ==========================================

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
        exception_count
    )

    print(
        "Match rate           :",
        round(match_rate, 2),
        "%"
    )

    # ==========================================
    # BATCH VALIDATION
    # ==========================================

    print("\n================================")
    print("       BATCH VALIDATION")
    print("================================")

    print(
        "Records accounted for :",
        accounted_records
    )

    print(
        "Unaccounted records   :",
        unaccounted_records
    )

    print(
        "Duplicate IDs detected:",
        duplicate_count
    )

    print(
        "Batch coverage        :",
        round(batch_coverage, 2),
        "%"
    )

    if unaccounted_records == 0:

        print(
            "Validation status     : PASS"
        )

    else:

        print(
            "Validation status     : REVIEW REQUIRED"
        )

    print(
        "\nException file created: "
        "exceptions.csv"
    )

    # ==========================================
    # EXCEPTION DETAILS
    # ==========================================

    print("\n---------- EXCEPTIONS ----------")

    for exception in exceptions:

        print(
            exception["transaction_id"],
            "|",
            exception["type"],
            "| Difference: ₹",
            exception["difference"],
            "| Detection:",
            exception["detection_method"]
        )


# ==============================================
# MAIN PROGRAM
# ==============================================
#
# IMPORTANT:
# This block only runs when this file is
# executed directly.
#
# Importing reconciliation.py from another
# Python file will NOT automatically run it.
# ==============================================

if __name__ == "__main__":

    (
        total_records,
        unique_transactions,
        matched,
        exceptions,
        match_rate
    ) = reconcile_transactions(
        "transactions.csv"
    )

    save_exceptions(
        exceptions,
        "exceptions.csv"
    )

    print_reconciliation_report(
        total_records,
        unique_transactions,
        matched,
        exceptions,
        match_rate
    )