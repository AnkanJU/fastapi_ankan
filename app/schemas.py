from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

# --- TODO SCHEMAS ---
class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(None, max_length=200)

    @field_validator("title")
    @classmethod
    def prevent_test_titles(cls, value: str) -> str:
        if value.strip().lower() in ["test", "todo", "temp"]:
            raise ValueError("Title is too generic.")
        return value.strip()

class TodoCreate(TodoBase):
    pass

class TodoPatch(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=50)
    description: str | None = Field(None, max_length=200)

class TodoResponse(TodoBase):
    id: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)

# --- USER SCHEMAS (NEW) ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)