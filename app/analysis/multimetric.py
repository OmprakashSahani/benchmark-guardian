def calculate_percent_change(baseline: float, current: float) -> float:
    if baseline == 0:
        raise ValueError("baseline must not be zero")

    return ((current - baseline) / baseline) * 100


def classify_metric_severity(change_percent: float) -> str:
    absolute_change = abs(change_percent)

    if absolute_change < 5:
        return "low"

    if absolute_change < 15:
        return "medium"

    return "high"


def analyze_metric(
    metric_name: str,
    baseline_value: float,
    current_value: float,
) -> dict:
    change_percent = calculate_percent_change(
        baseline_value,
        current_value,
    )

    regression = change_percent > 5

    return {
        "metric": metric_name,
        "baseline": baseline_value,
        "current": current_value,
        "change_percent": round(change_percent, 2),
        "regression": regression,
        "severity": classify_metric_severity(change_percent),
    }


def analyze_benchmark_metrics(
    baseline_metrics: dict,
    current_metrics: dict,
) -> dict:
    metric_results = []

    for metric_name, baseline_value in baseline_metrics.items():
        current_value = current_metrics[metric_name]

        metric_results.append(
            analyze_metric(
                metric_name,
                baseline_value,
                current_value,
            )
        )

    regression_detected = any(
        metric["regression"]
        for metric in metric_results
    )

    return {
        "metrics": metric_results,
        "regression_detected": regression_detected,
    }
