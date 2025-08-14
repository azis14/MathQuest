from sqlalchemy import ForeignKey, Enum, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class ProblemType(str, enum.Enum):
    MCQ = "MCQ"
    INPUT = "INPUT"

class Problem(Base):
    __tablename__ = "problems"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    type: Mapped[ProblemType] = mapped_column(Enum(ProblemType))
    prompt: Mapped[str] = mapped_column(String(256))
    correct_value: Mapped[str | None] = mapped_column(String(64), nullable=True)  # for INPUT

    lesson = relationship("Lesson", back_populates="problems")
    options = relationship("ProblemOption", back_populates="problem", cascade="all, delete-orphan")

class ProblemOption(Base):
    __tablename__ = "problem_options"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id", ondelete="CASCADE"), index=True)
    label: Mapped[str] = mapped_column(String(128))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    problem = relationship("Problem", back_populates="options")
