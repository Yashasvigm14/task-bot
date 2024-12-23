from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3

# Database setup
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT,
        assigned_to TEXT
    )
""")
conn.commit()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your Operations Bot. Type /help to see available commands.")

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
    Available commands:
    /start - Start the bot
    /help - List all commands
    /status - Check bot status
    /assign - Assign tasks to team members
    /tasks - View all assigned tasks
    """)

# Command: /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("The bot is running and ready to assist!")

# Command: /assign
async def assign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /assign [task] [user]")
        return

    task = " ".join(args[:-1])
    user = args[-1]

    # Save task to the database
    cursor.execute("INSERT INTO tasks (task, assigned_to) VALUES (?, ?)", (task, user))
    conn.commit()

    await update.message.reply_text(f"Task '{task}' assigned to {user}.")

# Command: /tasks
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    if rows:
        response = "\n".join([f"{row[1]} → {row[2]}" for row in rows])
    else:
        response = "No tasks assigned."
    await update.message.reply_text(response)

# Main function
def main():
   
    TOKEN = "7538917853:AAFX7G4yHuQ4egHJKHUEH3NMlDnkkj5KQQg"

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("assign", assign))  
    application.add_handler(CommandHandler("tasks", tasks))  

    # Run the Bot
    application.run_polling()

if __name__ == "__main__":
    main()

