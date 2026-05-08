def format_regression_report(result: dict) -> str:
    severity = result["severity"]

    severity_icon = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴",
    }.get(severity, "⚪")

    status = (
        "Regression detected"
        if result["regression"]
        else "No regression detected"
    )

    return (
        "# Benchmark Guardian Report\n\n"
        f"## {severity_icon} Status: {status}\n\n"
        "| Metric | Value |\n"
        "|---|---|\n"
        f"| Baseline | `{result['baseline']}` |\n"
        f"| Current | `{result['current']}` |\n"
        f"| Change | `{result['change_percent']:.2f}%` |\n"
        f"| Severity | `{severity}` |\n"
        f"| Regression | `{result['regression']}` |\n"
    )


def format_multi_metric_report(result: dict) -> str:
    status = (
        "Regression detected"
        if result["regression_detected"]
        else "No regression detected"
    )

    status_icon = "🔴" if result["regression_detected"] else "🟢"

    report = (
        "# Benchmark Guardian Report\n\n"
        f"## {status_icon} Status: {status}\n\n"
        "| Metric | Baseline | Current | Change | Severity | Regression |\n"
        "|---|---:|---:|---:|---|---|\n"
    )

    for metric in result["metrics"]:
        severity_icon = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴",
        }.get(metric["severity"], "⚪")

        report += (
            f"| `{metric['metric']}` "
            f"| `{metric['baseline']}` "
            f"| `{metric['current']}` "
            f"| `{metric['change_percent']:.2f}%` "
            f"| {severity_icon} `{metric['severity']}` "
            f"| `{metric['regression']}` |\n"
        )

    return report
