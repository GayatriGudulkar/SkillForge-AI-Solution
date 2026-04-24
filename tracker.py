from models import ProgressUpdate, LearningPlan
from database import SessionLocal, ProgressDB, StudentDB
from typing import Dict
import json

class ProgressTracker:
    
    def __init__(self):
        self.db = SessionLocal()
    
    def update_progress(self, update: ProgressUpdate) -> Dict:
        """Update student progress and adapt plan if needed"""
        
        # Save progress to database
        progress_record = ProgressDB(
            student_id=update.student_id,
            day=update.day,
            topic="",  # Would fetch from plan
            completed=update.task_completed,
            struggled=update.struggled,
            quiz_score=update.quiz_score or 0
        )
        self.db.add(progress_record)
        self.db.commit()
        
        # Check if adaptation needed
        if update.struggled:
            return self.adapt_plan(update.student_id, update.day)
        
        # Check if quiz score is low (below 60%)
        if update.quiz_score and update.quiz_score < 60:
            return self.adapt_plan(update.student_id, update.day, reason="low_quiz")
        
        return {"status": "progress_updated", "adaptation_needed": False}
    
    def adapt_plan(self, student_id: str, current_day: int, reason: str = "struggled") -> Dict:
        """Adapt learning plan based on struggle"""
        
        # Fetch current plan
        student = self.db.query(StudentDB).filter(StudentDB.id == student_id).first()
        if not student or not student.current_plan:
            return {"status": "no_plan_found"}
        
        plan_data = json.loads(student.current_plan)
        
        # Find struggling topic
        struggling_topic = None
        for task in plan_data.get("tasks", []):
            if task.get("day") == current_day:
                struggling_topic = task.get("topic")
                break
        
        # Adaptation strategy:
        adaptations = {
            "action": "insert_prerequisite",
            "message": f"You struggled with {struggling_topic}. Let's review easier concepts first.",
            "new_resources": [
                {"type": "video", "title": f"Basics of {struggling_topic} - Beginner Friendly",
                 "url": f"https://www.youtube.com/results?search_query={struggling_topic}+basics+for+beginners"}
            ],
            "postpone_days": 2
        }
        
        # Update plan (insert easier content)
        new_task = {
            "day": current_day,
            "topic": f"{struggling_topic}_basics",
            "resource_url": adaptations["new_resources"][0]["url"],
            "title": adaptations["new_resources"][0]["title"],
            "duration_mins": 20,
            "practice_task": f"Complete 3 simple exercises on {struggling_topic}"
        }
        
        # Insert at current position and shift others
        plan_data["tasks"].insert(current_day - 1, new_task)
        for i in range(current_day, len(plan_data["tasks"])):
            plan_data["tasks"][i]["day"] = i + 1
        
        # Save updated plan
        student.current_plan = json.dumps(plan_data)
        self.db.commit()
        
        return {
            "status": "plan_adapted",
            "adaptation": adaptations,
            "updated_plan": plan_data
        }
    
    def get_cohort_stats(self) -> Dict:
        """Get aggregated struggle statistics for dashboard"""
        
        struggles = self.db.query(ProgressDB).filter(ProgressDB.struggled == True).all()
        
        # Group by topic (simplified - would need topic field)
        stats = {
            "total_struggles": len(struggles),
            "top_struggles": [
                {"topic": "functions", "count": 15},
                {"topic": "loops", "count": 12},
                {"topic": "dictionaries", "count": 8}
            ]
        }
        
        return stats