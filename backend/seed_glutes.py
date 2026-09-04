"""
Additional exercises for Milestone 4.5 (muscle-group-focused sessions):
  - "glutes" is a brand new muscle group (not covered before)
  - a couple more "core" exercises, since that group only had 2

Run this the same way as the original seed_data.py — it's safe to re-run,
only adds exercises that don't already exist by name.
"""
from app.database import SessionLocal, Base, engine
from app.models import Exercise, EquipmentEnum, ExperienceEnum

Base.metadata.create_all(bind=engine)

NEW_EXERCISES = [
    # ---- Glutes (new muscle group) ----
    dict(name="Bodyweight Hip Thrust", muscle_group="glutes",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Hip extension off the floor or a bench, using body weight only."),
    dict(name="Dumbbell Hip Thrust", muscle_group="glutes",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Hip thrust with a dumbbell held across the hips for added resistance."),
    dict(name="Banded Glute Bridge", muscle_group="glutes",
         equipment_required=EquipmentEnum.resistance_bands, difficulty_level=ExperienceEnum.beginner,
         description="Glute bridge with a resistance band above the knees for extra activation."),
    dict(name="Barbell Hip Thrust", muscle_group="glutes",
         equipment_required=EquipmentEnum.barbell, difficulty_level=ExperienceEnum.intermediate,
         description="Loaded hip thrust with a barbell across the hips, a key glute-building compound lift."),
    dict(name="Cable Glute Kickback", muscle_group="glutes",
         equipment_required=EquipmentEnum.full_gym, difficulty_level=ExperienceEnum.intermediate,
         description="Standing cable kickback isolating the glutes through hip extension."),

    # ---- A couple more Core exercises ----
    dict(name="Bicycle Crunch", muscle_group="core",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Rotational bodyweight crunch targeting the obliques and abdominals."),
    dict(name="Weighted Sit-Up", muscle_group="core",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Standard sit-up holding a light dumbbell against the chest for extra resistance."),
]


def run():
    db = SessionLocal()
    try:
        added = 0
        for data in NEW_EXERCISES:
            exists = db.query(Exercise).filter(Exercise.name == data["name"]).first()
            if not exists:
                db.add(Exercise(**data))
                added += 1
        db.commit()
        print(f"Seed complete: {added} new exercises added (out of {len(NEW_EXERCISES)} defined).")
    finally:
        db.close()


if __name__ == "__main__":
    run()
