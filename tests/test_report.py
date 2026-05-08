from app.services.report import (
    format_multi_metric_report,
    format_regression_report,
)


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


def test_format_multi_metric_report():
    result = {
        "regression_detected": True,
        "metrics": [
            {
                "metric": "latency_ms",
                "baseline": 100,
                "current": 118,
                "change_percent": 18.0,
                "regression": True,
                "severity": "high",
            },
            {
                "metric": "throughput",
                "baseline": 512,
                "current": 470,
                "change_percent": -8.2,
                "regression": False,
                "severity": "medium",
            },
        ],
    }

    report = format_multi_metric_report(result)

    assert "Benchmark Guardian Report" in report
    assert "Regression detected" in report
    assert "latency_ms" in report
    assert "throughput" in report
    assert "18.00%" in report
    assert "-8.20%" in report
    assert "| Metric | Baseline | Current | Change | Severity | Regression |" in report
