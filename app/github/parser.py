def parse_pull_request_event(payload: dict) -> dict:
    pull_request = payload.get("pull_request", {})
    repository = payload.get("repository", {})
    installation = payload.get("installation", {})

    return {
        "action": payload.get("action"),
        "pr_number": pull_request.get("number"),
        "pr_title": pull_request.get("title"),
        "repository_name": repository.get("full_name"),
        "installation_id": installation.get("id"),
    }
