# backend/app/db/models/plan.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .base import Base

class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    name = Column(String, nullable=True, default="Weekly Plan")