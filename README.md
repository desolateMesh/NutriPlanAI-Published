# NutriPlan AI: Setup and Running Instructions

Welcome to the NutriPlan AI project! This guide will walk you through the steps to get the backend (FastAPI) and frontend (React) components of the application up and running on your local machine.

**Estimated Setup Time:** 15-30 minutes (depending on internet speed for downloads).

## Table of Contents

* [About](#about)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Prerequisites](#prerequisites)
* [Setup Steps](#setup-steps)
    * [Step 1: Clone the Project Repository](#step-1-clone-the-project-repository)
    * [Step 2: Set Up the Backend (Python FastAPI)](#step-2-set-up-the-backend-python-fastapi)
    * [Step 3: Set Up the Frontend (React TypeScript)](#step-3-set-up-the-frontend-react-typescript)
* [Running the Application](#running-the-application)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## About

NutriPlan AI addresses the challenge individuals face in creating personalized and effective dietary plans. It generates tailored 7-day meal plans, considering unique user profiles and objectives, and adapts over time based on user feedback.

## Features

* **Goal-Oriented Meal Planning**: Generate meal plans based on freeform user goals using a Neural Goal Classifier.
* **Personalized Recommendations**: Adapt meal suggestions over time through a feedback-driven adaptive learning module.
* **Dietary Rule Engine**: Filter meal candidates based on specific dietary tags or caloric constraints.
* **User Profiles**: Store and manage user information and preferences.
* **Interactive Frontend**: User-friendly interface for inputting goals, viewing weekly plans, and providing feedback.
* **Persistent Data Storage**: Utilizes SQLite for reliable data management.

## Technologies Used

### Backend (Python/FastAPI)

* **Python 3.x**: Core application logic.
* **FastAPI**: Web framework for building APIs.
* **TensorFlow**: Neural Goal Classifier model.
* **Hugging Face Transformers**: Pre-trained models (e.g., DistilBERT, BERT).
* **Pandas**: Data handling for meal data, macros, calories.
* **Scikit-learn**: Adaptive feedback model.
* **SQLite**: Lightweight embedded DB for users, plans, meals.
* **SQLAlchemy**: ORM abstraction for SQLite interactions.
* **Alembic**: Database migrations.
* **`python-dotenv`**: Environment variable handling.
* **BeautifulSoup & Requests**: Web scraping.

### Frontend (React/TypeScript)

* **React.js**: Dynamic and interactive user interface.
* **TypeScript**: Strongly typed JavaScript for frontend logic.
* **Axios**: HTTP client to communicate with FastAPI backend.
* **Tailwind CSS**: Responsive, utility-first styling.
* **Vite**: Frontend dev server and build tool.

### Data and Storage

* **`normalized_meals.json`**: Processed meal data for planning and seeding.
* **SQLite3**: Stores users, preferences, plans, feedback persistently.

## Prerequisites

Before you begin, please ensure you have the following software installed:

* **Git:** For cloning the project repository.
    * Download: [https://git-scm.com/downloads](https://git-scm.com/downloads)
* **Git LFS (Large File Storage):** Necessary for managing large model files that exceed GitHub's size limits. Install this immediately after Git.
    * Install: Follow instructions on [https://git-lfs.github.com/](https://git-lfs.github.com/)
    * After installation, run `git lfs install` in your terminal once.
* **Python 3.11.x:** The backend requires this specific version for compatibility with machine learning libraries.
    * Download: [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/) (or the latest 3.11.x release)
    * **Important:** During Python installation, make sure to check the box that says "Add Python to PATH" or similar.
* **pip (Python Package Installer):** This usually comes installed with Python. You'll use it to install Python libraries.
    * To check if you have pip, open your terminal and type: `pip --version`
    * If it's not found, please re-install Python ensuring it's added to PATH.
* **Node.js (LTS version recommended):** Includes `npm` (Node Package Manager) for frontend dependencies.
    * Download: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

## Setup Steps

Follow these steps in order to prepare and run the application.

### Step 1: Clone the Project Repository

First, you need to download the project code from GitHub.

1.  Open your terminal or command prompt (e.g., PowerShell on Windows, Terminal on macOS/Linux).
2.  Navigate to the directory where you want to save the project (e.g., `Documents/Projects/`).
3.  Execute the `git clone` command. Replace `desolateMesh` with the actual GitHub username where the repository is hosted.
    ```bash
    git clone [https://github.com/desolateMesh/NutriPlanAI-Published.git](https://github.com/desolateMesh/NutriPlanAI-Published.git)
    ```
4.  Move into the newly cloned project directory:
    ```bash
    cd NutriPlanAI-Published
    ```
5.  **Important: Initialize Git LFS for this repository.**
    ```bash
    git lfs install
    ```
    This command adds a Git hook to the repository, preparing it for LFS-tracked files.

### Step 2: Set Up the Backend (Python FastAPI)

Now, let's prepare the Python backend environment and database.

1.  **Navigate into the `backend` directory:**
    ```bash
    cd backend
    ```
2.  **Create a Python Virtual Environment:**
    This creates a clean, isolated space for your Python packages.
    ```bash
    python -m venv venv
    ```
3.  **Activate the Virtual Environment:**
    You **must** activate this environment every time you open a new terminal session to work on the backend. You'll know it's active when `(venv)` appears at the beginning of your command prompt.
    * **On Windows (PowerShell/Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux (Bash/Zsh):**
        ```bash
        source venv/bin/activate
        ```
4.  **Install Backend Dependencies:**
    This command reads the `requirements.txt` file and installs all the necessary Python packages (FastAPI, TensorFlow, etc.) into your activated virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    *This will also ensure `tf-keras` is installed for compatibility if needed.*
5.  **Initialize the Database Schema:**
    This step uses Alembic to create the database file (`nutriplan.db`) and set up all the necessary tables (User, Meal, Plan, Feedback) based on the application's models.
    ```bash
    alembic upgrade head
    ```
6.  **Seed the Database with Initial Data:**
    After the tables are created, this command populates the `meals` table with initial data from the `data/normalized_meals.json` file.
    ```bash
    python -m app.db.seed_meals
    ```
    *(Ensure `data/normalized_meals.json` is located in the `NutriPlanAI-Published/data/` directory relative to your project root.)*

### Step 3: Set Up the Frontend (React TypeScript)

Next, we'll install the necessary JavaScript packages for your React application.

1.  **Navigate back to the main project directory, then into `frontend`:**
    ```bash
    cd ..
    cd frontend
    ```
2.  **Install Frontend Dependencies:**
    This command reads your `package.json` file and installs all the JavaScript libraries (React, Tailwind CSS, Axios, etc.) into your `node_modules` folder.
    ```bash
    npm install
    ```
    *(You might see messages about "funding" or "low severity vulnerability"; these are generally safe to ignore for development purposes or can be addressed by running `npm audit fix`.)*
3.  **Create Frontend `.env` File:**
    This file configures the API base URL for your frontend to communicate with your backend.
    * In your `frontend` directory, create a new file named `.env` (note the dot).
    * Add the following line to it:
        ```ini
        VITE_API_BASE_URL=http://localhost:8000/api
        ```
    *(This file is specific to the frontend's environment variables and should not be committed to Git; it's already ignored by `frontend/.gitignore`.)*

## Running the Application

Now that both the backend and frontend are set up, you can run them concurrently. You will need **two separate terminal windows** for this.

### Terminal Window 1: Run the Backend API Server

1.  Open a **new terminal window** (or tab).
2.  Navigate to the `backend` directory:
    ```bash
    cd C:\Users\YourUser\Projects\NutriPlanAI-Published\backend
    ```
    *(Replace `C:\Users\YourUser\Projects\NutriPlanAI-Published` with your actual project path.)*
3.  Activate the Python virtual environment:
    ```bash
    .\venv\Scripts\activate
    ```
    *(Or `source venv/bin/activate` for macOS/Linux.)*
4.  Start the FastAPI server:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    You should see output indicating the server has started, likely on `http://0.0.0.0:8000`. You can access the API documentation at `http://localhost:8000/docs`.

### Terminal Window 2: Run the Frontend Development Server

1.  Open a **second, new terminal window** (or tab).
2.  Navigate to the `frontend` directory:
    ```bash
    cd C:\Users\YourUser\Projects\NutriPlanAI-Published\frontend
    ```
    *(Replace `C:\Users\YourUser\Projects\NutriPlanAI-Published` with your actual project path.)*
3.  Start the React development server:
    ```bash
    npm run dev
    ```
    This will usually open the application automatically in your default web browser at `http://localhost:5173` (or a similar port). If not, copy the URL provided in the terminal output and paste it into your browser.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
