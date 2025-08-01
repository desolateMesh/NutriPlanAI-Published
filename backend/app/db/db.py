import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

if getattr(sys, "frozen", False):                     
    BASE_DIR = Path(sys.executable).parent            
else:                                                
    BASE_DIR = Path(__file__).resolve().parent.parent  



engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},      
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI dependency that yields a scoped session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
