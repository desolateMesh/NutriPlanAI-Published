import os, sys
from pathlib import Path
from dotenv import load_dotenv

if getattr(sys, "frozen", False): 
    PROJECT_ROOT = Path(sys.executable).parent  
else:                                           
    PROJECT_ROOT = Path(__file__).resolve().parents[2]


if not getattr(sys, "frozen", False):
    load_dotenv(PROJECT_ROOT / ".env")

def _runtime_db_url() -> str:
    return f"sqlite:///{PROJECT_ROOT / 'nutriplan.db'}"

class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL", _runtime_db_url())
    BASE_DIR      = PROJECT_ROOT
    TOKENIZER_DIR = BASE_DIR / "models" / "tokenizer"
    MODEL_DIR     = BASE_DIR / "models" / "goal_classifier_model"

settings = Settings()
