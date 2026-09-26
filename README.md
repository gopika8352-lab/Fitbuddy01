# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a FastAPI web application that generates personalized 7-day workout plans and nutrition/recovery tips. It follows the architecture described in the supplied project document: FastAPI + Jinja2 + SQLite/SQLAlchemy + Gemini models.

## Features
- User form: name, user ID, age, weight, goal, intensity
- Personalized 7-day workout plan
- Nutrition/recovery tip
- Feedback-based plan update
- SQLite persistence using SQLAlchemy
- Admin/all-users view
- HTML/Jinja2 frontend
- JSON API endpoints
- Gemini integration with a local fallback, so the project can be demonstrated without an API key

## Project structure

```text
FitBuddy_AI_Project/
├── main.py
├── requirements.txt
├── .env.example
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── schemas.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── feedback_result.html
│   ├── all_users.html
│   └── error.html
└── static/
    ├── styles.css
    └── images/
```

## Windows / VS Code setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional Gemini setup:

```powershell
copy .env.example .env
```

Open `.env` and replace the placeholder with your Gemini API key.

Run:

```powershell
uvicorn main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/view-all-users

## Notes

The supplied project document specifies Gemini 1.5 Pro for workout generation/updates and Gemini Flash for nutrition tips. The code keeps those integration points, while providing a deterministic local fallback when the API key or model service is unavailable.

Do not commit `.env` or API keys to GitHub.
