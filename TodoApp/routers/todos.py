from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] #this is a type annotation that tells FastAPI that the return type of get_db() is Session

class TodoRequest(BaseModel):
    id : Optional[int] = None
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    completed: bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency): 
    #Depends(get_db) is a dependency injection that will run get_db() and pass the result to the function
    return db.query(Todos).all()

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_one(db : db_dependency, id : int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_todo(db : db_dependency, todo_request : TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db : db_dependency, id : int, todo_request : TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is None :
        raise HTTPException(status_code=404, detail="Todo not found")
    else :
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.completed = todo_request.completed
        db.add(todo_model)
        db.commit()
        return 
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db : db_dependency, id : int):
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is None :
        raise HTTPException(status_code=404, detail="Todo not found")
    else :
        db.delete(todo_model)
        db.commit()
        return