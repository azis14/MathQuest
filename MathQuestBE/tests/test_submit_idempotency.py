import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unittest.mock import AsyncMock, ANY
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
import app.api.routes_lessons as routes

client = TestClient(app)

def test_submit_success_mock(monkeypatch):
    payload = {
        "correct_count": 2,
        "earned_xp": 20,
        "new_total_xp": 120,
        "streak": {"current": 3, "best": 5},
        "lesson_progress": 0.6,
    }
    mock = AsyncMock(return_value=payload)
    monkeypatch.setattr(routes.LessonsService, "submit", mock)

    body = {
        "attempt_id": "c1b0b2a0-2a6e-4a7a-bb3a-1d6f5a8f2e91",
        "answers": [
            {"problem_id": 1, "option_id": 3},
            {"problem_id": 2, "option_id": 2},
        ],
    }

    r = client.post("/api/lessons/1/submit", json=body)

    assert r.status_code == 200
    assert r.json() == payload
    
    mock.assert_awaited_once()
    
    called_args, called_kwargs = mock.await_args
    assert called_args[2] == 1
    assert called_args[3] == body["attempt_id"]

def test_submit_duplicate_mock(monkeypatch):
    async def fake_submit(*args, **kwargs):
        raise HTTPException(status_code=409, detail={
            "error": "DuplicateAttempt",
            "message": "This attempt_id was already processed"
        })

    monkeypatch.setattr(routes.LessonsService, "submit", fake_submit)

    body = {
        "attempt_id": "c1b0b2a0-2a6e-4a7a-bb3a-1d6f5a8f2e91",
        "answers": [{"problem_id": 1, "option_id": 3}],
    }

    r = client.post("/api/lessons/1/submit", json=body)

    assert r.status_code == 409
    assert r.json()["detail"]["error"] == "DuplicateAttempt"

def test_validation_short_circuits_before_service(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr(routes.LessonsService, "submit", mock)

    body = {"attempt_id": "c1b0b2a0-2a6e-4a7a-bb3a-1d6f5a8f2e91", "answers": []}
    r = client.post("/api/lessons/1/submit", json=body)

    assert r.status_code == 400
    assert r.json()["detail"]["error"] == "Validation"
    mock.assert_not_awaited()

