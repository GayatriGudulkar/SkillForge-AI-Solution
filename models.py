from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date, datetime
from enum import Enum

class Subject(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    C_PROGRAMMING = "c_programming"
    DATA_STRUCTURES = "data_structures"
    ALGORITHMS = "algorithms"
    GIT = "git"

class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Question(BaseModel):
    id: str
    text: str
    options: List[str]
    correct: str
    topic: str
    difficulty: Difficulty
    prerequisite: Optional[str] = None

class DiagnosticResult(BaseModel):
    student_id: str
    timestamp: datetime
    topic_scores: Dict[str, float]  # topic -> score (0-100)
    weak_topics: List[str]
    strong_topics: List[str]
    recommended_resources: List[Dict]

class DailyTask(BaseModel):
    day: int
    topic: str
    resource_type: str  # youtube, nptel, github, docs
    resource_url: str
    title: str
    duration_mins: int
    practice_task: str
    completed: bool = False
    struggled: bool = False

class LearningPlan(BaseModel):
    student_id: str
    start_date: date
    end_date: date
    tasks: List[DailyTask]
    current_day: int = 1

class ProgressUpdate(BaseModel):
    student_id: str
    day: int
    task_completed: bool
    struggled: bool
    quiz_score: Optional[int] = None  # 0-100