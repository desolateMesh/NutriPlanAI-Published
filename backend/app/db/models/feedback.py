# C:\Users\jrochau\projects\NutriPlan AI\backend\app\db\models\feedback.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meal_id = Column(Integer, ForeignKey('meals.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=True)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)