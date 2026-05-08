from fastapi import FastAPI, Request
from app.services.benchmark import detect_regression
from app.services.report import format_regression_report

app = FastAPI()


@app.get("/")
def root():
    return {
        "app": "Benchmark Guardian",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "healthy": True
    }


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    event = request.headers.get("X-GitHub-Event", "unknown")

    print(f"Received GitHub event: {event}")

    return {
        "received": True,
        "event": event
    }


@app.post("/analyze")
async def analyze_benchmark(payload: dict):
    result = detect_regression(
        baseline=payload["baseline"],
        current=payload["current"],
        threshold_percent=payload.get("threshold_percent", 5.0),
    )

    report = format_regression_report(result)

    return {
        "analysis": result,
        "report": report,
    }
