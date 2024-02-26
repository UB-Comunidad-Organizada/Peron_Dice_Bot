import os
from dotenv import load_dotenv
from tokenize import Token
from hola import Hola
from cita import cita
from handle_message import handle_message
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
MessageHandler,
filters
)

load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

TOKEN = os.getenv('Token')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Cita", cita))

app.add_handler(MessageHandler(filters.Text(), handle_message))

app.run_polling()