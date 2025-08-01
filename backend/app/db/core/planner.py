# backend/app/db/core/planner.py

import random
import pandas as pd
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, ConfigDict
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta

from app.db.models.meal import Meal
from app.db.models.meal_plan import MealPlan as MealPlanModel
from app.db.core.rules import UserProfile, RuleEngine
from app.core.feedback import FeedbackEngine

class PlannedMeal(BaseModel):
    id: int
    title: str
    calories: float
    macros: Dict[str, float]
    ingredients: Optional[List[str]] = []
    recipe: Optional[str] = None
    paired_side_meal: Optional['PlannedMeal'] = None 

    model_config = ConfigDict(from_attributes=True)

class DailyPlan(BaseModel):
    breakfast: Optional[PlannedMeal] = None
    lunch: Optional[PlannedMeal] = None
    dinner: Optional[PlannedMeal] = None 

class WeeklyPlan(BaseModel):
    monday: DailyPlan
    tuesday: DailyPlan
    wednesday: DailyPlan
    thursday: DailyPlan
    friday: DailyPlan
    saturday: DailyPlan
    sunday: DailyPlan

class MealPlanner:
    def __init__(self, feedback_engine: FeedbackEngine, user_id: int, user_profile: UserProfile, db_session: Session):
        self.feedback_engine = feedback_engine
        self.user_id = user_id
        self.user_profile = user_profile
        self.db_session = db_session
        self.rule_engine = RuleEngine(user_profile=self.user_profile, db_session=self.db_session, user_id=self.user_id)
        self.daily_targets = self.rule_engine.daily_targets

    def _select_and_score_meal(self, meal_candidates: List[Meal], used_titles: Set[str], 
                               current_daily_calories: float, current_daily_macros: Dict[str, float], slot_calorie_budget: float) -> Optional[PlannedMeal]:
        """
        Selects a random meal from the candidates, avoiding duplicates within the week
        and applying combined predicted scores (feedback + macro suitability).
        """
        if not meal_candidates:
            return None

        processed_candidates = []
        for meal in meal_candidates:
            macros_data = {"protein": meal.protein or 0, "fat": meal.fat or 0, "carbs": meal.carbs or 0}
            
            processed_candidates.append({
                'id': meal.id,
                'title': meal.name,
                'calories': meal.calories or 0,
                'macros': macros_data,
                'tags': meal.tags or [],
                'ingredients': meal.ingredients or [],
                'recipe': meal.recipe,
                'type': meal.type,
                'combined_score': getattr(meal, 'macro_suitability_score', 1.0) * 1.0
            })
        
        candidates_df = pd.DataFrame(processed_candidates)
        
        if candidates_df.empty:
            return None

        available_meals_df = candidates_df[~candidates_df['title'].isin(used_titles)]
        
        if available_meals_df.empty and not candidates_df.empty:
            available_meals_df = candidates_df
            
        if available_meals_df.empty:
            return None

        weights = available_meals_df['combined_score'].tolist()
        sanitized_weights = [w if w > 0 else 0.001 for w in weights]
        
        selected_meal_data = random.choices(available_meals_df.to_dict('records'), weights=sanitized_weights, k=1)[0]
        
        return PlannedMeal(
            id=selected_meal_data['id'],
            title=selected_meal_data['title'],
            calories=selected_meal_data['calories'],
            macros=selected_meal_data['macros'],
            ingredients=selected_meal_data.get('ingredients', []),
            recipe=selected_meal_data.get('recipe')
        )


    def generate_weekly_plan(self) -> WeeklyPlan:
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        plan_dict = {}
        used_titles_this_week = set()
        
        all_meals_from_db = self.db_session.query(Meal).all()
        if not all_meals_from_db:
            raise ValueError("The 'meal' table is empty. Please run the seeder first.")
        daily_target_calories = self.daily_targets["calories"]
        daily_target_protein = self.daily_targets["protein"]
        daily_target_fat = self.daily_targets["fat"]
        daily_target_carbs = self.daily_targets["carbs"]

        print(f"Generating plan for User ID: {self.user_id} with Goal: {self.user_profile.goal} ({self.user_profile.sex})")
        print(f"Daily Calorie Target: {daily_target_calories}, Macros: P:{daily_target_protein}g, F:{daily_target_fat}g, C:{daily_target_carbs}g")

        for day in days:
            daily_meals = {}
            current_day_calories = 0.0
            current_day_macros = {"protein": 0.0, "fat": 0.0, "carbs": 0.0}
            
            slot_calorie_percentages = {
                "breakfast": 0.20, 
                "lunch": 0.35,     
                "dinner": 0.45     
            }
            
            slot_budgets = {
                slot: daily_target_calories * percent for slot, percent in slot_calorie_percentages.items()
            }

            print(f"\nPlanning for {day}...")

            print(f"  Planning breakfast for {day} (Target: {slot_budgets['breakfast']:.0f} cal)...")
            breakfast_candidates = self.rule_engine.apply_all_rules(
                all_meals_from_db, 
                requested_meal_slot_type="breakfast",
                current_day_calories=current_day_calories,
                current_day_macros=current_day_macros,
                slot_calorie_budget=slot_budgets['breakfast']
            )
            breakfast_meal = self._select_and_score_meal(
                breakfast_candidates, 
                used_titles_this_week,
                current_day_calories,
                current_day_macros,
                slot_budgets['breakfast']
            )
            if breakfast_meal:
                daily_meals["breakfast"] = breakfast_meal
                used_titles_this_week.add(breakfast_meal.title)
                current_day_calories += breakfast_meal.calories
                for macro_key in current_day_macros:
                    current_day_macros[macro_key] += breakfast_meal.macros.get(macro_key, 0.0)
            else:
                print(f"    No suitable breakfast meal found for {day}.")
                daily_meals["breakfast"] = None

            print(f"  Planning lunch for {day} (Target: {slot_budgets['lunch']:.0f} cal)...")
            lunch_candidates = self.rule_engine.apply_all_rules(
                all_meals_from_db, 
                requested_meal_slot_type="lunch",
                current_day_calories=current_day_calories,
                current_day_macros=current_day_macros,
                slot_calorie_budget=slot_budgets['lunch']
            )
            lunch_meal = self._select_and_score_meal(
                lunch_candidates, 
                used_titles_this_week,
                current_day_calories,
                current_day_macros,
                slot_budgets['lunch']
            )
            if lunch_meal:
                daily_meals["lunch"] = lunch_meal
                used_titles_this_week.add(lunch_meal.title)
                current_day_calories += lunch_meal.calories
                for macro_key in current_day_macros:
                    current_day_macros[macro_key] += lunch_meal.macros.get(macro_key, 0.0)
            else:
                print(f"    No suitable lunch meal found for {day}.")
                daily_meals["lunch"] = None

            print(f"  Planning dinner for {day} (main + optional side - Target: {slot_budgets['dinner']:.0f} cal)...")
            
            dinner_main_candidates = self.rule_engine.apply_all_rules(
                all_meals_from_db, 
                requested_meal_slot_type="dinner",
                current_day_calories=current_day_calories,
                current_day_macros=current_day_macros,
                slot_calorie_budget=slot_budgets['dinner'] 
            )
            main_meal = self._select_and_score_meal(dinner_main_candidates, used_titles_this_week, current_day_calories, current_day_macros, slot_budgets['dinner'])
            
            combined_dinner_meal: Optional[PlannedMeal] = None

            if main_meal:
                used_titles_this_week.add(main_meal.title)

                temp_day_calories = current_day_calories + main_meal.calories
                temp_day_macros = {k: current_day_macros[k] + main_meal.macros.get(k, 0.0) for k in current_day_macros}

                side_candidates = self.rule_engine.apply_all_rules(
                    all_meals_from_db, 
                    requested_meal_slot_type="side",
                    current_day_calories=temp_day_calories, 
                    current_day_macros=temp_day_macros,
                    slot_calorie_budget=max(0, slot_budgets['dinner'] - main_meal.calories) 
                )
                side_meal = self._select_and_score_meal(side_candidates, used_titles_this_week, temp_day_calories, temp_day_macros, max(0, slot_budgets['dinner'] - main_meal.calories))

                combined_dinner_meal = main_meal
                if side_meal:
                    used_titles_this_week.add(side_meal.title)
                    
                    combined_dinner_meal.calories += side_meal.calories
                    for macro_key in combined_dinner_meal.macros:
                        combined_dinner_meal.macros[macro_key] = round(
                            combined_dinner_meal.macros.get(macro_key, 0.0) + side_meal.macros.get(macro_key, 0.0), 2
                        )
                    
                    combined_dinner_meal.title = f"{main_meal.title} with {side_meal.title}"
                    combined_dinner_meal.ingredients.extend(side_meal.ingredients)
                    combined_dinner_meal.recipe = f"{main_meal.recipe}\n\n[Side Dish: {side_meal.title}]\n{side_meal.recipe}"
                    
                    combined_dinner_meal.paired_side_meal = side_meal
                    print(f"    Paired '{side_meal.title}' with '{main_meal.title}' for dinner.")
                else:
                    print(f"    No suitable side meal found for dinner on {day}. Using '{main_meal.title}' alone.")

                daily_meals["dinner"] = combined_dinner_meal
                
                current_day_calories += combined_dinner_meal.calories - main_meal.calories 
                for macro_key in current_day_macros:
                    current_day_macros[macro_key] += (combined_dinner_meal.macros.get(macro_key, 0.0) - main_meal.macros.get(macro_key, 0.0)) 
            else:
                print(f"    No suitable main dinner meal found for {day}. Skipping dinner slot.")
                daily_meals["dinner"] = None

            print(f"  {day} Daily Totals: Calories={current_day_calories:.0f}/{daily_target_calories:.0f}, Protein={current_day_macros['protein']:.0f}g, Fat={current_day_macros['fat']:.0f}g, Carbs={current_day_macros['carbs']:.0f}g")
            plan_dict[day] = DailyPlan(**daily_meals)
        return WeeklyPlan(**plan_dict)

def save_plan_to_db(db_session: Session, plan: WeeklyPlan, user_id: int):
    print(f"💾 Saving new weekly plan for user_id: {user_id}")
    
    last_plan_date = db_session.query(func.max(MealPlanModel.plan_date)).filter(MealPlanModel.user_id == user_id).scalar()
    
    start_date = last_plan_date + timedelta(days=1) if last_plan_date else date.today()
    print(f"   ...Starting new plan from date: {start_date}")
    
    current_date = start_date
    for day_name in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        daily_plan = getattr(plan, day_name)
        
        for meal_slot_attr in ["breakfast", "lunch", "dinner"]:
            meal = getattr(daily_plan, meal_slot_attr)
            if meal:
            
                plan_entry = MealPlanModel(user_id=user_id, meal_id=meal.id, plan_date=current_date)
                db_session.add(plan_entry)
                
        current_date += timedelta(days=1)
        
    db_session.commit()
    print("   ...✅ New weekly plan saved successfully.")

def create_and_save_weekly_plan(db_session: Session, user_id: int, restrictions: List[str], calorie_target: int, goal_text: str, sex: str, weight_kg: float, height_cm: float, activity_level: str) -> WeeklyPlan: # Added new user profile parameters
    print("--- Running Full Meal Planning Cycle ---")
    
    print("🧠 Training feedback model...")
    feedback_engine = FeedbackEngine()
    feedback_engine.train(db_session, user_id=user_id)
    
    user_profile = UserProfile(
        age=30, 
        dietary_preferences=restrictions, 
        allergies=[],
        disliked_categories=[],
        sex=sex,                 
        goal=goal_text,          
        weight_kg=weight_kg,     
        height_cm=height_cm,     
        activity_level=activity_level 
    )
    
    planner = MealPlanner(
        feedback_engine=feedback_engine,
        user_id=user_id,
        user_profile=user_profile,
        db_session=db_session
    )
    
    weekly_plan = planner.generate_weekly_plan()
    
    save_plan_to_db(db_session, weekly_plan, user_id)
    
    print("--- Plan Generated and Saved Successfully ---")
    return weekly_plan