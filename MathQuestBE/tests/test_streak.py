import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datetime import datetime, timezone
from app.services.streak import next_streak

d = lambda s: datetime.fromisoformat(s).astimezone(timezone.utc)

def test_first_activity():
    cur, best, _ = next_streak(0, 0, None, d("2025-08-12T10:00:00+00:00"))
    assert cur == 1 and best == 1

def test_next_day_increments():
    cur, best, _ = next_streak(1, 1, d("2025-08-11T00:00:00+00:00"), d("2025-08-12T08:00:00+00:00"))
    assert cur == 2 and best == 2

def test_same_day_unchanged():
    cur, best, _ = next_streak(2, 3, d("2025-08-12T00:00:00+00:00"), d("2025-08-12T23:59:00+00:00"))
    assert cur == 2 and best == 3
