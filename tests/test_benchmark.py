import pytest

from app.services.benchmark import (
    calculate_change_percent,
    classify_severity,
    detect_regression,
)


def test_calculate_change_percent():
    assert calculate_change_percent(100.0, 110.0) == 10.0


def test_classify_severity_low():
    assert classify_severity(3.0) == "low"


def test_classify_severity_medium():
    assert classify_severity(10.0) == "medium"


def test_classify_severity_high():
    assert classify_severity(20.0) == "high"


def test_detect_regression_true():
    result = detect_regression(100.0, 110.0, threshold_percent=5.0)

    assert result["regression"] is True
    assert result["severity"] == "medium"


def test_detect_regression_false():
    result = detect_regression(100.0, 103.0, threshold_percent=5.0)

    assert result["regression"] is False
    assert result["severity"] == "low"


def test_baseline_zero_raises_error():
    with pytest.raises(ValueError):
        calculate_change_percent(0.0, 100.0)
