import requests


def post_pull_request_comment(
    repository_name: str,
    pull_request_number: int,
    comment_body: str,
    access_token: str,
) -> dict:
    response = requests.post(
        f"https://api.github.com/repos/{repository_name}/issues/{pull_request_number}/comments",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github+json",
        },
        json={
            "body": comment_body,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
