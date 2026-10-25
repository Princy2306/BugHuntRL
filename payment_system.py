
def process_payment(amount, payment_id):
    # Reject negative payment amounts
    if amount < 0:
        return {
            "status": "error",
            "bug_ids": []
        }

    # Deliberate bug: zero-value payments are accepted
    if amount == 0:
        return {
            "status": "success",
            "bug_ids": ["ZERO_PAYMENT"]
        }

    # Reject missing payment IDs
    if not payment_id:
        return {
            "status": "error",
            "bug_ids": []
        }

    # Process normal payments
    return {
        "status": "success",
        "bug_ids": []
    }
