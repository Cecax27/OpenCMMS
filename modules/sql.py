import sqlite3 as sql

db = 'database.db'

def table(nombre):
	"""Agrega una tabla a la base de datos.
	Argumento:
		nombre = será el nombre de la tabla"""
	conn = sql.connect(db)
	instruccion = """CREATE TABLE 'empleados'
	('id'	INTEGER NOT NULL UNIQUE,
	'clave' INTEGER,
	'nombre' TEXT,
	PRIMARY KEY('id' AUTOINCREMENT)
	)"""
	cursor = conn.cursor()
	cursor.execute(instruccion)
	conn.commit()
	conn.close()

def peticion(peticion):
	"""Hace una petición a la base de datos SQL
	Argumento:
		peticion = un string con la petición"""
	conn = sql.connect(db)
	cursor = conn.cursor()
	cursor.execute(peticion)
	retorno = cursor.fetchall()
	conn.commit()
	conn.close()
	return retorno





if __name__ == '__main__':
	table('empleados')