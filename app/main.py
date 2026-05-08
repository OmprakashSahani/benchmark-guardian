from fastapi import FastAPI, Request

from app.db.database import initialize_database
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
from app.services.benchmark import detect_regression
from app.services.report import format_regression_report

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
    payload = await request.json()

    event = request.headers.get("X-GitHub-Event", "unknown")

    if event == "pull_request":
        pr_data = parse_pull_request_event(payload)

        benchmark_result = detect_regression(
            baseline=100.0,
            current=112.0,
            threshold_percent=5.0,
        )

        report = format_regression_report(benchmark_result)

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
        "runs": get_benchmark_runs()
    }