from fastapi import APIRouter, Depends, HTTPException, Body
from app.api.deps import get_db
from app.schemas.common import SubmitRequest, SubmitResponse
from app.core.config import settings
from app.services.lessons import LessonsService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/lessons", tags=["lessons"])
DEMO_USER_ID = settings.demo_user_id

@router.get("", summary="List lessons with progress")
async def list_lessons(db: AsyncSession = Depends(get_db)):
    return await LessonsService.list_with_progress(db, DEMO_USER_ID)

@router.get("/{lesson_id}", summary="Get lesson with problems (no correct answers leaked)")
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    lesson = await LessonsService.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail={"error":"NotFound", "message":"Lesson not found"})
    return lesson

@router.post("/{lesson_id}/submit", response_model=SubmitResponse)
async def submit_answers(lesson_id: int, payload: SubmitRequest = Body(...), db: AsyncSession = Depends(get_db)):
    if not payload.answers:
        raise HTTPException(status_code=400, detail={"error":"Validation","message":"answers must be non-empty"})
    try:
        return await LessonsService.submit(db, DEMO_USER_ID, lesson_id, str(payload.attempt_id), [a.model_dump() for a in payload.answers])
    except ValueError as e:
        msg = str(e)
        if msg.startswith("InvalidProblem:"):
            pid = msg.split(":")[1]
            raise HTTPException(status_code=422, detail={"error":"InvalidProblem","message":f"Problem {pid} not found"})
        if msg.startswith("InvalidOption:"):
            oid = msg.split(":")[1]
            raise HTTPException(status_code=422, detail={"error":"InvalidOption","message":f"Option {oid} not found"})
        raise
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail={"error":"Validation","message":str(e).replace('Validation:','')})
    except Exception:
        raise HTTPException(status_code=409, detail={"error":"DuplicateAttempt","message":"This attempt_id was already processed"})
