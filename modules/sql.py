import sqlite3 as sql
import logging

db = __file__.replace('modules\\sql.py', 'database.db')
logging.basicConfig(filename = __file__.replace('modules\\sql.py', 'errors.log'), level = logging.INFO)

def checkDatabase():
	with open(__file__.replace('sql.py', 'database.txt'), "r") as f:
		content = f.read()
		for line in content.split(';'):
			try:
				petition(line)
			except Exception as e:
				logging.info("An error ocurred: ")
				logging.info(e)
				logging.info("On instruction: ")
				logging.info(line)
				print(e)
    

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

def petitionWithParam(petition, values):
	"""Hace una petición a la base de datos SQL
	Argumento:
		petition = un string con la petición"""
	conn = sql.connect(db, detect_types = sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
	cursor = conn.cursor()
	cursor.execute(petition, values)
	conn.commit()
	conn.close()
 
def petition(petition):
	"""Hace una petición a la base de datos SQL
	Argumento:
		petition = un string con la petición"""
	conn = sql.connect(db, detect_types = sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
	cursor = conn.cursor()
	cursor.execute(petition)
	retorno = cursor.fetchall()
	conn.commit()
	conn.close()
	return retorno
 
def peticiontres(peticion):
	"""Hace una petición a la base de datos SQL
	Argumento:
		peticion = un string con la petición"""
	conn = sql.connect(db, detect_types = sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)
	cursor = conn.cursor()
	cursor.execute(peticion)
	retorno = cursor.fetchall()
	conn.commit()
	conn.close()
	return retorno

if __name__ == '__main__':
	pass