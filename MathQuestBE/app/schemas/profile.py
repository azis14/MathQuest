from pydantic import BaseModel

class ProfileOut(BaseModel):
    total_xp: int
    streak: dict
    progress_percentage: int
    lessons_completed: int
    lessons_total: int