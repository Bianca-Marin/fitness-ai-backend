from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/", response_model=schemas.ExerciseOut, status_code=201)
def create_exercise(payload: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    """Mainly used by seed_data.py to populate the exercise catalogue."""
    existing = db.query(models.Exercise).filter(models.Exercise.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Exercise with this name already exists")

    exercise = models.Exercise(**payload.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.get("/", response_model=List[schemas.ExerciseOut])
def list_exercises(
    muscle_group: Optional[str] = None,
    equipment_required: Optional[models.EquipmentEnum] = None,
    difficulty_level: Optional[models.ExperienceEnum] = None,
    db: Session = Depends(get_db),
):
    """
    List exercises, optionally filtered — this is the query the Milestone 2
    rule-based filter will build on (goal/equipment/experience/safety).
    """
    query = db.query(models.Exercise)
    if muscle_group:
        query = query.filter(models.Exercise.muscle_group == muscle_group)
    if equipment_required:
        query = query.filter(models.Exercise.equipment_required == equipment_required)
    if difficulty_level:
        query = query.filter(models.Exercise.difficulty_level == difficulty_level)
    return query.all()
