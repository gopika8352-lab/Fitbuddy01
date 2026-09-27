import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except Exception:
    genai = None

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro")

if genai and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception:
        pass

def _gemini_generate(prompt: str, model_name: str):
    if not (genai and API_KEY):
        return None
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None

def generate_workout_gemini(user_input: dict) -> str:
    goal = user_input.get("goal", "general wellness")
    intensity = user_input.get("intensity", "medium")
    prompt = f"""
You are a professional fitness-plan assistant.
Create a practical, structured 7-day workout plan for:
Fitness goal: {goal}
Workout intensity: {intensity}

For each day include:
- Focus
- Warm-up (5-10 minutes)
- Main workout with exercises, sets/reps or duration
- Cool-down/recovery

Keep the plan clear and realistic. Do not make medical diagnoses.
"""
    result = _gemini_generate(prompt, PRO_MODEL)
    return result or local_workout_plan(goal, intensity)

def local_workout_plan(goal: str, intensity: str) -> str:
    level = intensity.lower()
    multiplier = {"low": "2 sets", "medium": "3 sets", "high": "3-4 sets"}.get(level, "3 sets")
    return f"""FITBUDDY 7-DAY WORKOUT PLAN
Goal: {goal}
Intensity: {intensity}

Day 1 - Full Body Foundation
Warm-up: 5-10 minutes walking and mobility.
Main workout: Squats ({multiplier}), wall/incline push-ups ({multiplier}), glute bridges ({multiplier}), plank (3 x 20-40 sec).
Cooldown: Gentle stretching for 5 minutes.

Day 2 - Cardio & Core
Warm-up: 5-10 minutes.
Main workout: Brisk walk/cycle 20-30 minutes, dead bug ({multiplier}), bird dog ({multiplier}), plank (3 x 20-40 sec).
Cooldown: Easy walking and stretching.

Day 3 - Upper Body
Warm-up: Shoulder circles and light movement.
Main workout: Incline push-ups ({multiplier}), resistance-band rows ({multiplier}), shoulder raises ({multiplier}), biceps curls if available ({multiplier}).
Cooldown: Upper-body stretches.

Day 4 - Recovery & Mobility
Easy walk for 15-25 minutes plus gentle full-body mobility.
Focus on controlled movement and recovery.

Day 5 - Lower Body
Warm-up: 5-10 minutes.
Main workout: Squats ({multiplier}), reverse lunges ({multiplier}), glute bridges ({multiplier}), calf raises ({multiplier}).
Cooldown: Lower-body stretches.

Day 6 - Cardio & Core
Warm-up: 5-10 minutes.
Main workout: Brisk walk/cycle 20-30 minutes, step-ups ({multiplier}), dead bug ({multiplier}), side plank (2-3 x 15-30 sec).
Cooldown: Easy walking and stretching.

Day 7 - Active Recovery
Easy activity such as walking, light yoga or mobility for 20-30 minutes.
Review the week and prepare for the next week.

Safety note: Start gradually, use controlled technique, rest when needed, and seek professional medical advice for health conditions or pain."""
