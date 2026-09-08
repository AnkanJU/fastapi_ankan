from pydantic import BaseModel, ConfigDict, Field, field_validator

# Base Schema with common fields and validation rules
class TodoBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        description="Title must be between 3 and 50 characters"
    )
    description: str | None = Field(
        None, 
        max_length=200, 
        description="Optional description up to 200 characters"
    )

    # Custom Field Validator to reject generic/placeholder titles
    @field_validator("title")
    @classmethod
    def prevent_test_titles(cls, value: str) -> str:
        if value.strip().lower() in ["test", "todo", "temp"]:
            raise ValueError("Title is too generic. Please provide a meaningful title.")
        return value.strip()

# Schema for creating a Todo (inherits validation from TodoBase)
class TodoCreate(TodoBase):
    pass

# Schema for patching a Todo (all fields optional, retains validation rules)
class TodoPatch(BaseModel):
    title: str | None = Field(
        None, 
        min_length=3, 
        max_length=50
    )
    description: str | None = Field(
        None, 
        max_length=200
    )

    @field_validator("title")
    @classmethod
    def prevent_test_titles(cls, value: str | None) -> str | None:
        if value is not None:
            if value.strip().lower() in ["test", "todo", "temp"]:
                raise ValueError("Title is too generic. Please provide a meaningful title.")
            return value.strip()
        return value

# Schema for API Responses
class TodoResponse(TodoBase):
    id: int
    completed: bool

    model_config = ConfigDict(from_attributes=True)