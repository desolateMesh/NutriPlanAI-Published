# app/main.py
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.api.endpoints import router as api_router
from app.core.classifier import GoalClassifier
from app.db.db import engine
from app.db.models import Base  


def resource_path(relative_path: str) -> str:
    """
    Resolve paths both in development and when frozen by PyInstaller.
    When frozen, PyInstaller exposes bundled files under sys._MEIPASS.
    """
    try:
        base = sys._MEIPASS  
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    model_path = resource_path(os.path.join("models", "goal_classifier_model"))
    tokenizer_path = resource_path(os.path.join("models", "tokenizer"))
    app.state.classifier = GoalClassifier(model_path=model_path, tokenizer_path=tokenizer_path)

    try:
        yield
    finally:
        app.state.classifier = None


app = FastAPI(title="NutriPlan AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

bundle_dist = resource_path("dist")

backend_dir = Path(__file__).resolve().parents[1]
frontend_build = backend_dir.parent / "frontend" / "dist"

mount_dir: str | None = None
if os.path.exists(bundle_dist):
    mount_dir = bundle_dist
elif frontend_build.exists():
    mount_dir = str(frontend_build)

if mount_dir:
    app.mount("/", StaticFiles(directory=mount_dir, html=True), name="static")
    print(f"[NutriPlan AI] Serving SPA from: {mount_dir}")
else:
    print("[NutriPlan AI] No SPA build found. Serving API only.")
    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse("/docs")
