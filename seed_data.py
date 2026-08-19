"""
Populates the exercise catalogue. Safe to re-run — only adds exercises
that don't already exist by name, so running this again after Milestone 1
just adds the new ones below without duplicating anything.
"""
from app.database import SessionLocal, Base, engine
from app.models import Exercise, EquipmentEnum, ExperienceEnum

Base.metadata.create_all(bind=engine)

EXERCISES = [
    dict(name="Bodyweight Squat", muscle_group="legs",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="A fundamental lower-body movement using just body weight."),
    dict(name="Push-up", muscle_group="chest",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Classic bodyweight chest/triceps/shoulder exercise."),
    dict(name="Dumbbell Goblet Squat", muscle_group="legs",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Holding a single dumbbell at chest height while squatting."),
    dict(name="Dumbbell Romanian Deadlift", muscle_group="hamstrings",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.intermediate,
         description="Hip-hinge movement targeting hamstrings and glutes."),
    dict(name="Barbell Back Squat", muscle_group="legs",
         equipment_required=EquipmentEnum.barbell, difficulty_level=ExperienceEnum.intermediate,
         description="Compound lower-body lift using a barbell across the upper back."),
    dict(name="Barbell Bench Press", muscle_group="chest",
         equipment_required=EquipmentEnum.barbell, difficulty_level=ExperienceEnum.intermediate,
         description="Compound pressing movement for chest, shoulders and triceps."),
    dict(name="Barbell Deadlift", muscle_group="back",
         equipment_required=EquipmentEnum.barbell, difficulty_level=ExperienceEnum.advanced,
         description="Full posterior-chain compound lift."),
    dict(name="Resistance Band Row", muscle_group="back",
         equipment_required=EquipmentEnum.resistance_bands, difficulty_level=ExperienceEnum.beginner,
         description="Seated or standing row using a resistance band."),
    dict(name="Resistance Band Pull-Apart", muscle_group="shoulders",
         equipment_required=EquipmentEnum.resistance_bands, difficulty_level=ExperienceEnum.beginner,
         description="Shoulder/upper-back activation exercise."),
    dict(name="Lat Pulldown", muscle_group="back",
         equipment_required=EquipmentEnum.full_gym, difficulty_level=ExperienceEnum.beginner,
         description="Cable machine exercise targeting the lats."),
    dict(name="Leg Press", muscle_group="legs",
         equipment_required=EquipmentEnum.full_gym, difficulty_level=ExperienceEnum.beginner,
         description="Machine-based compound lower-body exercise."),
    dict(name="Barbell Overhead Press", muscle_group="shoulders",
         equipment_required=EquipmentEnum.barbell, difficulty_level=ExperienceEnum.advanced,
         description="Standing barbell press for shoulders and triceps."),
    dict(name="Walking Lunge", muscle_group="legs",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Alternating forward lunges using body weight."),
    dict(name="Dumbbell Lunge", muscle_group="legs",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Forward lunge holding a dumbbell in each hand."),
    dict(name="Bulgarian Split Squat", muscle_group="legs",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.intermediate,
         description="Single-leg squat with the rear foot elevated, holding dumbbells."),
    dict(name="Dumbbell Chest Press", muscle_group="chest",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Lying chest press using a dumbbell in each hand."),
    dict(name="Incline Push-up", muscle_group="chest",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Push-up with hands elevated on a bench or step, easier variant."),
    dict(name="Dumbbell Flyes", muscle_group="chest",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.intermediate,
         description="Lying chest flye movement using dumbbells."),
    dict(name="Superman", muscle_group="back",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Lying back extension using body weight only."),
    dict(name="Dumbbell Bent-Over Row", muscle_group="back",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Hinged-forward row using a dumbbell in each hand."),
    dict(name="Pike Push-up", muscle_group="shoulders",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Push-up variant with hips raised, targeting shoulders."),
    dict(name="Dumbbell Shoulder Press", muscle_group="shoulders",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Overhead press using a dumbbell in each hand."),
    dict(name="Dumbbell Lateral Raise", muscle_group="shoulders",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Raising dumbbells out to the sides to target the shoulders."),
    dict(name="Glute Bridge", muscle_group="hamstrings",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Hip raise using body weight, targeting hamstrings and glutes."),
    dict(name="Dumbbell Stiff-Leg Deadlift", muscle_group="hamstrings",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Hinge movement with straighter legs, holding dumbbells."),
    dict(name="Tricep Dips", muscle_group="arms",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Bodyweight dips using a bench or chair, targeting triceps."),
    dict(name="Dumbbell Bicep Curl", muscle_group="arms",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Standard curl using a dumbbell in each hand."),
    dict(name="Dumbbell Tricep Extension", muscle_group="arms",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Overhead extension using a single dumbbell, targeting triceps."),
    dict(name="Barbell Curl", muscle_group="arms",
         equipment_required=EquipmentEnum.barbell, difficulty_level=ExperienceEnum.intermediate,
         description="Standing bicep curl using a barbell."),
    dict(name="Plank", muscle_group="core",
         equipment_required=EquipmentEnum.none, difficulty_level=ExperienceEnum.beginner,
         description="Isometric core hold using body weight."),
    dict(name="Dumbbell Russian Twist", muscle_group="core",
         equipment_required=EquipmentEnum.dumbbells, difficulty_level=ExperienceEnum.beginner,
         description="Seated rotational core exercise holding a dumbbell."),
]


def run():
    db = SessionLocal()
    try:
        added = 0
        for data in EXERCISES:
            exists = db.query(Exercise).filter(Exercise.name == data["name"]).first()
            if not exists:
                db.add(Exercise(**data))
                added += 1
        db.commit()
        print(f"Seed complete: {added} new exercises added (out of {len(EXERCISES)} defined).")
    finally:
        db.close()


if __name__ == "__main__":
    run()
