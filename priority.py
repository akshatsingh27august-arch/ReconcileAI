import csv


def calculate_priority(exception_type, difference):

    difference = abs(float(difference))

    # Critical operational exceptions
    if exception_type == "Missing Settlement":
        return "HIGH", "Immediate human review"

    if exception_type == "Duplicate Transaction":
        return "HIGH", "Verify duplicate before settlement"

    # Date and fee issues require investigation
    if exception_type == "Date Mismatch":
        return "MEDIUM", "Investigate settlement timing"

    if exception_type == "Fee Mismatch":
        return "MEDIUM", "Verify processing fee"

    # Amount mismatch based on financial exposure
    if exception_type == "Amount Mismatch":

        if difference > 500:
            return "HIGH", "Immediate finance investigation"

        if difference > 100:
            return "MEDIUM", "Finance team review"

        return "LOW", "Batch review recommended"

    # Fallback for unexpected exception types
    if difference > 500:
        return "HIGH", "Immediate finance investigation"

    if difference > 100:
        return "MEDIUM", "Finance team review"

    return "LOW", "Batch review recommended"


# Read reconciliation exceptions
with open("exceptions.csv", "r") as file:

    exceptions = csv.DictReader(file)

    priority_records = []

    for exception in exceptions:

        priority, recommended_action = calculate_priority(
            exception["type"],
            exception["difference"]
        )

        priority_records.append({
            "transaction_id": exception["transaction_id"],
            "type": exception["type"],
            "difference": exception["difference"],
            "priority": priority,
            "recommended_action": recommended_action
        })


# Save prioritized exceptions
with open("prioritized_exceptions.csv", "w", newline="") as file:

    fieldnames = [
        "transaction_id",
        "type",
        "difference",
        "priority",
        "recommended_action"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for record in priority_records:
        writer.writerow(record)


# Count priorities
high = 0
medium = 0
low = 0

for record in priority_records:

    if record["priority"] == "HIGH":
        high += 1

    elif record["priority"] == "MEDIUM":
        medium += 1

    else:
        low += 1


# Display report
print("\n======================================")
print("       EXCEPTION PRIORITY REPORT")
print("======================================")

print("Total exceptions :", len(priority_records))
print("HIGH             :", high)
print("MEDIUM           :", medium)
print("LOW              :", low)

print("\nPriority file created:")
print("prioritized_exceptions.csv")

print("\n---------- SAMPLE RESULTS ----------")

for record in priority_records[:10]:

    print(
        record["transaction_id"],
        "|",
        record["type"],
        "| ₹",
        record["difference"],
        "|",
        record["priority"],
        "|",
        record["recommended_action"]
    )