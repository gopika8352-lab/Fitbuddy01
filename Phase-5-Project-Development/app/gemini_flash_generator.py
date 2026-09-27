from app.gemini_generator import _gemini_generate

def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip for a person whose fitness goal is "{goal}".
Use simple language. Avoid medical claims.
"""
    result = _gemini_generate(prompt, "gemini-1.5-flash")
    return result or local_tip(goal)

def local_tip(goal: str) -> str:
    g = goal.lower()
    if "muscle" in g:
        return "Nutrition tip: Include a protein source in balanced meals, stay hydrated, and support recovery with adequate sleep."
    if "weight" in g or "loss" in g:
        return "Nutrition tip: Prefer balanced meals with vegetables, protein, whole grains, and water while keeping portions appropriate for your needs."
    return "Recovery tip: Stay hydrated, eat balanced meals, and prioritize regular sleep to support consistent training."
