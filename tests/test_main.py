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
