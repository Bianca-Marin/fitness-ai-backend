"""
Milestone 2: rule-based recommendation engine.
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


def eligible_exercises(db: Session, profile: models.Profile):
    all_exercises = db.query(models.Exercise).all()
    user_level = EXPERIENCE_ORDER[profile.experience_level]
    return [
        ex for ex in all_exercises
        if (ex.equipment_required == profile.equipment or ex.equipment_required == models.EquipmentEnum.none)
        and EXPERIENCE_ORDER[ex.difficulty_level] <= user_level
    ]


def select_exercises(eligible: list, profile_equipment, max_exercises: int = 6):
    by_muscle_group = {}
    for ex in eligible:
        by_muscle_group.setdefault(ex.muscle_group, []).append(ex)

    selected = []
    for muscle_group, options in by_muscle_group.items():
        options_sorted = sorted(
            options,
            key=lambda ex: 0 if ex.equipment_required == profile_equipment else 1,
        )
        selected.append(options_sorted[0])
        if len(selected) >= max_exercises:
            break
    return selected


def explain(exercise: models.Exercise, profile: models.Profile) -> str:
    return (
        f"This exercise was selected because it targets your {exercise.muscle_group}, "
        f"matches the {profile.equipment.value} equipment you have available, "
        f"and is appropriate for your {profile.experience_level.value} experience level, "
        f"in line with your {profile.goal.value} goal."
    )


def generate_programme_exercises(db: Session, profile: models.Profile):
    eligible = eligible_exercises(db, profile)
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
