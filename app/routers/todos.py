from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DBTodo
from app.schemas import TodoCreate, TodoPatch, TodoResponse

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    db_todo = DBTodo(title=todo_in.title, description=todo_in.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("", response_model=list[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(DBTodo).all()

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return db_todo

@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_in: TodoPatch, db: Session = Depends(get_db)):
    db_todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")

    update_data = todo_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")

    db.delete(db_todo)
    db.commit()
    return {"message": f"Todo with ID {todo_id} deleted successfully"}