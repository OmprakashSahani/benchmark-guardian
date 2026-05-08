def calculate_change_percent(baseline: float, current: float) -> float:
    if baseline == 0:
        raise ValueError("baseline must not be zero")

    return ((current - baseline) / baseline) * 100


def detect_regression(
    baseline: float,
    current: float,
    threshold_percent: float = 5.0,
) -> dict:
    change_percent = calculate_change_percent(baseline, current)

    return {
        "baseline": baseline,
        "current": current,
        "change_percent": change_percent,
        "regression": change_percent > threshold_percent,
    }
