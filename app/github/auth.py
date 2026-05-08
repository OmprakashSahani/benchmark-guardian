import os
import time

import jwt
import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID", "")
PRIVATE_KEY_PATH = "benchmark_guardian_private_key.pem"


def create_jwt() -> str:
    with open(PRIVATE_KEY_PATH, "r", encoding="utf-8") as key_file:
        private_key = key_file.read()

    now = int(time.time())

    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),
        "iss": GITHUB_APP_ID,
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_access_token(installation_id: int) -> str:
    app_jwt = create_jwt()

    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Authorization": f"Bearer {app_jwt}",
            "Accept": "application/vnd.github+json",
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()["token"]
