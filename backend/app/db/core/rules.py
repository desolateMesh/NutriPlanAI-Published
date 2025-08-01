from typing import List, Set, Dict, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import random
from ..models.meal import Meal
from ..models.feedback import Feedback as FeedbackModel

class UserProfile(BaseModel):
    """Defines the user's profile for meal planning, extended for goal-based planning."""
    age: int = Field(..., ge=13)
    dietary_preferences: List[str] = Field(default=[])
    allergies: List[str] = Field(default=[])
    disliked_categories: List[str] = Field(default=[])

    sex: str = Field(..., description="User's biological sex ('male', 'female', 'other')")
    goal: str = Field(..., description="User's fitness goal ('maintain', 'bulk', 'cut_muscle_gain')")
    weight_kg: float = Field(..., gt=0) 
    height_cm: float = Field(..., gt=0) 
    activity_level: str = Field(..., description="User's activity level for TDEE calculation (e.g., 'sedentary', 'moderately_active')")


class RuleEngine:
    """Applies a series of filtering rules to a list of meals."""

    def __init__(self, user_profile: UserProfile, db_session: Session, user_id: int):
        if user_profile.age < 13:
            raise ValueError("NutriPlan AI is only available for users aged 13 and older.")
        self.profile = user_profile
        self.db = db_session
        self.user_id = user_id
        self.disliked_meal_ids = self._get_disliked_meal_ids()
        self.daily_targets = self._calculate_daily_targets()
        print(f"RuleEngine initialized. Daily Targets: {self.daily_targets}")


    def _get_disliked_meal_ids(self) -> Set[int]:
        """Queries the DB for all meals the user has rated poorly (e.g., <= 2)."""
        disliked_ratings = self.db.query(FeedbackModel.meal_id).filter(
            FeedbackModel.user_id == self.user_id,
            FeedbackModel.rating <= 2
        ).all()
        return {meal_id for (meal_id,) in disliked_ratings}

    def _filter_by_feedback_ratings(self, meals: List[Meal]) -> List[Meal]:
        """Removes meals from the pool if their ID is in the disliked set."""
        if not self.disliked_meal_ids:
            return meals
        return [meal for meal in meals if meal.id not in self.disliked_meal_ids]

    def _filter_by_allergies(self, meals: List[Meal]) -> List[Meal]:
        """Removes meals containing tags that match the user's allergies."""
        if not self.profile.allergies:
            return meals
        forbidden_tags = set(self.profile.allergies)
        return [meal for meal in meals if not forbidden_tags.intersection(set(meal.tags or []))]

    def _filter_by_disliked_categories(self, meals: List[Meal]) -> List[Meal]:
        """Hard-filters meals based on disliked categories (e.g. 'seafood')."""
        if not self.profile.disliked_categories:
            return meals
        disliked_tags = set(self.profile.disliked_categories)
        return [meal for meal in meals if disliked_tags.isdisjoint(set(meal.tags or []))]

    def _filter_by_dietary_preferences(self, meals: List[Meal]) -> List[Meal]:
        """Keeps meals that contain all required dietary preference tags."""
        if not self.profile.dietary_preferences:
            return meals
        required_tags = set(self.profile.dietary_preferences)
        return [meal for meal in meals if required_tags.issubset(set(meal.tags or []))]

    def _filter_by_meal_type(self, meals: List[Meal], requested_meal_slot_type: str) -> List[Meal]:
        """
        Filters meals based on whether their 'type' field allows them for the requested meal slot.
        'lunch/dinner' meals are considered suitable for both 'lunch' and 'dinner' slots.
        """
        if not requested_meal_slot_type:
            return meals

        filtered_meals = []
        for meal in meals:
            meal_type_in_db = meal.type

            if requested_meal_slot_type == "breakfast":
                if meal_type_in_db == "breakfast":
                    filtered_meals.append(meal)
            
            elif requested_meal_slot_type == "lunch":
                if meal_type_in_db == "lunch" or meal_type_in_db == "lunch/dinner":
                    filtered_meals.append(meal)
            
            elif requested_meal_slot_type == "dinner":
                if meal_type_in_db == "dinner" or meal_type_in_db == "lunch/dinner":
                    filtered_meals.append(meal)
            
            elif requested_meal_slot_type == "side":
                if meal_type_in_db == "side":
                    filtered_meals.append(meal)
            
            elif requested_meal_slot_type == "dessert":
                if meal_type_in_db == "dessert":
                    filtered_meals.append(meal)
            
        return filtered_meals

    def _calculate_daily_targets(self) -> Dict[str, float]:
        """
        Calculates daily caloric and macronutrient targets based on user's sex, goal,
        and other profile data. This uses simplified target ranges as requested.
        """
        base_calories = 0
        target_protein_g = 0
        target_fat_g = 0
        target_carbs_g = 0

        if self.profile.sex == "male":
            if self.profile.goal == "maintain":
                base_calories = random.randint(2000, 3000)
                target_protein_g = base_calories * 0.25 / 4
                target_fat_g = base_calories * 0.30 / 9
                target_carbs_g = base_calories * 0.45 / 4
            elif self.profile.goal == "bulk":
                base_calories = 4000
                target_protein_g = base_calories * 0.25 / 4
                target_fat_g = base_calories * 0.35 / 9    
                target_carbs_g = base_calories * 0.40 / 4  
            elif self.profile.goal == "cut_muscle_gain":
                base_calories = random.randint(2200, 2500)
                target_protein_g = base_calories * 0.40 / 4 
                target_fat_g = base_calories * 0.20 / 9    
                target_carbs_g = base_calories * 0.40 / 4  
            else:
                base_calories = 2500
                target_protein_g = 150
                target_fat_g = 70
                target_carbs_g = 200

        elif self.profile.sex == "female":
            if self.profile.goal == "maintain":
                base_calories = random.randint(1500, 2000)
                target_protein_g = base_calories * 0.25 / 4
                target_fat_g = base_calories * 0.30 / 9
                target_carbs_g = base_calories * 0.45 / 4
            elif self.profile.goal == "bulk":
                base_calories = 2500 
                target_protein_g = base_calories * 0.25 / 4
                target_fat_g = base_calories * 0.35 / 9
                target_carbs_g = base_calories * 0.40 / 4
            elif self.profile.goal == "cut_muscle_gain":
                base_calories = random.randint(1700, 2000)
                target_protein_g = base_calories * 0.35 / 4 
                target_fat_g = base_calories * 0.20 / 9   
                target_carbs_g = base_calories * 0.45 / 4 
            else:
                base_calories = 1800
                target_protein_g = 100
                target_fat_g = 60
                target_carbs_g = 180
        else:

            base_calories = 2000
            target_protein_g = 120
            target_fat_g = 60
            target_carbs_g = 180

        return {
            "calories": float(base_calories),
            "protein": round(max(0.0, target_protein_g), 2),
            "fat": round(max(0.0, target_fat_g), 2),
            "carbs": round(max(0.0, target_carbs_g), 2)
        }

    def _score_meal_by_macros_and_calories(self, meals: List[Meal], daily_targets: Dict[str, float], current_day_calories: float, current_day_macros: Dict[str, float], slot_calorie_budget: float) -> List[Meal]:
        """
        Scores meals based on how well their individual macros and calories align
        with the user's daily goal and the current remaining budget.
        Adds a 'macro_suitability_score' attribute to each Meal object.
        """
        if not meals:
            return []

        for meal in meals:
            meal.macro_suitability_score = 1.0

            if self.profile.goal == "cut_muscle_gain":
                protein_ratio = (meal.protein or 0) / meal.calories if meal.calories else 0
                fat_ratio = (meal.fat or 0) / meal.calories if meal.calories else 0
                carbs_ratio = (meal.carbs or 0) / meal.calories if meal.calories else 0

                if protein_ratio > 0.15:
                    meal.macro_suitability_score += 0.5
                if fat_ratio > 0.05: 
                    meal.macro_suitability_score -= 0.3
                if carbs_ratio > 0.20: 
                    meal.macro_suitability_score -= 0.2


        return meals

    def apply_all_rules(self, all_meals: List[Meal], requested_meal_slot_type: str, 
                        current_day_calories: float = 0.0, current_day_macros: Dict[str, float] = None, slot_calorie_budget: float = 0.0) -> List[Meal]:
        """
        Applies the full sequence of filtering rules, including meal type filtering
        and scoring based on user goals and current daily totals.
        """
        if current_day_macros is None:
            current_day_macros = {"protein": 0.0, "fat": 0.0, "carbs": 0.0}

        print(f"Starting with {len(all_meals)} meals for '{requested_meal_slot_type}' slot...")
        
        type_filtered_meals = self._filter_by_meal_type(all_meals, requested_meal_slot_type)
        print(f"Meals after '{requested_meal_slot_type}' type filter: {len(type_filtered_meals)}")

        safe_meals = self._filter_by_allergies(type_filtered_meals)
        without_rated_dislikes = self._filter_by_feedback_ratings(safe_meals)
        without_disliked_categories = self._filter_by_disliked_categories(without_rated_dislikes)
        preferred_meals = self._filter_by_dietary_preferences(without_disliked_categories)
        print(f"Meals after general filters: {len(preferred_meals)}")

        scored_meals = self._score_meal_by_macros_and_calories(
            preferred_meals, 
            self.daily_targets, 
            current_day_calories, 
            current_day_macros, 
            slot_calorie_budget
        )

        
        print(f"Final valid meal pool for '{requested_meal_slot_type}': {len(scored_meals)} meals.")
        
        return scored_meals