from app.analysis.multimetric import (
    analyze_benchmark_metrics,
)


def test_analyze_benchmark_metrics():
    baseline = {
        "latency_ms": 100,
        "memory_mb": 2048,
        "throughput": 512,
    }

    current = {
        "latency_ms": 118,
        "memory_mb": 2500,
        "throughput": 470,
    }

    result = analyze_benchmark_metrics(
        baseline,
        current,
    )

    assert result["regression_detected"] is True
    assert len(result["metrics"]) == 3

    latency_metric = result["metrics"][0]

    assert latency_metric["metric"] == "latency_ms"
    assert latency_metric["severity"] == "high"
