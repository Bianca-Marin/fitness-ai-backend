"""
Milestone 3: LLM-generated explanations.

Rewrites the rule-based explanation from Milestone 2 into more natural
language, referencing the user's specific goal/equipment/experience. The
LLM never chooses which exercises appear - it only explains a shortlist
that has already been safety-checked by the rule-based filter.

If the LLM call fails for any reason, falls back to the rule-based
template explanation rather than leaving the programme without one.
"""
import os
from openai import OpenAI
from app import models
from app.recommendation import explain as rule_based_explain

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        _client = OpenAI(api_key=api_key)
    return _client


def llm_explain(exercise: models.Exercise, profile: models.Profile) -> str:
    client = get_client()
    if client is None:
        return rule_based_explain(exercise, profile)

    prompt = (
        f"A user with a '{profile.goal.value}' fitness goal, "
        f"'{profile.experience_level.value}' experience level, and access to "
        f"'{profile.equipment.value}' equipment has been recommended the exercise "
        f"'{exercise.name}' (targets: {exercise.muscle_group}). "
        f"In one or two short, friendly sentences, explain to the user why this "
        f"exercise fits their profile. Do not suggest a different exercise. "
        f"Do not mention that you are an AI."
    )

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-nano"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7,
        )
        text = response.choices[0].message.content.strip()
        return text if text else rule_based_explain(exercise, profile)
    except Exception as e:
        print(f"[llm_explainer] LLM call failed, using fallback: {e}")
        return rule_based_explain(exercise, profile)
