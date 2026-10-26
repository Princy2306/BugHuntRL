
from src.testing_engine import TestingEngine
from src.sample_app import sample_target

import pytest


def sample_target(amount, payment_id):
    """Temporary target for testing the engine."""
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


def test_random_strategy():
    engine = TestingEngine(sample_target, seed=42)
    report = engine.run(strategy=0)

    assert report["tests_executed"] == 10
    assert "new_bug_ids" in report


def test_boundary_strategy():
    engine = TestingEngine(sample_target, seed=42)
    report = engine.run(strategy=1)

    assert report["tests_executed"] == 8
    assert "ZERO_VALUE" in report["new_bug_ids"]
    assert "NEGATIVE_VALUE" in report["new_bug_ids"]


def test_mutation_strategy():
    engine = TestingEngine(sample_target, seed=42)
    report = engine.run(strategy=2)

    assert report["tests_executed"] == 6
    assert "new_bug_ids" in report


def test_sequence_strategy():
    engine = TestingEngine(sample_target, seed=42)
    report = engine.run(strategy=3)

    assert report["tests_executed"] == 3
    assert "ZERO_VALUE" in report["new_bug_ids"]





@pytest.mark.parametrize("strategy", [-1, 4, 5, 6, 100])
def test_invalid_strategy(strategy):
    engine = TestingEngine(sample_target)

    with pytest.raises(
        ValueError,
        match="Strategy must be between 0 and 3\\."
    ):
        engine.run(strategy=strategy)



def test_insufficient_budget():
    engine = TestingEngine(sample_target)

    with pytest.raises(
        ValueError,
        match="Insufficient budget for this strategy\\."
    ):
        engine.run(strategy=1, budget=5)



def test_target_exception_is_recorded():
    def crashing_target(amount, payment_id):
        if amount == 0:
            raise RuntimeError("Simulated crash")

        return {"status": "success", "bug_ids": []}

    engine = TestingEngine(crashing_target, seed=42)
    report = engine.run(strategy=1)

    errors = [
        result for result in report["results"]
        if result["error"] is not None
    ]

    assert len(errors) > 0
    assert "RuntimeError: Simulated crash" in errors[0]["error"]



def test_duplicate_bugs_are_not_reported_as_new():
    engine = TestingEngine(sample_target, seed=42)

    first_report = engine.run(strategy=1)
    second_report = engine.run(strategy=1)

    assert "ZERO_VALUE" in first_report["new_bug_ids"]
    assert "NEGATIVE_VALUE" in first_report["new_bug_ids"]

    assert second_report["new_bug_ids"] == []




