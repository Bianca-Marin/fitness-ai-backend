from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.recommendation import generate_programme_exercises, VALID_MUSCLE_GROUPS
from app.llm_explainer import llm_explain

router = APIRouter(prefix="/users/{user_id}/programmes", tags=["programmes"])


@router.post("/", response_model=schemas.ProgrammeOut, status_code=201)
def create_programme(
    user_id: int, payload: schemas.ProgrammeCreate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="User must have a profile before a programme can be generated",
        )

    if payload.target_muscle_group not in VALID_MUSCLE_GROUPS:
        raise HTTPException(
            status_code=400,
            detail=f"target_muscle_group must be one of: {', '.join(VALID_MUSCLE_GROUPS)}",
        )

    programme = models.Programme(
        user_id=user_id, name=payload.name, target_muscle_group=payload.target_muscle_group
    )
    db.add(programme)
    db.flush()

    generated = generate_programme_exercises(db, profile, payload.target_muscle_group)
    if not generated:
        raise HTTPException(
            status_code=422,
            detail=f"No {payload.target_muscle_group} exercises match this profile's equipment/experience",
        )

    for item in generated:
        exercise_obj = db.query(models.Exercise).filter(models.Exercise.id == item["exercise_id"]).first()
        item["explanation"] = llm_explain(exercise_obj, profile)
        db.add(models.ProgrammeExercise(programme_id=programme.id, **item))

    db.commit()
    db.refresh(programme)
    return programme


@router.get("/", response_model=List[schemas.ProgrammeOut])
def list_programmes(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Programme).filter(models.Programme.user_id == user_id).all()


@router.get("/{programme_id}", response_model=schemas.ProgrammeOut)
def get_programme(user_id: int, programme_id: int, db: Session = Depends(get_db)):
    programme = (
        db.query(models.Programme)
        .filter(models.Programme.id == programme_id, models.Programme.user_id == user_id)
        .first()
    )
    if not programme:
        raise HTTPException(status_code=404, detail="Programme not found")
    return programme
