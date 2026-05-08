from app.services.report import format_regression_report


def test_format_regression_report():
    result = {
        "baseline": 100.0,
        "current": 112.0,
        "change_percent": 12.0,
        "regression": True,
        "severity": "medium",
    }

    report = format_regression_report(result)

    assert "Benchmark Guardian Report" in report
    assert "Regression detected" in report
    assert "12.00%" in report
    assert "medium" in report
    assert "| Metric | Value |" in report