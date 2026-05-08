import pytest

from app.services.benchmark import calculate_change_percent, detect_regression


def test_calculate_change_percent():
    assert calculate_change_percent(100.0, 110.0) == 10.0


def test_detect_regression_true():
    result = detect_regression(100.0, 110.0, threshold_percent=5.0)

    assert result["regression"] is True


def test_detect_regression_false():
    result = detect_regression(100.0, 103.0, threshold_percent=5.0)

    assert result["regression"] is False


def test_baseline_zero_raises_error():
    with pytest.raises(ValueError):
        calculate_change_percent(0.0, 100.0)
