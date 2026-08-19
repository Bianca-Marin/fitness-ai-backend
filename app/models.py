"""
SQLAlchemy models — this IS the database schema (Milestone 1).

Tables:
    users               one row per registered user
    profiles            one-to-one with users: goal, experience, equipment
    exercises           the exercise "catalogue" (seeded, not user-generated)
    programmes          a generated training programme belonging to a user
    programme_exercises join table: which exercises are in a programme,
                        in what order, with what sets/reps, and WHY
                        (the `explanation` column is where the LLM-generated
                        plain-language reasoning from Section 2.2 of the
                        report gets stored)

Milestone 2 (recommendation engine) will populate `programme_exercises`;
this file only defines the shape of the data.
"""
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Enum, UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class GoalEnum(str, enum.Enum):
    strength = "strength"
    hypertrophy = "hypertrophy"
    endurance = "endurance"
    general_fitness = "general_fitness"


class ExperienceEnum(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class EquipmentEnum(str, enum.Enum):
    none = "none"                  # bodyweight only
    dumbbells = "dumbbells"
    barbell = "barbell"
    resistance_bands = "resistance_bands"
    full_gym = "full_gym"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False,
                            cascade="all, delete-orphan")
    programmes = relationship("Programme", back_populates="user",
                               cascade="all, delete-orphan")


class Profile(Base):
    """
    One profile per user: the inputs the recommendation engine (Milestone 2)
    will actually use — goal, experience level, and available equipment.
    """
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    goal = Column(Enum(GoalEnum), nullable=False)
    experience_level = Column(Enum(ExperienceEnum), nullable=False)
    equipment = Column(Enum(EquipmentEnum), nullable=False)

    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="profile")


class Exercise(Base):
    """
    The exercise catalogue. This is seeded data (see seed_data.py), not
    something users create — it's what the rule-based filter in Milestone 2
    will filter and the LLM will pick from and explain.
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    muscle_group = Column(String, nullable=False)          # e.g. "chest", "legs", "back"
    equipment_required = Column(Enum(EquipmentEnum), nullable=False)
    difficulty_level = Column(Enum(ExperienceEnum), nullable=False)
    description = Column(Text, nullable=True)

    programme_entries = relationship("ProgrammeExercise", back_populates="exercise")


class Programme(Base):
    """A single generated training programme belonging to one user."""
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False, default="My Programme")
    created_at = Column(DateTime(timezone=True), default=utcnow)

    user = relationship("User", back_populates="programmes")
    exercises = relationship(
        "ProgrammeExercise", back_populates="programme",
        cascade="all, delete-orphan", order_by="ProgrammeExercise.order_index"
    )


class ProgrammeExercise(Base):
    """
    One exercise slot within a programme.

    `explanation` is the plain-language, LLM-generated reason this exercise
    was recommended (Section 2.2 / Section 2.4 of the progress report) —
    this is the field the trust/explanation evaluation actually depends on.
    """
    __tablename__ = "programme_exercises"

    id = Column(Integer, primary_key=True, index=True)
    programme_id = Column(Integer, ForeignKey("programmes.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    order_index = Column(Integer, nullable=False, default=0)
    sets = Column(Integer, nullable=False, default=3)
    reps = Column(Integer, nullable=False, default=10)
    explanation = Column(Text, nullable=True)  # filled in by Milestone 3 (LLM)

    __table_args__ = (
        UniqueConstraint("programme_id", "order_index", name="uq_programme_order"),
    )

    programme = relationship("Programme", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="programme_entries")
