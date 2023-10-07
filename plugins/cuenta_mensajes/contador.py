import time
import random
import sqlite3
import logging
import telegram
from collections import Counter



# Configurando el módulo de registro en Python.
logging.basicConfig(filename= 'logs\error_contador.log', level=logging.ERROR)


# Función para obtener las etiquetas y etiquetas secundarias desde la base de datos
def etiquetas_de_citas():
    etiquetas = []

    # Conexión a la base de datos
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect("database/citas.db")
        cursor = conn.cursor()

        # Consulta para obtener las etiquetas
        cursor.execute("SELECT Etiqueta, `Etiquetas Secundarias` FROM Etiqueta")
        etiquetas = [row[0] for row in cursor.fetchall()]
        etiquetas_secundarias = [
            tag for row in cursor.fetchall() for tag in row[1].split(",") if row[1]
        ]

        # Extender la lista de etiquetas con las etiquetas secundarias
        etiquetas.extend(etiquetas_secundarias)

    except Exception as e:
        logging.exception(e)

    finally:
        # Cerrar el cursor y la conexión a la base de datos
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return etiquetas

# Función para realizar el conteo de palabras en cada chat
def contar_palabras_en_chat(chat_id, tiempo, repeticiones):
    # Obtener la lista de etiquetas de citas
    etiquetas = etiquetas_de_citas()

    # Crear una instancia del cliente de Telegram
    bot = telegram.Bot(token='TOKEN')

    # Obtener los mensajes del chat
    mensajes = bot.get_chat(chat_id).get('messages', [])

    # Filtrar los mensajes según el rango de tiempo
    mensajes_filtrados = [mensaje for mensaje in mensajes if mensaje.date >= tiempo]

    # Obtener todas las palabras de los mensajes filtrados y convertirlas a minúsculas
    palabras = [
        palabra.lower() for mensaje in mensajes_filtrados 
        for palabra in mensaje.text.split()
    ]

    # Crear un contador de palabras
    conteo_palabras = Counter()

    # Contar las palabras que están en la lista de etiquetas de citas
    for palabra in palabras:
        if palabra in etiquetas:
            conteo_palabras[palabra] += 1

    # Obtener la palabra más utilizada si cumple con el criterio de repeticiones
    palabra_mas_utilizada = None
    max_repeticiones = 0
    for palabra, repeticiones in conteo_palabras.items():
        if repeticiones >= repeticiones and repeticiones > max_repeticiones:
            palabra_mas_utilizada = palabra
            max_repeticiones = repeticiones

    return palabra_mas_utilizada
# Función para determinar la etiqueta más repetida que cumple con las condiciones
def determinar_etiqueta_mas_repetida(etiquetas, tiempo, repeticiones):
    # Código para determinar la etiqueta más repetida que cumple con las condiciones
    pass

# Función para actualizar el conteo y enviar la etiqueta a la cola de citas
def actualizar_conteo_y_enviar_etiqueta(chat_id, etiqueta):
    # Código para actualizar el conteo y enviar la etiqueta a la cola de citas
    pass

# Función para realizar el análisis periódico de los mensajes en cada chat
def analisis_periodico():
    # Bucle infinito para realizar el análisis periódico
    while True:
        # Obtener las etiquetas desde la base de datos
        etiquetas = etiquetas_de_citas()

        # Recorrer cada chat y realizar el conteo de palabras
        for chat_id in lista_chat_ids:
            contar_palabras(chat_id)

            # Determinar la etiqueta más repetida que cumple con las condiciones
            etiqueta_mas_repetida = determinar_etiqueta_mas_repetida(etiquetas, tiempo, repeticiones)

            # Actualizar el conteo y enviar la etiqueta a la cola de citas
            if etiqueta_mas_repetida:
                actualizar_conteo_y_enviar_etiqueta(chat_id, etiqueta_mas_repetida)

        # Esperar 30 segundos antes de realizar el próximo análisis
        time.sleep(30)

# Función principal para iniciar el análisis periódico
def main():
    # Obtener la lista de chat IDs en los que el bot está interactuando
    lista_chat_ids = obtener_lista_chat_ids()

    # Iniciar el análisis periódico
    analisis_periodico()

# Ejecutar la función principal
if __name__ == "__main__":
    main()