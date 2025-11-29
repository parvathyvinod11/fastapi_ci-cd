from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Task
from .schemas import TaskCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/tasks/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
