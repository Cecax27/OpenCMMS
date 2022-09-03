from modules import sql

def new(nombre, descripcion, responsable, departamento):
    peticion = f"INSERT INTO areas VALUES (NULL, '{nombre}', '{descripcion}', {responsable}, {departamento})"

    sql.peticion(peticion)

def eliminarArea(id):
    instruccion = f"DELETE FROM areas WHERE id = {id}"
    sql.peticion(instruccion)

def nuevoDepartamento(nombre):
    instruccion = f"INSERT INTO departamentos VALUES (NULL, '{nombre}')"
    sql.peticion(instruccion)

def modificarDepartamento(id, nombre):
    instruccion = f"UPDATE departamentos SET nombre='{nombre}' WHERE id = {id}"
    sql.peticion(instruccion)

def eliminarDepartamento(id):
    instruccion = f"DELETE FROM departamentos WHERE id = {id}"
    sql.peticion(instruccion)

def getDepartamentos():
    instruccion = f"SELECT * FROM departamentos ORDER BY id DESC"
    resultado = sql.peticion(instruccion)
    for x in resultado:
        resultado[resultado.index(x)] = list(x)
    return resultado

def buscarPorDepartamento(departamento):
    #print(departamento)
    instruccion = f"SELECT *, descripcion, responsable FROM areas WHERE departamento = '{departamento}'"
    lista = sql.peticion(instruccion)
    return lista

def ver():
    peticion = f"SELECT * FROM areas ORDER BY id DESC"

    lista = sql.peticion(peticion)
    
    for x in lista:
        lista[lista.index(x)]=list(x)
        x = list(x)

        peticion = f"SELECT nombre FROM empleados WHERE clave = {x[3]}"
        resultado = sql.peticion(peticion)
        indice = lista.index(x)
        lista[indice][3] = resultado[0][0]

        instruccion = f"SELECT nombre FROM departamentos WHERE id = {x[4]}"
        resultado = sql.peticion(instruccion)
        lista[indice][4] = resultado[0][0]

    return lista

def buscar(id):
    """Busca un registro en la base de datos por id"""

    peticion=f"SELECT * FROM areas WHERE id='{id}'"
    lista = sql.peticion(peticion)

    for x in lista:
        lista[lista.index(x)]=list(x)
        x = list(x)

        peticion = f"SELECT nombre FROM empleados WHERE clave = {x[3]}"
        resultado = sql.peticion(peticion)
        indice = lista.index(x)
        lista[indice][3] = resultado[0][0]

        instruccion = f"SELECT nombre FROM departamentos WHERE id = {x[4]}"
        resultado = sql.peticion(instruccion)
        lista[indice][4] = resultado[0][0]

    return lista[0]

def buscarDepartamento(id):
    peticion=f"SELECT * from departamentos WHERE id = {id}"
    resultado = sql.peticion(peticion)
    return resultado


def modificar(idNo, nombre, descripcion, responsable, departamento):
    peticion= f"UPDATE areas SET nombre='{nombre}', descripcion='{descripcion}', responsable={responsable}, departamento= {departamento} WHERE id={idNo}"
    sql.peticion(peticion)

def areasEnDepartamento(id):
    """Retorna un int con la cantidad de areas que tiene registrado un departamento"""
    peticion = f"SELECT * FROM areas WHERE departamento = {id}"
    resultado = len(sql.peticion(peticion))
    return resultado

#Para hacer pruebas
if __name__ == '__main__':
    areasEnDepartamento(2)


        
