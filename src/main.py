from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import auth, tasks
from src.database import create_db_and_tables

app = FastAPI(title="Todo App API")

# ✅ CORS settings (React frontend ke liye)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 👈 IMPORTANT
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB create on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ✅ Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def root():
    return {"message": "Todo API running successfully 🚀"}
