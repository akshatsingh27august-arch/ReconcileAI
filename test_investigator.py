import csv

from reconciliation import reconcile_transactions


def test_reconciliation_batch():

    (
        total_records,
        unique_transactions,
        matched,
        exceptions,
        match_rate
    ) = reconcile_transactions("transactions.csv")

    # ==========================================
    # BASIC DATA VALIDATION
    # ==========================================

    assert total_records >= 50, (
        "Buildathon requirement failed: "
        "batch must contain at least 50 physical records."
    )

    assert unique_transactions > 0, (
        "No unique transactions found."
    )

    # ==========================================
    # EXCEPTION VALIDATION
    # ==========================================

    exception_count = len(exceptions)

    accounted_transactions = (
        matched + exception_count
    )

    # Every unique transaction must be accounted for
    assert accounted_transactions == unique_transactions, (
        "Batch validation failed: "
        "some transactions are unaccounted for."
    )

    # ==========================================
    # MATCH RATE VALIDATION
    # ==========================================

    calculated_match_rate = (
        matched / unique_transactions * 100
    )

    assert abs(
        calculated_match_rate - match_rate
    ) < 0.01, (
        "Match rate calculation is inconsistent."
    )

    # ==========================================
    # EXCEPTION STRUCTURE VALIDATION
    # ==========================================

    required_fields = [
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

    for exception in exceptions:

        for field in required_fields:

            assert field in exception, (
                f"Missing exception field: {field}"
            )

    # ==========================================
    # DUPLICATE DETECTION VALIDATION
    # ==========================================

    duplicate_exceptions = [
        exception
        for exception in exceptions
        if exception["type"] == "Duplicate Transaction"
    ]

    for exception in duplicate_exceptions:

        assert exception["detection_method"] == (
            "Duplicate ID Detection"
        )

    # ==========================================
    # DATE DETECTION VALIDATION
    # ==========================================

    date_exceptions = [
        exception
        for exception in exceptions
        if exception["type"] == "Date Mismatch"
    ]

    for exception in date_exceptions:

        assert exception["detection_method"] == (
            "Settlement Date Rule"
        )

    # ==========================================
    # EXCEPTION IDs MUST BE UNIQUE
    # ==========================================

    exception_ids = [
        exception["transaction_id"]
        for exception in exceptions
    ]

    assert len(exception_ids) == len(set(exception_ids)), (
        "Exception list contains duplicate transaction IDs."
    )

    # ==========================================
    # FINAL TEST MESSAGE
    # ==========================================

    print("\n================================")
    print("       RECONCILIATION TEST")
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

    print(
        "Batch coverage       :",
        round(
            accounted_transactions /
            unique_transactions * 100,
            2
        ),
        "%"
    )

    print(
        "Validation result    : PASS"
    )