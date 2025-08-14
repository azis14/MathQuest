from datetime import datetime
from app.utils.date_utils import to_utc_date_only, days_between

def next_streak(current: int, best: int, last_activity: datetime | None, activity_at: datetime) -> tuple[int, int, datetime]:
    today = to_utc_date_only(activity_at)
    if last_activity is None:
        cur = 1
        return cur, max(cur, best), today
    diff = days_between(last_activity, today)
    if diff == 0:
        return current, best, last_activity
    if diff == 1:
        cur = current + 1
        return cur, max(cur, best), today
    cur = 1
    return cur, max(cur, best), today
