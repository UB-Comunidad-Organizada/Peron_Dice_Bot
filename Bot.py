import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')

# Lista de citas disponibles
citas_disponibles = [
    "Cita 1",
    "Cita 2",
    "Cita 3"
]


async def Hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}')


async def SolicitarCita(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtener el índice de la cita seleccionada
    cita_index = int(context.args[0]) - 1

    if cita_index < 0 or cita_index >= len(citas_disponibles):
        await update.message.reply_text("La cita seleccionada no es válida.")
    else:
        cita_seleccionada = citas_disponibles[cita_index]
        await update.message.reply_text(f"Has solicitado la cita: {cita_seleccionada}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("SolicitarCita", SolicitarCita))

app.run_polling()
