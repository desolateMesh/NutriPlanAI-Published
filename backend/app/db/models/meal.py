# backend/app/db/models/meal.py
from sqlalchemy import Column, Integer, String, Float, JSON
from .base import Base

class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    ingredients = Column(JSON, nullable=True)
    recipe = Column(String, nullable=True) 
    tags = Column(JSON, nullable=True)
    type = Column(String, nullable=True) 