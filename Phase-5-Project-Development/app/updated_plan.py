from app.gemini_generator import _gemini_generate, local_workout_plan

def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    prompt = f"""
You are a professional fitness-plan assistant.
Here is the original 7-day workout plan:

{original_plan}

User feedback:
{user_feedback}

Revise the plan according to the feedback while preserving useful parts of the original plan.
Return a clear, structured 7-day plan.
"""
    result = _gemini_generate(prompt, "gemini-1.5-pro")
    if result:
        return result
    return original_plan + f"""

UPDATED USING USER FEEDBACK
Feedback: {user_feedback}
Suggested adjustment: Apply the requested changes gradually and keep adequate recovery days."""
