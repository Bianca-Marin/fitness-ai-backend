"""
Pydantic schemas — these define what the API actually accepts and returns.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

from app.models import GoalEnum, ExperienceEnum, EquipmentEnum


# ---------- Users ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


# ---------- Profiles ----------
class ProfileCreate(BaseModel):
    goal: GoalEnum
    experience_level: ExperienceEnum
    equipment: EquipmentEnum
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    goal: GoalEnum
    experience_level: ExperienceEnum
    equipment: EquipmentEnum
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    updated_at: datetime


# ---------- Exercises ----------
class ExerciseCreate(BaseModel):
    name: str
    muscle_group: str
    equipment_required: EquipmentEnum
    difficulty_level: ExperienceEnum
    description: Optional[str] = None


class ExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    muscle_group: str
    equipment_required: EquipmentEnum
    difficulty_level: ExperienceEnum
    description: Optional[str] = None


# ---------- Programmes ----------
class ProgrammeCreate(BaseModel):
    name: Optional[str] = "My Programme"
    target_muscle_group: str  # e.g. "glutes", "back", "chest" — required: which day is this?


class ProgrammeExerciseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    exercise: ExerciseOut
    order_index: int
    sets: int
    reps: int
    explanation: Optional[str] = None


class ProgrammeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str
    target_muscle_group: Optional[str] = None
    created_at: datetime
    exercises: List[ProgrammeExerciseOut] = []
