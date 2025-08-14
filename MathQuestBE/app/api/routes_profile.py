from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.user_progress import UserProgress
from app.schemas.profile import ProfileOut
from app.core.config import settings

router = APIRouter(prefix="/api/profile", tags=["profile"])
DEMO_USER_ID = settings.demo_user_id

@router.get("", response_model=ProfileOut)
async def get_profile(db: AsyncSession = Depends(get_db)):
    user = await db.get(User, DEMO_USER_ID)
    total_lessons = (await db.execute(select(func.count(Lesson.id)))).scalar_one()
    completed = (await db.execute(
        select(func.count(UserProgress.id)).where(UserProgress.user_id==DEMO_USER_ID, UserProgress.completed==True)
    )).scalar_one()
    avg = (await db.execute(
        select(func.avg(UserProgress.progress)).where(UserProgress.user_id==DEMO_USER_ID)
    )).scalar_one()
    pct = round(100 * float(avg or 0))
    return {
        "total_xp": user.total_xp if user else 0,
        "streak": {"current": user.current_streak if user else 0, "best": user.best_streak if user else 0},
        "progress_percentage": pct,
        "lessons_completed": int(completed or 0),
        "lessons_total": int(total_lessons or 0)
    }
