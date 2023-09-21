import os
import json
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler
)

# Configurando el módulo de registro en Python.
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')

# Accede al valor de chat

def cargar_verdades():
    # Cargar archivo JSON con verdades
    with open("verdades.json", "r", encoding="utf-8") as file:
        verdades = json.load(file)
        # Obtener verdades disponibles
        verdades_disponibles = verdades.get("Verdades_disponibles")
    # Retornar verdades disponibles
    return verdades_disponibles


# Cargar el diccionario desde el archivo .json
Verdades_disponibles = cargar_verdades()


async def Hola(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    try:
        await update.message.reply_text(
            f'Hola {update.effective_user.first_name}'
            )
    except Exception as e:
        logging.exception(e)


async def Verdad(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
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
        logging.exception("La verdad seleccionada no es válida.")


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        await print("Lo siento, no entiendo ese comando.")
    except Exception as e:
        logging.exception(e)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Verdad", Verdad))

# Maneja todos los mensajes de texto
app.add_handler(MessageHandler(filters.Text(), handle_message))

# Arranca el Bot
app.run_polling()
