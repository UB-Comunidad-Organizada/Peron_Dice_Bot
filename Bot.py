import os
import time
import asyncio
import threading
# from collections import Counter
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
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
logging.basicConfig(filename='error.log', level=logging.ERROR)

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


def cargar_verdades():
    # Conectarse a la base de datos SQLite
    conn = sqlite3.connect('citas.db')
    c = conn.cursor()

    # Ejecutar una consulta de selección para obtener las verdades
    c.execute("""
    CREATE TABLE IF NOT EXISTS verdades (
        id INTEGER PRIMARY KEY,
        verdad TEXT
    )
""")
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
    Verdades_disponibles = cargar_verdades()

    try:
        condicion = Verdades_disponibles and Verdad_index >= 0
        condicion = condicion and Verdad_index < len(Verdades_disponibles)

        if condicion:
            verdad_seleccionada = Verdades_disponibles[Verdad_index]
            await update.message.reply_text(
                f"Verdad {Verdad_index + 1}: {verdad_seleccionada}"
            )
        else:
            await update.message.reply_text(
                "El número de verdad seleccionado no es válido."
            )
    except IndexError:
        await update.message.reply_text(
            "El índice de verdad está fuera de rango."
        )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    conn = None
    try:
        # Extraer el texto y dividirlo en palabras
        texto = update.message.text
        palabras = texto.split()
        # Conectar a la base de datos
        conn = sqlite3.connect('mi_base_de_datos.db')
        c = conn.cursor()
        # Crear la tabla 'palabras' si no existe
        c.execute('''
            CREATE TABLE IF NOT EXISTS palabras (
                palabra TEXT,
                timestamp INTEGER
            )
        ''')
        # Insertar palabras en la base de datos con la marca de tiempo actual
        timestamp = int(time.time())
        for palabra in palabras:
            c.execute(
                "INSERT INTO palabras VALUES (?, ?)", (palabra, timestamp)
            )
        # Confirmar los cambios
        conn.commit()
    except Exception as e:
        logging.exception(e)
    finally:
        # Cerrar la conexión
        if conn is not None:
            conn.close()


async def actualizar_palabra_mas_usada():
    while True:
        conn = sqlite3.connect('mi_base_de_datos.db')
        c = conn.cursor()
        # Consultar la BD para contar las palabras en los últimos 10 minutos
        timestamp = int(time.time())
        memoria_corta = timestamp - 600  # 600 segundos = 10 minutos
        c.execute(
            "SELECT palabra, COUNT(*) AS count FROM "
            "palabras WHERE timestamp > ? GROUP BY palabra",
            (memoria_corta,)
        )
        conteo_palabras = c.fetchall()
        # Encontrar la palabra más usada
        if conteo_palabras:
            palabra_mas_usada = max(conteo_palabras, key=lambda x: x[1])[0]
            print(
                f"La palabra más usada en los últimos 10 minutos es: "
                f"{palabra_mas_usada}"
            )
        else:
            print("No se usaron palabras en los últimos 10 minutos.")
        # Cerrar la conexión
        conn.close()
        # Esperar 10 minutos
        await asyncio.sleep(600)

# Iniciar la función actualizar_palabra_mas_usada en segundo plano
# asyncio.create_task(actualizar_palabra_mas_usada())


"""

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        # Extract the text and split it into words
        texto = update.message.text
        palabras = texto.split()
        # Connect to the database
        conn = sqlite3.connect('mi_base_de_datos.db')
        if conn:
            c = conn.cursor()
            # Create the 'palabras' table if it doesn't exist
            c.execute('''
                CREATE TABLE IF NOT EXISTS palabras (
                    palabra TEXT,
                    timestamp INTEGER
                )
            ''')
            # Insert words into the database with the current timestamp
            timestamp = int(time.time())
            for palabra in palabras:
                c.execute(
                    "INSERT INTO palabras VALUES (?, ?)", (palabra, timestamp)
                )
            # Commit the changes
            conn.commit()
            # Query the database to count the words in the last 10 minutes
            memoria_corta = timestamp - 600  # 600 seconds = 10 minutes
            c.execute(
                "SELECT palabra, COUNT(*) AS count FROM "
                "palabras WHERE timestamp > ? GROUP BY palabra",
                (memoria_corta,)
            )
            conteo_palabras = c.fetchall()
            # Find the most used word
            if conteo_palabras:
                palabra_mas_usada = max(conteo_palabras, key=lambda x: x[1])[0]
                print(
                    f"The most used word in the last 10 minutes is: "
                    f"{palabra_mas_usada}"
                )
            else:
                print("No words were used in the last 10 minutes.")
            # Close the connection
            conn.close()
    except Exception as e:
        logging.exception(e)

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        # Extraer el texto y dividirlo en palabras
        texto = update.message.text
        palabras = texto.split()
        # Conectar a la base de datos
        conn = sqlite3.connect('mi_base_de_datos.db')
        if conn:
            c = conn.cursor()
            try:
                c.execute('''
                    CREATE TABLE IF NOT EXISTS palabras (
                        palabra TEXT,
                        timestamp INTEGER
                        )
                ''')
            except sqlite3.OperationalError:
                logging.exception("No se pudo crear la tabla 'palabras'.")
        # Insertar palabras en la base de datos con la marca de tiempo actual
        timestamp = int(time.time())
        for palabra in palabras:
            c.execute(
                "INSERT INTO palabras VALUES (?, ?)", (palabra, timestamp)
            )
        # Confirmar los cambios
        conn.commit()
        # Consultar la BD para contar las palabras en los últimos 10 minutos
        memoria_corta = timestamp - 600  # 600 segundos = 10 minutos
        c.execute(
            "SELECT palabra, COUNT(*) AS count FROM "
            "palabras WHERE timestamp > ? GROUP BY palabra",
            (memoria_corta,)
        )
        conteo_palabras = c.fetchall()
        # Encontrar la palabra más utilizada
        if conteo_palabras:
            palabra_mas_usada = max(conteo_palabras, key=lambda x: x[1])[0]
            print(
                f"La palabra más utilizada en los últimos 10 minutos es: "
                f"{palabra_mas_usada}"
            )
        else:
            print("No se utilizaron palabras en los últimos 10 minutos.")
        # Cerrar la conexión
        conn.close()
    except Exception as e:
        logging.exception(e)
"""

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Verdad", Verdad))

# Maneja todos los mensajes de texto
app.add_handler(MessageHandler(filters.Text(), handle_message))


# Luego, en la parte inferior de tu script,
# puedes iniciar el bucle de eventos asyncio así:
def run_bot():
    app.run_polling()


async def main():
    asyncio.create_task(actualizar_palabra_mas_usada())
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
