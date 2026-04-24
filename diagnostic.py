from models import Question, Difficulty, DiagnosticResult
from typing import List, Dict
import random
from datetime import datetime

# Question bank for programming topics
QUESTION_BANK = {
    "python_basics": [
        Question(
            id="py_001",
            text="What is the output of: print(2**3)?",
            options=["5", "6", "8", "9"],
            correct="8",
            topic="python_basics",
            difficulty=Difficulty.BEGINNER
        ),
        Question(
            id="py_002",
            text="Which of these creates a list?",
            options=["{}", "()", "[]", "<>"],
            correct="[]",
            topic="python_basics",
            difficulty=Difficulty.BEGINNER
        ),
        Question(
            id="py_003",
            text="What does len([1,2,3]) return?",
            options=["2", "3", "4", "1"],
            correct="3",
            topic="python_basics",
            difficulty=Difficulty.BEGINNER
        )
    ],
    "functions": [
        Question(
            id="func_001",
            text="What is the output?\ndef add(a,b):\n    return a+b\nprint(add(2,3))",
            options=["2", "3", "5", "23"],
            correct="5",
            topic="functions",
            difficulty=Difficulty.BEGINNER
        ),
        Question(
            id="func_002",
            text="What keyword defines a function?",
            options=["def", "func", "define", "function"],
            correct="def",
            topic="functions",
            difficulty=Difficulty.BEGINNER
        )
    ],
    "loops": [
        Question(
            id="loop_001",
            text="How many times will this loop run?\nfor i in range(3):\n    print(i)",
            options=["2", "3", "4", "1"],
            correct="3",
            topic="loops",
            difficulty=Difficulty.BEGINNER
        ),
        Question(
            id="loop_002",
            text="Which loop is guaranteed to run at least once?",
            options=["for", "while", "do-while", "foreach"],
            correct="do-while",
            topic="loops",
            difficulty=Difficulty.INTERMEDIATE
        )
    ],
    "lists": [
        Question(
            id="list_001",
            text="How to add an item to the end of a list?",
            options=["append()", "add()", "insert()", "push()"],
            correct="append()",
            topic="lists",
            difficulty=Difficulty.BEGINNER
        ),
        Question(
            id="list_002",
            text="What does fruits[1] return?\nfruits = ['apple', 'banana', 'cherry']",
            options=["apple", "banana", "cherry", "error"],
            correct="banana",
            topic="lists",
            difficulty=Difficulty.BEGINNER
        )
    ],
    "dictionaries": [
        Question(
            id="dict_001",
            text="How to get 'red' from this dict?\ncolor = {'primary': 'red', 'secondary': 'blue'}",
            options=["color[0]", "color['primary']", "color.primary", "color.get(0)"],
            correct="color['primary']",
            topic="dictionaries",
            difficulty=Difficulty.INTERMEDIATE
        )
    ],
    "conditionals": [
        Question(
            id="cond_001",
            text="What prints?\nx = 5\nif x > 3:\n    print('A')\nelif x > 7:\n    print('B')",
            options=["A", "B", "nothing", "error"],
            correct="A",
            topic="conditionals",
            difficulty=Difficulty.BEGINNER
        )
    ]
}

def run_diagnostic(student_id: str, answers: Dict[str, str]) -> DiagnosticResult:
    """Run 15-min adaptive diagnostic based on student answers"""
    
    topic_scores = {}
    weak_topics = []
    strong_topics = []
    
    # Group questions by topic
    topic_questions = {}
    for topic, questions in QUESTION_BANK.items():
        topic_questions[topic] = questions
    
    # Evaluate each topic
    for topic, questions in topic_questions.items():
        correct_count = 0
        for q in questions:
            if answers.get(q.id) == q.correct:
                correct_count += 1
        
        score = (correct_count / len(questions)) * 100
        topic_scores[topic] = score
        
        if score < 50:
            weak_topics.append(topic)
        elif score > 80:
            strong_topics.append(topic)
    
    # Generate recommended resources for weak topics
    recommended_resources = []
    for topic in weak_topics[:3]:  # Top 3 weakest
        recommended_resources.append({
            "topic": topic,
            "priority": "high",
            "why": f"Score: {topic_scores[topic]:.0f}%"
        })
    
    return DiagnosticResult(
        student_id=student_id,
        timestamp=datetime.now(),
        topic_scores=topic_scores,
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        recommended_resources=recommended_resources
    )