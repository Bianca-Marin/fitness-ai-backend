"""
FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for interactive API docs (Swagger UI) —
useful for demoing this to your supervisor without building the frontend yet.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import users, profiles, exercises, programmes

# Creates tables if they don't exist yet. Fine for an MVP/dissertation project;
# a production app would use Alembic migrations instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Explainable AI Fitness Recommender — API",
    description="Backend for the personalised strength-training recommendation system (QHO656).",
    version="0.1.0",
)

# Allow the React frontend (running on a different port during development) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(exercises.router)
app.include_router(programmes.router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Fitness AI backend is running"}
