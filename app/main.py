from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Task
from .schemas import TaskCreate

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "API running with PostgreSQL!"}


# --- REAL DATABASE TASK ENDPOINTS --- #

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@app.post("/tasks")
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()
    return {"message": "Task deleted!"}
