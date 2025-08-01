import traceback
from fastapi import APIRouter, HTTPException, Depends, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.db.models.feedback import Feedback
from typing import List
from sqlalchemy import delete

from app.db.db import get_db
from app.db.models.user import User
from app.db.models.meal import Meal
from app.db.models.feedback import Feedback as FeedbackModel

from app.core.classifier import GoalClassifier
from app.db.core.planner import create_and_save_weekly_plan, WeeklyPlan

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    name: str
    age: int = Field(..., ge=13)
    weight_kg: float | None = None
    height_cm: float | None = None
    sex: str | None = None
    activity_level: str | None = None
    preferences: Dict[str, bool] = {}
    goal_text: str
    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    username: str
    name: str
    age: int
    weight_kg: float | None
    height_cm: float | None
    sex: str | None
    activity_level: str | None
    preferences: Dict[str, bool] | None
    goal_text: str
    model_config = ConfigDict(from_attributes=True)

class PlanRequest(BaseModel):
    user_id: int
    dietary_preferences: List[str] = []
    allergies: List[str] = []
    calorie_target: int = 2200 
    goal_text: str 

class FeedbackCreate(BaseModel):
    user_id: int
    meal_id: int
    plan_id: Optional[int] = None
    rating: float = Field(..., ge=1, le=5, description="User rating from 1 to 5")
    comment: Optional[str] = None

class FeedbackOut(FeedbackCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class LikedMealOut(BaseModel):
    id: int
    title: str
    rating: float

class ClassifyRequest(BaseModel):
    goal_text: str

class ClassifyResponse(BaseModel):
    label: str
    confidence: float

class DemoPlanResponse(BaseModel):
    before_plan: WeeklyPlan
    after_plan: WeeklyPlan


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    new_user = User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/by-username/{username}", response_model=UserOut)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/plan/demo", response_model=DemoPlanResponse, tags=["plan"])
def generate_demo_plan(db: Session = Depends(get_db)):
    """
    Runs the full feedback loop demonstration and returns before/after plans.
    """
    TEST_USER_ID = 1  

    demo_user = db.query(User).filter(User.id == TEST_USER_ID).first()
    if not demo_user:
        raise HTTPException(status_code=404, detail=f"Demo user with ID {TEST_USER_ID} not found. Please run seed_meals.py first to create it.")

    db.execute(delete(Feedback).where(Feedback.user_id == TEST_USER_ID))
    db.commit()

    plan_before = create_and_save_weekly_plan(
        db, 
        TEST_USER_ID, 
        [], 
        2000, 
        demo_user.goal_text, 
        demo_user.sex, 
        demo_user.weight_kg, 
        demo_user.height_cm, 
        demo_user.activity_level 
    )

    liked = db.query(Meal).filter(Meal.name.ilike('%chicken%')).limit(5).all()
    disliked = db.query(Meal).filter(Meal.name.ilike('%salmon%')).limit(5).all()
    for meal in liked:
        db.add(Feedback(user_id=TEST_USER_ID, meal_id=meal.id, rating=5))
    for meal in disliked:
        db.add(Feedback(user_id=TEST_USER_ID, meal_id=meal.id, rating=1))
    db.commit()

    plan_after = create_and_save_weekly_plan(
        db, 
        TEST_USER_ID, 
        [], 
        2000, 
        demo_user.goal_text,
        demo_user.sex, 
        demo_user.weight_kg,
        demo_user.height_cm,
        demo_user.activity_level 
    )

    return DemoPlanResponse(before_plan=plan_before, after_plan=plan_after)

@router.post("/classify", response_model=ClassifyResponse)
async def classify_goal(payload: ClassifyRequest, request: Request):
    """
    Accepts a user's freeform goal text and returns a classification.
    """
    classifier = request.app.state.classifier
    
    if not payload.goal_text:
        raise HTTPException(status_code=400, detail="goal_text cannot be empty.")
    try:
        result = classifier.classify(payload.goal_text)
        return ClassifyResponse(label=result["label"], confidence=result["confidence"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during classification: {e}")

@router.post("/plan", response_model=WeeklyPlan)
def generate_meal_plan(request: PlanRequest, db_session: Session = Depends(get_db)):
    """
    Generates a personalized 7-day meal plan based on user's profile and goals.
    """
    user = db_session.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {request.user_id} not found.")

    if not user.sex or not user.weight_kg or not user.height_cm or not user.activity_level:
        raise HTTPException(status_code=400, detail="User profile is incomplete. 'sex', 'weight_kg', 'height_cm', and 'activity_level' are required for meal planning.")
    
    try:
        return create_and_save_weekly_plan(
            db_session=db_session,
            user_id=request.user_id,
            restrictions=request.dietary_preferences,
            calorie_target=request.calorie_target, 
            goal_text=request.goal_text,         
            sex=user.sex,
            weight_kg=user.weight_kg,
            height_cm=user.height_cm,
            activity_level=user.activity_level
        )
    except ValueError as ve:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

@router.post("/feedback", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == payload.user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not db.query(Meal).filter(Meal.id == payload.meal_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")
    new_feedback = FeedbackModel(**payload.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@router.get("/users/{user_id}/liked-meals", response_model=List[LikedMealOut])
def get_liked_meals(
    user_id: int, 
    min_rating: float = Query(4.0, ge=1, le=5, description="Minimum rating to be considered 'liked'"),
    db: Session = Depends(get_db)
):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    liked_meals_query = (
        db.query(
            Meal.id,
            Meal.name.label("title"),
            FeedbackModel.rating
        )
        .join(FeedbackModel, Meal.id == FeedbackModel.meal_id)
        .filter(
            FeedbackModel.user_id == user_id,
            FeedbackModel.rating >= min_rating
        )
        .order_by(FeedbackModel.rating.desc(), FeedbackModel.id.desc())
        .limit(20)
    )
    
    results = liked_meals_query.all()
    
    return [LikedMealOut(id=r.id, title=r.title, rating=r.rating) for r in results]