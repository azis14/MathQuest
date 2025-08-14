from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import asyncio
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.lesson import Lesson
from app.models.problem import Problem, ProblemOption, ProblemType
from app.models.user_progress import UserProgress

async def main():
    async with AsyncSessionLocal() as session:
        user = await session.get(User, 1)
        if not user:
            user = User(id=1, username="demo")
            session.add(user)

        lessons_data = [
            ("Basic Arithmetic","Addition & subtraction",[
                ("MCQ","5 + 7 = ?",[("10",False),("11",False),("12",True),("13",False)],None),
                ("MCQ","9 - 4 = ?",[("3",False),("5",True),("7",False)],None),
                ("INPUT","8 + 6 = ?",[], "14")
            ]),
            ("Multiplication Mastery","Times tables",[
                ("MCQ","3 × 4 = ?",[("7",False),("12",True),("14",False)],None),
                ("INPUT","6 × 7 = ?",[], "42"),
                ("MCQ","9 × 2 = ?",[("18",True),("16",False),("20",False)],None)
            ]),
            ("Division Basics","Simple division",[
                ("INPUT","12 ÷ 3 = ?",[], "4"),
                ("MCQ","15 ÷ 5 = ?",[("2",False),("3",True),("5",False)],None),
                ("MCQ","20 ÷ 4 = ?",[("4",False),("5",True),("6",False)],None)
            ])
        ]

        for title, desc, probs in lessons_data:
            l = Lesson(title=title, description=desc)
            session.add(l)
            await session.flush()
            for t, prompt, opts, correct in probs:
                p = Problem(lesson_id=l.id, type=ProblemType[t], prompt=prompt, correct_value=correct)
                session.add(p); await session.flush()
                for label, is_correct in opts:
                    session.add(ProblemOption(problem_id=p.id, label=label, is_correct=is_correct))
            session.add(UserProgress(user_id=1, lesson_id=l.id, progress=0.0, completed=False))

        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
