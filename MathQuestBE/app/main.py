from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_lessons import router as lessons_router
from app.api.routes_profile import router as profile_router

app = FastAPI(title="MathQuest API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(lessons_router)
app.include_router(profile_router)
