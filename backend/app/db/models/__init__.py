# This file serves as the public API for the 'models' package.
# By importing the models here, we ensure that any other part of the application
# can import them from a single, consistent source, which resolves the
# "Multiple classes found" error in SQLAlchemy.

from .base import Base
from .user import User
from .meal import Meal
from .meal_plan import MealPlan
from .plan import Plan
from .feedback import Feedback

# This __all__ list defines which names are exported when a script does `from .models import *`
__all__ = [
    "Base",
    "User",
    "Meal",
    "Plan",
    "MealPlan",
    "Feedback"
]
