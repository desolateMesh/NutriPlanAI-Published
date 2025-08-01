# backend/app/db/models/meal_plan.py

from datetime import date
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    meal_id: Mapped[int] = mapped_column(ForeignKey('meals.id'))

    plan_date: Mapped[date] = mapped_column(Date)

    user: Mapped["User"] = relationship(back_populates="meal_plans")
    meal: Mapped["Meal"] = relationship() 