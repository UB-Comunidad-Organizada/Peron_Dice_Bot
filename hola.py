import logging  # Importa el módulo logging

async def Hola(update, context):
    try:
        await update.message.reply_text(f'Hola {update.effective_user.first_name}')
    except Exception as e:
        logging.exception(e)