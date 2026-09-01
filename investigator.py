import csv


def investigate_exception(exception):
    exception_type = exception["type"]

    transaction_id = exception["transaction_id"]

    order_amount = float(exception["order_amount"])
    settlement_amount = float(exception["settlement_amount"])
    expected_settlement = float(exception["expected_settlement"])
    difference = float(exception["difference"])

    if exception_type == "Amount Mismatch":
        reason = (
            "The settlement amount is lower than the expected "
            "settlement amount."
        )
        action = (
            "Review settlement adjustments and compare the payment "
            "and settlement records."
        )
        confidence = 0.92
        review = "REQUIRED"

    elif exception_type == "Missing Settlement":
        reason = (
            "No settlement amount was recorded for this transaction."
        )
        action = (
            "Check whether the payment was successfully captured "
            "and investigate the missing settlement."
        )
        confidence = 0.98
        review = "REQUIRED"

    elif exception_type == "Duplicate Transaction":
        reason = (
            "The transaction appears to have been processed more "
            "than once."
        )
        action = (
            "Compare transaction identifiers and settlement records "
            "before approving any adjustment."
        )
        confidence = 0.90
        review = "REQUIRED"

    elif exception_type == "Fee Mismatch":
        reason = (
            "The settlement deduction does not match the expected "
            "processing fee."
        )
        action = (
            "Compare the recorded fee with the applicable payment "
            "fee and tax."
        )
        confidence = 0.88
        review = "REQUIRED"

    elif exception_type == "Date Mismatch":
        reason = (
            "The settlement date differs significantly from the "
            "expected settlement timeline."
        )
        action = (
            "Check settlement batch timing, holidays, delays, and "
            "bank processing records."
        )
        confidence = 0.91
        review = "REQUIRED"

    else:
        reason = (
            "The system detected an unexpected difference that "
            "requires investigation."
        )
        action = (
            "Review the transaction, payment, and settlement records."
        )
        confidence = 0.70
        review = "REQUIRED"

    return {
        "transaction_id": transaction_id,
        "type": exception_type,
        "order_amount": order_amount,
        "expected_settlement": expected_settlement,
        "actual_settlement": settlement_amount,
        "difference": difference,
        "likely_reason": reason,
        "recommended_action": action,
        "confidence": confidence,
        "human_review": review
    }


with open("exceptions.csv", "r") as file:
    exceptions = csv.DictReader(file)

    investigations = []

    for exception in exceptions:
        investigation = investigate_exception(exception)
        investigations.append(investigation)


with open("investigations.csv", "w", newline="") as file:

    fieldnames = [
        "transaction_id",
        "type",
        "order_amount",
        "expected_settlement",
        "actual_settlement",
        "difference",
        "likely_reason",
        "recommended_action",
        "confidence",
        "human_review"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for investigation in investigations:
        writer.writerow(investigation)


print("\n======================================")
print("       EXCEPTION INVESTIGATOR")
print("======================================")

print("Exceptions investigated:", len(investigations))
print("Investigation file created: investigations.csv")

print("\n---------- SAMPLE INVESTIGATIONS ----------")

for investigation in investigations[:5]:

    print("\nTransaction:", investigation["transaction_id"])
    print("Type:", investigation["type"])
    print("Difference: ₹", investigation["difference"])
    print("Likely reason:", investigation["likely_reason"])
    print("Recommended action:", investigation["recommended_action"])
    print(
        "Confidence:",
        investigation["confidence"] * 100,
        "%"
    )
    print("Human review:", investigation["human_review"])