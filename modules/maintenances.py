try:
    import sql
except:
    from modules import sql
try:
    from modules import inventory
except:
    import inventory
try:
    import plants
except:
    from modules import plants
try:
    from activities import nuevaActividadAsignada, Activity
except:
    from modules.activities import nuevaActividadAsignada, Activity
try:
    import pdf
except:
    from modules import pdf
from datetime import date
from datetime import datetime
from datetime import timedelta


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
        self.products = []
        if(type == 'predictive'):
            self.status = '' #WIP
            self.type = Predictive
        elif type == Preventive:
            self.status = Programmed
            self.type = Preventive
            self.plants = []
            self.activities = []
        elif type == Corrective:
            print('Creating corrective maintenance...')
            self.status = Done
            self.type = Corrective
            self.plants = []
            
    def __repr__(self) -> str:
        return f"Maintenance with Id {self.id}:\n\tDescription: {self.description}\n"

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
            return 0
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
                agregarActividad(self.id, i.id)
                print(f"Activity Id {i.id} added")
                
        if self.products != None:
            for mov in self.products:
                if mov.id == 0:
                    mov.date = datetime.combine(self.date, datetime.min.time())
                    mov.origin_id = self.id
                    mov.save()
                    
    def scheduleNext(self):
        """Schedule the next maintenance in the database.

        Returns:
            Maintenance object: The new maintenance. True if the maintenance cannot be schedule.
        """
        if self.status == Done and self.repeat != None and self.next==None:
            newMaintenance = Maintenance(id = self.id)
            newMaintenance.id = 0
            newMaintenance.status = Programmed
            newMaintenance.previous = self.id
            newMaintenance.date = self.date+timedelta(days=self.repeat)
            newMaintenance.save()
            self.next = newMaintenance.id
            self.save()
            print(f"The maintenance with ID {newMaintenance.id} was scheduled")
            return newMaintenance
        print("The maintenance can not be schedule")
        return 1

    def getActivities(self):
        """Look for the activities of the maintenance.

        Returns:
            bool: True if there is an error.
        """
        if self.type != Preventive:
            print(f"Error: The maintenance with ID {self.id} is not preventive type")
            return 1
        self.activities = buscarActividades(self.id)

    def findById(self, id):
        """Look for the maintenance data in the database.

        Args:
            id (int): The maintenance id.

        Returns:
            bool: True if there is an error. False else.
        """
        rawData = buscar(id)
        if len(rawData) == 0:
            print(f"Maintenance with ID {id} was not found")
            return 1
        self.id = rawData[0]
        self.date = rawData[1]
        self.status = rawData[2]
        self.responsible = rawData[3]
        self.description = rawData[4]
        self.type = rawData[5]
        if self.type == Preventive: #If is a preventive maintenance
            self.activities = []
            self.plants = []
            for i in buscarActividades(self.id):
                self.activities.append(Activity(id = i[2], assigned = True))
            for activity in self.activities:
                if self.activities.index(activity) == 0:
                    self.plants.append(activity.plant)
                    self.plants[0].activities.append(activity)
                    continue
                flag = False
                for plant in self.plants:
                    if activity.plant.id == plant.id:
                        self.plants[self.plants.index(plant)].activities.append(activity)
                        flag = True
                        break
                if not flag:
                    self.plants.append(activity.plant)
                    self.plants[self.plants.index(activity.plant)].activities.append(activity)
        elif self.type == Corrective: #If is a corrective maintenance
            self.plants = []
            for i in buscarActividades(self.id):
                self.plants.append(Activity(id = i[2], assigned = True).plant)
        self.repeat = rawData[6]
        self.previous = rawData[7]
        self.next = rawData[8]
        self.products = findProducts(self.id)
        #print(f"Maintenance with ID {id} was found")
        return 0
    
    def addMovement(self, productId = 0, product = None, quantity = 0, type = inventory.OUTPUT, comment = None):
        newMov = inventory.InventoryMovement()
        newMov.product = productId if productId != 0 else product.id
        newMov.date = datetime.combine(self.date, datetime.min.time())
        newMov.type = type
        newMov.quantity = quantity
        newMov.comment = comment
        newMov.origin = inventory.MAINTENANCE
        newMov.origin_id = self.id
        self.products.append(newMov)  
        
    def cancel(self):
        """Change the maintenance status to cancel in the database.

        Returns:
            bool: False if ok.
        """
        self.status = Cancelled
        self.date = datetime.now()
        self.save()
        return 0

    def delete(self):
        """Delete the maintenance in the database.

        Returns:
            bool: False if ok.
        """
        for activity in buscarActividades(self.id):
            eliminarActividad(activity[0])
        eliminar(self.id)
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

    # if comentario == None:
    #     comentario = 'NULL'
    # if tiempoProgramado == None:
    #     tiempoProgramado = 'NULL'
    # if anteriorId == None:
    #     anteriorId = 'NULL'
    # if siguienteId == None:
    #     siguienteId = 'NULL'
    sql.petitionWithParam(f"INSERT INTO mantenimientos VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (fecha, estado, responsable, comentario, tipo, tiempoProgramado, anteriorId, siguienteId))
    
def findPendingMaintenances(employerId = 0):
    """Find pending maintenances. If you give the employer id, it find pending maintenances for that employer"""
    if employerId != 0:
        instruction = f"SELECT id FROM mantenimientos WHERE estado = '{Programmed}' AND responsable = {employerId}"
        maintenancesList = []
        for id in sql.peticion(instruction):
            maintenancesList.append(Maintenance(id = id[0]))
        return maintenancesList
    
def findOverdueMaintenances(employerId = 0):
    """Find overdue maintenances. If you give the employer id, it find pending maintenances for that employer"""
    if employerId != 0:
        instruction = f"SELECT id FROM mantenimientos WHERE estado = '{Programmed}' AND responsable = {employerId}"
        maintenancesList = []
        for id in sql.peticion(instruction):
            newMaintenance = Maintenance(id = id[0])
            if newMaintenance.date <= datetime.now():
                maintenancesList.append(newMaintenance)
        return maintenancesList

def findCorrectiveActivity(id):
    """Find the id of the activity corrective maintenance of a plant"""
    instruction = f"SELECT id FROM actividadesAsignadas WHERE idEquipo = {id} AND nombre = 'Mantenimiento correctivo'"
    result = sql.peticion(instruction)
    if len(result) == 0:
        return False
    return result[0][0]   

def findProducts(id):
    """Look for the products used in the maintenance.

    Args:
        id (int): The maintenance id
        
    Returns:
        list: a list with InventoryMovement objects.
    """
    list = []
    for id in sql.peticion(f"SELECT id FROM inventory_detail WHERE origin = '{inventory.MAINTENANCE}' AND origin_id = {id}"):
        list.append(inventory.InventoryMovement(id = id[0]))
    return list

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
        
    # if comentario == None:
    #     comentario = 'NULL'
    # if tiempoProgramado == None:
    #     tiempoProgramado = 'NULL'
    # if anteriorId == None:
    #     anteriorId = 'NULL'
    # if siguienteId == None:
    #     siguienteId = 'NULL'
    sql.petitionWithParam(f"UPDATE mantenimientos SET fecha=?, estado=?, responsable=?, comentario=?, tipo=?, tiempoProgramado=?, anteriorId=?, siguienteId=? WHERE id = {id}", (fecha, estado, responsable, comentario, tipo, tiempoProgramado, anteriorId, siguienteId))

def buscar(id):
    """Busca en la base de datos un mantenimiento por su id"""
    resultado = sql.peticiontres(f"SELECT * FROM mantenimientos WHERE id = {id}")
    return resultado[0]

def buscarTodos():
    """Busca todos los mantenimientos en la base de datos"""
    instruccion = f"SELECT * FROM mantenimientos ORDER BY id DESC"
    resultado = sql.peticion(instruccion)
    return resultado

def getMaintenanceDate(maintenance):
    return maintenance.date

def getAll():
    """Return all the maintenances in the database"""
    instruction = "SELECT id FROM mantenimientos"
    listIds = sql.peticion(instruction)
    listMaintenances = []
    for i in listIds:
        listMaintenances.append(Maintenance(i[0]))
    listMaintenances.sort(key=getMaintenanceDate, reverse=True)
    return listMaintenances

def getProgrammed():
    """Return all maintenances in the database where status is Programmed"""
    instruction = f"SELECT id FROM mantenimientos WHERE estado='{Programmed}'"
    listIds = sql.peticion(instruction)
    listMaintenances = []
    for i in listIds:
        listMaintenances.append(Maintenance(i[0]))
    listMaintenances.sort(key=getMaintenanceDate)
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
    return Maintenance(id = sql.petition(f"SELECT mantenimientos.id, MAX(mantenimientos.fecha) FROM mantenimientos LEFT JOIN mantenimientos_actividadesAsignadas ON mantenimientos.id = mantenimientos_actividadesAsignadas.mantenimientoId LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id WHERE actividadesAsignadas.idEquipo = {id} AND mantenimientos.estado = '{Done}'")[0][0])

def ultimoMantenimientoProgramado(id):
    """Busca el último mantenimiento registrado de un equipo"""
    maintenances = buscarPorEquipo(id)
    programmed = []
    for main in maintenances:
        if main.status == Programmed:
            programmed.append(main)
    programmed.sort(key= lambda plant: plant.date, reverse= True)
    return programmed[0] if len(programmed) > 0 else None

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
    mantList = []
    for mant in sql.peticion(f"SELECT DISTINCT mantenimientos_actividadesAsignadas.mantenimientoId FROM mantenimientos_actividadesAsignadas LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id WHERE actividadesAsignadas.idEquipo = {id}"):
        mantList.append(Maintenance(id = mant[0]))
    mantList.sort(key= lambda plant: plant.date, reverse= True)
    return mantList

def find(overdue = False, employerId = 0, status = None):
    """Find all the maintenances with an employer id"""
    instruction = f"SELECT id FROM mantenimientos WHERE"
    restrictionList = []
    if employerId != 0:
        restrictionList.append(f" responsable = {employerId} ")
    if status != None:
        restrictionList.append(f" estado = '{status}' ")
    for restriction in restrictionList:
        instruction += restriction
        if restrictionList.index(restriction) != len(restrictionList)-1:
            instruction += "AND"
    maintenancesList = []
    for id in sql.peticion(instruction):
        newMaintenance = Maintenance(id = id[0])
        if overdue:
            if newMaintenance.date <= datetime.date(datetime.now()):
                maintenancesList.append(newMaintenance)
        else:
            maintenancesList.append(newMaintenance)
    return maintenancesList
        
    

if __name__ == '__main__':
    print(ultimoMantenimientoRealizado(11))
    #for maint in getAll():)
        #print(maint.id)
        #print(maint.date)
        #print(type(maint.date))
        #maint.save()
    #print(maint.date)
    #print(type(maint.date))