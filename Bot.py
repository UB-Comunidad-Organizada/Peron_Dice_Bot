import os
import logging
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')


def ultimo_chat_id(
    update: Update, context: CallbackContext, usuario_id: int
) -> int:

    # Obtener el último mensaje del usuario
    ultimo_mensaje = context.bot.get_chat(usuario_id).last_message

    # Obtener el ID del chat en el que se escribió el último mensaje
    chat_id = ultimo_mensaje.chat_id

    return chat_id


def cargar_verdades():
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()

    # Ejecutar una consulta de selección para obtener las verdades
    c.execute("SELECT * FROM verdades")
    verdades_disponibles = [row[0] for row in c.fetchall()]

    # Cerrar la conexión
    conn.close()

    # Devolver las verdades
    return verdades_disponibles


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
    # Llamando a la función para asignar a la variable `Verdades_disponibles`.
    Verdades_disponibles = []

    try:
        if Verdad_index >= 0 and Verdad_index < len(Verdades_disponibles):
            verdad_seleccionada = Verdades_disponibles[Verdad_index]
            await update.message.reply_text(
                f"Verdad {Verdad_index + 1}: {verdad_seleccionada}"
            )
        else:
            await update.message.reply_text(
                "El número de verdad seleccionado no es válido."
            )
    except IndexError:
        logging.exception("La verdad seleccionada no es válida.")


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        # Extraer texto y dividirse en palabras
        text = update.message.text
        words = text.split()

        # Conectarse a la base de datos
        conn = sqlite3.connect('my_database.db')
        c = conn.cursor()

        # Insertar palabras en la base de datos
        for word in words:
            c.execute("Insertar en valores de palabras (?)", (word,))

        # Confirme los cambios y cierre la conexión
        conn.commit()
        conn.close()

        # Consulta la base de datos para los recuentos de palabras
        c.execute(
            "Seleccione Word, Count (*) como recuento del "
            "grupo de palabras por palabra"
        )
        word_counts = c.fetchall()

        # Generar una nube de palabras
        wordcloud = WordCloud().generate_from_frequencies(dict(word_counts))

        # Muestra la nube de palabras
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    except Exception as e:
        logging.exception(e)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Verdad", Verdad))

# Maneja todos los mensajes de texto
app.add_handler(MessageHandler(filters.Text(), handle_message))

# Arranca el Bot
app.run_polling()
