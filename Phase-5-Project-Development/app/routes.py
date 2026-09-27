from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import WorkoutRequest, UserInput, FeedbackRequest
from app.database import (
    save_user,
    save_plan,
    get_latest_plan,
    update_plan,
    get_all_users
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ============================================================
# HOME PAGE
# ============================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ============================================================
# GENERATE WORKOUT
# ============================================================

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:

        # Create user input
        user_data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        # Save user information
        save_user(
            user_id,
            username,
            age,
            weight,
            goal,
            intensity
        )

        # Generate workout plan using Gemini
        plan = generate_workout_gemini(
            user_data.model_dump()
        )

        # Generate nutrition/recovery tip
        tip = generate_nutrition_tip_with_flash(goal)

        # Save generated plan
        save_plan(
            user_id,
            plan,
            tip
        )

        # Display result page
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": username,
                "user_id": user_id,
                "age": age,
                "weight": weight,
                "goal": goal,
                "intensity": intensity,
                "workout_plan": plan,
                "nutrition_tip": tip,
                "updated": False
            }
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# ============================================================
# SUBMIT FEEDBACK
# ============================================================

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    latest = get_latest_plan(user_id)

    if not latest:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": "No workout plan was found for this User ID."
            },
            status_code=404
        )

    # Update workout plan using feedback
    updated = update_workout_plan(
        latest.original_plan,
        feedback
    )

    # Save updated plan
    update_plan(
        user_id,
        updated
    )

    # Display updated plan
    return templates.TemplateResponse(
        request=request,
        name="feedback_result.html",
        context={
            "updated_plan": updated,
            "user_id": user_id
        }
    )


# ============================================================
# VIEW ALL USERS
# ============================================================

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )


# ============================================================
# JSON API - GENERATE WORKOUT
# ============================================================

@router.post("/api/generate-workout")
def api_generate_workout(payload: WorkoutRequest):

    plan = generate_workout_gemini(
        payload.model_dump()
    )

    return {
        "model": "Gemini",
        "workout_plan": plan
    }


# ============================================================
# JSON API - NUTRITION TIP
# ============================================================

@router.get("/api/nutrition-tip")
def api_nutrition_tip(goal: str):

    tip = generate_nutrition_tip_with_flash(goal)

    return {
        "goal": goal,
        "nutrition_tip": tip
    }


# ============================================================
# JSON API - UPDATE PLAN
# ============================================================

@router.post("/api/update-plan")
def api_update_plan(payload: FeedbackRequest):

    latest = get_latest_plan(
        payload.user_id
    )

    if not latest:
        raise HTTPException(
            status_code=404,
            detail="Original plan not found for this user."
        )

    # Generate updated plan
    updated = update_workout_plan(
        latest.original_plan,
        payload.feedback
    )

    # Save updated plan
    update_plan(
        payload.user_id,
        updated
    )

    return {
        "updated_plan": updated
    }
