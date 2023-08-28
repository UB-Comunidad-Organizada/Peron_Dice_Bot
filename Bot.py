import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cargar variables de entorno desde el archivo config.env en la carpeta env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'env', 'config.env'))

# Accede al valor del TOKEN
TOKEN = os.getenv('Token')

# Lista de Verdades disponibles
Verdades_disponibles = [
    "La verdadera democracia es aquella donde el gobierno hace lo que el pueblo quiere y defiende un solo interés: el del pueblo.",
    "El peronismo es esencialmente popular. Todo círculo político es antipopular y, por lo tanto, no peronista.",
    "El peronista trabaja para el Movimiento. El que, en su nombre, sirve a un círculo o a un caudillo, lo es solo de nombre.",
    "No existe para el peronismo más que una sola clase de personas: los que trabajan.",
    "En la nueva Argentina de Perón, el trabajo es un derecho que crea la dignidad del Hombre y es un deber, porque es justo que cada uno produzca por lo menos lo que consume.",
    "Para un peronista no puede haber nada mejor que otro peronista.",
    "Ningún peronista debe sentirse más de lo que es ni menos de lo que debe ser. Cuando un peronista comienza a sentirse más de lo que es, empieza a convertirse en oligarca.",
    "En la acción política, la escala de valores de todo peronista es la siguiente: primero la patria, después el Movimiento y luego los hombres.",
    "La política no es para nosotros un fin, sino solo el medio para el bien de la Patria, que es la felicidad de sus hijos y la grandeza nacional.",
    "Los dos brazos del peronismo son la justicia social y la ayuda social. Con ellos, damos al pueblo un abrazo de justicia y amor.",
    "El peronismo anhela la unidad nacional y no la lucha. Desea héroes, pero no mártires.",
    "En la nueva Argentina, los únicos privilegiados son los niños.",
    "Un gobierno sin doctrina es un cuerpo sin alma. Por eso, el peronismo tiene una doctrina política, económica y social: el justicialismo.",
    "El justicialismo es una nueva filosofía de la vida, simple, práctica, popular, profundamente cristiana y profundamente humanista.",
    "Como doctrina política, el justicialismo realiza el equilibrio del derecho del individuo con el de la comunidad.",
    "Como doctrina económica, el justicialismo realiza la economía social, poniendo el capital al servicio de la economía y ésta al servicio del bienestar social.",
    "Como doctrina social, el justicialismo realiza la justicia social, que da a cada persona su derecho en función social.",
    "Queremos una Argentina socialmente justa, económicamente libre y políticamente soberana.",
    "Constituimos un gobierno centralizado, un Estado organizado y un pueblo libre.",
    "En esta tierra, lo mejor que tenemos es el pueblo."
]


async def Hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}')


async def Verdad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Obtener el índice de la verdad seleccionada
    Verdad_index = int(context.args[0]) - 1

    if Verdad_index < 0 or Verdad_index >= len(Verdades_disponibles):
        await update.message.reply_text("La verdad seleccionada no es válida.")
    else:
        verdad_seleccionada = Verdades_disponibles[Verdad_index]
        await update.message.reply_text(f"Verdad {Verdad_index + 1}: {verdad_seleccionada}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("Hola", Hola))
app.add_handler(CommandHandler("Verdad", Verdad))

app.run_polling()
