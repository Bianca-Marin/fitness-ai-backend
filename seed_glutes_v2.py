"""
Third seed top-up: adds the specific glute exercises requested —
Romanian Deadlift (re-tagged from hamstrings, since it's equally a glute
exercise), a Bulgarian-split-squat-style movement, and a Curtsy Lunge.

Safe to re-run.
"""
from app.database import SessionLocal, Base, engine
from app.models import Exercise, EquipmentEnum, ExperienceEnum

Base.metadata.create_all(bind=engine)

NEW_EXERCISES = [
    dict(name="Rear-Foot-Elevated Split Squat", muscle_group="glutes",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.intermediate,
         description="Single-leg squat with the rear foot elevated on a bench, holding dumbbells — the formal name for a Bulgarian split squat, strongly glute-focused."),
    dict(name="Curtsy Lunge", muscle_group="glutes",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Lunge stepping diagonally behind the body, targeting the glutes (particularly the glute medius) from a different angle than a standard lunge."),
]


def run():
    db = SessionLocal()
    try:
        # Re-tag Dumbbell Romanian Deadlift as glutes (it was originally under
        # hamstrings, but it's just as much a glute exercise — hamstrings
        # still has enough other beginner options without it).
        rdl = db.query(Exercise).filter(Exercise.name == "Dumbbell Romanian Deadlift").first()
        if rdl and rdl.muscle_group != "glutes":
            rdl.muscle_group = "glutes"
            print("Re-tagged 'Dumbbell Romanian Deadlift' as glutes.")

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
