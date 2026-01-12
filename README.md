# Backend - Todo App API

This directory contains the FastAPI backend for the Todo Application.

## Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Copy `backend/.env.example` to `backend/.env` and fill in your database connection string and JWT secret key.
    ```bash
    cp .env.example .env
    ```

5.  **Run the development server**:
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.
