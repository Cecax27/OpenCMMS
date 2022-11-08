try:
    import sql
except:
    from modules import sql

#Classes
class Employer():
    
    def __init__(self, id = 0):
        """When creating anew employer object, you can give the id of an existing employer or create a blank object"""
        self.id = id
        if self.id != 0:
            self.findById(self.id)
        
    def __repr__(self):
        return f"Employer Id {self.id}:\n\tName: {self.name}\n\tKey: {self.key}\n"
            
    def findById(self, id):
        rawData = buscar(id)
        self.key = rawData[1]
        self.name = rawData[2]
        

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

def getAll():
    peticion = "SELECT id FROM empleados"
    resultado = sql.peticion(peticion)
    list = []
    for i in resultado:
        list.append(Employer(id = i[0]))
    return list

if __name__ == '__main__':
    print(getAll())
