def format_regression_report(result: dict) -> str:
    status = "Regression detected" if result["regression"] else "No regression detected"

    return (
        "## Benchmark Guardian Report\n\n"
        f"**Status:** {status}\n\n"
        f"- Baseline: `{result['baseline']}`\n"
        f"- Current: `{result['current']}`\n"
        f"- Change: `{result['change_percent']:.2f}%`\n"
        f"- Regression: `{result['regression']}`\n"
    )
