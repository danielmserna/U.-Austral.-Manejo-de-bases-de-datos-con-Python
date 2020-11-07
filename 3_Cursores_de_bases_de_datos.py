import sqlite3

#Conexión a la base de datos
conn = sqlite3.connect(':memory:')

#Cursor
cursor = conn.cursor()

#Crear la tabla
cursor.execute(
    """CREATE TABLE currency(ID integer primary key, name text, symbol text)"""
)

#Insertar datos de las monedas
cursor.execute("INSERT INTO currency VALUES (1, 'Peso (ARG)', '$')")
cursor.execute("INSERT INTO currency VALUES (2, 'Dólar', 'US $')")

#Guardar los cambios
conn.commit()

#Consulto todas las monedas
query = "SELECT * FROM currency"

#Busco el resultado
currency = cursor.execute(query).fetchone()

print(currency)
print(cursor.fetchone())
print(cursor.fetchone())

currencies = cursor.execute(query).fetchall()
print(currencies)

#Cierro la conexión a la base de datos
conn.close()