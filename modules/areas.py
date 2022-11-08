try:
    import sql
except:
    from modules import sql
try:
    import employers
except:
    from modules import employers

#Classes
class Area():
    
    def __init__(self, id = 0):
        self.id = id
        if self.id != 0:
            self.findById(self.id)
            return
        self.name = ''
        self.description = ''
        self.responsible = employers.Employer()
        self.department = Department()
        
    def __repr__(self) -> str:
        return f"Area ID {self.id}:\n\tName: {self.name}\n\tDescription: {self.description}\n\tResponsible: {self.responsible.id}\n\tDepartment: {self.department.id}"
            
    def findById(self, id):
        self.id = id
        rawData = buscar(id)
        self.name = rawData[1]
        self.description = rawData[2]
        self.responsible = employers.Employer(id = rawData[3])
        self.department = Department(id = rawData[4])
        
class Department():
    
    def __init__(self, id = 0):
        self.id = id
        if self.id != 0:
            self.findById(self.id)
            return
        self.name = ''
    
    def __repr__(self) -> str:
        return f"Department ID {self.id}:\n\tName: {self.name}"

    def findById(self, id):
        self.id = id
        rawData = buscarDepartamento(id)
        self.name = rawData[1]
    
        

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

        peticion = f"SELECT nombre FROM empleados WHERE id = {x[3]}"
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
    return lista[0]

def buscarDepartamento(id):
    peticion=f"SELECT * from departamentos WHERE id = {id}"
    resultado = sql.peticion(peticion)
    return resultado[0]


def modificar(idNo, nombre, descripcion, responsable, departamento):
    peticion= f"UPDATE areas SET nombre='{nombre}', descripcion='{descripcion}', responsable={responsable}, departamento= {departamento} WHERE id={idNo}"
    sql.peticion(peticion)

def areasEnDepartamento(id):
    """Retorna un int con la cantidad de areas que tiene registrado un departamento"""
    peticion = f"SELECT * FROM areas WHERE departamento = {id}"
    resultado = len(sql.peticion(peticion))
    return resultado

def findByEmployerId(id):
    """Find all the areas with an employer id"""
    areasList = []
    for id in sql.peticion(f"SELECT id FROM areas WHERE responsable = {id}"):
        areasList.append(Area(id = id[0]))
    return areasList

#Para hacer pruebas
if __name__ == '__main__':
    findByEmployerId(15)
    


        
