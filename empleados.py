from modules import sql

def new(clave, nombre):
    """Agrega un nuevo empleado en la base de datos.
    Argumentos:
        clave = Clave del empleado
        nombre = Nombre del empleado"""
    peticion = f"INSERT INTO empleados VALUES (NULL, {clave}, '{nombre}')"

    sql.peticion(peticion)


def ver(columns = '*'):
    """Return the employers from database. Columns is a string to say what columns you want."""
    peticion = f"SELECT {columns} FROM empleados ORDER BY clave DESC"
    listaEmpleados = sql.peticion(peticion)
    if len(listaEmpleados) == 1:
        pass 
    if len(listaEmpleados[0]) == 1:
        for i in listaEmpleados:
            listaEmpleados[listaEmpleados.index(i)] = i[0]
    return listaEmpleados

def buscar(id):
    peticion = f"SELECT * FROM empleados WHERE id='{id}'"
    resultado = sql.peticion(peticion)
    return resultado[0]

if __name__ == '__main__':
    print(ver('nombre'))
