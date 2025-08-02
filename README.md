# NutriPlan AI

NutriPlan AI is an intelligent meal planning application designed to generate personalized 7-day meal plans based on user goals, dietary restrictions, and preferences. [cite_start]It leverages machine learning models for goal classification and adaptive learning to refine meal suggestions over time[cite: 39].

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

- [cite_start]**Personalized Meal Plans**: Generates a tailored 7-day meal plan for users, taking into account their unique profile and objectives[cite: 39].
- [cite_start]**Goal Classification**: Interprets freeform user goals using a Neural Goal Classifier (NLP) powered by Hugging Face Transformers and TensorFlow[cite: 45].
- [cite_start]**Adaptive Learning**: Employs a scikit-learn model to adjust meal scoring based on user behavior[cite: 47].
- [cite_start]**Dietary Rule Engine**: Filters meal candidates based on dietary tags or caloric constraints[cite: 47].
- [cite_start]**User Feedback System**: Processes user feedback to refine meal suggestions[cite: 44, 47].
- [cite_start]**SQLite Database**: Stores user profiles, meal data, meal plans, and feedback for persistent storage[cite: 76, 90].
- [cite_start]**Web Scraping (Data Preparation)**: Utilizes BeautifulSoup and `requests` to gather raw meal data[cite: 52, 89].
- [cite_start]**Responsive User Interface**: Built with React.js and TypeScript for a dynamic and interactive user experience[cite: 42, 81, 82].

## Technologies Used

### Backend (AI + API Layer)
- [cite_start]**Python 3.x**: Core application logic[cite: 70].
- [cite_start]**FastAPI**: Web framework for building the API endpoints[cite: 41, 71].
- [cite_start]**TensorFlow**: Machine learning framework for the Neural Goal Classifier model[cite: 72].
- [cite_start]**Hugging Face Transformers**: Provides pre-trained models for NLP tasks[cite: 73].
- [cite_start]**pandas**: Data manipulation and analysis for handling meal data, macros, and calories[cite: 46, 74].
- [cite_start]**scikit-learn**: Machine learning library for the adaptive feedback model[cite: 47, 75].
- [cite_start]**SQLite**: Lightweight embedded database for users, plans, and meals[cite: 51, 61, 76].
- [cite_start]**SQLAlchemy**: ORM for abstracting SQLite interactions[cite: 77].
- **Alembic**: Database migration tool.
- [cite_start]**`python-dotenv`**: Manages secure environment variables and application configurations[cite: 53, 78, 96].
- [cite_start]**BeautifulSoup**: For web scraping meal data[cite: 52, 66, 89].
- [cite_start]**`requests`**: For making HTTP requests in web scraping[cite: 52, 89].
- [cite_start]**PyInstaller**: For packaging the backend into an executable[cite: 93].

### Frontend (User Interface)
- [cite_start]**React.js**: JavaScript library for building the user interface[cite: 42, 81].
- [cite_start]**TypeScript**: Strongly typed JavaScript for frontend logic[cite: 42, 82].
- [cite_start]**axios**: HTTP client for communicating with the FastAPI backend[cite: 55, 83].
- [cite_start]**Tailwind CSS**: Utility-first CSS framework for responsive styling[cite: 84].
- [cite_start]**Vite**: Frontend build tool for a fast development server[cite: 94].

### Development & DevOps
- [cite_start]**Git**: Version control system[cite: 95].
- [cite_start]**GitHub**: Code repository and collaboration platform[cite: 95].
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

[cite_start]NutriPlan AI uses SQLite for its database and Alembic for migrations[cite: 76].
- **Database File**: `nutriplan_ai/backend/nutriplan.db`
- [cite_start]**Models**: Defined in `backend/app/db/models/`[cite: 49].
- [cite_start]**Seeding**: `backend/app/db/seed_meals.py` loads data from `data/normalized_meals.json` into the `Meal` table[cite: 52].

## Machine Learning Models

- [cite_start]**Goal Classifier**: A TensorFlow model using Hugging Face Transformers is located in `backend/models/goal_classifier_model/` and `backend/models/tokenizer/`[cite: 45].
- [cite_start]**Feedback Model**: A scikit-learn model in `backend/app/core/feedback.py` adapts meal scoring based on user feedback[cite: 47].

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
