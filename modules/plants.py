try:
    import sql
except:
    from modules import sql
try:
    import areas
    import maintenances
except:
    from modules import areas, maintenances

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
        
    def getMaintenances(self):
        return [maintenances.Maintenance(id[0]) for id in sql.petition(f"SELECT DISTINCT mantenimientos_actividadesAsignadas.mantenimientoId FROM mantenimientos_actividadesAsignadas LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id LEFT JOIN mantenimientos ON mantenimientos_actividadesAsignadas.mantenimientoId = mantenimientos.id WHERE actividadesAsignadas.idEquipo = {self.id} ORDER BY mantenimientos.fecha DESC")]
    
    def getLastMaintenance(self):
        id = sql.petition(f"SELECT mantenimientos.id, MAX(mantenimientos.fecha) FROM mantenimientos LEFT JOIN mantenimientos_actividadesAsignadas ON mantenimientos.id = mantenimientos_actividadesAsignadas.mantenimientoId LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id WHERE actividadesAsignadas.idEquipo = {self.id} AND mantenimientos.estado = '{maintenances.Done}'")[0][0]
        if id == None:
            return None
        return maintenances.Maintenance(id)

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

def get(all = False, name = None, department = None, area = None):
    if all:
        return [Plant(id[0]) for id in sql.petition(f"SELECT id FROM equipos ORDER BY area")]
    instruction = f"SELECT equipos.id FROM equipos LEFT JOIN areas ON equipos.area = areas.id WHERE "
    if name != None and name != "":
        instruction += f" equipos.nombre LIKE '%{name}%' "
    if department != None and department != -1:
        instruction += "AND" if (name != None and name != "") else "" 
        instruction += f" areas.departamento = {department} "
    if area != None and area != -1:
        instruction += "AND" if ((name != None and name != "") or (department != None and department != -1)) else "" 
        instruction += f" equipos.area = {area} "
    instruction += " ORDER BY area"
    return [Plant(id[0]) for id in sql.petition(instruction)]


