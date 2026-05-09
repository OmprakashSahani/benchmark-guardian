from fastapi import FastAPI, Request

from app.analysis.multimetric import analyze_benchmark_metrics
from app.db.database import initialize_database
from app.github.auth import get_installation_access_token
from app.github.comments import post_pull_request_comment
from app.github.parser import parse_pull_request_event
from app.models.benchmark import (
    AnalyzeResponse,
    BenchmarkAnalysis,
    BenchmarkRequest,
)
from app.repositories.benchmark_repository import (
    get_benchmark_runs,
    save_benchmark_run,
)
from app.security.webhook import verify_github_signature
from app.services.benchmark import detect_regression
from app.services.report import (
    format_multi_metric_report,
    format_regression_report,
)

app = FastAPI()

initialize_database()


@app.get("/")
def root():
    return {
        "app": "Benchmark Guardian",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "healthy": True,
    }


@app.post("/webhook")
async def github_webhook(request: Request):
    payload_bytes = await request.body()

    signature = request.headers.get("X-Hub-Signature-256", "")

    if not verify_github_signature(payload_bytes, signature):
        print("Invalid webhook signature")

        return {
            "error": "invalid webhook signature",
        }

    payload = await request.json()
    event = request.headers.get("X-GitHub-Event", "unknown")

    print(f"Received event: {event}")
    print(f"Payload action: {payload.get('action')}")

    if event == "pull_request":
        pr_data = parse_pull_request_event(payload)

        print(f"PR data: {pr_data}")

        baseline_metrics = {
            "latency_ms": 100,
            "memory_mb": 2048,
            "throughput": 512,
        }

        current_metrics = {
            "latency_ms": 118,
            "memory_mb": 2500,
            "throughput": 470,
        }

        benchmark_result = analyze_benchmark_metrics(
            baseline_metrics,
            current_metrics,
        )

        report = format_multi_metric_report(
            benchmark_result,
        )

        access_token = get_installation_access_token(
            pr_data["installation_id"],
        )

        comment_response = post_pull_request_comment(
            repository_name=pr_data["repository_name"],
            pull_request_number=pr_data["pr_number"],
            comment_body=report,
            access_token=access_token,
        )

        print(f"Comment posted: {comment_response.get('html_url')}")

        return {
            "event": event,
            "pull_request": pr_data,
            "analysis": benchmark_result,
            "report": report,
        }

    return {
        "received": True,
        "event": event,
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_benchmark(payload: BenchmarkRequest):
    result = detect_regression(
        baseline=payload.baseline,
        current=payload.current,
        threshold_percent=payload.threshold_percent,
    )

    report = format_regression_report(result)

    save_benchmark_run(result)

    return {
        "analysis": BenchmarkAnalysis(**result),
        "report": report,
    }


@app.get("/benchmarks")
async def get_benchmarks():
    return {
        "runs": get_benchmark_runs(),
    }