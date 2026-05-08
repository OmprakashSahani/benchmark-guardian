from app.github.parser import parse_pull_request_event


def test_parse_pull_request_event():
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 42,
            "title": "Improve benchmark engine",
        },
        "repository": {
            "full_name": "OmprakashSahani/benchmark-guardian",
        },
        "installation": {
            "id": 123456,
        },
    }

    result = parse_pull_request_event(payload)

    assert result == {
        "action": "opened",
        "pr_number": 42,
        "pr_title": "Improve benchmark engine",
        "repository_name": "OmprakashSahani/benchmark-guardian",
        "installation_id": 123456,
    }
