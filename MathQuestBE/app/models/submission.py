from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (UniqueConstraint("user_id", "attempt_id", name="uq_user_attempt"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    attempt_id: Mapped[str] = mapped_column(String(64))
    correct_count: Mapped[int] = mapped_column(Integer)
    earned_xp: Mapped[int] = mapped_column(Integer)
    created_at_utc: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="submissions")
    lesson = relationship("Lesson")
