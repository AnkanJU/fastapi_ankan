import time
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.exceptions import TodoNotFoundException
from app.routers import todos, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phase 7 - Authentication & Security")

# 1. Custom Exception Handler
@app.exception_handler(TodoNotFoundException)
async def todo_not_found_exception_handler(request: Request, exc: TodoNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "TODO_NOT_FOUND",
            "message": f"Todo item with ID {exc.todo_id} does not exist.",
            "path": str(request.url)
        },
    )

# 2. Validation Error Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for error in exc.errors():
        field = " -> ".join([str(loc) for loc in error["loc"] if loc != "body"])
        formatted_errors.append({"field": field, "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation failed.",
            "errors": formatted_errors,
            "path": str(request.url)
        },
    )

# 3. Custom Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response

# Register Routers
app.include_router(todos.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Phase 7 - Authentication API running!"}