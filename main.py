from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import todos, users

app = FastAPI(
    title="FastAPI Practice API",
    description="Production-ready Todo API with JWT Auth and SQLite/PostgreSQL support",
    version="1.0.0"
)

# Define allowed frontend origins (e.g., React, Vue, Next.js apps)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API is online and running cleanly."}