from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.core.config import settings
from app.repositories.lessons import LessonsRepo
from app.repositories.users import UsersRepo

XP = settings.xp_per_correct

class LessonsService:
    @staticmethod
    async def list_with_progress(session: AsyncSession, user_id: int):
        return await LessonsRepo.list_with_progress(session, user_id)

    @staticmethod
    async def get_lesson(session: AsyncSession, lesson_id: int):
        return await LessonsRepo.get_lesson_playable(session, lesson_id)

    @staticmethod
    async def submit(session: AsyncSession, user_id: int, lesson_id: int, attempt_id: str, answers: list[dict]):
        correct, total = await LessonsRepo.grade_inputs(session, lesson_id, answers)
        earned = correct * XP
        activity = datetime.now(timezone.utc)

        res = await UsersRepo.apply_submission_effects(
            session,
            user_id=user_id, lesson_id=lesson_id, attempt_id=str(attempt_id),
            correct_count=correct, earned_xp=earned, activity_at=activity
        )

        if res == "duplicate":
            pass

        await LessonsRepo.upsert_progress(session, user_id, lesson_id, correct, total)

        user = await UsersRepo.get_user(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail={"error": "NotFound"})
        progress = (await LessonsRepo.list_with_progress(session, user_id))
        lp = next((p for p in progress if p["id"] == lesson_id), None)
        return {
            "correct_count": correct,
            "earned_xp": earned,
            "new_total_xp": user.total_xp,
            "streak": {"current": user.current_streak, "best": user.best_streak},
            "lesson_progress": float(lp["progress"]) if lp else 0.0
        }
