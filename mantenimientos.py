from modules import sql
from datetime import date
from datetime import datetime
from datetime import timedelta
from actividades import nuevaActividadAsignada, Activity

#Const-----
Done = 'Realizado'
Programmed = 'Programado'
Cancelled = 'Cancelado'

Corrective = 'Correctivo'
Predictive = 'Predictivo'
Preventive = 'Preventivo'

#Objetos
class Maintenance:
    def __init__(self, id = 0, type=''):
        """When creating a new maintenance, you must specify the type of maintenance that will be. 
        The parameter type receive a string 'predictive' for predictive maintenances, and 'corrective' for corrective maintenance."""
        self.id = id
        if id != 0:
            self.findById(id)
            return
        self.date = date(2000, 1, 1)
        self.resposible = 0
        self.description = ''
        self.repeat = None
        self.previous = None
        self.next = None
        if(type == 'predictive'):
            self.status = '' #WIP
            self.type = Predictive
        elif type == Preventive:
            self.status = Programmed
            self.type = Preventive
            self.activities = []
        elif type == 'corrective':
            print('Creating corrective maintenance...')
            self.status = Done
            self.type = Corrective
            self.plants = []

    def save(self):
        """Save the maintenance in the database"""
        if self.id == 0: #If is a new maintenance
            print("Saving maintenance...")
            nuevo(
                self.date,
                self.status,
                self.responsible,
                self.description,
                self.type,
                self.repeat,
                self.previous,
                self.next)
            self.id = ultimoMantenimiento()
            print(f"The maintenance was created with id {self.id}")
        else: #If isnt a new maintenance
            editar(self.id, self.date, self.status, self.responsible, self.description, self.type, self.repeat, self.previous, self.next)
            print(f"Maintenance with ID {self.id} was updated")
        if self.type == Corrective:
            for plant in self.plants:
                if findCorrectiveActivity(plant[0]):
                    agregarActividad(self.id, findCorrectiveActivity(plant[0]))
                    print(f"Plant Id {plant[0]} added")
                else:
                    nuevaActividadAsignada('Mantenimiento correctivo', 'Se corrigió alguna falla en el equipo', 2, plant[0])
                    agregarActividad(self.id, findCorrectiveActivity(plant[0]))
                    print(f"Plant Id {plant[0]} added")
        elif self.type == Preventive:
            for i in self.activities:
                i.save()

    def scheduleNext(self):
        if self.status == Done and self.repeat != None and self.next==None:
            newMaintenance = Maintenance()
            newMaintenance.findById(self.id)
            newMaintenance.id = 0
            newMaintenance.status = Programmed
            newMaintenance.previous = self.id
            newMaintenance.date = self.date+timedelta(days=self.repeat)
            newMaintenance.save()
            self.next = newMaintenance.id
            self.save()
            for activity in buscarActividades(self.id):
                agregarActividad(newMaintenance.id, activity[2])
            print(f"The maintenance with ID {newMaintenance.id} was scheduled")
            return newMaintenance
        print("The maintenance can not be schedule")
        return 1

    def getActivities(self):
        if self.type != Preventive:
            print(f"Error: The maintenance with ID {self.id} is not preventive type")
            return 1
        self.activities = buscarActividades(self.id)

    def findById(self, id):
        rawData = buscar(id)
        if len(rawData) == 0:
            print(f"Maintenance with ID {id} was not found")
            return 1
        self.id = rawData[0]
        self.date = date(int(rawData[1].split('/')[2]),int(rawData[1].split('/')[1]),int(rawData[1].split('/')[0]))
        self.status = rawData[2]
        self.responsible = rawData[3]
        self.description = rawData[4]
        self.type = rawData[5]
        if self.type == Preventive: #If is a preventive maintenance
            self.activities = []
            for i in buscarActividades(self.id):
                self.activities.append(Activity(id = i[2], assigned = True))
        elif self.type == Corrective: #If is a corrective maintenance
            pass
        self.repeat = rawData[6]
        self.previous = rawData[7]
        self.next = rawData[8]
        #print(f"Maintenance with ID {id} was found")
        return 0



#Consultas SQL
def nuevo(fecha, estado, responsable, comentario, tipo, tiempoProgramado, anteriorId, siguienteId):
    """Crea un nuevo mantenimiento y lo guarda en la base de datos.
    Parámetros:
        fecha: un objeto datetime.
        estado: un str, puede ser 'Cancelado', 'Programado' o 'Realizado'
        responsable: un int, el id del responsable
        comentario: un str, es libre
        tipo: un str, puede ser 'Preventivo' o 'Correctivo'
        tiempoProgramado: un int"""

    fecha = fecha.strftime('%d/%m/%Y')
    if comentario == None:
        comentario = 'NULL'
    if tiempoProgramado == None:
        tiempoProgramado = 'NULL'
    if anteriorId == None:
        anteriorId = 'NULL'
    if siguienteId == None:
        siguienteId = 'NULL'
    instruccion = f"INSERT INTO mantenimientos VALUES (NULL, '{fecha}','{estado}',{responsable}, '{comentario}', '{tipo}', {tiempoProgramado}, {anteriorId}, {siguienteId})"
    sql.peticion(instruccion)

def findCorrectiveActivity(id):
    """Find the id of the activity corrective maintenance of a plant"""
    instruction = f"SELECT id FROM actividadesAsignadas WHERE idEquipo = {id} AND nombre = 'Mantenimiento correctivo'"
    result = sql.peticion(instruction)
    if len(result) == 0:
        return False
    return result[0][0]   

def editar(id, fecha, estado, responsable, comentario, tipo, tiempoProgramado, anteriorId, siguienteId):
    """Edita un mantenimiento y lo guarda en la base de datos.
    Parámetros:
        id: id del mantenimiento a editar
        fecha: un objeto datetime.
        estado: un str, puede ser 'Cancelado', 'Programado' o 'Realizado'
        responsable: un int, el id del responsable
        comentario: un str, es libre
        tipo: un str, puede ser 'Preventivo' o 'Correctivo'
        tiempoProgramado: un int"""
        
    fecha = fecha.strftime('%d/%m/%Y')
    if comentario == None:
        comentario = 'NULL'
    if tiempoProgramado == None:
        tiempoProgramado = 'NULL'
    if anteriorId == None:
        anteriorId = 'NULL'
    if siguienteId == None:
        siguienteId = 'NULL'
    instruccion = f"UPDATE mantenimientos SET fecha='{fecha}', estado='{estado}', responsable={responsable}, comentario='{comentario}', tipo='{tipo}', tiempoProgramado={tiempoProgramado}, anteriorId={anteriorId}, siguienteId={siguienteId} WHERE id = {id}"
    sql.peticion(instruccion)

def buscar(id):
    """Busca en la base de datos un mantenimiento por su id"""
    instruccion = f"SELECT * FROM mantenimientos WHERE id = {id}"
    resultado = sql.peticion(instruccion)
    return resultado[0]

def buscarTodos():
    """Busca todos los mantenimientos en la base de datos"""
    instruccion = f"SELECT * FROM mantenimientos ORDER BY id DESC"
    resultado = sql.peticion(instruccion)
    return resultado

def getAll():
    """Return all the maintenances in the database"""
    instruction = "SELECT id FROM mantenimientos ORDER BY id DESC"
    listIds = sql.peticion(instruction)
    listMaintenances = []
    for i in listIds:
        listMaintenances.append(Maintenance(i[0]))
    return listMaintenances

def eliminar(id):
    """Elimina un mantenimiento en la base de datos por su id"""
    instruccion = f"DELETE FROM mantenimientos WHERE id = {id}"
    sql.peticion(instruccion)

def agregarActividad(idMantenimiento, idActividad):
    """Agrega una actividad al mantenimiento"""
    instruccion = f"INSERT INTO mantenimientos_actividadesAsignadas VALUES (NULL, {idMantenimiento}, {idActividad})"
    sql.peticion(instruccion)

def eliminarActividad(id):
    """Elimina una actividad"""
    instruccion = f"DELETE FROM mantenimientos_actividadesAsignadas WHERE id = {id}"
    sql.peticion(instruccion)

def buscarActividades(id):
    """Busca las actividades registradas en un mantenimiento"""
    instruccion = f"SELECT * FROM mantenimientos_actividadesAsignadas WHERE mantenimientoId = {id}"
    resultado = sql.peticion(instruccion)
    return resultado

def ultimoMantenimiento():
    instruccion = f"SELECT MAX(id) AS id FROM mantenimientos"
    resultado = sql.peticion(instruccion)
    return resultado[0][0]

def ultimoMantenimientoRealizado(id):
    """Busca el último mantenimiento registrado de un equipo"""
    instruccion = f"""SELECT MAX(mantenimientos.id) as id
        FROM mantenimientos LEFT JOIN mantenimientos_actividadesAsignadas ON mantenimientos.id = mantenimientos_actividadesAsignadas.mantenimientoId
        LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id
        LEFT JOIN equipos ON actividadesAsignadas.idEquipo = equipos.id WHERE equipos.id = {id} AND mantenimientos.estado LIKE 'Realizado%' """
    resultado = sql.peticion(instruccion)
    if resultado[0][0] == None:
        return None
    return buscar(resultado[0][0])

def ultimoMantenimientoProgramado(id):
    """Busca el último mantenimiento registrado de un equipo"""
    instruccion = f"""SELECT MAX(mantenimientos.id) as id
        FROM mantenimientos LEFT JOIN mantenimientos_actividadesAsignadas ON mantenimientos.id = mantenimientos_actividadesAsignadas.mantenimientoId
        LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id
        LEFT JOIN equipos ON actividadesAsignadas.idEquipo = equipos.id WHERE equipos.id = {id} AND mantenimientos.estado LIKE '%Programado%' """
    resultado = sql.peticion(instruccion)
    if resultado[0][0] == None:
        return None
    return buscar(resultado[0][0])

def buscarNoProgramados():
    instruccion = f"SELECT * FROM mantenimientos WHERE estado = 'Realizado' AND tipo = 'Preventivo' AND tiempoProgramado > 0"
    resultado = sql.peticion(instruccion)
    return resultado

def buscarAtrasados(fecha):
    instruccion = f"SELECT * FROM mantenimientos WHERE estado = 'Programado'"
    resultado = sql.peticion(instruccion)
    lista = []
    for i in resultado:
        fechaMant = i[1]
        fechaMant = fechaMant.split('/')
        fechaMant = date(int(fechaMant[2]), int(fechaMant[1]), int(fechaMant[0]))
        if fechaMant <= fecha:
            lista.append(i)
    return lista

def buscarPorEquipo(id):
    """Busca los matenimientos correspondientes a un equipo por su id"""
    instruccion = f"""SELECT mantenimientos.id, mantenimientos.fecha, mantenimientos.estado, mantenimientos.responsable, mantenimientos.comentario,
mantenimientos.tipo, actividadesAsignadas.nombre, actividadesAsignadas.descripcion
 FROM mantenimientos LEFT JOIN mantenimientos_actividadesAsignadas ON mantenimientos.id = mantenimientos_actividadesAsignadas.mantenimientoId
LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id
LEFT JOIN equipos ON actividadesAsignadas.idEquipo = equipos.id WHERE equipos.id = {id}"""
    resultado = sql.peticion(instruccion)
    listaDepurada = []
    for activity in resultado:
        if not activity[0] in listaDepurada:
            listaDepurada.append(activity[0])
    listaDepurada.sort(reverse=True)
    for maintenance in listaDepurada:
        listaDepurada[listaDepurada.index(maintenance)] = buscar(maintenance)
    return listaDepurada

if __name__ == '__main__':
    listMan = getAll()
    print(listMan[0].id)







