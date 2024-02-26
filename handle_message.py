import logging
from hola import Hola
from cita import cita

async def handle_message(update, context):
    try:
        texto = update.message.text
        palabras = texto.split()
        comandos = {
            "Hola": Hola,
            "Cita": cita
        }

        for palabra in palabras:
            if palabra in comandos:
                await comandos[palabra](update, context)

    except Exception as e:
        logging.exception(e)