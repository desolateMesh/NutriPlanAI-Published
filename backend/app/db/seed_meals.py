# C:\Users\jrochau\projects\NutriPlan AI\backend\app\db\seed_meals.py
import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.db import SessionLocal, engine
from app.db.models.base import Base
from app.db.models.user import User
from app.db.models.meal import Meal
from app.db.models.meal_plan import MealPlan
from app.db.models.plan import Plan
from app.db.models.feedback import Feedback

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"

def create_demo_user(db: Session):
    """Creates a demo user if one does not already exist."""
    print("-> Checking for demo user...")
    demo_user = db.query(User).filter(User.username == "demo_user").first()
    if not demo_user:
        print(" -> Demo user not found, creating one...")
        user = User(
            username="demo_user",
            name="Demo User",
            age=30,
            weight_kg=80,
            height_cm=180,
            sex="male",
            activity_level="moderately_active",
            goal_text="I want to build lean muscle",
            preferences={"vegetarian": False, "vegan": False}
        )
        db.add(user)
        db.commit()
        print(" -> ✅ Demo user created successfully.")
    else:
        print(" -> Demo user already exists.")

def seed_meals_data(db: Session, data_file: Path) -> int: 
    """Seeds the database with meals from a specific normalized JSON file."""
    print(f"  -> Seeding from file: {data_file.name}")
    try:
        with data_file.open(encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"  -> ERROR: Could not read or parse {data_file.name}")
        return 0

    if not isinstance(data, list):
        print(f"  -> ERROR: JSON data is not a list of recipes.")
        return 0

    meal_count = 0
    titles_in_session = set()

    for item in data:
        meal_title = item.get("title")
        if not meal_title or meal_title in titles_in_session:
            continue
        titles_in_session.add(meal_title)
        
        macros = item.get("macros", {})
        
        meal = Meal(
            name=meal_title,
            calories=item.get("calories", 0),
            protein=macros.get("protein", 0.0),
            fat=macros.get("fat", 0.0),
            carbs=macros.get('carbs') or macros.get('carb', 0.0),
            recipe=' '.join(item.get('directions', [])),
            tags=item.get('tags', []),
            ingredients=item.get('ingredients', []),
            type=item.get('type') 
        )
        
        db.add(meal)
        meal_count += 1

    try:
        db.commit()
        print(f"\n  -> ✅ Committed {meal_count} new meals.")
    except Exception as e:
        db.rollback()
        print(f"\n  -> ❗ An error occurred during commit: {e}")

    return meal_count


def main() -> None:
    """Initializes the database by creating tables and then runs the seeding process."""
    print("--- Starting database seeding process ---")

    db = SessionLocal()
    try:
        print("Wiping all existing data and re-creating tables...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")

        normalized_files = sorted(DATA_DIR.glob("normalized_meals.json"))
        if not normalized_files:
            print(f"❌ No 'normalized_meals.json' files found in '{DATA_DIR}'.")
            return

        total_seeded = seed_meals_data(db, normalized_files[0])
        print("\n" + "="*50)
        print(f"✅ Seeding process finished. Total meals added: {total_seeded}")
        print("="*50 + "\n")
        create_demo_user(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()