"""
Milestone 2 (updated): rule-based recommendation engine.

CHANGED: sessions are now focused on ONE target muscle group per generation
(e.g. "glute day", "back day") instead of one balanced full-body programme.
This mirrors how people actually structure real gym splits, and lets the
app give more depth (several exercises) per muscle group instead of just
one.

This module still does NOT call any AI/LLM — it is the safety-checked
filtering step that runs BEFORE the LLM call (Milestone 3).
"""
from sqlalchemy.orm import Session
from app import models

EXPERIENCE_ORDER = {
    models.ExperienceEnum.beginner: 0,
    models.ExperienceEnum.intermediate: 1,
    models.ExperienceEnum.advanced: 2,
}

GOAL_SCHEME = {
    models.GoalEnum.strength: {"sets": 5, "reps": 5},
    models.GoalEnum.hypertrophy: {"sets": 4, "reps": 10},
    models.GoalEnum.endurance: {"sets": 3, "reps": 15},
    models.GoalEnum.general_fitness: {"sets": 3, "reps": 10},
}

VALID_MUSCLE_GROUPS = [
    "legs", "chest", "back", "shoulders", "glutes", "hamstrings", "arms", "core",
]


def eligible_exercises(db: Session, profile: models.Profile, target_muscle_group: str):
    """
    Safety-first filter: an exercise is eligible only if
      - it belongs to the requested target muscle group, AND
      - its required equipment matches the user's equipment (or needs none), AND
      - its difficulty is at or below the user's experience level.
    """
    all_exercises = db.query(models.Exercise).filter(
        models.Exercise.muscle_group == target_muscle_group
    ).all()
    user_level = EXPERIENCE_ORDER[profile.experience_level]

    return [
        ex for ex in all_exercises
        if (ex.equipment_required == profile.equipment or ex.equipment_required == models.EquipmentEnum.none)
        and EXPERIENCE_ORDER[ex.difficulty_level] <= user_level
    ]


def select_exercises(eligible: list, profile_equipment, max_exercises: int = 5):
    """
    From the eligible pool (all from the same target muscle group), prefer
    exercises matching the user's specific equipment over bodyweight-only
    ones, and return up to max_exercises.
    """
    sorted_eligible = sorted(
        eligible,
        key=lambda ex: 0 if ex.equipment_required == profile_equipment else 1,
    )
    return sorted_eligible[:max_exercises]


def explain(exercise: models.Exercise, profile: models.Profile) -> str:
    """Rule-based fallback explanation, used if the Milestone 3 LLM call fails."""
    return (
        f"This exercise was selected because it targets your {exercise.muscle_group}, "
        f"matches the {profile.equipment.value} equipment you have available, "
        f"and is appropriate for your {profile.experience_level.value} experience level, "
        f"in line with your {profile.goal.value} goal."
    )


def generate_programme_exercises(db: Session, profile: models.Profile, target_muscle_group: str):
    """Runs the full pipeline for one muscle-group-focused session."""
    eligible = eligible_exercises(db, profile, target_muscle_group)
    selected = select_exercises(eligible, profile.equipment)
    scheme = GOAL_SCHEME[profile.goal]

    return [
        {
            "exercise_id": ex.id,
            "order_index": idx,
            "sets": scheme["sets"],
            "reps": scheme["reps"],
            "explanation": explain(ex, profile),
        }
        for idx, ex in enumerate(selected)
    ]
