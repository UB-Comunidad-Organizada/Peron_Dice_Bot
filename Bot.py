import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')

# Lista de Verdades disponibles


def cargar_verdades():
    with open("verdades.json", "r", encoding="utf-8") as file:
        verdades = json.load(file)
        verdades_disponibles = verdades.get("Verdades_disponibles")
    return verdades_disponibles


# Cargar el diccionario desde el archivo .json
Verdades_disponibles = cargar_verdades()


async def Hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}')


async def Verdad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "No se ha proporcionado un número de verdad."
            )
        return

    Verdad_index = int(context.args[0]) - 1

    try:
        verdad_seleccionada = Verdades_disponibles[Verdad_index]
        await update.message.reply_text(
            f"Verdad {Verdad_index + 1}: {verdad_seleccionada}"
            )
    except IndexError:
        await update.message.reply_text("La verdad seleccionada no es válida.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Verdad", Verdad))

app.run_polling()
