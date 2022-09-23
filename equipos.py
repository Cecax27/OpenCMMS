from modules import sql
import areas

class Plant:
    def __init__(self, id = 0):
        self.id = id
        if self.id != 0:
            self.findById(self.id)
            return
        self.name = ''
        self.description = ''
        self.area = 0
        self.department = 0
        
    def __repr__(self):
        info = f"Plant ID {self.id}\n{self.name}"
        return info

    def findById(self, id):
        rawData = buscar(id)
        if rawData == None:
            print(f"Plant with ID {id} was not found")
            return 1
        self.name = rawData[1]
        self.description = rawData[2]
        rawDataArea = areas.buscar(rawData[3])
        self.area = rawDataArea[1]
        self.department = rawDataArea[4]

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

def asignarActividad():
    try:
        with open(rutaActividades, 'rb') as f:
            listaActividades = pickle.load(f)
    except:
        print('No se encontraron actividades registradas.')
        return 0
    try:
        with open(rutaEquipos, 'rb') as f:
            listaEquipos = pickle.load(f)
    except:
        print('No se encontraron equipos registradas.')
        return 0
    print('Equipos disponibles:\n ')
    for x in listaEquipos:
        print(x)
        print()
    bandera = True
    while bandera:
        clave = input('Clave del equipo: ')
        for x in listaEquipos:
            if x.clave == clave:
                equipo = x
                bandera = False
                exit
        if bandera:
            print('Clave de equipo no válida, intente de nuevo.')
    for x in listaActividades:
        print(x)
        print()
    bandera = True
    while bandera:
        clave = input('Clave de la actividad: ')
        for x in listaActividades:
            if x.clave == clave:
                actividad = x
                bandera = False
                exit
        if bandera:
            print('Clave de actividad no válida, intente de nuevo.')
    print('Se asignará al equipo: \n', equipo, '\n la actividad:\n', actividad)
    if input('Continuar? (s/n): ') == 's':
        equipo.asignarActividad(actividad)
        for x in listaEquipos:
            if equipo.clave == x.clave:
                listaEquipos[listaEquipos.index(x)]=equipo
                with open(rutaEquipos, 'wb') as f:
                    pickle.dump(listaEquipos, f)
        print('Actividad asignada')

def agregarMantenimiento(equipoClave, fecha, comentario, estado, empleado, actividades):
    try:
        with open(rutaEquipos, 'rb') as f:
            listaEquipos = pickle.load(f)
    except:
        return False

    bandera = False
    for x in listaEquipos:
        if x.clave == equipoClave:
            x.registrarMantenimiento(fecha, comentario, estado, empleado, actividades)
            #print('Equipo encontrado')
            #print(x)
            listaEquipos.pop(listaEquipos.index(x))
            listaEquipos.append(x)
            bandera = True
            exit
    if bandera:
        listaEquipos.sort(key= lambda x: x.clave)
        with open(rutaEquipos, 'wb') as f:
            pickle.dump(listaEquipos, f)
        return True
    return False

def eliminar(id):
    instruccion = f"DELETE FROM equipos WHERE id = '{id}'"
    sql.peticion(instruccion)



