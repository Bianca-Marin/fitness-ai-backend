from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/users/{user_id}/profile", tags=["profiles"])


@router.post("/", response_model=schemas.ProfileOut, status_code=201)
def create_or_update_profile(
    user_id: int, payload: schemas.ProfileCreate, db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if profile:
        # update existing profile in place
        profile.goal = payload.goal
        profile.experience_level = payload.experience_level
        profile.equipment = payload.equipment
        profile.height_cm = payload.height_cm
        profile.weight_kg = payload.weight_kg
    else:
        profile = models.Profile(user_id=user_id, **payload.model_dump())
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/", response_model=schemas.ProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for this user")
    return profile
