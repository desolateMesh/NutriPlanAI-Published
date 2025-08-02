# NutriPlan AI

NutriPlan AI is an intelligent meal planning application designed to generate personalized 7-day meal plans based on user goals, dietary restrictions, and preferences. It leverages machine learning models for goal classification and adaptive learning to refine meal suggestions over time.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Running the Application](#running-the-application)
- [Database Management](#database-management)
- [Machine Learning Models](#machine-learning-models)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Personalized Meal Plans**: Generates a tailored 7-day meal plan for users, taking into account their unique profile and objectives.
- **Goal Classification**: Interprets freeform user goals using a Neural Goal Classifier (NLP) powered by Hugging Face Transformers and TensorFlow.
- **Adaptive Learning**: Employs a scikit-learn model to adjust meal scoring based on user behavior.
- **Dietary Rule Engine**: Filters meal candidates based on dietary tags or caloric constraints.
- **User Feedback System**: Processes user feedback to refine meal suggestions.
- **SQLite Database**: Stores user profiles, meal data, meal plans, and feedback for persistent storage.
- **Web Scraping (Data Preparation)**: Utilizes BeautifulSoup and `requests` to gather raw meal data.
- **Responsive User Interface**: Built with React.js and TypeScript for a dynamic and interactive user experience.

## Technologies Used

### Backend (AI + API Layer)
- **Python 3.x**: Core application logic.
- **FastAPI**: Web framework for building the API endpoints.
- **TensorFlow**: Machine learning framework for the Neural Goal Classifier model.
- **Hugging Face Transformers**: Provides pre-trained models for NLP tasks.
- **pandas**: Data manipulation and analysis for handling meal data, macros, and calories.
- **scikit-learn**: Machine learning library for the adaptive feedback model.
- **SQLite**: Lightweight embedded database for users, plans, and meals.
- **SQLAlchemy**: ORM for abstracting SQLite interactions.
- **Alembic**: Database migration tool.
- **`python-dotenv`**: Manages secure environment variables and application configurations.
- **BeautifulSoup**: For web scraping meal data.
- **`requests`**: For making HTTP requests in web scraping.
- **PyInstaller**: For packaging the backend into an executable.

### Frontend (User Interface)
- **React.js**: JavaScript library for building the user interface.
- **TypeScript**: Strongly typed JavaScript for frontend logic.
- **axios**: HTTP client for communicating with the FastAPI backend.
- **Tailwind CSS**: Utility-first CSS framework for responsive styling.
- **Vite**: Frontend build tool for a fast development server.

### Development & DevOps
- **Git**: Version control system.
- **GitHub**: Code repository and collaboration platform.
- **`pytest`**: Python testing framework.

## Getting Started

Follow these steps to set up and run NutriPlan AI locally.

### Prerequisites

- Python 3.8+
- Node.js (LTS) & npm (or yarn)
- Git

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd nutriplan_ai/backend
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Alembic for database migrations:**
    ```bash
    alembic init alembic
    ```
    * **Edit `alembic.ini`**: Find the line `# sqlalchemy.url =` and uncomment it, setting the database URL:
        ```ini
        sqlalchemy.url = sqlite:///nutriplan.db
        ```
    * **Edit `alembic/env.py`**: Add the following imports and set `target_metadata` to point to your SQLAlchemy `Base`:
        ```python
        import os
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from app.db.models.base import Base # Import your Base

        # ... (rest of the file)

        target_metadata = Base.metadata
        ```

5.  **Create initial database migrations:**
    ```bash
    alembic revision --autogenerate -m "Initial database setup"
    alembic upgrade head
    ```

6.  **Seed the database with meal data:**
    Ensure `data/normalized_meals.json` exists at the project root (`nutriplan_ai/data/normalized_meals.json`).
    ```bash
    python app/db/seed_meals.py
    ```

7.  **Create a `.env` file in the project root (`nutriplan_ai/.env`)**:
    ```dotenv
    DATABASE_URL="sqlite:///./backend/nutriplan.db"
    MODEL_PATH="./backend/models/goal_classifier_model"
    TOKENIZER_PATH="./backend/models/tokenizer"
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd nutriplan_ai/frontend
    ```

2.  **Install frontend dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Configure Tailwind CSS:**
    Ensure `tailwind.config.js` is set up to scan your React files. (This should be handled by the Vite React TypeScript template).

### Running the Application

1.  **Start the Backend (in `nutriplan_ai/backend` directory):**
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```
    The FastAPI server will be running at `http://localhost:8000`. You can access the auto-generated API documentation at `http://localhost:8000/docs`.

2.  **Start the Frontend (in `nutriplan_ai/frontend` directory):**
    ```bash
    npm run dev
    # or yarn dev
    ```
    The React development server will typically run at `http://localhost:5173` (or another available port).

## Database Management

NutriPlan AI uses SQLite for its database and Alembic for migrations.
- **Database File**: `nutriplan_ai/backend/nutriplan.db`
- **Models**: Defined in `backend/app/db/models/`.
- **Seeding**: `backend/app/db/seed_meals.py` loads data from `data/normalized_meals.json` into the `Meal` table.

## Machine Learning Models

- **Goal Classifier**: A TensorFlow model using Hugging Face Transformers is located in `backend/models/goal_classifier_model/` and `backend/models/tokenizer/`.
- **Feedback Model**: A scikit-learn model in `backend/app/core/feedback.py` adapts meal scoring based on user feedback.

## Contributing

Contributions are welcome! Please follow the standard Git workflow:
1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Commit your changes following conventional commit messages.
5.  Push your branch.
6.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.