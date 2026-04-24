from models import LearningPlan, DailyTask, DiagnosticResult
from resource_finder import get_resources_for_topic
from datetime import date, timedelta
from typing import List

# Skill progression order (prerequisites)
SKILL_ORDER = [
    "python_basics",
    "conditionals", 
    "loops",
    "lists",
    "functions",
    "dictionaries"
]

def generate_learning_plan(diagnostic: DiagnosticResult) -> LearningPlan:
    """Generate personalized 30-day learning plan"""
    
    tasks = []
    current_day = 1
    
    # Prioritize weak topics
    topics_to_learn = diagnostic.weak_topics.copy()
    
    # Add strong topics for revision (only if weak topics < 15 days)
    if len(topics_to_learn) < 15:
        # Review strong topics every 5 days
        for strong_topic in diagnostic.strong_topics[:3]:
            topics_to_learn.append(f"review_{strong_topic}")
    
    # Ensure logical order (prerequisites first)
    ordered_topics = []
    for skill in SKILL_ORDER:
        if skill in topics_to_learn:
            ordered_topics.append(skill)
    
    # Add remaining topics
    for topic in topics_to_learn:
        if topic not in ordered_topics and not topic.startswith("review_"):
            ordered_topics.append(topic)
    
    # Generate daily tasks (2-3 per day)
    days_per_topic = max(1, 30 // max(len(ordered_topics), 1))
    
    for topic in ordered_topics:
        for day_offset in range(days_per_topic):
            if current_day > 30:
                break
                
            # Get resources for this topic
            if topic.startswith("review_"):
                actual_topic = topic.replace("review_", "")
                resource_type = "youtube"
                title = f"Review: {actual_topic}"
            else:
                actual_topic = topic
                resource_type = "youtube"
                title = f"Learn {actual_topic}"
            
            resources = get_resources_for_topic(actual_topic, resource_type)
            if not resources:
                resources = [{"title": f"Practice {actual_topic}", "url": f"https://www.google.com/search?q={actual_topic}+practice", "duration": 30}]
            
            resource = resources[0]
            
            # Create practice task based on topic
            practice_task = generate_practice_task(actual_topic)
            
            task = DailyTask(
                day=current_day,
 topic=actual_topic,
                resource_type=resource_type,
                resource_url=resource["url"],
                title=resource["title"],
                duration_mins=resource.get("duration", 30),
                practice_task=practice_task
            )
            tasks.append(task)
            current_day += 1
            
            if current_day > 30:
                break
    
    # Fill remaining days with projects
    while current_day <= 30:
        task = DailyTask(
            day=current_day,
            topic="mini_project",
            resource_type="github",
            resource_url="https://github.com/topics/python-project",
            title="Build a Small Project (Calculator/Todo List/Quiz App)",
            duration_mins=60,
            practice_task="Create a working Python program applying what you've learned"
        )
        tasks.append(task)
        current_day += 1
    
    return LearningPlan(
        student_id=diagnostic.student_id,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
        tasks=tasks
    )

def generate_practice_task(topic: str) -> str:
    """Generate simple coding practice based on topic"""
    
    practice_tasks = {
        "python_basics": "Write a program that prints your name 5 times using a loop",
        "conditionals": "Write a program that checks if a number is even or odd",
        "loops": "Print numbers 1 to 10 using a for loop",
        "lists": "Create a list of 3 fruits and print the second one",
        "functions": "Write a function that takes two numbers and returns their sum",
        "dictionaries": "Create a dictionary of 3 people and their ages, then print one",
        "mini_project": "Combine everything into a small working program"
    }
    
    return practice_tasks.get(topic, f"Write 3 examples using {topic}")