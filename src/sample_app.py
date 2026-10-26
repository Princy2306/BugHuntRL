
def sample_target(amount, payment_id):
    """Temporary target application for coverage experiments."""
    bugs = []

    if amount == 0:
        bugs.append("ZERO_VALUE")

    if amount < 0:
        bugs.append("NEGATIVE_VALUE")

    if not payment_id:
        bugs.append("MISSING_ID")

    return {
        "status": "error" if bugs else "success",
        "bug_ids": bugs,
    }
