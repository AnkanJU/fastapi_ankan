from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models import DBTodo, DBUser
from app.schemas import TodoCreate, TodoPatch, TodoResponse

router = APIRouter(
    prefix="/todos",
    tags=["Todo Operations"]
)

@router.get("/", response_model=list[TodoResponse])
def get_all_todos(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """Retrieves all todos owned by the logged-in user."""
    return db.query(DBTodo).filter(DBTodo.owner_id == current_user.id).all()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_in: TodoCreate, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """Creates a new todo belonging to the logged-in user."""
    new_todo = DBTodo(**todo_in.model_dump(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo_by_id(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """Retrieves a specific todo owned by the logged-in user."""
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )
    return todo

@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, 
    todo_update: TodoPatch, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """Partially updates a todo owned by the logged-in user."""
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )

    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    """Deletes a todo owned by the logged-in user."""
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Todo with ID {todo_id} not found."
        )

    db.delete(todo)
    db.commit()
    return None