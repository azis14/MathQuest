from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lesson import Lesson
from app.models.problem import Problem, ProblemOption
from app.models.user_progress import UserProgress

class LessonsRepo:
    @staticmethod
    async def list_with_progress(session: AsyncSession, user_id: int):
        lessons = (await session.execute(select(Lesson))).scalars().all()
        # prefetch counts
        problem_counts = {
            l.id: (await session.execute(select(Problem).where(Problem.lesson_id==l.id))).scalars().all()
            for l in lessons
        }
        progress_rows = (await session.execute(select(UserProgress).where(UserProgress.user_id==user_id))).scalars().all()
        prog_map = { (p.lesson_id): p for p in progress_rows }
        out = []
        for l in lessons:
            probs = problem_counts[l.id]
            p = prog_map.get(l.id)
            out.append({
                "id": l.id, "title": l.title, "description": l.description,
                "total_problems": len(probs), "progress": float(p.progress) if p else 0.0,
                "completed": bool(p.completed) if p else False
            })
        return out

    @staticmethod
    async def get_lesson_playable(session: AsyncSession, lesson_id: int):
        l = await session.get(Lesson, lesson_id)
        if not l: return None
        # fetch problems + options
        probs = (await session.execute(select(Problem).where(Problem.lesson_id==lesson_id))).scalars().all()
        out_probs = []
        for p in probs:
            if p.type.name == "MCQ":
                opts = (await session.execute(select(ProblemOption).where(ProblemOption.problem_id==p.id))).scalars().all()
                out_probs.append({"id": p.id, "type": p.type.value, "prompt": p.prompt,
                                  "options": [{"id": o.id, "label": o.label} for o in opts]})
            else:
                out_probs.append({"id": p.id, "type": p.type.value, "prompt": p.prompt, "options": None})
        return {"id": l.id, "title": l.title, "description": l.description, "problems": out_probs}

    @staticmethod
    async def grade_inputs(session: AsyncSession, lesson_id: int, answers: list[dict]) -> tuple[int, int]:
        # returns (correct_count, total)
        probs = (await session.execute(select(Problem).where(Problem.lesson_id==lesson_id))).scalars().all()
        by_id = { p.id: p for p in probs }
        # also pull options once
        options = (await session.execute(select(ProblemOption))).scalars().all()
        opts_by_problem = {}
        for o in options:
            opts_by_problem.setdefault(o.problem_id, []).append(o)

        correct = 0
        for a in answers:
            pid = a["problem_id"]
            p = by_id.get(pid)
            if not p:
                raise ValueError(f"InvalidProblem:{pid}")
            if p.type.name == "MCQ":
                option_id = a.get("option_id")
                if option_id is None:
                    raise RuntimeError("Validation:option_id required")
                if not any(o.id == option_id for o in opts_by_problem.get(pid, [])):
                    raise ValueError(f"InvalidOption:{option_id}")
                if any(o.id == option_id and o.is_correct for o in opts_by_problem.get(pid, [])):
                    correct += 1
            else:
                val = a.get("value")
                if val is None:
                    raise RuntimeError("Validation:value required")
                if (p.correct_value or "").strip() == str(val).strip():
                    correct += 1
        return correct, len(probs)

    @staticmethod
    async def upsert_progress(session: AsyncSession, user_id: int, lesson_id: int, correct: int, total: int):
        ratio = 0.0 if total == 0 else correct / total
        completed = ratio >= 0.999
        row = (await session.execute(
            select(UserProgress).where(UserProgress.user_id==user_id, UserProgress.lesson_id==lesson_id)
        )).scalar_one_or_none()
        if row:
            row.progress = ratio
            row.completed = completed
        else:
            row = UserProgress(user_id=user_id, lesson_id=lesson_id, progress=ratio, completed=completed)
            session.add(row)
