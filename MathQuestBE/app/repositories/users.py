from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.user import User
from app.models.submission import Submission
from app.services.streak import next_streak

class UsersRepo:
    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def apply_submission_effects(
        session: AsyncSession,
        *,
        user_id: int,
        lesson_id: int,
        attempt_id: str,
        correct_count: int,
        earned_xp: int,
        activity_at: datetime
    ) -> Submission | str:
        submission = Submission(
            user_id=user_id, lesson_id=lesson_id, attempt_id=attempt_id,
            correct_count=correct_count, earned_xp=earned_xp, created_at_utc=activity_at
        )
        session.add(submission)
        try:
            await session.flush()  # tries to insert (can raise IntegrityError)
        except IntegrityError:
            await session.rollback()
            # Fetch the existing submission
            existing = (await session.execute(
                select(Submission).where(Submission.user_id==user_id, Submission.attempt_id==attempt_id)
            )).scalar_one()
            return "duplicate"

        # If we got here → new submission, apply XP & streak
        user = await session.get(User, user_id)
        assert user
        cur, best, last_date = next_streak(user.current_streak, user.best_streak, user.last_activity_utc_date, activity_at)
        user.total_xp = (user.total_xp or 0) + earned_xp
        user.current_streak = cur
        user.best_streak = best
        user.last_activity_utc_date = last_date
        return submission
