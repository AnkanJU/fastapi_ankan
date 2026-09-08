import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phase 5 - Professional Structure")

# 1. CORS Configuration (New in Lesson 20)
origins = [
    "http://localhost:3000",      # Frontend dev server (React/Next.js)
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],           # Allows GET, POST, PATCH, DELETE, etc.
    allow_headers=["*"],           # Allows all headers
)

# 2. Custom Timing Middleware (Added in Lesson 19)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response

# 3. Router Integration
app.include_router(todos.router)

@app.get("/")
def root():
    return {"message": "API running with modular structure!"}