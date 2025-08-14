from datetime import datetime, timezone

def to_utc_date_only(dt: datetime) -> datetime:
    dt = dt.astimezone(timezone.utc)
    return datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)

def days_between(a: datetime, b: datetime) -> int:
    return int((to_utc_date_only(b) - to_utc_date_only(a)).days)