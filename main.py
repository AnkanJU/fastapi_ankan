from fastapi import FastAPI
from app.database import engine, Base
from app.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phase 5 - Professional Structure")

app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "API running with modular structure!"}