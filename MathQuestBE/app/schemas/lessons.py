from pydantic import BaseModel

class ProblemOptionOut(BaseModel):
    id: int
    label: str

class ProblemOut(BaseModel):
    id: int
    type: str
    prompt: str
    options: list[ProblemOptionOut] | None = None

class LessonOut(BaseModel):
    id: int
    title: str
    description: str
    problems: list[ProblemOut]

class LessonListItem(BaseModel):
    id: int
    title: str
    description: str
    total_problems: int
    progress: float
    completed: bool
