from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated, Optional
from database import SessionLocal, create_db
import models
from sqlalchemy.orm import Session

app = FastAPI()

# Call create_db() to create tables at startup
create_db()

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    gender: Optional[str] =None
    age: Optional[str] = None

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


@app.get("/api/employee/get")
async def get_all_users(db:db_dependency):
    employees = db.query(models.Employee).all()
    return employees

@app.delete("/api/employee/{emp_id}")
async def delete_employee(emp_id: int, db: db_dependency):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail=f"employee not found with id: '{emp_id}'")
    db.delete(db_emp)
    db.commit()
    return {"detail": "Employee deleted successfully"}

@app.put("/api/employee/update")
async def update_employee(emp_id:int, emp : EmployeeBase, db: db_dependency):
    db_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404, detail=f"employee not found with id: '{emp_id}'")
    db_emp.first_name = emp.first_name
    db_emp.last_name = emp.last_name
    db_emp.gender = emp.gender
    db_emp.age = emp.age
    db.commit()
    db.refresh(db_emp)
    return db_emp
