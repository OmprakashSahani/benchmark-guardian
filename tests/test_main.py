from fastapi.testclient import TestClient

from app.main import app
import hashlib
import hmac
import json


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"healthy": True}


def test_webhook_endpoint_receives_event():
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 42,
            "title": "Improve benchmark engine",
        },
        "repository": {
            "full_name": "OmprakashSahani/benchmark-guardian",
        },
    }

    payload_bytes = json.dumps(payload).encode()

    signature = "sha256=" + hmac.new(
        "benchmark-guardian-secret".encode(),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()

    response = client.post(
        "/webhook",
        headers={
            "X-GitHub-Event": "pull_request",
            "X-Hub-Signature-256": signature,
            "Content-Type": "application/json",
        },
        content=payload_bytes,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["event"] == "pull_request"
    assert body["pull_request"]["pr_number"] == 42
    assert body["analysis"]["regression"] is True
    assert body["analysis"]["severity"] == "medium"
    assert "Benchmark Guardian Report" in body["report"]


def test_analyze_endpoint_detects_regression():
    response = client.post(
        "/analyze",
        json={
            "baseline": 100.0,
            "current": 112.0,
            "threshold_percent": 5.0,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["analysis"] == {
    "baseline": 100.0,
    "current": 112.0,
    "change_percent": 12.0,
    "regression": True,
    "severity": "medium",
}

    assert "Benchmark Guardian Report" in body["report"]
    assert "Regression detected" in body["report"]
    assert "12.00%" in body["report"]