import random
from citas import cargar_citas

async def cita(update, context):
    if not context.args:
        await update.message.reply_text("No se ha proporcionado una etiqueta.")

async def send_random_cita(update, context):
    etiqueta = context.args[0]
    citas_disponibles = cargar_citas(etiqueta)

    if not citas_disponibles:
        await update.message.reply_text("No se encontraron citas para la etiqueta proporcionada.")
        return

    cita_seleccionada = random.choice(citas_disponibles)
    await update.message.reply_text(f"Cita: {cita_seleccionada}")
