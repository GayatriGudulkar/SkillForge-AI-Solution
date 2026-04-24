from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests
import os

# Configuration
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Get from @BotFather
API_URL = "http://localhost:8000"

# User session storage (in production, use Redis)
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    
    user_id = str(update.effective_user.id)
    user_sessions[user_id] = {"step": "welcome"}
    
    await update.message.reply_text(
        "🎓 *Welcome to AI Learning Agent!*\n\n"
        "I'll help you master programming in 30 days. "
        "First, let me understand what you already know.\n\n"
        "Type /diagnostic to begin the 15-minute assessment.",
        parse_mode="Markdown"
    )

async def diagnostic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the diagnostic assessment"""
    
    user_id = str(update.effective_user.id)
    user_sessions[user_id] = {"step": "diagnostic", "answers": {}, "question_index": 0}
    
    # Load first question
    questions = get_questions()
    user_sessions[user_id]["questions"] = questions
    
    await send_question(update, user_id)

async def send_question(update: Update, user_id: str):
    """Send current question to user"""
    
    session = user_sessions[user_id]
    idx = session["question_index"]
    questions = session["questions"]
    
    if idx >= len(questions):
        await submit_diagnostic(update, user_id)
        return
    
    q = questions[idx]
    
    keyboard = []
    for option in q["options"]:
        keyboard.append([InlineKeyboardButton(option, callback_data=f"ans_{q['id']}_{option}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        f"📝 *Question {idx+1}/{len(questions)}*\n\n{q['text']}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user's answer"""
    
    query = update.callback_query
    await query.answer()
    
    user_id = str(update.effective_user.id)
    data = query.data
    
    if data.startswith("ans_"):
        _, q_id, answer = data.split("_", 2)
        
        session = user_sessions[user_id]
        session["answers"][q_id] = answer
        session["question_index"] += 1
        
        await send_question(update, user_id)

async def submit_diagnostic(update: Update, user_id: str):
    """Submit answers and get results"""
    
    session = user_sessions[user_id]
    
    # Send to backend
    response = requests.post(
        f"{API_URL}/diagnostic",
        params={"student_id": user_id},
        json=session["answers"]
    )
    
    if response.status_code == 200:
        result = response.json()
        
        weak_topics = ", ".join(result["weak_topics"])
        message = (
            "✅ *Diagnostic Complete!*\n\n"
            f"📊 *Your weak areas:* {weak_topics}\n\n"
            "Generating your personalized 30-day plan..."
        )
        
        await update.callback_query.edit_message_text(message, parse_mode="Markdown")
        
        # Generate learning plan
        plan_response = requests.post(
            f"{API_URL}/generate_plan",
            params={"student_id": user_id}
        )
        
        if plan_response.status_code == 200:
            await update.callback_query.edit_message_text(
                "🎯 *Your 30-Day Learning Plan is Ready!*\n\n"
                "Type /today to see your first task.\n"
                "Type /progress when you complete a task.",
                parse_mode="Markdown"
            )
    else:
        await update.callback_query.edit_message_text("❌ Something went wrong. Please try /diagnostic again.")

async def today_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's learning task"""
    
    user_id = str(update.effective_user.id)
    
    response = requests.get(
        f"{API_URL}/today_task",
        params={"student_id": user_id}
    )
    
    if response.status_code == 200:
        task = response.json()
        message = (
            f"📚 *Task for Day {task['day']}*\n\n"
            f"📖 *Topic:* {task['topic']}\n"
            f"🎬 *Watch:* {task['title']}\n"
            f"🔗 {task['resource_url']}\n"
            f"⏱️ Duration: {task['duration_mins']} minutes\n\n"
            f"✍️ *Practice:* {task['practice_task']}\n\n"
            f"Reply with:\n"
            f"✅ 'done' - if completed\n"
            f"❌ 'stuck' - if you need help"
        )
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Run /diagnostic first to generate your plan.")

async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle daily progress updates"""
    
    user_id = str(update.effective_user.id)
    text = update.message.text.lower()
    
    if text == "done":
        progress_data = {
            "student_id": user_id,
            "day": 1,  # Would get from plan
            "task_completed": True,
            "struggled": False
        }
        
        response = requests.post(f"{API_URL}/progress", json=progress_data)
        
        if response.status_code == 200:
            await update.message.reply_text(
                "🎉 Great job! Keep going.\n"
                "Type /today for tomorrow's task."
            )
    
    elif text == "stuck":
        progress_data = {
            "student_id": user_id,
            "day": 1,
            "task_completed": False,
            "struggled": True
        }
        
        response = requests.post(f"{API_URL}/progress", json=progress_data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("adaptation_needed"):
                await update.message.reply_text(
                    "🔄 *Plan adapted!*\n\n"
                    "I've adjusted your learning path to make it easier.\n"
                    "Type /today to see your new task.",
                    parse_mode="Markdown"
                )

def get_questions():
    """Fetch questions from backend or return sample"""
    
    # Sample questions (in production, fetch from API)
    return [
        {"id": "q1", "text": "What does print(2**3) output?", "options": ["5", "6", "8", "9"]},
        {"id": "q2", "text": "How do you create a list in Python?", "options": ["{}", "()", "[]", "<>"]},
        {"id": "q3", "text": "What keyword defines a function?", "options": ["def", "func", "define", "function"]}
    ]

def main():
    """Start the bot"""
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("diagnostic", diagnostic))
    app.add_handler(CommandHandler("today", today_task))
    app.add_handler(CallbackQueryHandler(handle_answer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_progress))
    
    print("🤖 Telegram bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()