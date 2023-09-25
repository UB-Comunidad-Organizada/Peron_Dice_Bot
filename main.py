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

# Configurando el módulo de registro en Python.
logging.basicConfig(filename= 'logs\error.log', level=logging.ERROR)

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')


def ultimo_chat_id(
    update: Update, context: CallbackContext, usuario_id: int
) -> int:

    # Obtener el último mensaje del usuario
    try:
        ultimo_mensaje = context.bot.get_chat(usuario_id).last_message
        if ultimo_mensaje:
            chat_id = ultimo_mensaje.chat_id
        else:
            chat_id = None
        return chat_id
    except AttributeError:
        logging.exception("El usuario no tiene mensajes.")
        chat_id = None


def cargar_citas(etiqueta):
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()

    # Ejecutar una consulta de selección para obtener las citas
    c.execute("SELECT cita FROM citas WHERE etiqueta = ?", (etiqueta,))

    citas_disponibles = [row[0] for row in c.fetchall()]

    # Cerrar la conexión
    conn.close()

    # Devolver las citas
    return citas_disponibles


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


async def cita(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not context.args:
        await update.message.reply_text(
            "No se ha proporcionado una etiqueta."
        )
        return

    etiqueta = context.args[0]
    citas_disponibles = cargar_citas(etiqueta)

    if not citas_disponibles:
        await update.message.reply_text(
            "No se encontraron citas para la etiqueta proporcionada."
        )
        return

    cita_seleccionada = random.choice(citas_disponibles)
    await update.message.reply_text(f"Cita: {cita_seleccionada}")


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        # Extraer el texto y dividirlo en palabras
        texto = update.message.text
        palabras = texto.split()

        # Definir los comandos y las funciones correspondientes
        comandos = {
            "Hola": Hola,
            "Cita": cita
        }

        # Verificar si alguna de las palabras es un comando
        for palabra in palabras:
            if palabra in comandos:
                # Si la palabra es un comando, 
                # ejecutar la función correspondiente
                await comandos[palabra](update, context)

    except Exception as e:
        logging.exception(e)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Cita", cita))

# Maneja todos los mensajes de texto
app.add_handler(MessageHandler(filters.Text(), handle_message))

# Arranca el Bot
app.run_polling()
