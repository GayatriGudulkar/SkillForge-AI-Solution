from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from datetime import datetime

from models import DiagnosticResult, ProgressUpdate, LearningPlan
from diagnostic import run_diagnostic
from plan_generator import generate_learning_plan
from tracker import ProgressTracker
from database import get_db, StudentDB, ProgressDB
import json

app = FastAPI(title="AI Learning Agent", description="15-min diagnostic + 30-day adaptive learning")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tracker = ProgressTracker()

@app.get("/")
def root():
    return {"message": "AI Learning Agent API", "version": "1.0"}

@app.post("/diagnostic")
def diagnostic(student_id: str, answers: Dict[str, str], db=Depends(get_db)):
    """Submit answers to 15-min diagnostic"""
    
    # Run diagnostic
    result = run_diagnostic(student_id, answers)
    
    # Save to database
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not student:
        student = StudentDB(id=student_id, name=f"Student_{student_id}")
        db.add(student)
    
    student.diagnostic_results = json.dumps(result.dict(), default=str)
    db.commit()
    
    return result

@app.post("/generate_plan")
def generate_plan(student_id: str, db=Depends(get_db)):
    """Generate 30-day learning plan based on diagnostic"""
    
    # Get diagnostic results
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not student or not student.diagnostic_results:
        raise HTTPException(status_code=400, detail="Run diagnostic first")
    
    diagnostic_data = json.loads(student.diagnostic_results)
    diagnostic = DiagnosticResult(**diagnostic_data)
    
    # Generate plan
    plan = generate_learning_plan(diagnostic)
    
    # Save plan
    student.current_plan = json.dumps(plan.dict(), default=str)
    db.commit()
    
    return plan

@app.get("/today_task")
def get_today_task(student_id: str, db=Depends(get_db)):
    """Get today's learning task"""
    
    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not student or not student.current_plan:
        raise HTTPException(status_code=400, detail="No active plan")
    
    plan_data = json.loads(student.current_plan)
    
    # Find current day's task
    today = datetime.now().date()
    for task in plan_data.get("tasks", []):
        # Simple logic - in production, track actual start date
        return task
    
    return {"message": "Plan completed!"}

@app.post("/progress")
def update_progress(update: ProgressUpdate):
    """Update daily progress and get adaptations"""
    
    result = tracker.update_progress(update)
    return result

@app.get("/cohort_stats")
def cohort_stats():
    """Get aggregated stats for faculty dashboard"""
    
    return tracker.get_cohort_stats()