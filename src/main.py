from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import auth, tasks
from src.database import create_db_and_tables

origins = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API!"}
