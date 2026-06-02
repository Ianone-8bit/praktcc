# ============ FILE: medication-service/app/services/push_service.py ============
import os
from typing import List

import firebase_admin
from firebase_admin import credentials, messaging


_app = None


def _init_app():
    global _app
    if _app:
        return _app

    cred_path = os.getenv("FCM_SERVICE_ACCOUNT", "credentials/firebase-service-account.json")
    if not os.path.exists(cred_path):
        return None

    try:
        cred = credentials.Certificate(cred_path)
        _app = firebase_admin.initialize_app(cred)
        return _app
    except Exception:
        return None


def send_push(tokens: List[str], title: str, body: str, data: dict) -> List[str]:
    app = _init_app()
    if not app or not tokens:
        return []

    message = messaging.MulticastMessage(
        tokens=tokens,
        notification=messaging.Notification(title=title, body=body),
        data={k: str(v) for k, v in data.items()},
    )

    response = messaging.send_multicast(message, app=app)

    invalid_tokens = []
    for idx, resp in enumerate(response.responses):
        if resp.success:
            continue
        err = resp.exception
        if isinstance(err, messaging.UnregisteredError):
            invalid_tokens.append(tokens[idx])

    return invalid_tokens
