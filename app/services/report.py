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
