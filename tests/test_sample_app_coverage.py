
from coverage import Coverage
from src.sample_app import sample_target


def test_sample_app_coverage():
    cov = Coverage(
        branch=True,
        source=["src.sample_app"],
        data_file=None,
    )

    cov.start()

    sample_target(0, "ID1")
    sample_target(-1, "ID2")
    sample_target(10, "")
    sample_target(10, "ID4")

    cov.stop()
    cov.save()

    analysis = cov.analysis2(sample_target.__code__.co_filename)

    statements = set(analysis[1])
    missing_statements = set(analysis[3])
    executed_statements = statements - missing_statements

    coverage_percentage = (
        100 * len(executed_statements) / len(statements)
        if statements
        else 100
    )

    assert coverage_percentage > 0
    print(f"\nSample app statement coverage: {coverage_percentage:.1f}%")
