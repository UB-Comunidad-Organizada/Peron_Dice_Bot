import sqlite3

def cargar_citas(etiqueta):
conn = sqlite3.connect('citas.db')
c = conn.cursor()
c.execute("SELECT cita FROM citas WHERE etiqueta = ?", (etiqueta,))
citas_disponibles = [row[0] for row in c.fetchall()]
conn.close()
return citas_disponibles