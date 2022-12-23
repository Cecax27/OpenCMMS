import sqlite3 as sql

db = 'database.db'

def checkDatabase():
    peticion('''CREATE TABLE IF NOT EXISTS "workorders" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	TIMESTAMP NOT NULL,
	"status"	TEXT NOT NULL,
	"responsible"	INTEGER NOT NULL,
	"comment"	TEXT,
	FOREIGN KEY("responsible") REFERENCES "empleados"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
	);''')
    
    peticion('''CREATE TABLE IF NOT EXISTS "workorders_detail" (
	"id"	INTEGER NOT NULL UNIQUE,
	"workorder_id"	INTEGER NOT NULL,
	"maintenance_id"	INTEGER NOT NULL,
	FOREIGN KEY("workorder_id") REFERENCES "workorders"("id"),
	FOREIGN KEY("maintenance_id") REFERENCES "mantenimientos"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
	);''')
    
    peticion('''CREATE TABLE IF NOT EXISTS "requisitions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	TIMESTAMP NOT NULL,
	"status"	TEXT NOT NULL,
	"description"	TEXT,
 	"delivered"	TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
	);''')
    
    peticion('''CREATE TABLE IF NOT EXISTS "requisitions_detail" (
	"id"	INTEGER NOT NULL UNIQUE,
	"requisition_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"comment"	TEXT,
	"status"	TEXT NOT NULL,
	FOREIGN KEY("requisition_id") REFERENCES "requisitions"("id"),
	FOREIGN KEY("product_id") REFERENCES "inventory"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
	);''')
    
    peticion('''CREATE TABLE IF NOT EXISTS "inventory_detail" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	BLOB NOT NULL,
	"type"	TEXT NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"comment"	TEXT,
	"origin"	TEXT,
	"origin_id"	INTEGER,
	FOREIGN KEY("product_id") REFERENCES "inventory"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
	);''')
    

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
	table('empleados')