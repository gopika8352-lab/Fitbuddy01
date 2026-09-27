from pydantic import BaseModel, Field

class UserInput(BaseModel):
    username: str
    user_id: str
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=0, le=500)
    goal: str
    intensity: str

class WorkoutRequest(BaseModel):
    goal: str
    intensity: str

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str
