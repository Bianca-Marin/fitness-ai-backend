# Fitness AI Backend — Milestone 1

Data model + FastAPI scaffold for the explainable AI-powered strength training
recommendation system (QHO656). This covers **Milestone 1 only**:
PostgreSQL schema + basic CRUD endpoints. No recommendation logic yet —
that's Milestone 2.

## What's here

```
fitness-ai-backend/
├── app/
│   ├── main.py          # FastAPI app + router registration
│   ├── database.py       # SQLAlchemy engine/session setup
│   ├── models.py         # THE SCHEMA: User, Profile, Exercise, Programme, ProgrammeExercise
│   ├── schemas.py         # Pydantic request/response models
│   └── routers/
│       ├── users.py       # POST/GET users (registration)
│       ├── profiles.py    # POST/GET profile (goal, experience, equipment)
│       ├── exercises.py   # POST/GET exercise catalogue
│       └── programmes.py  # POST/GET programme shells
├── seed_data.py            # populates 12 starter exercises
├── requirements.txt
├── .env.example
└── README.md
```

## Setup (run this locally — not tested in this sandbox, no internet there)

1. **Install PostgreSQL** if you don't have it (e.g. via Postgres.app on Mac,
   or the official installer on Windows), and create a database:
   ```sql
   CREATE DATABASE fitness_ai;
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   cd fitness-ai-backend
   python3 -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up your environment file:**
   ```bash
   cp .env.example .env
   # then edit .env with your actual Postgres username/password
   ```

4. **Seed the exercise catalogue:**
   ```bash
   python seed_data.py
   ```

5. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open the interactive docs:** http://127.0.0.1:8000/docs
   This gives you a clickable UI to test every endpoint — genuinely useful
   to screenshot/demo in your supervisor meeting or dissertation appendix,
   even before the frontend exists.

## Quick test flow (via the /docs UI, in order)

1. `POST /users/` — create a user (email + password)
2. `POST /users/{user_id}/profile/` — set their goal/experience/equipment
3. `GET /exercises/` — confirm the seeded exercises are there
4. `POST /users/{user_id}/programmes/` — create an empty programme shell
5. `GET /users/{user_id}/programmes/` — confirm it's linked to the user

Steps 1-5 prove the whole data layer works end to end — user → profile →
programme → (empty) exercises. Milestone 2 fills in step 4's exercises
automatically instead of leaving the programme empty.

## Design notes (for your dissertation write-up)

- **Why SQLAlchemy over raw SQL:** gives you migrations-ready models and
  keeps the schema in Python, which matters when the recommendation logic
  in Milestone 2 needs to query "exercises where equipment matches AND
  difficulty <= user's experience".
- **Why `explanation` lives on `programme_exercises`, not `exercises`:** the
  explanation is specific to *why this exercise was picked for this user in
  this programme* — it's not a property of the exercise itself. This is the
  field your evaluation study (Section 2.4) will actually be testing.
- **Why enums (Goal/Experience/Equipment) instead of free-text:** keeps the
  rule-based filter in Milestone 2 simple (exact matching) rather than
  needing fuzzy text matching.
