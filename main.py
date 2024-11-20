from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated, List
from database import SessionLocal, create_db
import models
from sqlalchemy.orm import Session

app = FastAPI()

# Call create_db() to create tables at startup
create_db()

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    gender: str
    age: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/api/employee/add")
async def register_user(emp: EmployeeBase, db: db_dependency):
    db_emp = models.Employee(first_name=emp.first_name, last_name=emp.last_name, gender=emp.gender, age=emp.age)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return {"id": db_emp.id, "first_name": db_emp.first_name, "last_name": db_emp.last_name}

@app.get("/api/mployee/get")
async def get_all_users(db:db_dependency):
    employees = db.query(models.Employee).all()
    return employees
