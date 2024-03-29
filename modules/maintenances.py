try:
    from modules import sql, inventory, activities
except:
    import sql, inventory, activities
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
            sql.petitionWithParam(f"INSERT INTO mantenimientos VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (self.date, self.status, self.responsible, self.description, self.type, self.repeat, self.previous, self.next))
            self.id = sql.petition("SELECT MAX(id) FROM mantenimientos")[0][0]
            print(f"The maintenance was created with id {self.id}")
            if self.type == Corrective:
                for plant in self.plants:
                    if findCorrectiveActivity(plant.id):
                        agregarActividad(self.id, findCorrectiveActivity(plant.id))
                        print(f"Plant Id {plant.id} added")
                    else:
                        activities.nuevaActividadAsignada('Mantenimiento correctivo', 'Se corrigió alguna falla en el equipo', 2, plant.id)
                        agregarActividad(self.id, findCorrectiveActivity(plant.id))
                        print(f"Plant Id {plant.id} added")
            elif self.type == Preventive:
                for i in self.activities:
                    sql.petition(f"INSERT INTO mantenimientos_actividadesAsignadas VALUES (NULL, {self.id}, {i.id})")
                    print(f"Activity Id {i.id} added")
        else: #If isnt a new maintenance
            editar(self.id, self.date, self.status, self.responsible, self.description, self.type, self.repeat, self.previous, self.next)
            print(f"Maintenance with ID {self.id} was updated")
                
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
            newMaintenance = Maintenance(self.id)
            newMaintenance.id = 0
            newMaintenance.status = Programmed
            newMaintenance.previous = self.id
            newMaintenance.date = self.date+timedelta(days=self.repeat)
            newMaintenance.save()
            self.next = newMaintenance.id
            sql.petitionWithParam(f"UPDATE mantenimientos SET siguienteId=? WHERE id = {self.id}", (self.next,))
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
        rawData = sql.petition(f"SELECT * FROM mantenimientos WHERE id = {id}")[0]
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
            for i in sql.petition(f"SELECT * FROM mantenimientos_actividadesAsignadas WHERE mantenimientoId = {id}"):
                self.activities.append(activities.Activity(id = i[2], assigned = True))
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
            for i in sql.petition(f"SELECT * FROM mantenimientos_actividadesAsignadas WHERE mantenimientoId = {id}"):
                self.plants.append(activities.Activity(id = i[2], assigned = True).plant)
        self.repeat = rawData[6]
        self.previous = rawData[7]
        self.next = rawData[8]
        self.products = findProducts(self.id)
        return 0
    
    def addMovement(self, productId = 0, product = None, quantity = 0, type = 'output', comment = None):
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
        return [Maintenance(id = x[0]) for x in sql.petition(f"SELECT id FROM mantenimientos WHERE estado = '{Programmed}' AND responsable = {employerId}")]

def getMaintenancesToWorkOrders():
    return [Maintenance(id = x[0]) for x in sql.petition("SELECT id FROM mantenimientos WHERE estado='Programado' ORDER BY fecha DESC")]
    
def findOverdueMaintenances(employerId = 0):
    """Find overdue maintenances. If you give the employer id, it find pending maintenances for that employer"""
    if employerId != 0:
        return list(filter(lambda x: x.date <= datetime.now(),[Maintenance(id = x[0]) for x in sql.petition(f"SELECT id FROM mantenimientos WHERE estado = '{Programmed}' AND responsable = {employerId}")]))

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

def getAll(limit = None, offset = None, order = 'date'):
    """Return all the maintenances in the database. You can limit the search with limit argument.

    Args:
        limit (int, optional): The max quantity of maintenances. Defaults to 0 (No limit).

    Returns:
        list: A list with Maintenances objects
    """
    return [Maintenance(id = x[0]) for x in sql.petition(f"SELECT id FROM mantenimientos{' ORDER BY fecha DESC' if order == 'date' else ''}{' LIMIT '+str(limit) if limit != None else ''}{' OFFSET '+str(offset) if offset != None else ''}")]

def getProgrammed():
    """Return all maintenances in the database where status is Programmed"""
    return [Maintenance(id = x[0]) for x in sql.petition(f"SELECT id FROM mantenimientos WHERE estado = '{Programmed}' ORDER BY fecha ASC")]

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
    maintenanceId = sql.petition(f"SELECT mantenimientos.id, MAX(mantenimientos.fecha) FROM mantenimientos LEFT JOIN mantenimientos_actividadesAsignadas ON mantenimientos.id = mantenimientos_actividadesAsignadas.mantenimientoId LEFT JOIN actividadesAsignadas ON mantenimientos_actividadesAsignadas.actividadesId = actividadesAsignadas.id WHERE actividadesAsignadas.idEquipo = {id} AND mantenimientos.estado = '{Done}'")[0][0]
    if maintenanceId == None:
        return None
    return Maintenance(id = maintenanceId)

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

def find(overdue = False, employerId = 0, status = None, order = None):
    """Find all the maintenances with an employer id"""
    instruction = f"SELECT id FROM mantenimientos WHERE"
    restrictionList = []
    if employerId != 0:
        restrictionList.append(f" responsable = {employerId} ")
    if status != None:
        restrictionList.append(f" estado = '{status}' ")
    if overdue:
        restrictionList.append(f" fecha < '{datetime.now()}'")
        restrictionList.append(f" estado = 'Programado' ")
    for restriction in restrictionList:
        instruction += restriction
        if restrictionList.index(restriction) != len(restrictionList)-1:
            instruction += "AND"
    if order:
        instruction += f"ORDER BY {order}"

    return [Maintenance(id = id[0]) for id in sql.petition(instruction)]

def count():
    return sql.petition("SELECT count(id) FROM mantenimientos")[0][0]
        
    

if __name__ == '__main__':
    print(ultimoMantenimientoRealizado(11))
    #for maint in getAll():)
        #print(maint.id)
        #print(maint.date)
        #print(type(maint.date))
        #maint.save()
    #print(maint.date)
    #print(type(maint.date))