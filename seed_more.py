"""
Adds more exercises to the catalogue, covering muscle groups that had too few
options after the initial seed_data.py run: back, hamstrings, chest,
shoulders and arms. Safe to re-run — skips any exercise whose name already
exists in the database.

Usage:
    python seed_more.py
"""

from app.database import SessionLocal
from app.models import Exercise

NEW_EXERCISES = [
    # --- Back ---
    {
        "name": "Bent-Over Barbell Row",
        "muscle_group": "back",
        "equipment_required": "barbell",
        "difficulty_level": "intermediate",
        "description": "Hinge at the hips and row a barbell to your lower ribs, keeping your back flat.",
    },
    {
        "name": "Dumbbell Single-Arm Row",
        "muscle_group": "back",
        "equipment_required": "dumbbells",
        "difficulty_level": "beginner",
        "description": "Supporting yourself on a bench, row a dumbbell up towards your hip with one arm at a time.",
    },
    {
        "name": "Resistance Band Lat Pulldown",
        "muscle_group": "back",
        "equipment_required": "resistance_bands",
        "difficulty_level": "beginner",
        "description": "Anchor a band overhead and pull the handles down towards your chest, squeezing your shoulder blades together.",
    },
    {
        "name": "Bodyweight Superman",
        "muscle_group": "back",
        "equipment_required": "none",
        "difficulty_level": "beginner",
        "description": "Lying face down, lift your arms and legs off the floor together to work the lower back.",
    },
    # --- Hamstrings ---
    {
        "name": "Dumbbell Romanian Deadlift",
        "muscle_group": "hamstrings",
        "equipment_required": "dumbbells",
        "difficulty_level": "intermediate",
        "description": "Hinge at the hips with a slight knee bend, lowering dumbbells along your shins to stretch the hamstrings.",
    },
    {
        "name": "Bodyweight Glute-Ham Raise",
        "muscle_group": "hamstrings",
        "equipment_required": "none",
        "difficulty_level": "advanced",
        "description": "Anchoring your feet, lower your torso forward under control and pull back up using your hamstrings.",
    },
    {
        "name": "Resistance Band Leg Curl",
        "muscle_group": "hamstrings",
        "equipment_required": "resistance_bands",
        "difficulty_level": "beginner",
        "description": "Anchor a band around your ankle and curl your heel towards your glutes against the resistance.",
    },
    # --- Chest ---
    {
        "name": "Barbell Bench Press",
        "muscle_group": "chest",
        "equipment_required": "barbell",
        "difficulty_level": "intermediate",
        "description": "Lower a barbell to your chest and press back up, keeping your shoulder blades pinned to the bench.",
    },
    {
        "name": "Dumbbell Chest Press",
        "muscle_group": "chest",
        "equipment_required": "dumbbells",
        "difficulty_level": "beginner",
        "description": "Press a pair of dumbbells up from chest level, allowing a greater range of motion than a barbell.",
    },
    {
        "name": "Bodyweight Push-Up",
        "muscle_group": "chest",
        "equipment_required": "none",
        "difficulty_level": "beginner",
        "description": "Lower your chest towards the floor and press back up, keeping your core braced throughout.",
    },
    # --- Shoulders ---
    {
        "name": "Dumbbell Shoulder Press",
        "muscle_group": "shoulders",
        "equipment_required": "dumbbells",
        "difficulty_level": "intermediate",
        "description": "Press dumbbells overhead from shoulder height, keeping your ribs down to protect your lower back.",
    },
    {
        "name": "Resistance Band Lateral Raise",
        "muscle_group": "shoulders",
        "equipment_required": "resistance_bands",
        "difficulty_level": "beginner",
        "description": "Stand on a band and raise your arms out to the sides against the resistance to target the side delts.",
    },
    {
        "name": "Bodyweight Pike Push-Up",
        "muscle_group": "shoulders",
        "equipment_required": "none",
        "difficulty_level": "advanced",
        "description": "In a pike position with hips high, lower your head towards the floor and press back up to load the shoulders.",
    },
    # --- Arms ---
    {
        "name": "Dumbbell Bicep Curl",
        "muscle_group": "arms",
        "equipment_required": "dumbbells",
        "difficulty_level": "beginner",
        "description": "Curl dumbbells up towards your shoulders, keeping your elbows tucked in close to your body.",
    },
    {
        "name": "Barbell Overhead Tricep Extension",
        "muscle_group": "arms",
        "equipment_required": "barbell",
        "difficulty_level": "intermediate",
        "description": "Lower a barbell behind your head with control, then extend your elbows to press it back up.",
    },
    {
        "name": "Bodyweight Tricep Dip",
        "muscle_group": "arms",
        "equipment_required": "none",
        "difficulty_level": "intermediate",
        "description": "Using a bench or chair, lower your body by bending your elbows, then press back up to work the triceps.",
    },
]


def seed_more():
    db = SessionLocal()
    added = 0
    skipped = 0
    try:
        for ex in NEW_EXERCISES:
            existing = db.query(Exercise).filter(Exercise.name == ex["name"]).first()
            if existing:
                skipped += 1
                continue
            db.add(Exercise(**ex))
            added += 1
        db.commit()
        print(f"Done. Added {added} new exercises, skipped {skipped} that already existed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_more()
