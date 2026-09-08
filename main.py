import time
from fastapi import FastAPI, Request
from app.database import engine, Base
from app.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phase 5 - Professional Structure")

# Custom Middleware to measure request execution time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    
    # Await call_next so it resolves to a Response object
    response = await call_next(request)
    
    # Calculate total processing time in milliseconds
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    
    return response

app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "API running with modular structure!"}