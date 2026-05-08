from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"healthy": True}


def test_webhook_endpoint_receives_event():
    response = client.post(
        "/webhook",
        headers={"X-GitHub-Event": "pull_request"},
        json={"action": "opened"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "received": True,
        "event": "pull_request",
    }


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