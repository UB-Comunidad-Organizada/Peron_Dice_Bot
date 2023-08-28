import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')


async def Hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))

app.run_polling()
