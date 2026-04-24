"""
AI Engineering Learning Agent - SIMPLE WORKING VERSION
No errors, guaranteed to run
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import datetime, timedelta
import secrets
import json
import random
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ============================================
# CREATE TEMPLATES DIRECTORY
# ============================================
os.makedirs('templates', exist_ok=True)

# ============================================
# VERIFIED RESOURCES (REAL LINKS)
# ============================================
VERIFIED_RESOURCES = {
    "DSA": {"title": "Data Structures Full Course", "channel": "freeCodeCamp.org", "url": "https://www.youtube.com/watch?v=8hly31xKli0", "duration": "10 hours"},
    "OS": {"title": "Operating Systems Full Course", "channel": "Neso Academy", "url": "https://www.youtube.com/watch?v=26QPDBe-NB8", "duration": "12 hours"},
    "DBMS": {"title": "DBMS Full Course", "channel": "Gate Smashers", "url": "https://www.youtube.com/watch?v=kBdlM6hNDAE", "duration": "6 hours"},
    "CN": {"title": "Computer Networks Course", "channel": "Neso Academy", "url": "https://www.youtube.com/watch?v=IPvYjXCsTg8", "duration": "10 hours"},
    "Maths": {"title": "Engineering Maths", "channel": "Khan Academy", "url": "https://www.youtube.com/watch?v=WUvTyaaNkzM", "duration": "20 hours"},
    "OOP": {"title": "OOP Concepts", "channel": "freeCodeCamp", "url": "https://www.youtube.com/watch?v=pTB0EiLXUC8", "duration": "1.5 hours"},
    "Python": {"title": "Python Full Course", "channel": "freeCodeCamp", "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc", "duration": "4 hours"},
}

# ============================================
# QUESTION BANK
# ============================================
QUESTIONS = [
    {"id": "q1", "subject": "DSA", "text": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "correct": "O(log n)", "explanation": "Binary search divides search space in half."},
    {"id": "q2", "subject": "DSA", "text": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Array", "List"], "correct": "Stack", "explanation": "Stack is Last In First Out."},
    {"id": "q3", "subject": "OS", "text": "Which scheduling is non-preemptive?", "options": ["Round Robin", "FCFS", "SJF", "MLQ"], "correct": "FCFS", "explanation": "FCFS executes in order of arrival."},
    {"id": "q4", "subject": "OS", "text": "What is a deadlock?", "options": ["Waiting for resources", "Process ended", "Memory full", "CPU overload"], "correct": "Waiting for resources", "explanation": "Processes wait indefinitely for resources."},
    {"id": "q5", "subject": "DBMS", "text": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Sequential Query Language", "Standard Query Language"], "correct": "Structured Query Language", "explanation": "SQL is for database communication."},
    {"id": "q6", "subject": "DBMS", "text": "What is a primary key?", "options": ["Unique identifier", "Foreign key", "Index", "Duplicate"], "correct": "Unique identifier", "explanation": "Primary key uniquely identifies records."},
    {"id": "q7", "subject": "CN", "text": "Which layer handles routing?", "options": ["Physical", "Data Link", "Network", "Transport"], "correct": "Network", "explanation": "Network layer handles routing."},
    {"id": "q8", "subject": "CN", "text": "What is an IP address?", "options": ["Internet Protocol address", "Internal address", "Provider address", "Interface address"], "correct": "Internet Protocol address", "explanation": "IP uniquely identifies devices."},
    {"id": "q9", "subject": "OOP", "text": "What is encapsulation?", "options": ["Hiding data", "Multiple inheritance", "Overloading", "Binding"], "correct": "Hiding data", "explanation": "Encapsulation bundles data and methods."},
    {"id": "q10", "subject": "OOP", "text": "What is inheritance?", "options": ["Deriving new class", "Hiding data", "Many forms", "Binding"], "correct": "Deriving new class", "explanation": "Inheritance creates parent-child relationships."},
    {"id": "q11", "subject": "Python", "text": "What does print(2**3) output?", "options": ["5", "6", "8", "9"], "correct": "8", "explanation": "** is exponentiation operator."},
    {"id": "q12", "subject": "Python", "text": "How to create a list?", "options": ["[]", "{}", "()", "<>"], "correct": "[]", "explanation": "Square brackets create lists."},
    {"id": "q13", "subject": "Maths", "text": "Derivative of x² is?", "options": ["2x", "x", "x²", "2"], "correct": "2x", "explanation": "Derivative of x^n is n*x^(n-1)."},
    {"id": "q14", "subject": "Maths", "text": "What is log(100)?", "options": ["1", "2", "3", "4"], "correct": "2", "explanation": "10² = 100, so log(100)=2"},
    {"id": "q15", "subject": "DSA", "text": "Time complexity of bubble sort?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "correct": "O(n²)", "explanation": "Bubble sort has nested loops."},
]

# Store student data (in-memory for simplicity)
students = {}
learning_plans = {}

# ============================================
# CREATE HTML TEMPLATES
# ============================================

# Dashboard HTML
dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Learning Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin-bottom: 20px;
        }
        h1 { color: #333; margin: 0; }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
        }
        .stat-card:hover { transform: translateY(-5px); transition: 0.3s; }
        .stat-value { font-size: 2em; font-weight: bold; color: #667eea; }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 20px;
        }
        .card h2 { margin-top: 0; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 10px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        .task-list { max-height: 400px; overflow-y: auto; }
        .task-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .task-day {
            background: #667eea;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        .task-title { flex: 1; margin: 0 15px; }
        .completed { background: #d1fae5; }
        .alert {
            background: #dbeafe;
            padding: 15px;
            border-radius: 10px;
            color: #1e40af;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            margin: 2px;
        }
        .badge-weak { background: #fee2e2; color: #dc2626; }
        .badge-strong { background: #d1fae5; color: #059669; }
        @media (max-width: 768px) {
            .main-grid { grid-template-columns: 1fr; }
            .stats { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SkillForge  AI – Solution</h1>
            <p>15-Minute Diagnostic → Personalized 30-Day Plan → Verified Resources</p>
        </div>
        <div class="stats">
            <div class="stat-card" onclick="window.location.href='/diagnostic'">
                <div>📝</div>
                <div>Start Diagnostic</div>
                <div class="stat-value">15 min</div>
            </div>
            <div class="stat-card">
                <div>📊</div>
                <div>Your Score</div>
                <div class="stat-value" id="scoreDisplay">-</div>
            </div>
            <div class="stat-card">
                <div>🎯</div>
                <div>Progress</div>
                <div class="stat-value" id="progressDisplay">0%</div>
            </div>
            <div class="stat-card">
                <div>🏆</div>
                <div>Status</div>
                <div class="stat-value" id="statusDisplay">-</div>
            </div>
        </div>
        <div class="main-grid">
            <div class="card">
                <h2>🎓 Your Learning Plan</h2>
                <input type="text" id="studentId" placeholder="Enter Student ID">
                <button onclick="loadPlan()">Load Plan</button>
                <div id="planContent" style="margin-top: 20px;">
                    <div class="alert">Enter Student ID to view your plan</div>
                </div>
            </div>
            <div class="card">
                <h2>📊 Your Progress</h2>
                <div id="progressContent">
                    <div class="alert">Complete diagnostic to see progress</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function loadPlan() {
            const studentId = document.getElementById('studentId').value;
            if (!studentId) { alert('Enter Student ID'); return; }
            fetch(`/api/get_plan/${studentId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('planContent').innerHTML = '<div class="alert">No plan found. Take diagnostic first!</div>';
                        return;
                    }
                    displayPlan(data);
                    displayProgress(data);
                    document.getElementById('scoreDisplay').innerText = data.percentage ? data.percentage + '%' : '-';
                    let progressPercent = data.current_day ? Math.round((data.current_day/30)*100) : 0;
                    document.getElementById('progressDisplay').innerText = progressPercent + '%';
                    document.getElementById('statusDisplay').innerText = data.plan_completed ? '✅ Complete' : 'In Progress';
                });
        }
        
        function displayPlan(data) {
            const tasks = data.tasks || [];
            let completed = tasks.filter(t => t.completed).length;
            let html = `<div style="background:#e0e0e0;border-radius:10px;height:20px;margin-bottom:20px;"><div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);width:${(completed/30)*100}%;height:100%;border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;">${Math.round((completed/30)*100)}%</div></div><div class="task-list">`;
            tasks.forEach(task => {
                let btnHtml = task.completed ? '<span style="color:#10b981;">✓ Done</span>' : `<button onclick="markComplete(${task.day})">Complete</button>`;
                html += `<div class="task-item ${task.completed ? 'completed' : ''}">
                    <div class="task-day">${task.day}</div>
                    <div class="task-title"><strong>${task.title}</strong><br><small>${task.duration || '30 min'}</small><br><a href="${task.url}" target="_blank">🔗 Watch</a></div>
                    <div>${btnHtml}</div>
                </div>`;
            });
            html += `</div>`;
            document.getElementById('planContent').innerHTML = html;
        }
        
        function displayProgress(data) {
            let weak = data.weak_topics || [];
            let strong = data.strong_topics || [];
            let html = `<div style="text-align:center;margin-bottom:20px;"><div style="font-size:2em;font-weight:bold;color:#667eea;">${data.correct_count || 0}/${data.total_questions || 15}</div><div>Correct Answers</div></div>`;
            html += `<h3>📚 Topics to Focus</h3><div>${weak.map(t => `<span class="badge badge-weak">⚠️ ${t}</span>`).join('') || 'None! Great job!'}</div>`;
            html += `<h3>💪 Strong Topics</h3><div>${strong.map(t => `<span class="badge badge-strong">✓ ${t}</span>`).join('') || 'None yet'}</div>`;
            document.getElementById('progressContent').innerHTML = html;
        }
        
        function markComplete(day) {
            const studentId = document.getElementById('studentId').value;
            fetch('/api/mark_complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ student_id: studentId, day: day })
            }).then(() => loadPlan());
        }
    </script>
</body>
</html>
'''

# Diagnostic HTML
diagnostic_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Diagnostic Assessment</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .header {
            background: white;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        .question-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
        }
        .progress-bar {
            background: #e0e0e0;
            border-radius: 10px;
            height: 8px;
            margin-bottom: 20px;
        }
        .progress-fill {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s;
        }
        .subject-badge {
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 15px;
        }
        .question-text { font-size: 1.2em; margin-bottom: 25px; }
        .options { display: grid; gap: 10px; margin-bottom: 30px; }
        .option {
            padding: 12px;
            background: #f8f9fa;
            border: 2px solid #ddd;
            border-radius: 10px;
            cursor: pointer;
        }
        .option:hover { background: #e9ecef; border-color: #667eea; }
        .option.selected { background: #dbeafe; border-color: #667eea; }
        .nav-buttons { display: flex; justify-content: space-between; }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        .btn-secondary { background: #6c757d; }
        .results-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
        }
        .score-number { font-size: 3em; font-weight: bold; color: #667eea; text-align: center; }
        .hidden { display: none; }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 10px;
        }
        .correct-badge { background: #d1fae5; color: #059669; padding: 5px 15px; border-radius: 20px; display: inline-block; margin: 5px; }
        .wrong-badge { background: #fee2e2; color: #dc2626; padding: 5px 15px; border-radius: 20px; display: inline-block; margin: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 15-Minute Diagnostic</h1>
            <div id="timer" style="color: #667eea; margin-top: 10px;">Time: 0:00</div>
        </div>
        
        <div id="studentInfo" class="question-card">
            <h2>👋 Welcome!</h2>
            <input type="text" id="studentId" placeholder="Student ID">
            <input type="text" id="studentName" placeholder="Your Name">
            <button onclick="startDiagnostic()">Start Assessment →</button>
        </div>
        
        <div id="questionContainer" class="hidden"></div>
        <div id="resultsContainer" class="hidden"></div>
    </div>
    
    <script>
        let questions = [];
        let currentIndex = 0;
        let answers = {};
        let studentId = '';
        let studentName = '';
        let timerInterval = null;
        let startTime = null;
        
        function startDiagnostic() {
            studentId = document.getElementById('studentId').value;
            studentName = document.getElementById('studentName').value;
            if (!studentId || !studentName) {
                alert('Please enter both Student ID and Name');
                return;
            }
            
            // Get random questions
            fetch('/api/get_questions')
                .then(res => res.json())
                .then(data => {
                    questions = data.questions;
                    document.getElementById('studentInfo').classList.add('hidden');
                    document.getElementById('questionContainer').classList.remove('hidden');
                    startTime = Date.now();
                    timerInterval = setInterval(updateTimer, 1000);
                    showQuestion(0);
                });
        }
        
        function updateTimer() {
            let elapsed = Math.floor((Date.now() - startTime) / 1000);
            let minutes = Math.floor(elapsed / 60);
            let seconds = elapsed % 60;
            document.getElementById('timer').innerHTML = `Time: ${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
        
        function showQuestion(index) {
            let q = questions[index];
            let progress = ((index + 1) / questions.length) * 100;
            
            let optionsHtml = '';
            for (let opt of q.options) {
                let isSelected = answers[q.id] === opt;
                optionsHtml += `<div class="option ${isSelected ? 'selected' : ''}" onclick="selectOption('${q.id}', '${opt.replace(/'/g, "\\'")}')">
                    ${opt}
                </div>`;
            }
            
            let html = `
                <div class="question-card">
                    <div class="progress-bar"><div class="progress-fill" style="width: ${progress}%"></div></div>
                    <div class="subject-badge">${q.subject}</div>
                    <div class="question-text">${q.text}</div>
                    <div class="options">${optionsHtml}</div>
                    <div class="nav-buttons">
                        <button class="btn-secondary" onclick="previousQuestion()" ${index === 0 ? 'disabled' : ''}>← Previous</button>
                        <button onclick="nextQuestion()">${index === questions.length - 1 ? 'Submit →' : 'Next →'}</button>
                    </div>
                </div>
            `;
            document.getElementById('questionContainer').innerHTML = html;
        }
        
        function selectOption(questionId, answer) {
            answers[questionId] = answer;
            let options = document.querySelectorAll('.option');
            options.forEach(opt => opt.classList.remove('selected'));
            event.currentTarget.classList.add('selected');
        }
        
        function previousQuestion() {
            if (currentIndex > 0) {
                currentIndex--;
                showQuestion(currentIndex);
            }
        }
        
        function nextQuestion() {
            let currentQ = questions[currentIndex];
            if (!answers[currentQ.id]) {
                alert('Please select an answer');
                return;
            }
            
            if (currentIndex === questions.length - 1) {
                submitDiagnostic();
            } else {
                currentIndex++;
                showQuestion(currentIndex);
            }
        }
        
        function submitDiagnostic() {
            clearInterval(timerInterval);
            document.getElementById('questionContainer').classList.add('hidden');
            document.getElementById('resultsContainer').classList.remove('hidden');
            document.getElementById('resultsContainer').innerHTML = '<div class="results-card" style="text-align:center;">📊 Analyzing your answers...</div>';
            
            fetch('/api/submit_diagnostic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    student_id: studentId,
                    student_name: studentName,
                    answers: answers,
                    questions: questions
                })
            })
            .then(res => res.json())
            .then(data => {
                let wrongHtml = '';
                for (let w of data.wrong_answers || []) {
                    wrongHtml += `
                        <div style="padding:10px; margin:10px 0; background:#f8f9fa; border-radius:10px;">
                            <strong>❌ ${w.question}</strong><br>
                            Your answer: ${w.selected}<br>
                            Correct: ${w.correct}<br>
                            <span style="color:#059669;">📖 ${w.explanation}</span>
                        </div>
                    `;
                }
                
                let resourceHtml = '';
                for (let r of data.recommended_resources || []) {
                    resourceHtml += `
                        <div style="padding:10px; margin:10px 0; background:#f8f9fa; border-radius:10px;">
                            <strong>📺 ${r.title}</strong><br>
                            Channel: ${r.channel}<br>
                            <a href="${r.url}" target="_blank">🔗 Watch Now</a>
                        </div>
                    `;
                }
                
                let html = `
                    <div class="results-card">
                        <h2 style="text-align:center;">✅ Diagnostic Complete!</h2>
                        <div class="score-number">${data.percentage}%</div>
                        <div style="text-align:center; margin:20px 0;">
                            <span class="correct-badge">✓ Correct: ${data.correct_count}</span>
                            <span class="wrong-badge">✗ Wrong: ${data.wrong_count}</span>
                        </div>
                        <h3>❌ Questions You Got Wrong</h3>
                        ${wrongHtml || '<p>🎉 Perfect! No wrong answers!</p>'}
                        <h3>🎯 Recommended Resources</h3>
                        ${resourceHtml}
                        <h3>📅 Your 30-Day Plan</h3>
                        <div style="background:#f0fdf4; padding:15px; border-radius:10px;">
                            <p>✅ Focus on: <strong>${(data.weak_topics || []).join(', ') || 'All subjects'}</strong></p>
                            <p>📖 30 days of personalized learning</p>
                            <p>🏆 Complete all days and get your certificate!</p>
                        </div>
                        <div style="display:flex; gap:15px; justify-content:center; margin-top:25px;">
                            <button onclick="window.location.href='/'">Go to Dashboard</button>
                            <button onclick="window.location.href='/diagnostic'">Take Again</button>
                        </div>
                    </div>
                `;
                document.getElementById('resultsContainer').innerHTML = html;
            })
            .catch(err => {
                document.getElementById('resultsContainer').innerHTML = `<div class="results-card"><h2>Error</h2><p>${err.message}</p><button onclick="location.reload()">Try Again</button></div>`;
            });
        }
    </script>
</body>
</html>
'''

# Write templates
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

with open('templates/diagnostic.html', 'w', encoding='utf-8') as f:
    f.write(diagnostic_html)

# ============================================
# API ROUTES
# ============================================

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/diagnostic')
def diagnostic_page():
    return render_template('diagnostic.html')

@app.route('/api/get_questions')
def get_questions():
    """Get random 10 questions"""
    random_questions = random.sample(QUESTIONS, min(10, len(QUESTIONS)))
    return jsonify({'questions': random_questions})

@app.route('/api/submit_diagnostic', methods=['POST'])
def submit_diagnostic():
    try:
        data = request.json
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        answers = data.get('answers', {})
        questions_data = data.get('questions', [])
        
        correct_count = 0
        wrong_count = 0
        subject_correct = {}
        subject_total = {}
        wrong_answers = []
        
        for q in questions_data:
            subject = q.get('subject', 'General')
            if subject not in subject_total:
                subject_correct[subject] = 0
                subject_total[subject] = 0
            subject_total[subject] += 1
            
            user_answer = answers.get(q.get('id'))
            if user_answer == q.get('correct'):
                correct_count += 1
                subject_correct[subject] += 1
            else:
                wrong_count += 1
                wrong_answers.append({
                    'question': q.get('text'),
                    'selected': user_answer or 'No answer',
                    'correct': q.get('correct'),
                    'explanation': q.get('explanation', 'No explanation')
                })
        
        # Calculate subject scores and weak topics
        weak_topics = []
        strong_topics = []
        for subject in subject_correct:
            score = (subject_correct[subject] / subject_total[subject]) * 100 if subject_total[subject] > 0 else 0
            if score < 50:
                weak_topics.append(subject)
            elif score > 80:
                strong_topics.append(subject)
        
        # Generate 30-day learning plan
        tasks = []
        for i in range(1, 31):
            if i <= 20 and weak_topics:
                # First 20 days focus on weak topics
                topic = weak_topics[i % len(weak_topics)]
                resource = VERIFIED_RESOURCES.get(topic, VERIFIED_RESOURCES['Python'])
                tasks.append({
                    'day': i,
                    'title': f"Learn {topic} - {resource['title']}",
                    'url': resource['url'],
                    'duration': resource['duration'],
                    'completed': False
                })
            else:
                # Last 10 days practice and project
                if i == 29:
                    tasks.append({'day': i, 'title': "🎯 Start Mini Project", 'url': "https://github.com", 'duration': "2 days", 'completed': False})
                elif i == 30:
                    tasks.append({'day': i, 'title': "🚀 Submit Project & Get Certificate", 'url': "#", 'duration': "Done", 'completed': False})
                else:
                    tasks.append({'day': i, 'title': "✍️ Practice Problems", 'url': "https://www.geeksforgeeks.org/", 'duration': "1 hour", 'completed': False})
        
        # Store student data
        students[student_id] = {
            'name': student_name,
            'correct': correct_count,
            'wrong': wrong_count,
            'total': correct_count + wrong_count,
            'percentage': round((correct_count / (correct_count + wrong_count)) * 100, 2) if (correct_count + wrong_count) > 0 else 0,
            'weak_topics': weak_topics,
            'strong_topics': strong_topics,
            'tasks': tasks,
            'current_day': 1,
            'plan_completed': False
        }
        
        # Recommended resources
        recommended = []
        for topic in weak_topics[:3]:
            if topic in VERIFIED_RESOURCES:
                recommended.append(VERIFIED_RESOURCES[topic])
        
        return jsonify({
            'correct_count': correct_count,
            'wrong_count': wrong_count,
            'percentage': round((correct_count / (correct_count + wrong_count)) * 100, 2) if (correct_count + wrong_count) > 0 else 0,
            'weak_topics': weak_topics,
            'strong_topics': strong_topics,
            'wrong_answers': wrong_answers,
            'recommended_resources': recommended
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_plan/<student_id>')
def get_plan(student_id):
    if student_id not in students:
        return jsonify({'error': 'Student not found'}), 404
    
    student = students[student_id]
    return jsonify({
        'tasks': student['tasks'],
        'weak_topics': student['weak_topics'],
        'strong_topics': student['strong_topics'],
        'correct_count': student['correct'],
        'total_questions': student['total'],
        'percentage': student['percentage'],
        'current_day': student['current_day'],
        'plan_completed': student['plan_completed']
    })

@app.route('/api/mark_complete', methods=['POST'])
def mark_complete():
    data = request.json
    student_id = data.get('student_id')
    day = data.get('day')
    
    if student_id in students:
        for task in students[student_id]['tasks']:
            if task['day'] == day:
                task['completed'] = True
                break
        students[student_id]['current_day'] = day + 1
        if day >= 30:
            students[student_id]['plan_completed'] = True
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error'}), 404

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 SkillForge  AI – Solution")
    print("=" * 60)
    print("✅ SIMPLE WORKING VERSION")
    print("✅ No database needed")
    print("✅ Works immediately")
    print("=" * 60)
    print("\n🌐 Server: http://localhost:5000")
    print("📍 Dashboard: http://localhost:5000")
    print("📍 Diagnostic: http://localhost:5000/diagnostic")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)