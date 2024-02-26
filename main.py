import os
import random
import sqlite3
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
ContextTypes,
MessageHandler,
CallbackContext,
filters
)

load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

TOKEN = os.getenv('Token')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Cita", cita))

app.add_handler(MessageHandler(filters.Text(), handle_message))

app.run_polling()