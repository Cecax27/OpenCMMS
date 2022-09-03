import csv
from datetime import datetime
import pickle

class Equipo:


    def __init__(self, clave, nombre, descripcion, area):
        self.clave = clave
        self.nombre = nombre
        self.descripcion = descripcion
        self.area = area
        self.actividades = []
        self.mantenimientos = []

    def __repr__(self):
        cadena = str('%(clave)-8s %(nombre)-20s %(area)-10s %(descripcion)-20s \n' % {'clave':'Clave', 'nombre':'Nombre', 'area':'Area', 'descripcion':'Descripción'})
        cadena += str('%(clave)-8s %(nombre)-20s %(area)-10s %(descripcion)-20s \n' % {'clave':self.clave, 'nombre':self.nombre, 'area':self.area, 'descripcion':self.descripcion})
        cadena += '\n\tActividades registradas:\n\n'
        for x in self.actividades:
            cadena += str('\t'+repr(x)+'\n')
        return cadena

    def asignarActividad(self, actividadAsignada):
        self.actividades.append(actividadAsignada)

    def registrarMantenimiento(self, fecha, comentario, estado, empleado, actividades):
        nuevo = Mantenimiento(fecha, comentario, estado, empleado, actividades)
        self.mantenimientos.append(nuevo)

class Mantenimiento:
    #Estados 0-programado, 1-realizado, 2-cancelado

    def __init__(self, fecha, comentario, estado, empleado, actividades):
        self.fecha = fecha
        self.comentario = comentario
        self.estado = estado
        self.empleado = empleado
        self.actividades = actividades

    def __repr__(self):
        estado = ''
        if self.estado == 0:
            estado = 'programado'
        elif self.estado == 1:
            estado = 'realizado'
        else:
            estado ='cancelado'
        return('Mantenimiento '+estado+' el '+self.fecha.strftime('%d del %m de %Y')+ ' por '+self.empleado)
    
class Actividad:

    def __init__(self, clave, nombre, descripcion, tiempo):
        self.clave = clave
        self.nombre = nombre
        self.descripcion = descripcion
        self.tiempo = tiempo

    def __repr__(self):
        return(self.clave + ' - ' + self.nombre + ': ' + self.descripcion)

class Empleado:

    def __init__(self, nombre, numero):
        self.nombre = nombre
        self.numero = numero

    def __repr__(self):
        return(str(self.numero) +' - '+self.nombre) 

class Area:

    def __init__(self, nombre, descripcion, noEmpleado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.responsable = noEmpleado
    def __repr__(self):
        return(self.nombre + ': '+self.descripcion +'\nResponsable: '+self.responsable)
