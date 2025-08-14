from pydantic import BaseModel, Field, UUID4
from typing import Optional, Union

class Answer(BaseModel):
    problem_id: int = Field(gt=0)
    option_id: Optional[int] = Field(default=None, gt=0)
    value: Optional[Union[str, int]] = None

class SubmitRequest(BaseModel):
    attempt_id: UUID4
    answers: list[Answer]

class SubmitResponse(BaseModel):
    correct_count: int
    earned_xp: int
    new_total_xp: int
    streak: dict
    lesson_progress: float
