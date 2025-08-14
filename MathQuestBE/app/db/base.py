from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models import user, lesson, problem, submission, user_progress

__all__ = ["Base"]
