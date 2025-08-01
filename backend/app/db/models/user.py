# backend/app/db/models/user.py

from typing import Dict, List
from sqlalchemy import String, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=True)
    height_cm: Mapped[float] = mapped_column(Float, nullable=True)
    sex: Mapped[str] = mapped_column(String, nullable=True)
    activity_level: Mapped[str] = mapped_column(String, nullable=True)
    preferences: Mapped[Dict] = mapped_column(JSON, nullable=True)
    goal_text: Mapped[str] = mapped_column(String, nullable=True)

    meal_plans: Mapped[List["MealPlan"]] = relationship(
        "MealPlan",
        back_populates="user",
        cascade="all, delete-orphan",
    )