from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "fitbuddy.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(20), nullable=False)
    plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
    user = relationship("User", back_populates="plans")

def init_db():
    Base.metadata.create_all(bind=engine)

def save_user(user_id: str, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.name, user.age, user.weight = name, age, weight
            user.goal, user.intensity = goal, intensity
        else:
            user = User(user_id=user_id, name=name, age=age, weight=weight,
                        goal=goal, intensity=intensity)
            db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def save_plan(user_id: str, plan: str, nutrition_tip: str = ""):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        workout = WorkoutPlan(
            user_id=user.id,
            original_plan=plan,
            updated_plan=None,
            nutrition_tip=nutrition_tip
        )
        db.add(workout)
        db.commit()
        db.refresh(workout)
        return workout
    finally:
        db.close()

def get_latest_plan(user_id: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or not user.plans:
            return None
        return sorted(user.plans, key=lambda x: x.id)[-1]
    finally:
        db.close()

def update_plan(user_id: str, updated_text: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or not user.plans:
            return None
        workout = sorted(user.plans, key=lambda x: x.id)[-1]
        workout.updated_plan = updated_text
        db.commit()
        db.refresh(workout)
        return workout
    finally:
        db.close()

def get_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.id.desc()).all()
        result = []
        for user in users:
            latest = sorted(user.plans, key=lambda x: x.id)[-1] if user.plans else None
            result.append({
                "id": user.id,
                "user_id": user.user_id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": latest.original_plan if latest else "N/A",
                "updated_plan": latest.updated_plan if latest and latest.updated_plan else "Not updated"
            })
        return result
    finally:
        db.close()
