try:
    import sql
except:
    from modules import sql
try:
    import areas
except:
    from modules import areas

class Plant:
    def __init__(self, id = 0):
        self.id = id
        if self.id != 0:
            self.findById(self.id)
            return
        self.name = ''
        self.description = ''
        self.area = areas.Area()
        self.department = areas.Department()
        self.activities = []
        
    def __repr__(self):
        return f"Plant ID {self.id}:\n\tName: {self.name}\n\tDescription: {self.description}\n\tDepartment: {self.department}\tArea: {self.area}\n"

    def findById(self, id):
        self.id = id
        rawData = buscar(id)
        if rawData == None:
            print(f"Plant with ID {id} was not found")
            return 1
        self.name = rawData[1]
        self.description = rawData[2]
        rawDataArea = areas.buscar(rawData[3])
        self.area = areas.Area(id =rawDataArea[0])
        self.department = areas.Department(id = rawDataArea[4])
        self.activities = []

def new(nombre, descripcion, area):
    """Inserta un nuevo equipo en la base de datos.
    parametors: nombre, descripcion, area"""
    instruccion = f"INSERT INTO equipos VALUES (NULL, '{nombre}', '{descripcion}', '{area}')"
    sql.peticion(instruccion)

def modificar(id, nombre, descripcion, area):
    """Modificar un equipo en la base de datos.
    Parámetros:
        id: id del equipo a modificar.
        Str nombre: Nombre nuevo del equipo.
        Str descripcion: Descripción nueva del equipo.
        id area: id del area modificada.
    """
    instruccion = f"UPDATE equipos SET nombre='{nombre}', descripcion='{descripcion}', area={area} WHERE id ={id}"
    sql.peticion(instruccion)

def buscar(id):
    """Busca un registro en la base de datos por el id."""
    instruccion = f"SELECT * FROM equipos WHERE id={id}"
    resultado = sql.peticion(instruccion)
    return resultado[0]

def ver():
    instruccion = f"SELECT * FROM equipos ORDER BY area"
    lista = sql.peticion(instruccion)
    return lista

def buscarPorArea(area):
    """Busca todos los equipos por area. Como parámetro se pasa el id del area."""
    instruccion = f"SELECT * FROM equipos WHERE area = {area}"
    lista = sql.peticion(instruccion)
    return lista

def eliminar(id):
    instruccion = f"DELETE FROM equipos WHERE id = '{id}'"
    sql.peticion(instruccion)



