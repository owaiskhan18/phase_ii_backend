# main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import auth, tasks
from src.database import create_db_and_tables

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="Todo App API")

# ---------------------------
# CORS settings
# ---------------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://phase-ii-frontend.vercel.app",  # <-- your deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Only allow listed origins
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],          # Allow all headers
)

# ---------------------------
# Startup event: create DB
# ---------------------------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ---------------------------
# Routers
# ---------------------------
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

# ---------------------------
# Root route
# ---------------------------
@app.get("/")
def root():
    return {"message": "Todo API running successfully 🚀"}
