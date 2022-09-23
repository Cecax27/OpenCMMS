from modules import sql
import equipos

#Classes
class Activity:
    def __init__(self, id = 0, assigned = False):
        self.id = id
        if self.id != 0:
            self.findById(self.id, assigned = assigned)
            return
        self.name = ''
        self.description = ''
        self.time = None
        
    def __repr__(self):
        info = f"Activity ID {self.id}\n{self.name}"
        if hasattr(self, 'plant'):
            info += f"\nAssigned to plant ID {self.plant}"
        return info

    def findById(self, id, assigned = False):
        if assigned:
            rawData = buscarActividadAsignada(id)
        else:
            rawData = buscar(id)
        if rawData == None:
            print(f"Activity with ID {id} was not found")
            return 1
        self.name = rawData[1]
        self.description = rawData[2]
        if rawData[3] == 0 or rawData[3] == 'NULL':
            self.time = None
        else:
            self.time = rawData[3]
        if assigned:
            self.plant = equipos.Plant(id = rawData[4])

    def save(self):
        """Save the activity in the database"""
        if hasattr(self, 'plant'):  #If is a assigned activity
            if self.id == 0: #If is a new activity
                self.id = nuevaActividadAsignada(self.name, self.description, self.time, self.plant)
                print(f"The activity with ID {self.id} was created")
            else: #If is a old activity
                modificarActividadAsignada(self.id, self.name, self.description, self.time)
                print(f"The activity with ID {self.id} was updated")
        else: #If is a unssigned activity
            if self.id == 0: #If is a new activity
                self.id = new(self.name, self.description, self.time)
                print(f"The activity with ID {self.id} was created")
            else: #If is a old activity
                modificar(self.id, self.name, self.description, self.time)
                print(f"The activity with ID {self.id} was updated")
                
    def delete(self):
        pass

        


def new(nombre, descripcion, tiempoAproximado):
    """Crea una nueva actividad y la guarda en la base de datos.
    Parámetros:
        Nombre=Nombre de la actividad 
        Descripcion = Descripción de la actividad
        tiempoAproximado = Tiempo aproximado de la actividad en horas.
    """
    instruccion = f"INSERT INTO actividades VALUES (NULL, '{nombre}', '{descripcion}', {tiempoAproximado})"
    sql.peticion(instruccion)
    instruccion = f"SELECT MAX(id) AS id FROM actividades"
    return sql.peticion(instruccion)[0][0]

def modificar(id, nombre, descripcion, tiempoAproximado):
    """Modificar una actividad.
    Parámetros:
        id: id de la actividad a modificar
        nombre: Nombre de la actividad
        descripción: str Descripción de la actividad
        int tiempoAproximado: tiempo aproximado de la actividad en horas."""
    instruccion = f"UPDATE actividades SET nombre = '{nombre}', descripcion = '{descripcion}', tiempo = {tiempoAproximado} WHERE id = {id}"
    sql.peticion(instruccion)

def ver():
    """Devuelve todas las actividades en una lista desde la base de datos.
    """
    instruccion = f"SELECT * FROM actividades ORDER BY id DESC"
    lista = sql.peticion(instruccion)
    return lista

def buscar(id):
    """Busca un registro en la base de datos que coincida con el id"""
    instruccion = f"SELECT * FROM actividades WHERE id = {id}"
    resultado = sql.peticion(instruccion)
    if len(resultado) == 0:
        return None
    return resultado[0]

def eliminar(id):
    """Elimina un registro en la base de datos que coincida con el id"""
    instruccion = f"DELETE FROM actividades WHERE id = {id}"
    sql.peticion(instruccion)

def buscarPorEquipo(idEquipo):
    """Busca las actividadas asignada a un equipo por su id"""
    instruccion = f"SELECT id, nombre, descripcion, tiempo FROM actividadesAsignadas WHERE idEquipo = {idEquipo} ORDER BY id DESC"
    lista = sql.peticion(instruccion)
    return lista

def nuevaActividadAsignada(nombre, descripcion, tiempo, idEquipo):
    """Crea en la base de datos una nueva actividad asignada a un equipo"""
    instruccion = f"INSERT INTO actividadesAsignadas VALUES (NULL, '{nombre}', '{descripcion}', {tiempo}, {idEquipo})"
    sql.peticion(instruccion)
    instruccion = f"SELECT MAX(id) AS id FROM actividadesAsignadas"
    return sql.peticion(instruccion)[0][0]

def modificarActividadAsignada(id, nombre, descripcion, tiempo):
    """Crea en la base de datos una nueva actividad asignada a un equipo"""
    instruccion = f"UPDATE actividadesAsignadas SET nombre =  '{nombre}', descripcion='{descripcion}', tiempo={tiempo} WHERE id = {id}"
    sql.peticion(instruccion)

def eliminarActividadAsignada(id):
    """Elimina una actividad asignada a un equipo de la base de datos"""
    instruccion = f"DELETE FROM actividadesAsignadas WHERE id = {id}"
    sql.peticion(instruccion)

def buscarActividadAsignada(id):
    """Busca un registro en la base de datos que coincida con el id"""
    instruccion = f"SELECT * FROM actividadesAsignadas WHERE id = {id}"
    resultado = sql.peticion(instruccion)
    return resultado[0]

if __name__ == '__main__':
    myActivity = Activity(1)
    print(myActivity.name)
    myActivity.save()