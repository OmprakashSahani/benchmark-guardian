from fastapi import FastAPI, Request

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
