# Fitness AI Backend

Backend for my dissertation project — an explainable AI-powered strength
training recommendation system (Southampton Solent University, QHO656).
This covers Milestones 1–3: the data layer, the rule-based recommendation
engine, and LLM-generated explanations. The frontend (Milestone 4) is a
separate repo, linked in the Appendix of my dissertation report.

## What this does

You set up a profile (goal, experience level, equipment you have access to),
then pick a muscle group to train (e.g. "glutes"). The system:

1. **Filters** the exercise catalogue using hard safety rules — your
   equipment has to actually be available to you (having "full gym" access
   unlocks dumbbells, barbell and resistance bands too, not just
   gym-machine exercises), and the difficulty has to be at or below your
   experience level.
2. **Selects** a shortlist for that muscle group, preferring exercises that
   match your specific equipment over generic bodyweight substitutes.
3. **Explains** each pick using an LLM (OpenAI API), which rewrites a
   rule-based template into more natural language. If the LLM call fails
   for any reason, it falls back to the rule-based explanation instead of
   returning nothing.

## What's here

## Setup

You'll need Python 3.11+, PostgreSQL, and an OpenAI API key (for the
Milestone 3 explanations — the system still runs and returns rule-based
explanations without one, via the fallback described above).

1. **Install PostgreSQL** if you don't have it (I used Postgres.app on
   Mac), and create a database:
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
```
   Then edit `.env` with your own values:

4. **Seed the exercise catalogue** (run all three, in order — each is safe
   to re-run and only adds exercises that don't already exist):
```bash
   python seed_data.py
   python seed_more.py
   python seed_glutes_v2.py
```

5. **Run the server:**
```bash
   uvicorn app.main:app --reload --reload-dir app
```

## Testing / verifying it works

With the server running, open **http://127.0.0.1:8000/docs** — this is
FastAPI's interactive Swagger UI, which I used throughout development to
manually test each endpoint (see Section 5.1.3 of my dissertation report
for a documented example).

A minimal end-to-end test:

1. `POST /users/` — create a user (email + password)
2. `POST /users/{user_id}/profile/` — attach a profile (goal, experience_level, equipment)
3. `GET /exercises/` — confirm the catalogue is seeded (optionally filter by muscle_group/equipment_required/difficulty_level)
4. `POST /users/{user_id}/programmes/` — generate a session, supplying `target_muscle_group` (e.g. `"glutes"`, `"back"`, `"chest"`, `"shoulders"`, `"legs"`, `"hamstrings"`, `"arms"`, `"core"`)

The response should include a list of exercises with `sets`, `reps`, and a
populated `explanation` field for each. If `OPENAI_API_KEY` is missing or
invalid, the explanation will still be present, just in the simpler
rule-based wording — that's the tested fallback, not a bug.

## Known limitation

The exercise catalogue (~40 exercises) is intentionally modest in size for
a dissertation-scope project — see Chapter 8 (Recommendations for Further
Work) in the dissertation report.
