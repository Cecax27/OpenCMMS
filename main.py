from cgitb import text
from math import prod
from msilib.schema import ComboBox
import textwrap
from tkinter import *
from tkinter.filedialog import asksaveasfile
import tkinter.ttk as ttk
from tkinter import messagebox
from turtle import back, width
import modules.employers as employers
import modules.plants as plants
import modules.activities as activities
import modules.areas as areas
import modules.maintenances as maintenances
from tkcalendar import Calendar
from datetime import datetime
from datetime import date
from datetime import timedelta
from modules.ui.scrollableFrame import *
from modules import inventory
from modules import sql
from modules import workorders
import locale
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

#locale.setlocale(locale.LC_ALL, 'es-ES')

#Constantes-----
colorGreen = '#37c842'
colorRed = '#c83737'
colorBlue = '#37abc8'
colorGray = '#f2f2f2'
colorDarkGray = '#dadada'
colorWhite = "#ffffff"
colorBlack = "#454545"

#Functios--------
def crearTabla(encabezados, ids, anchos, matriz, lugar, altura, funcion):
    """Crea una tabla con un Treeview de Tkinter.
    Parámetros: matriz = matriz de la tabla,
    lugar = widget padre de Tkinter,
    altura = altura de la tabla"""

    if len(matriz) == 0:
        return Label(text='No hay datos')

    nuevaTabla = ttk.Treeview(lugar, height = altura, columns = encabezados[1:], selectmode = 'browse')
    nuevaTabla.tag_configure("color", background = "#ffffff", font=("Segoe UI", "9", "normal"))
    if funcion != '':
        nuevaTabla.tag_bind("mytag", "<<TreeviewSelect>>", funcion)
        
    for x in encabezados:
        posicion = '#' + str(encabezados.index(x))
        nuevaTabla.heading(posicion, text=encabezados[encabezados.index(x)], anchor=CENTER)
        nuevaTabla.column(posicion, minwidth=0, width=anchos[encabezados.index(x)])
    if funcion != '':
        for x in matriz:
            nuevaTabla.insert('', 0, id=ids[matriz.index(x)],values = x[1:], text = x[0],tags=("mytag","color"))
    else:
        for x in matriz:
            nuevaTabla.insert('', 0, id=ids[matriz.index(x)], values = x[1:], text = x[0], tags=("color",))

    return nuevaTabla

def crearFuncion(id, objeto):
    return lambda:objeto.padre.objetoMantenimientos.displayMaintenance(id)

def deleteActivityFromList(activity, objeto):
    return lambda:objeto.padre.objetoMantenimientos.eliminarActividadAsignada(activity)

def clearMainFrame():
    global mainFrame
    global root
    
    global imgCorrective
    global imgPreventive
    global imgIn
    global imgOut
    imgCorrective = PhotoImage(file='img/corrective.png').subsample(8)
    imgPreventive = PhotoImage(file='img/preventive.png').subsample(8)
    imgIn = PhotoImage(file='img/in.png')
    imgOut = PhotoImage(file='img/out.png')
    
    mainFrame.destroy()
    mainFrame = Frame(root)
    mainFrame.config(bg="#ffffff",
        width=root.winfo_width(),
        height=root.winfo_height()-50)
    mainFrame.grid(column=0, row=1)

class Crm:

    def __init__(self):
        #Root----------------------
        global root
        root = Tk()
        self.root = root
        self.root.state('zoomed') #abrir maximizado
        self.root.title('Gestión de Mantenimiento Emman')

        #Objetos--------
        self.objetoDepartamentos = Departamentos()
        self.objetoAreas = Areas()
        self.objetoEquipos = Equipos(self)
        self.objetoActividades = Actividades()
        self.objetoMantenimientos = Mantenimientos(self)
        self.objetoEmpleados = Empleados(self)
        self.inventory = Inventory(self)
        self.workorders = WorkOrders(self)

        #Menu---------------------
        root.update()
        global menuFrame
        menuFrame = Frame(root)
        menuFrame.config(width=root.winfo_width(), height=50, bg="#37abc8")
        menuFrame.grid(column=0, row=0)

        colorButton = "#37abc8"

        Button(menuFrame, 
            text='Mantenimientos',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.objetoMantenimientos.main
            ).place(x=0.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Equipos',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.objetoEquipos.main
            ).place(x=1.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Inventario',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.inventory.inventoryMainWindow
            ).place(x=2.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Ordenes de trabajo',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=18,
            borderwidth=5,
            relief=FLAT,
            command=self.workorders.mainWindow
            ).place(x=3.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Requisiciones',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.inventory.requisitionsMainWindow
            ).place(x=4.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Empleados',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.objetoEmpleados.main
            ).place(x=5.25*root.winfo_width()/6, y=4)

        global barraMenu
        barraMenu = BarraMenu(self)

        global mainFrame
        mainFrame = Frame(self.root)

        self.mainframe = mainFrame

    def actividades(self):
        clearMainFrame()

        lblMain = Label(self.mainframe, text='Actividades')
        lblMain.grid(column=0, row=0)

        listaActividades = activities.ver()
        self.tablaActividades = ttk.Treeview(self.mainframe, height = 10, columns = ('descripcion', 'tiempo'), selectmode = 'browse')
        self.tablaActividades.grid(row = 2, column = 0, columnspan = 5)
        self.tablaActividades.heading('#0', text='Nombre', anchor=CENTER)
        self.tablaActividades.heading('#1', text='Descripción', anchor=CENTER)
        self.tablaActividades.heading('#2', text='Tiempo aproximado (hrs)', anchor=CENTER)

        for x in listaActividades:
            self.tablaActividades.insert('', END, text = x[1], values = [x[2], x[3]])

        self.btinfo =  Button(self.mainframe, text='Ver más información',command=self.equiposVer)
        self.btinfo.grid(column=0,row=3)

        self.btnuevo =  Button(self.mainframe, text='Nuevo',command=self.actividadesNuevo)
        self.btnuevo.grid(column=1,row=3)

        self.bteditar =  Button(self.mainframe, text='Editar',command=self.empleadosEditar)
        self.bteditar.grid(column=2,row=3)

        self.btborrar =  Button(self.mainframe, text='Eliminar',command=self.empleadosBorrar)
        self.btborrar.grid(column=3,row=3)

    
    def departamentos(self):
        self.mainframe.destroy()
        self.mainframe = Frame(self.root, relief=RIDGE, borderwidth=2)
        self.mainframe.grid(column=0, row=1, sticky='nesw')

        lblMain = Label(self.mainframe, text='Departamentos')
        lblMain.grid(column=0, row=0)

        encabezados = ['Id','Nombre', 'No. de áreas']
        anchos = [40, 80, 80]
        lista = areas.getDepartamentos()
        for departamento in lista:
            lista[lista.index(departamento)].append(areas.areasEnDepartamento(departamento[0]))

        self.tablaDepartamentos = crearTabla(encabezados,anchos, lista, self.mainframe, 10, self.departamentoSeleccionado)
        #Etiqueta cuando seleccionemos un departamento
        
        self.tablaDepartamentos.grid(row=1, column=0, padx=5, pady=5)

        self.btnuevo =  Button(self.mainframe, text='Nuevo',command=self.objetoDepartamentos.nuevo)
        self.btnuevo.grid(column=0,row=3)

        self.bteditar =  Button(self.mainframe, text='Editar',command=self.areasModificar)
        self.bteditar.grid(column=1,row=3)

        self.btborrar =  Button(self.mainframe, text='Eliminar',command=self.empleadosBorrar)
        self.btborrar.grid(column=2,row=3)

    def areas(self):
        self.mainframe.destroy()
        self.mainframe = Frame(self.root, relief=RIDGE, borderwidth=2)
        self.mainframe.grid(column=0, row=1)

        lblMain = Label(self.mainframe, text='Areas')
        lblMain.grid(column=0, row=0)

        encabezados = ['Id','Nombre']
        anchos = [40, 80]
        lista = areas.getDepartamentos()
        self.tablaDepartamentos = crearTabla(encabezados,anchos, lista, self.mainframe, 10, self.departamentoSeleccionado)
        #Etiqueta cuando seleccionemos un departamento
        
        self.tablaDepartamentos.grid(row=1, column=0, padx=5, pady=5)

        self.btnuevo =  Button(self.mainframe, text='Nuevo',command=self.areasNuevo)
        self.btnuevo.grid(column=0,row=3)

        self.bteditar =  Button(self.mainframe, text='Editar',command=self.areasModificar)
        self.bteditar.grid(column=1,row=3)

        self.btborrar =  Button(self.mainframe, text='Eliminar',command=self.empleadosBorrar)
        self.btborrar.grid(column=2,row=3)

    def departamentoSeleccionado(self, event):
        theid = self.tablaDepartamentos.focus()
        text = self.tablaDepartamentos.item(theid, option='text')
        lista = areas.buscarPorDepartamento(text)
        encabezados = ['Id','Nombre', 'Descripción', 'Responsable']
        anchos = [40,80, 150,80]
        self.tabla2 = crearTabla(encabezados, anchos, lista, self.mainframe, 10, self.areas)
        self.tabla2.grid(row=1, column=1, padx=5, pady=5)        

    def areasModificar(self):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')

        self.area = areas.buscar(text)[0]

        self.ventana = Toplevel()
        self.ventana.title('Nueva área')

        self.frame = LabelFrame(self.ventana, text='Registrar área')
        self.frame.grid(column=0,row=0,pady=5,padx=5,sticky='w e')

        Label(self.frame, text='Nombre: ').grid(column=0, row=0)
        self.nombre = Entry(self.frame)
        self.nombre.insert(0,self.area[1])
        self.nombre.grid(column=1,row=0)
        Label(self.frame, text='Descripcion: ').grid(column=0, row=1)
        self.descripcion = Entry(self.frame)
        self.descripcion.insert(0,self.area[2])
        self.descripcion.grid(column=1,row=1)

         #Responsable------------
        listaEmpleados = employers.ver()
        listaNombres = []
        for x in listaEmpleados:
            listaNombres.append(x[2])
        Label(self.frame, text='Responsable: ').grid(column=0, row=2)
        self.responsable = ttk.Combobox(self.frame, state='readonly',values=listaNombres)
        contador = 0
        for x in listaEmpleados:
            if x[1] == self.area[3]:
                posicion = listaEmpleados.index(x)
            else:
                contador+=1
        self.responsable.current(posicion)
        self.responsable.grid(column=1,row=2,pady=5,padx=5)

        btGuardar = Button(self.frame, text='Guardar', command= self.areasModificarGuardar).grid(column=0, row=3)
        btCancelar = Button(self.frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=3)

    def areasModificarGuardar(self):
        codigo = employers.buscar(self.responsable.get())[0][0]
        areas.modificar(self.area[0],self.nombre.get(), self.descripcion.get(), codigo)
        self.ventana.destroy()
        self.areas()    

    def empleadosNuevo(self):
        self.ventana = Toplevel()
        self.ventana.title('Nuevo empleado')

        self.frame = LabelFrame(self.ventana, text='Registrar empleado')
        self.frame.grid(column=0,row=0,pady=5,padx=5,sticky='w e')

        Label(self.frame, text='Nombre: ').grid(column=0, row=0)
        self.nombre = Entry(self.frame)
        self.nombre.grid(column=1,row=0)
        Label(self.frame, text='Clave: ').grid(column=0, row=1)
        self.clave = Entry(self.frame)
        self.clave.grid(column=1,row=1)

        #print(self.nombre.get())
        btGuardar = Button(self.frame, text='Guardar', command= self.empleadosGuardar).grid(column=0, row=6)
        btCancelar = Button(self.frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=6)

class BarraMenu(Crm):

    def __init__(self, padre):

        self.menubar = Menu(padre.root)
        padre.root.config(menu=self.menubar)

        #Objetos menu
        filemenu = Menu(self.menubar)
        editmenu = Menu(self.menubar)

        #Menú areas----------------
        menuAreas = Menu(self.menubar, tearoff=0)
        menuAreas.add_command(label='Crear departamento', 
            command= lambda:padre.objetoDepartamentos.nuevo())
        menuAreas.add_command(label='Editar departamento', 
            command= lambda:padre.objetoDepartamentos.editar())
        menuAreas.add_command(label='Eliminar departamento', 
            command= lambda:padre.objetoDepartamentos.eliminar())
        menuAreas.add_separator()
        menuAreas.add_command(label='Crear área', 
            command= lambda:padre.objetoAreas.nuevo())
        menuAreas.add_command(label='Editar área', 
            command= lambda:padre.objetoAreas.editar())
        menuAreas.add_command(label='Eliminar área', 
            command= lambda:padre.objetoAreas.eliminar())

        #Menú equipos-----------------
        menuEquipos = Menu(self.menubar, tearoff=0)
        menuEquipos.add_command(label='Crear equipo', 
            command= lambda:padre.objetoEquipos.nuevo())

        #Menú actividades---------------------
        menuActividades = Menu(self.menubar, tearoff=0)
        menuActividades.add_command(label='Crear actividad', 
            command= lambda:padre.objetoActividades.nuevo())
        menuActividades.add_command(label='Editar actividad', 
            command= lambda:padre.objetoActividades.editar())
        menuActividades.add_command(label='Eliminar actividad', 
            command= lambda:padre.objetoActividades.eliminar())

        #Menú mantenimientos-------------------
        menuMantenimientos = Menu(self.menubar, tearoff=0)
        menuMantenimientos.add_command(label='Crear mantenimiento', command= lambda:padre.objetoMantenimientos.nuevo())
        menuMantenimientos.add_command(label='Programar mantenimientos', command= lambda:padre.objetoMantenimientos.programar())
        menuMantenimientos.add_command(label='Estadísticas', command= lambda:padre.objetoMantenimientos.statistics())

        #Inventory menu------------------------
        productMenu = Menu(self.menubar, tearoff=0)
        productMenu.add_command(label='Crear producto', command= lambda:padre.inventory.new())
        
        categoryMenu = Menu(self.menubar, tearoff=0)
        categoryMenu.add_command(label='Crear categoría', command= lambda:padre.inventory.newCategory())
        
        requisitionMenu = Menu(self.menubar, tearoff=0)
        requisitionMenu.add_command(label='Crear requisición', command=lambda: padre.inventory.newRequisition())
        
        inventoryMenu = Menu(self.menubar, tearoff=0)
        inventoryMenu.add_cascade(label='Productos', menu=productMenu)
        inventoryMenu.add_cascade(label='Categorías', menu=categoryMenu)
        inventoryMenu.add_cascade(label='Requisiciones', menu=requisitionMenu)
        
        
        helpmenu = Menu(self.menubar)
        
        #Etiquetas
        self.menubar.add_cascade(label="Archivo", menu=filemenu)
        self.menubar.add_cascade(label="Editar", menu=editmenu)
        self.menubar.add_cascade(label="Departamentos y areas", menu=menuAreas)
        self.menubar.add_cascade(label="Equipos", menu=menuEquipos)
        self.menubar.add_cascade(label="Actividades", menu=menuActividades)
        self.menubar.add_cascade(label="Mantenimientos", menu=menuMantenimientos)
        self.menubar.add_cascade(label="Inventario", menu=inventoryMenu)
        self.menubar.add_cascade(label="Ayuda", menu=helpmenu)

class Departamentos():

    def __init__(self):
        pass

    def nuevo(self):
        self.ventana = Toplevel()
        self.ventana.title('Crear departamento')

        self.frame = LabelFrame(self.ventana, text='Crear departamento:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        Label(self.frame, text='Nombre: ').grid(column=0, row=0,pady=5,padx=5)
        self.nombre = Entry(self.frame)
        self.nombre.grid(column=1,row=0,pady=5,padx=5)

        Button(self.frame, text='Guardar', command= self.registrar).grid(column=0, row=3)
        Button(self.frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=3)

    def registrar(self):
        areas.nuevoDepartamento(self.nombre.get())
        texto = 'El departamento ' + self.nombre.get() + ' ha sido registrado.'
        messagebox.showinfo(title='Departamento registrado', message=texto)
        self.ventana.destroy()

    def editar(self):
        self.ventana = Toplevel()
        self.ventana.title('Editar departamento')

        self.frame = LabelFrame(self.ventana, text='Seleccione un departamento:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        self.tabla = ttk.Treeview(self.frame, height = 10, columns = ('nombre',), selectmode = 'browse')
        self.tabla.tag_bind("mytag", "<<TreeviewSelect>>", self.editarActualizar)
        self.tabla.heading('#0', text='Id', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.column('#0', minwidth=0, width=40)
        self.tabla.column('#1', minwidth=0, width=120)

        lista = areas.getDepartamentos()
        for x in lista:
            self.tabla.insert('', 0, values = x[1:], text = x[0],tags=("mytag",))

        self.tabla.grid(row=0, column=0, pady=5, padx=5)

        self.frameEditar = LabelFrame(self.ventana, text='Editar información:')
        self.frameEditar.grid(column=1,row=0,pady=5,padx=5, sticky='w e s n')
        Label(self.frameEditar, text='Nombre: ').grid(column=0, row=0,pady=5,padx=5)
        self.nombre = Entry(self.frameEditar)
        self.nombre.grid(column=1,row=0,pady=5,padx=5)

        frameBotones = Frame(self.frameEditar)
        frameBotones.grid(column=0, row=3, columnspan=2)
        Button(frameBotones, text='Guardar', command= self.guardar).grid(column=0, row=3,pady=5, padx=5, sticky='w e')
        Button(frameBotones, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=3,pady=5, padx=5, sticky='w e') 

    def editarActualizar(self, event):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        resultado = areas.buscarDepartamento(text) 
        #print(resultado)
        self.nombre.delete(0, "end")
        self.nombre.insert(0, resultado[1])

    def guardar(self):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        resultado = areas.buscarDepartamento(text) 
        areas.modificarDepartamento(resultado[0], self.nombre.get())
        texto = "El departamento "+self.nombre.get()+" se ha modificado exitosamente."
        messagebox.showinfo(title='Departamento modificado', message=texto)
        self.ventana.destroy()
        self.editar()

    def eliminar(self):
        self.ventana = Toplevel()
        self.ventana.title('Eliminar departamento')

        self.frame = LabelFrame(self.ventana, text='Seleccione un departamento:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        self.tabla = ttk.Treeview(self.frame, height = 10, columns = ('nombre',), selectmode = 'browse')
        self.tabla.heading('#0', text='Id', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.column('#0', minwidth=0, width=40)
        self.tabla.column('#1', minwidth=0, width=120)

        lista = areas.getDepartamentos()
        for x in lista:
            self.tabla.insert('', 0, values = x[1:], text = x[0],tags=("mytag",))

        self.tabla.grid(row=0, column=0, pady=5, padx=5)

        self.frameEditar = LabelFrame(self.ventana, text='Eliminar')
        self.frameEditar.grid(column=1,row=0,pady=5,padx=5, sticky='w e s n')

        Button(self.frameEditar, text='Eliminar', command= self.eliminarELiminar).grid(column=0, row=0,pady=5, padx=5, sticky='w e')
        Button(self.frameEditar, text='Cancelar', command=self.ventana.destroy).grid(column=0, row=1,pady=5, padx=5, sticky='w e') 

    def eliminarELiminar(self):
        id = self.tabla.focus()
        clave = self.tabla.item(id, option='text')
        nombre = self.tabla.item(id, option='values')[0]
        texto = '¿En verdad desea eliminar el departamento ' + nombre +'? Esta eliminación será permantente'

        if messagebox.askyesno(title='¿Eliminar el departamento?', message=texto):
            areas.eliminarDepartamento(clave)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Equipo eliminado', message=texto)
        self.ventana.destroy()

class Areas():

    def __init__(self):
        pass

    def nuevo(self):
        self.ventana = Toplevel()
        self.ventana.title('Nueva área')

        self.frame = LabelFrame(self.ventana, text='Registrar área')
        self.frame.grid(column=0,row=0,pady=5,padx=5,sticky='w e')

        #Nombre------------
        Label(self.frame, text='Nombre: ').grid(column=0, row=0, padx=5, pady=5)
        self.nombre = Entry(self.frame)
        self.nombre.grid(column=1,row=0, padx=5, pady=5)

        #Descripcion-------------
        Label(self.frame, text='Descripcion: ').grid(column=0, row=1, padx=5, pady=5)
        self.descripcion = Entry(self.frame)
        self.descripcion.grid(column=1,row=1, padx=5, pady=5)

        #Responsable------------
        self.listaEmpleados = employers.ver()
        self.listaNombres=[]
        self.dictEmpleado = {}
        for x in self.listaEmpleados:
            self.listaNombres.append(x[2])
            self.dictEmpleado[x[2]]=x[0]
        Label(self.frame, text='Responsable: ').grid(column=0, row=2, padx=5, pady=5)
        self.responsable = ttk.Combobox(self.frame, state='readonly',values=self.listaNombres)
        self.responsable.grid(column=1,row=2,pady=5,padx=5)

        #Departamento------------
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(self.frame, text='Departamento: ').grid(column=0, row=3, padx=5, pady=5)
        self.departamento = ttk.Combobox(self.frame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.grid(column=1,row=3,pady=5,padx=5)

        btGuardar = Button(self.frame, text='Guardar', command= self.guardar).grid(column=0, row=4, padx=5, pady=5)
        btCancelar = Button(self.frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=4, padx=5, pady=5)

    def guardar(self):
        codigoDepartamento = self.listaDepartamentos[self.listaNombresDepartamentos.index(self.departamento.get())][0]
        #print(self.dictEmpleado[self.responsable.get()])
        codigo = self.dictEmpleado[self.responsable.get()]
        idDepartamento = self.listaDepartamentos[0]
        areas.new(self.nombre.get(),  self.descripcion.get(), codigo, codigoDepartamento)
        texto = 'El área ' + self.nombre.get() + ' ha sido registrada.'
        messagebox.showinfo(title='Área registrada', message=texto)
        self.ventana.destroy()

    def editar(self):
        self.ventana = Toplevel()
        self.ventana.title('Editar área')

        self.frame = LabelFrame(self.ventana, text='Seleccione un área:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        self.tabla = ttk.Treeview(self.frame, height = 10, columns = ('nombre','departamento'), selectmode = 'browse')
        self.tabla.tag_bind("mytag", "<<TreeviewSelect>>", self.editarActualizar)
        self.tabla.heading('#0', text='Id', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.heading('#2', text='Departamento', anchor=CENTER)
        self.tabla.column('#0', minwidth=0, width=40)
        self.tabla.column('#1', minwidth=0, width=120)
        self.tabla.column('#2', minwidth=0, width=120)

        lista = areas.ver()
        for x in lista:
            self.tabla.insert('', 0, values = (x[1],x[4]), text = x[0],tags=("mytag",))

        self.tabla.grid(row=0, column=0, pady=5, padx=5)

        self.frameEditar = LabelFrame(self.ventana, text='Editar información:')
        self.frameEditar.grid(column=1,row=0,pady=5,padx=5, sticky='w e s n')
        
        #Nombre------------
        Label(self.frameEditar, text='Nombre: ').grid(column=0, row=0, padx=5, pady=5)
        self.nombre = Entry(self.frameEditar)
        self.nombre.grid(column=1,row=0, padx=5, pady=5)

        #Descripcion-------------
        Label(self.frameEditar, text='Descripcion: ').grid(column=0, row=1, padx=5, pady=5)
        self.descripcion = Entry(self.frameEditar)
        self.descripcion.grid(column=1,row=1, padx=5, pady=5)

        #Responsable------------
        self.listaEmpleados = employers.ver()
        self.listaNombres=[]
        for x in self.listaEmpleados:
            self.listaNombres.append(x[2])
        Label(self.frameEditar, text='Responsable: ').grid(column=0, row=2, padx=5, pady=5)
        self.responsable = ttk.Combobox(self.frameEditar, state='readonly',values=self.listaNombres)
        self.responsable.grid(column=1,row=2,pady=5,padx=5)

        #Departamento------------
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(self.frameEditar, text='Departamento: ').grid(column=0, row=3, padx=5, pady=5)
        self.departamento = ttk.Combobox(self.frameEditar, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.grid(column=1,row=3,pady=5,padx=5)

        frameBotones = Frame(self.frameEditar)
        frameBotones.grid(column=0, row=4, columnspan=2)
        btGuardar = Button(frameBotones, text='Guardar', command= self.editarGuardar).grid(column=0, row=4, padx=5, pady=5, sticky='w e')
        btCancelar = Button(frameBotones, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=4, padx=5, pady=5, sticky='w e')

    def editarActualizar(self, event):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        resultado = areas.buscar(text) 
        #Nombre
        self.nombre.delete(0, "end")
        self.nombre.insert(0, resultado[1])
        #Descripcion
        self.descripcion.delete(0, "end")
        self.descripcion.insert(0, resultado[2])
        #Responsable
        self.responsable.current(self.listaNombres.index(resultado[3]))
        #Departamento
        self.departamento.current(self.listaNombresDepartamentos.index(resultado[4]))

    def editarGuardar(self):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        codigoDepartamento = self.listaDepartamentos[self.listaNombresDepartamentos.index(self.departamento.get())][0]
        #print(self.responsable.get())
        codigo = employers.buscar(self.responsable.get())[0][1]
        idDepartamento = self.listaDepartamentos[0]
        areas.modificar(text, self.nombre.get(),  self.descripcion.get(), codigo, codigoDepartamento)
        texto = 'El área ' + self.nombre.get() + ' ha sido modificada.'
        messagebox.showinfo(title='Área modificada', message=texto)
        self.ventana.destroy()
        self.editar()

    def eliminar(self):
        self.ventana = Toplevel()
        self.ventana.title('Eliminar área')

        self.frame = LabelFrame(self.ventana, text='Seleccione un área:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        self.tabla = ttk.Treeview(self.frame, height = 10, columns = ('nombre','departamento'), selectmode = 'browse')
        self.tabla.heading('#0', text='Id', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.heading('#2', text='Departamento', anchor=CENTER)
        self.tabla.column('#0', minwidth=0, width=40)
        self.tabla.column('#1', minwidth=0, width=120)
        self.tabla.column('#2', minwidth=0, width=120)

        lista = areas.ver()
        for x in lista:
            self.tabla.insert('', 0, values = (x[1],x[4]), text = x[0],tags=("mytag",))

        self.tabla.grid(row=0, column=0, pady=5, padx=5)

        self.frameEditar = LabelFrame(self.ventana, text='Eliminar')
        self.frameEditar.grid(column=1,row=0,pady=5,padx=5, sticky='w e s n')

        Button(self.frameEditar, text='Eliminar', command= self.eliminarELiminar).grid(column=0, row=0,pady=5, padx=5, sticky='w e')
        Button(self.frameEditar, text='Cancelar', command=self.ventana.destroy).grid(column=0, row=1,pady=5, padx=5, sticky='w e') 

    def eliminarELiminar(self):
        id = self.tabla.focus()
        clave = self.tabla.item(id, option='text')
        nombre = self.tabla.item(id, option='values')[0]
        texto = '¿En verdad desea eliminar el área ' + nombre +'? Esta eliminación será permantente'

        if messagebox.askyesno(title='¿Eliminar el área?', message=texto):
            areas.eliminarArea(clave)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Área eliminada', message=texto)
        self.ventana.destroy()

class Equipos(Crm):

    def __init__(self, padre):
        self.padre = padre
        self.root = padre.root

    def main(self):
        self.verTodos = IntVar()
        self.verTodos.set(0)

        global mainFrame

        clearMainFrame()

        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Departamento------------
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        
        Label(mainFrame, text='Departamento', fg='#666666', bg='#ffffff', font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        self.departamento2 = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento2.bind("<<ComboboxSelected>>", self.editarActualizarAreas)
        self.departamento2.place(x=10, y=70)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', fg='#666666', bg='#ffffff', font=("Segoe UI", "10", "normal")).place(x=10, y=110)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.editarActualizarEquipos)
        self.area.place(x=10, y=140)

        #Tabla de equipos-----------------------
        Label(mainFrame, text='Equipos', fg='#666666', bg='#ffffff', font=("Segoe UI", "10", "normal")).place(x=10, y=180)
        self.tabla = crearTabla(
            ['Nombre',],
            [0],
            [200,],
            [('',)],
            mainFrame,
            10,
            self.actualizarInformacion
        )
        self.tabla.place(x=10, y=210)

        Button(mainFrame, text='+ Agregar equipo',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.nuevo).place(x=10, y=450)

        self.info = Frame(mainFrame)
        self.info.config(bg=colorGray, width=root.winfo_width()-250, height=root.winfo_height()-50)
        self.info.place(x=250, y=0)

        Label(self.info, text='No se ha seleccionado ningún equipo', bg=colorGray, font=("Segoe UI", "11", "bold")).place(x=10, y=10)

    def actualizarInformacion(self, *event):
        global root
        try:
            self.info.destroy()
        except:
            pass
        self.info = Frame(mainFrame)
        self.info.config(bg=colorGray, width=root.winfo_width()-250, height=root.winfo_height()-50)
        self.info.place(x=250, y=0)

        #Seleccionando mantenimiento de base de datos
        select = list(plants.buscar(self.tabla.focus()))
        selectMantenimientos = maintenances.buscarPorEquipo(self.tabla.focus())
        select[3] = areas.buscar(select[3])[1]

        #Labels principales
        Label(self.info, text=select[1], bg=colorGray, font=("Segoe UI", "10", "bold"), wraplength=400, justify='left').place(x=10, y=10)
        Label(self.info, text=select[2], bg=colorGray, font=("Segoe UI", "9", "normal"), wraplength=400, justify='left').place(x=10, y=40)

        #Ultimo mantenimiento realizado
        Label(self.info, text="Último mantenimiento", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=10, y=80)
        text = maintenances.ultimoMantenimientoRealizado(select[0])
        if text == None:
            text = 'No se ha hecho ninguno'
        else:
            text = text.date.strftime('%d/%m/%Y')
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Segoe UI", "9", "bold")).place(x=140, y=80)

        #Ultimo mantenimiento programado
        Label(self.info, text="Siguiente mantenimiento programado", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=400, y=80)
        text = maintenances.ultimoMantenimientoProgramado(select[0])
        if text == None:
            text = 'No hay mantenimiento programado'
        else:
            text = text.date.strftime('%d/%m/%Y')
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Segoe UI", "9", "bold")).place(x=620, y=80)

        #Botones
        Button(self.info, text='Editar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.editar(select[0])).place(x=root.winfo_width()-500, y=10)

        Button(self.info, text='Eliminar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.eliminar(select[0])).place(x=root.winfo_width()-445, y=10)

        Button(self.info, text='Asignar actividades',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command = lambda: self.asignarActividades(select[0], mantFrame)).place(x=root.winfo_width()-380, y=10)

        #Frame con barra de desplazamiento
        maintenancesFrame = Frame(self.info, highlightthickness=0, bg=colorGray)
        maintenancesFrame.place(x=25,y=150)

        mantFrame = Canvas(maintenancesFrame,bg=colorGray, height=260, width=root.winfo_width()-300, highlightthickness=0)
        
        v = Scrollbar(maintenancesFrame, orient='horizontal', command=mantFrame.xview)
        scrollableFrame = Frame(mantFrame, bg=colorGray)
        scrollableFrame.bind("<Configure>", lambda e: mantFrame.configure(scrollregion=mantFrame.bbox("all")))
        mantFrame.create_window((0, 0), window=scrollableFrame, anchor='nw')
        mantFrame.configure(xscrollcommand=v.set)
        
        #Mostrar mantenimientos
        for i in selectMantenimientos:
            #Creando frame
            mant = Frame(scrollableFrame)
            mant.config(bg=colorDarkGray, highlightthickness=0, highlightbackground="#cccccc", width=250, height=250)
            mant.pack(pady=5, padx=5, side=LEFT)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i.id), fg='#111111', bg=colorDarkGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=10)
            Label(mant, text=i.date.strftime('%d/%m/%Y'), fg='#111111', bg=colorDarkGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
            Label(mant, text=i.status, fg='#111111', bg=colorDarkGray, font=("Segoe UI", "8", "normal"), wraplength=120, justify='right').place(x=100, y=30)
            #Descripción
            Label(mant, text='Matenimiento '+i.type, fg='#333333', bg=colorDarkGray, font=("Segoe UI", "8", "bold")).place(x=10, y=60)
            Label(mant, text=i.description, fg='#333333', bg=colorDarkGray, font=("Segoe UI", "8", "normal"), wraplength=230, justify='left').place(x=10, y=80)
            #Botón
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i.id, self)).place(x=180, y=200)

        mantFrame.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        v.pack(side="bottom", fill="x")

    def nuevo(self):
        self.verTodos = IntVar()
        self.verTodos.set(0)
        self.ventana = Toplevel()
        self.ventana.title('Nuevo equipo')

        frame = LabelFrame(self.ventana, text='Registrar equipo')
        frame.grid(column=0, row=0, padx=5, pady=5)

        #Nombre
        Label(frame, text='Nombre: ').grid(column=0,row=2)
        self.nombre = Entry(frame)
        self.nombre.grid(column=1,row=2, padx=5, pady=5)

        #Descripcion    
        Label(frame, text='Descripción: ').grid(column=0, row=3, padx=5, pady=5)
        self.descripcion = Entry(frame)
        self.descripcion.grid(column=1,row=3, padx=5, pady=5)

        #Departamento------------
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(frame, text='Departamento: ').grid(column=0, row=4, padx=5, pady=5)
        self.departamento = ttk.Combobox(frame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.nuevoActualizarAreas)
        self.departamento.grid(column=1,row=4,pady=5,padx=5)

        #Area
        self.listaNombresAreas=[]
        Label(frame, text='Área: ').grid(column=0, row=5, padx=5, pady=5)
        self.area = ttk.Combobox(frame, state='readonly',values=self.listaNombresAreas)
        self.area.grid(column=1,row=5,pady=5,padx=5)

        btGuardar = Button(frame, text='Guardar', command= self.nuevoGuardar).grid(column=0, row=6, padx=5, pady=5)
        btCancelar = Button(frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=6, padx=5, pady=5)

    def nuevoActualizarAreas(self, event):
        #print(self.departamento.current())
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
        #print(self.listaNombresAreas)
        self.area["values"]=self.listaNombresAreas

    def nuevoGuardar(self):
        #Preparando los datos
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        area = self.listaAreas[self.area.current()][0]
        #Enviando la solicitud
        plants.new(nombre, descripcion, area)

        texto = 'El equipo ' + self.nombre.get() + ' ha sido registrado.'
        messagebox.showinfo(title='Equipo registrado', message=texto)
        self.ventana.destroy()

    def editar(self, idEquipo):
        global root
        try:
            self.info.destroy()
        except:
            pass
        self.info = Frame(mainFrame)
        self.info.config(bg=colorGray, width=root.winfo_width()-250, height=root.winfo_height()-50)
        self.info.place(x=250, y=0)

        #Seleccionando mantenimiento de base de datos
        select = list(plants.buscar(self.tabla.focus()))
        selectMantenimientos = maintenances.buscarPorEquipo(self.tabla.focus())
        select[3] = areas.buscar(select[3])[1]
        
        #Nombre------------
        nombre = Entry(self.info, font=("Segoe UI", "10", "bold"), bg='#ffffff', fg="#000000", highlightthickness=0, borderwidth=2, relief=FLAT, width=30)
        nombre.insert(0,select[1])
        nombre.place(x=10, y=10)

        #Descripcion-------------
        descripcion = Entry(self.info, font=("Segoe UI", "9", "normal"), bg='#ffffff', fg="#000000", highlightthickness=0, borderwidth=2, relief=FLAT, width=100)
        descripcion.insert(0,select[2])
        descripcion.place(x=10, y=40)

        #Ultimo mantenimiento realizado
        Label(self.info, text="Último mantenimiento", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=10, y=80)
        text = maintenances.ultimoMantenimientoRealizado(select[0])
        if text == None:
            text = 'No se ha hecho ninguno'
        else:
            text = text.date.strftime('%d/%m/%Y')
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Segoe UI", "9", "bold")).place(x=140, y=80)

        #Ultimo mantenimiento programado
        Label(self.info, text="Siguiente mantenimiento programado", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=400, y=80)
        text = maintenances.ultimoMantenimientoProgramado(select[0])
        if text == None:
            text = 'No hay mantenimiento programado'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Segoe UI", "9", "bold")).place(x=620, y=80)

        #Botones
        Button(self.info, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.editarGuardar(idEquipo,nombre.get(), descripcion.get())).place(x=root.winfo_width()-510, y=10)

        Button(self.info, text='Eliminar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.eliminar(select[0])).place(x=root.winfo_width()-445, y=10)

        Button(self.info, text='Asignar actividades',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command = lambda: self.asignarActividades(select[0], mantFrame)).place(x=root.winfo_width()-380, y=10)

        #Frame con barra de desplazamiento
        v = Scrollbar(self.info, orient='horizontal')
        v.place(x=10, y=0)

        mantFrame = Canvas(self.info, height=250, width=root.winfo_width()-250, xscrollcommand=v.set, scrollregion=(0,0,250,1000))
        mantFrame.configure(bg=colorGray)
        mantFrame.place(x=0,y=150)

        #Mostrar mantenimientos
        for i in selectMantenimientos:
            #Creando frame
            mant = Frame(mantFrame)
            mant.config(bg=colorGray, highlightthickness=1, highlightbackground="#cccccc", width=250, height=250)
            mant.place(x=10+selectMantenimientos.index(i)*260, y=0)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i[0]), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=10)
            Label(mant, text=i[1], fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
            Label(mant, text=i[2], fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=120, justify='right').place(x=100, y=30)
            #Descripción
            Label(mant, text='Matenimiento '+i[5], fg='#333333', bg=colorGray, font=("Segoe UI", "8", "bold")).place(x=10, y=60)
            Label(mant, text=i[4], fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=230, justify='left').place(x=10, y=80)
            #Botón
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i[0], self)).place(x=180, y=200)

        v.config(command=mantFrame.xview)

    def editarGuardar(self, id, nombre, descripcion):
        equipoActual = plants.buscar(id)
        plants.modificar(id, nombre,  descripcion, equipoActual[3])
        texto = 'El equipo ' + nombre + ' ha sido modificado.'
        messagebox.showinfo(title='Equipo modificada', message=texto)
        self.actualizarInformacion()

    def editarActualizarEquipos(self, *event):
        #print(self.verTodos.get())
        if self.verTodos.get() == 1:
            self.listaEquipos = plants.ver()
        elif not hasattr(self, 'listaAreas'):
            self.listaEquipos = [[' ','Seleccione un area',' ']]
        else:
            self.listaEquipos = plants.buscarPorArea( self.listaAreas[self.area.current()][0])
            if len(self.listaEquipos) == 0:
                self.listaEquipos = [[' ','Area sin equipos',' ']]
        self.tabla.delete(*self.tabla.get_children())
        #print(self.listaAreas[self.area.current()][0])
        
        for x in self.listaEquipos:
            self.tabla.insert('', 0, id=x[0], values = (x[2],), text = x[1], tags=('mytag',))

    def editarActualizarAreas(self, event):
        #print(self.departamento2.current())
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento2.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
        #print(self.listaNombresAreas)
        self.area["values"]=self.listaNombresAreas

    def eliminar(self, id):
        nombre = plants.buscar(id)[1]
        texto = '¿En verdad desea eliminar el equipo ' + nombre +'? Esta eliminación será permantente'
        if messagebox.askyesno(title='¿Eliminar el equipo?', message=texto):
            plants.eliminar(id)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Equipo eliminada', message=texto)

    def asignarActividades(self, id, mantFrame):
        #Limpiar el frame
        mantFrame.destroy()
        #Variables

        #Tabla de actividades para asignar--------------
        Label(self.info, text='Actividades disponibles',fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=150)
        lista = activities.ver()
        listaIds = []
        for activity in lista:
            listaIds.append(activity[0])
            lista[lista.index(activity)] = [lista[lista.index(activity)][1], lista[lista.index(activity)][2]]
        self.tablaActividades = crearTabla(
            ['Nombre', 'Descripción'],
            listaIds,
            [200,300],
            lista,
            self.info,
            10,
            ''
        )
        self.tablaActividades.place(x=10, y=180)

        #Botón para asignar actividad
        Button(self.info, text='Asignar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = lambda:self.asignarActividad(self.tablaActividades.focus(),id)).place(x=10, y=420)

        #Tabla de actividades asignadas-------------
        Label(self.info, text='Actividades asignadas',fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=root.winfo_width()/2-150, y=150)
        lista = activities.buscarPorEquipo(id)
        listaIds = []
        for activity in lista:
            listaIds.append(activity[0])
            lista[lista.index(activity)] = [lista[lista.index(activity)][1], lista[lista.index(activity)][2]]
        self.tablaActividadesAsignadas = crearTabla(
            ['Nombre', 'Descripción'],
            listaIds,
            [200,300],
            lista,
            self.info,
            10,
            ''
        )
        self.tablaActividadesAsignadas.place(x=root.winfo_width()/2-150, y=180)

        #Botón para eliminar actividad asignada
        Button(self.info, text='Eliminar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = lambda:self.eliminarActividadAsignada(self.tablaActividadesAsignadas.focus())).place(x=root.winfo_width()/2-150, y=420)
   
    def actualizarActividades(self, *event):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        self.listaActividadesAsignadas = activities.buscarPorEquipo(id)
        if len(self.listaActividadesAsignadas) < 1:
            self.listaActividadesAsignadas =(['','Equipo sin actividades','',''],)
        self.tablaActividadesAsignadas.delete(*self.tablaActividadesAsignadas.get_children())        
        for x in self.listaActividadesAsignadas:
            #print(x)
            self.tablaActividadesAsignadas.insert('', 0, values = (x[1],x[2],x[3]), text = x[0],tags=("mytag",))

    def asignarActividad(self, idActividad, idEquipo):
        actividad = activities.buscar(idActividad)
        activities.nuevaActividadAsignada(actividad[1], actividad[2], actividad[3], idEquipo)
        texto = 'La actividad ' + actividad[1] + ' ha sido asignada al equipo.'
        messagebox.showinfo(title='Actividad asignada', message=texto)


    def eliminarActividadAsignada(self, idActividad):
        actividad = activities.buscarActividadAsignada(idActividad)
        activities.eliminarActividadAsignada(idActividad)
        texto = 'La actividad ' + actividad[1] + ' ha sido eliminada.'
        messagebox.showinfo(title='Actividad eliminada', message=texto)

class Actividades():

    def __init__(self):
        pass

    def nuevo(self):
        self.ventana = Toplevel()
        self.ventana.title('Nueva actividad')

        self.frame = LabelFrame(self.ventana, text='Registrar actividad')
        self.frame.grid(column=0,row=0,pady=5,padx=5,sticky='w e')

        Label(self.frame, text='Nombre: ').grid(column=0, row=0,pady=5,padx=5)
        self.nombre = Entry(self.frame)
        self.nombre.grid(column=1,row=0,pady=5,padx=5)
        Label(self.frame, text='Descripcion: ').grid(column=0, row=1,pady=5,padx=5)
        self.descripcion = Entry(self.frame)
        self.descripcion.grid(column=1,row=1,pady=5,padx=5)
        Label(self.frame, text='Tiempo aproximado (hrs): ').grid(column=0, row=2,pady=5,padx=5)
        self.tiempo = Entry(self.frame)
        self.tiempo.grid(column=1,row=2,pady=5,padx=5)

        btGuardar = Button(self.frame, text='Guardar', command= self.nuevoGuardar).grid(column=0, row=3)
        btCancelar = Button(self.frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=3)    

    def nuevoGuardar(self):
        activities.new(self.nombre.get(), self.descripcion.get(),int(self.tiempo.get()))
        texto = 'La actividad ' + self.nombre.get() + ' ha sido registrada.'
        messagebox.showinfo(title='Actividad registrada', message=texto)
        self.ventana.destroy()

    def editar(self):
        self.ventana = Toplevel()
        self.ventana.title('Editar actividad')

        self.frame = LabelFrame(self.ventana, text='Seleccione una actividad:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        self.tabla = ttk.Treeview(self.frame, height = 10, columns = ('nombre','descripcion','tiempo'), selectmode = 'browse')
        self.tabla.tag_bind("mytag", "<<TreeviewSelect>>", self.editarActualizar)
        self.tabla.heading('#0', text='Id', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.heading('#2', text='Descripción', anchor=CENTER)
        self.tabla.heading('#3', text='Tiempo aprox. (hrs)', anchor=CENTER)
        self.tabla.column('#0', minwidth=0, width=40)
        self.tabla.column('#1', minwidth=0, width=120)
        self.tabla.column('#2', minwidth=0, width=120)
        self.tabla.column('#3', minwidth=0, width=60)

        lista = activities.ver()
        for x in lista:
            self.tabla.insert('', 0, values = (x[1],x[2],x[3]), text = x[0],tags=("mytag",))

        self.tabla.grid(row=0, column=0, pady=5, padx=5)

        self.frameEditar = LabelFrame(self.ventana, text='Editar información:')
        self.frameEditar.grid(column=1,row=0,pady=5,padx=5, sticky='w e s n')
        
        #Nombre------------
        Label(self.frameEditar, text='Nombre: ').grid(column=0, row=0, padx=5, pady=5)
        self.nombre = Entry(self.frameEditar)
        self.nombre.grid(column=1,row=0, padx=5, pady=5)

        #Descripcion-------------
        Label(self.frameEditar, text='Descripcion: ').grid(column=0, row=1, padx=5, pady=5)
        self.descripcion = Entry(self.frameEditar)
        self.descripcion.grid(column=1,row=1, padx=5, pady=5)

        #Tiempo aproximado----------
        Label(self.frameEditar, text='Tiempo aproximado (hrs): ').grid(column=0, row=2,pady=5,padx=5)
        self.tiempo = Entry(self.frameEditar)
        self.tiempo.grid(column=1,row=2,pady=5,padx=5)

        frameBotones = Frame(self.frameEditar)
        frameBotones.grid(column=0, row=3, columnspan=2)
        btGuardar = Button(frameBotones, text='Guardar', command= self.editarGuardar).grid(column=0, row=0, padx=5, pady=5, sticky='w e')
        btCancelar = Button(frameBotones, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=0, padx=5, pady=5, sticky='w e')

    def editarActualizar(self, event):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        resultado = activities.buscar(text) 
        #Nombre
        self.nombre.delete(0, "end")
        self.nombre.insert(0, resultado[0][1])
        #Descripcion
        self.descripcion.delete(0, "end")
        self.descripcion.insert(0, resultado[0][2])
        #Tiempo
        self.tiempo.delete(0, "end")
        self.tiempo.insert(0, resultado[0][3])

    def editarGuardar(self):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        activities.modificar(text, self.nombre.get(),  self.descripcion.get(), self.tiempo.get())
        texto = 'La actividad ' + self.nombre.get() + ' ha sido modificada.'
        messagebox.showinfo(title='Actividad modificada', message=texto)
        self.ventana.destroy()

    def eliminar(self):
        self.ventana = Toplevel()
        self.ventana.title('Eliminar actividad')

        self.frame = LabelFrame(self.ventana, text='Seleccione una actividad:')
        self.frame.grid(column=0,row=0,pady=10,padx=10,sticky='w e')

        self.tabla = ttk.Treeview(self.frame, height = 10, columns = ('nombre','descripcion','tiempo'), selectmode = 'browse')
        self.tabla.heading('#0', text='Id', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        self.tabla.heading('#2', text='Descripción', anchor=CENTER)
        self.tabla.heading('#3', text='Tiempo aprox. (hrs)', anchor=CENTER)
        self.tabla.column('#0', minwidth=0, width=40)
        self.tabla.column('#1', minwidth=0, width=120)
        self.tabla.column('#2', minwidth=0, width=120)
        self.tabla.column('#3', minwidth=0, width=60)

        lista = activities.ver()
        for x in lista:
            self.tabla.insert('', 0, values = (x[1],x[2],x[3]), text = x[0])

        self.tabla.grid(row=0, column=0, pady=5, padx=5)

        self.frameEditar = LabelFrame(self.ventana, text='Eliminar')
        self.frameEditar.grid(column=1,row=0,pady=5,padx=5, sticky='w e s n')

        Button(self.frameEditar, text='Eliminar', command= self.eliminarELiminar).grid(column=0, row=0,pady=5, padx=5, sticky='w e')
        Button(self.frameEditar, text='Cancelar', command=self.ventana.destroy).grid(column=0, row=1,pady=5, padx=5, sticky='w e') 

    def eliminarELiminar(self):
        id = self.tabla.focus()
        clave = self.tabla.item(id, option='text')
        nombre = self.tabla.item(id, option='values')[0]
        texto = '¿En verdad desea eliminar la actividad ' + nombre +'? Esta eliminación será permantente'

        if messagebox.askyesno(title='¿Eliminar la actividad?', message=texto):
            activities.eliminar(clave)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Actividad eliminada', message=texto)
        self.ventana.destroy()

def func_displayMaintenance(id, object):
    return lambda event: object.parent.objetoMantenimientos.displayMaintenance(id) 

class Mantenimientos(Crm):
    def __init__(self, padre):
        self.padre = padre
        self.parent = padre
        global mainFrame
        
    def main(self):
        global mainFrame
        global root
        
        clearMainFrame()

        #Title
        Label(mainFrame, text='Mantenimientos', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Buttons
        Button(mainFrame, text='+ Mantenimiento preventivo',font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.nuevo).place(x=10, y=40)

        Button(mainFrame, text='+ Mantenimiento correctivo',font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.newCorrective).place(x=200, y=40)
        
        Button(mainFrame, text='Ver todos',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.allMaintenancesWindow).place(x=390, y=40)

        #Show all maintenances
        lista = maintenances.getAll(limit = 10)
        allMaintenances = Frame(mainFrame, highlightthickness=0, bg="#ffffff")
        allMaintenances.place(x=10, y=90)
        canvas = Canvas(allMaintenances, bg="#ffffff", width=root.winfo_width()/2-70, height=root.winfo_height()-200, highlightthickness=0)
        scrollbar = Scrollbar(allMaintenances, orient='vertical', command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#ffffff")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        for i in lista:
            mant = Frame(scrollable_frame)
            mant.config(bg=colorGray, highlightthickness=0, highlightbackground="#eeeeee", width=root.winfo_width()/2-100, height=100)
            mant.pack(pady=10, padx=15)
            #Tittle
            Label(mant, text='Mantenimiento ID '+str(i.id), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=45, y=10)
            #Date
            Label(mant, text=i.date.strftime('%d/%m/%Y'), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=45, y=30)
            #Status
            if i.status == 'Realizado' or i.status == 'Realizado Programado':
                color = colorGreen
            elif i.status == 'Programado':
                color = colorBlue
            elif i.status == 'Cancelado':
                color = colorRed
            Label(mant, text=i.status, fg=color, bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, anchor="e", width=20).place(x=root.winfo_width()/2-255, y=10)
            #type
            if i.type == maintenances.Corrective:
                Label(mant, image = imgCorrective, bd=0, width=25, height=25).place(x=10, y=15)
            elif i.type == maintenances.Preventive:
                Label(mant, image = imgPreventive, bd=0, width=25, height=25).place(x=10, y=15)
            else:
                Label(mant, image = imgCorrective, bd=0, width=25, height=25).place(x=10, y=15)
            Label(mant, text='Matenimiento '+i.type, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "bold")).place(x=185, y=30)
            
            #Descripción
            Label(mant, text=i.description, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=root.winfo_width()/2-190, justify='left').place(x=10, y=50)
            #Botón
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i.id, self)).place(x=root.winfo_width()/2-170, y=60)

        canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        #Programmed maintenances
        Label(mainFrame, text='Mantenimientos programado', bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=root.winfo_width()/2, y=60)
        
        lista = maintenances.getProgrammed()
        
        programmedMaintenances = Frame(mainFrame, highlightthickness=0, bg="#ffffff")
        programmedMaintenances.place(x=root.winfo_width()/2, y=90)
        canvasprogrammedMaintenances = Canvas(programmedMaintenances, bg="#ffffff", width=root.winfo_width()/2-70, height=root.winfo_height()-200, highlightthickness=0)
        scrollbarprogrammedMaintenances = Scrollbar(programmedMaintenances, orient='vertical', command=canvasprogrammedMaintenances.yview)
        scrollable_frameprogrammedMaintenances = Frame(canvasprogrammedMaintenances, bg="#ffffff")
        scrollable_frameprogrammedMaintenances.bind("<Configure>", lambda e: canvasprogrammedMaintenances.configure(scrollregion=canvasprogrammedMaintenances.bbox("all")))
        canvasprogrammedMaintenances.create_window((0, 0), window=scrollable_frameprogrammedMaintenances, anchor='nw')
        canvasprogrammedMaintenances.configure(yscrollcommand=scrollbarprogrammedMaintenances.set)

        for i in lista:
            mant = Frame(scrollable_frameprogrammedMaintenances)
            mant.config(bg=colorGray, highlightthickness=0, highlightbackground="#eeeeee", width=root.winfo_width()/2-100, height=100)
            mant.pack(pady=10, padx=15)
            if i.date < datetime.now():
                actualColor = colorRed
            else:
                actualColor = colorGreen
            Frame(mant, bg=actualColor, height=100, width=3).place(x=0, y=0)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i.id), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=10)
            #Date
            Label(mant, text=i.date.strftime('%d/%m/%Y'), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
            #Status
            if i.status == 'Realizado' or i.status == 'Realizado Programado':
                color = colorGreen
            elif i.status == 'Programado':
                color = colorBlue
            elif i.status == 'Cancelado':
                color = colorRed
            Label(mant, text=i.status, fg=color, bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, anchor="e", width=20).place(x=root.winfo_width()/2-255, y=10)
            #type
            Label(mant, text='Matenimiento '+i.type, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "bold")).place(x=140, y=30)
            #Descripción
            Label(mant, text=i.description, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=root.winfo_width()/2-190, justify='left').place(x=10, y=50)
            #Botón
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i.id, self)).place(x=root.winfo_width()/2-170, y=60)

        canvasprogrammedMaintenances.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbarprogrammedMaintenances.pack(side="right", fill="y")

    def allMaintenancesWindow(self):
        global mainFrame
        clearMainFrame()
        
        Label(mainFrame, text='Mantenimientos', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)
        maintenancesList = maintenances.getAll()
        
        maintenancesFrame = ScrollableFrame(mainFrame, x=10, y=60, width=root.winfo_width()-40, height=root.winfo_height()-120)
        maintenancesFrame.place(x=0, y=0)
        
        Label(mainFrame, text='Id', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=20, y=40)
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=90, y=40)
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=270, y=40)
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=370, y=40)
        
        for maint in maintenancesList:
            reqNumber = maintenancesList.index(maint)
            backColor = colorGray if reqNumber%2==0 else colorWhite
            frame = Frame(maintenancesFrame.scrollableFrame)
            frame.config(width=root.winfo_width()-80, height=30, bg=backColor)
            frame.bind('<Button-1>', func_displayMaintenance(maint.id, self))
            frame.pack(pady=1)
            Label(frame, text=maint.id, bg=backColor, font=("Segoe UI", "10", "normal")).place(x=10, y=4)
            Label(frame, text=datetime.date(maint.date).strftime("%d %B %Y"), bg=backColor, font=("Segoe UI", "10", "normal")).place(x=80, y=4)
            Label(frame, text=maint.status.capitalize(), bg=backColor, font=("Segoe UI", "10", "normal")).place(x=260, y=4)
            Label(frame, text=maint.description, bg=backColor, font=("Segoe UI", "10", "normal")).place(x=360, y=4)
    
    def ActualizarAreas(self, event):
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
        self.area["values"]=self.listaNombresAreas

    def ActualizarEquipos(self, *event):
        self.listaEquipos = plants.buscarPorArea( self.listaAreas[self.area.current()][0])
        if len(self.listaEquipos) == 0:
            self.listaEquipos = [[' ','Area sin equipos']]
        self.tabla.delete(*self.tabla.get_children())
        
        for x in self.listaEquipos:
            self.tabla.insert('', 0,id=x[0], text = x[1], values =x[2], tags=("mytag","color"))

    def actualizarActividades(self, *event):
        id = self.tabla.focus()
        self.listaActividadesAsignadas = activities.buscarPorEquipo(id)
        if len(self.listaActividadesAsignadas) < 1:
            self.listaActividadesAsignadas =(['','Equipo sin actividades'],)
        self.tablaActividadesAsignadas.delete(*self.tablaActividadesAsignadas.get_children())        
        for x in self.listaActividadesAsignadas:
            self.tablaActividadesAsignadas.insert('', 0, id= x[0], values = x[2], text = x[1])

    def nuevo(self):
        global mainFrame
        clearMainFrame()
        
        self.varRepeat = IntVar()
        
        self.newMaintenance = maintenances.Maintenance(type=maintenances.Preventive)
        
        #Tittle
        Label(mainFrame, text='Mantenimiento preventivo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=10, y=70)

        #Estado------------
        self.listaEstados=[maintenances.Done, maintenances.Programmed]
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=280)
        self.estado = ttk.Combobox(mainFrame, state='readonly',values=self.listaEstados)
        self.estado.place(x=10, y=310)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=340)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = employers.ver('nombre'))
        self.responsible.place(x=10, y=370)

        #Repeat
        self.repeatOn = Checkbutton(mainFrame, bg="#ffffff", text="Repetir cada", font=("Segoe UI", "10", "normal"), variable=self.varRepeat, onvalue=1, offvalue=0)
        self.repeatOn.place(x=10, y=400)
        self.repeat = Entry(mainFrame, width=5, highlightthickness=2)
        self.repeat.place(x=120, y=400)
        Label(mainFrame, text='días', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=160, y=400)

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=430)
        self.description = Text(mainFrame, width=40, height=9, font=("Segoe UI", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.place(x=10, y=460)

        Button(mainFrame, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.nuevoGuardar).place(x=root.winfo_width()-100, y=10)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=400, y=10)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=400, y=40)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=600, y=10)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=40)

        #Plants table
        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=400, y=80)
        self.tabla = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('','Seleccione un area y departamento'),],
            mainFrame,
            10,
            self.actualizarActividades
        )
        self.tabla.place(x=400, y=110)

        #Activities table
        Label(mainFrame, text='Actividades', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=400, y=340)
        self.tablaActividadesAsignadas = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('',''),],
            mainFrame,
            10,
            ''
        )

        self.tablaActividadesAsignadas.place(x=400, y=370)

        #Botón para asignar actividad
        Button(mainFrame, text=' + ',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = self.asignarActividad).place(x=650, y=600)

        #Botón para eliminar actividad asignada
        #Button(self.frameA, text='-', command = self.eliminarActividadAsignada).grid(row=2, column=7)

        #Tabla de equipos
        self.activitiesTable = ScrollableFrame(mainFrame, x=800, y=10, width=300, height=root.winfo_height()-100)
        self.activitiesTable.place(800, 10)
        # self.tablaEquipos = crearTabla(['Nombre','Descripción'],[0,],[120,120],[['Nd','']],mainFrame,10,'')
        # self.tablaEquipos.place(x=800,y=10)

        # self.listaEquiposSeleccionados = []
        # self.listaActividadesSeleccionadas = []

    def newCorrective(self):
        global mainFrame
        clearMainFrame()
        
        #Var
        self.newMaintenance = maintenances.Maintenance(type = maintenances.Corrective)
        self.searchString = StringVar(mainFrame)
        descriptionString = StringVar(mainFrame)
        self.quantity = StringVar(mainFrame)

        self.selectedPlants = []

        #Tittle
        Label(mainFrame, text='Mantenimiento correctivo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=10, y=70)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=300, y=40)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = employers.ver('nombre'))
        self.responsible.place(x=300, y=70  )

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=300, y=100)
        self.description = Text(mainFrame, width=120, height=4, font=("Segoe UI", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.place(x=300, y=130)

        Button(mainFrame, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.saveCorrective).place(x=root.winfo_width()-100, y=10)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=450, y=40)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=450, y=70)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=600, y=40)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=70)
        
        #Status
        self.statusList=[maintenances.Done, maintenances.Programmed]
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=750, y=40)
        self.status = ttk.Combobox(mainFrame, state='readonly',values=self.statusList)
        self.status.place(x=750, y=70)

        #Plants table
        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=280)
        self.tabla = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [200, 200],
            [('','Seleccione un area y departamento'),],
            mainFrame,
            5, 
            ''
        )
        self.tabla.place(x=10, y=310)

        Button(mainFrame, text='+',font=("Segoe UI", "11", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.selectPlant).place(x=420, y=320)

        #Plants table
        Label(mainFrame, text='Equipos seleccionados', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=450)
        self.selectedPlantsTable = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [200, 200],
            [('','Aún no hay nada seleccionado'),],
            mainFrame,
            5, 
            ''
        )
        self.selectedPlantsTable.place(x=10, y=480)

        Button(mainFrame, text='-',font=("Segoe UI", "11", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.deselectPlant).place(x=420, y=490)

        #Search
        Label(mainFrame, text='Productos usados', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=500, y=230)
        search = Frame(mainFrame)
        search.config(bg='#ECECEC', width=400, height=30)
        search.place(x=500 , y=260)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=50, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#ECECEC', highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventorySearch)
        
        #Products table
        self.productsTable = crearTabla(['Nombre', 'Descripción', 'Marca', 'Modelo'], [1,], [100,100,100,100], [['','','',''],], mainFrame, 4, '' )
        self.productsTable.place(x=500, y=300)
        
        #Coment
        Label(mainFrame, text='Comentario',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=500, y=430)
        self.comment = Text(mainFrame, width=43, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=590, y=430)
        
        #Quantity
        Label(mainFrame, text='Cantidad',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=500, y=500)
        Entry(mainFrame, width=20, textvariable=self.quantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=590, y=500)
        
        #Add product
        Button(mainFrame, text='+ Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.addProductToMaintenance).place(x=820, y=530)
        
        #Products
        Label(mainFrame, text='Productos',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=950, y=230)
        
        self.productsFrame = ScrollableFrame(mainFrame, width=380, height=200, x=950, y=260)
        self.productsFrame.place(x=950, y=260)
        
    def editPreventiveWindow(self, maintenance):
        """Open a window to edit a preventive maintenance.

        Args:
            maintenance (Maintenance): _description_
        """ 
        global mainFrame
        clearMainFrame()
        
        self.varRepeat = IntVar()
        self.newMaintenance = maintenance
        self.varRepeat.set(1) if self.newMaintenance.repeat != None else self.varRepeat.set(0)
        
        #Tittle
        Label(mainFrame, text='Mantenimiento preventivo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
    
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(maintenance.date.strftime('%Y')), month = int(maintenance.date.strftime('%m')), day = int(maintenance.date.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=10, y=70)

        #Estado------------
        self.listaEstados=[maintenances.Done, maintenances.Programmed]
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=280)
        self.estado = ttk.Combobox(mainFrame, state='readonly',values=self.listaEstados)
        self.estado.set(self.newMaintenance.status)
        self.estado.place(x=10, y=310)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=340)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = employers.ver('nombre'))
        self.responsible.set(employers.Employer(id=self.newMaintenance.responsible).name)
        self.responsible.place(x=10, y=370)

        #Repeat
        self.repeatOn = Checkbutton(mainFrame, bg="#ffffff", text="Repetir cada", font=("Segoe UI", "10", "normal"), variable=self.varRepeat, onvalue=1, offvalue=0)
        self.repeatOn.place(x=10, y=400)
        self.repeat = Entry(mainFrame, width=5, highlightthickness=2)
        self.repeat.insert(0, self.newMaintenance.repeat)
        self.repeat.place(x=120, y=400)
        Label(mainFrame, text='días', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=160, y=400)

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=430)
        self.description = Text(mainFrame, width=40, height=9, font=("Segoe UI", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1, wrap=WORD)
        self.description.insert(INSERT, self.newMaintenance.description)
        self.description.place(x=10, y=460)

        Button(mainFrame, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.nuevoGuardar).place(x=root.winfo_width()-100, y=10)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=400, y=10)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=400, y=40)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=600, y=10)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=40)

        #Plants table
        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=400, y=80)
        self.tabla = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('','Seleccione un area y departamento'),],
            mainFrame,
            10,
            self.actualizarActividades
        )
        self.tabla.place(x=400, y=110)

        #Activities table
        Label(mainFrame, text='Actividades', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=400, y=340)
        self.tablaActividadesAsignadas = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('',''),],
            mainFrame,
            10,
            ''
        )
        self.tablaActividadesAsignadas.place(x=400, y=370)

        #Botón para asignar actividad
        Button(mainFrame, text=' + ',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = self.asignarActividad).place(x=650, y=600)

        #Tabla de equipos
        self.activitiesTable = ScrollableFrame(mainFrame, x=800, y=10, width=300, height=root.winfo_height()-100)
        self.activitiesTable.place(800, 10)
        
        for activity in self.newMaintenance.activities:
            actualFrame = Frame(self.activitiesTable.scrollableFrame)
            actualFrame.config(bg=colorGray, highlightthickness=0, width=290, height=100)
            actualFrame.pack(pady=5, padx=5)
            #Plant
            Label(actualFrame, text=activity.plant.department.name + ' > ' + activity.plant.area.name + ' > '+ activity.plant.name, fg='#444444', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='left').place(x=10, y=10)
            #Name
            Label(actualFrame, text=activity.name, fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=30)
            #Description
            Label(actualFrame, text=activity.description, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=270, justify='left').place(x=10, y=50)
            #Button
            Button(actualFrame, text=' - ',font=("Segoe UI", "9", "bold"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=deleteActivityFromList(self.newMaintenance.activities.index(activity), self)).place(x=260, y=10)
    
    def editCorrectiveWindow(self, maintenance):
        """Open a window to edit a preventive maintenance.

        Args:
            maintenance (Maintenance): _description_
        """ 
        global mainFrame
        clearMainFrame()
        
        #Var
        self.newMaintenance = maintenance
        self.searchString = StringVar(mainFrame)
        descriptionString = StringVar(mainFrame)
        self.quantity = StringVar(mainFrame)

        self.selectedPlants = self.newMaintenance.plants

        #Tittle
        Label(mainFrame, text='Mantenimiento correctivo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(self.newMaintenance.date.strftime('%Y')), month = int(self.newMaintenance.date.strftime('%m')), day = int(self.newMaintenance.date.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=10, y=70)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=300, y=40)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = employers.ver('nombre'))
        self.responsible.set(employers.Employer(id = self.newMaintenance.responsible).name)
        self.responsible.place(x=300, y=70  )

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=300, y=100)
        self.description = Text(mainFrame, width=120, height=4, font=("Segoe UI", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.insert(INSERT, self.newMaintenance.description)
        self.description.place(x=300, y=130)

        Button(mainFrame, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.saveCorrective).place(x=root.winfo_width()-100, y=10)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=450, y=40)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=450, y=70)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=600, y=40)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=70)
        
        #Status
        self.statusList=[maintenances.Done, maintenances.Programmed]
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=750, y=40)
        self.status = ttk.Combobox(mainFrame, state='readonly',values=self.statusList)
        self.status.set(self.newMaintenance.status)
        self.status.place(x=750, y=70)

        #Plants table
        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=280)
        self.tabla = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [200, 200],
            [('','Seleccione un area y departamento'),],
            mainFrame,
            5, 
            ''
        )
        self.tabla.place(x=10, y=310)

        Button(mainFrame, text='+',font=("Segoe UI", "11", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.selectPlant).place(x=420, y=320)

        #Plants table
        Label(mainFrame, text='Equipos seleccionados', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=450)
        self.selectedPlantsTable = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [200, 200],
            [('','Aún no hay nada seleccionado'),],
            mainFrame,
            5, 
            ''
        )
        self.selectedPlantsTable.place(x=10, y=480)

        Button(mainFrame, text='-',font=("Segoe UI", "11", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.deselectPlant).place(x=420, y=490)

        #Search
        Label(mainFrame, text='Productos usados', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=500, y=230)
        search = Frame(mainFrame)
        search.config(bg='#ECECEC', width=400, height=30)
        search.place(x=500 , y=260)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=50, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#ECECEC', highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventorySearch)
        
        #Products table
        self.productsTable = crearTabla(['Nombre', 'Descripción', 'Marca', 'Modelo'], [1,], [100,100,100,100], [['','','',''],], mainFrame, 4, '' )
        self.productsTable.place(x=500, y=300)
        
        #Coment
        Label(mainFrame, text='Comentario',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=500, y=430)
        self.comment = Text(mainFrame, width=43, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=590, y=430)
        
        #Quantity
        Label(mainFrame, text='Cantidad',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=500, y=500)
        Entry(mainFrame, width=20, textvariable=self.quantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=590, y=500)
        
        #Add product
        Button(mainFrame, text='+ Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.addProductToMaintenance).place(x=820, y=530)
        
        #Products
        Label(mainFrame, text='Productos',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=950, y=230)
        
        self.productsFrame = ScrollableFrame(mainFrame, width=380, height=200, x=950, y=260)
        self.productsFrame.place(x=950, y=260)
        
        self.updateProductsFrame()
        self.updatePlantsTable()
        
    def updateInventorySearch(self, event):
        productsList = inventory.findByName(self.searchString.get())
        self.productsTable.delete(*self.productsTable.get_children())
        for product in productsList:
            self.productsTable.insert('', 0, id=product.id, text=product.name, values=(product.description, product.brand, product.model))
            
    def addProductToMaintenance(self):
        self.newMaintenance.addMovement(productId = self.productsTable.focus(), quantity=int(self.quantity.get()), comment=None if self.comment.get('1.0',END) == '' else self.comment.get('1.0',END))
        self.quantity.set('')
        self.comment.delete("1.0", END)
        self.updateProductsFrame()
        
    def updateProductsFrame(self):
        self.productsFrame.clear()
        for mov in self.newMaintenance.products:
            product = inventory.Product(id = mov.product)
            productFrame = Frame(self.productsFrame.scrollableFrame)
            productFrame.config(bg=colorGray, highlightthickness=0, width=360, height=70)
            productFrame.pack(pady=5, padx=5)
            #Plant
            name = Label(productFrame, text=product.name, fg='#000000', bg=colorGray, font=("Segoe UI", "11", "normal"), wraplength=300, justify='left')
            name.place(x=10, y=10)
            name.update()
            Label(productFrame, text='Cantidad: '+str(mov.quantity), fg=colorBlue, bg=colorGray, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=name.winfo_width()+15, y=10)
            Label(productFrame, text=mov.comment, fg='#4d4d4d', bg=colorGray, font=("Segoe UI", "9", "normal"), wraplength=600, justify='left').place(x=10, y=35)
            productFrame.update()
            #Button(productFrame, text=' X ',font=("Segoe UI", "9", "bold"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=1, relief=FLAT, command=self.addProductToRequisition).place(x=productFrame.winfo_width()-35, y=10)

    def selectPlant(self):
        plantId = self.tabla.focus()
        plantData = plants.Plant(id = plantId)
        if not plantData in self.selectedPlants:
            self.selectedPlants.append(plantData)
            print(f"Plant with id {plantId} added to the maintenance")
        self.updatePlantsTable()

    def deselectPlant(self):
        plantId = self.selectedPlantsTable.focus()
        plantData = plants.Plant(id = plantId)
        for plant in self.selectedPlants:
            if plantData.id == plant.id:
                self.selectedPlants.pop(self.selectedPlants.index(plant))
                print(f"Plant with id {plantId} removed to the maintenance")
        self.updatePlantsTable()

    def updatePlantsTable(self):
        self.selectedPlantsTable.delete(*self.selectedPlantsTable.get_children())
        if len(self.selectedPlants) == 0:
            self.selectedPlantsTable.insert('', 0, id = 0, values = 'Aún no hay nada seleccionado', text = '',tags=("mytag",))
            return
        for x in self.selectedPlants:
            self.selectedPlantsTable.insert('', 0, id = x.id, values = x.description, text = x.name,tags=("mytag",))

    def saveCorrective(self):
        self.newMaintenance.date = datetime.combine(self.cal.selection_get(), datetime.min.time())
        self.newMaintenance.responsible = employers.ver('id')[self.responsible.current()]
        self.newMaintenance.status = self.statusList[self.status.current()]
        self.newMaintenance.description = self.description.get('1.0', END)
        self.newMaintenance.plants = self.selectedPlants
        
        self.newMaintenance.save()

        texto = f"El mantenimiento ha sido registrado con id {self.newMaintenance.id}."
        messagebox.showinfo(title='Mantenimiento registrado', message=texto)
        self.displayMaintenance(self.newMaintenance.id)

    def asignarActividad(self):
        #Get activity
        newActivity = activities.Activity(id = self.tablaActividadesAsignadas.focus(), assigned= True)
        if newActivity not in self.newMaintenance.activities:
            self.newMaintenance.activities.append(newActivity)
            self.newMaintenance.activities.sort(key=lambda x: x.name)

        self.activitiesTable.clear()
        for activity in self.newMaintenance.activities:
            actualFrame = Frame(self.activitiesTable.scrollableFrame)
            actualFrame.config(bg=colorGray, highlightthickness=0, width=290, height=100)
            actualFrame.pack(pady=5, padx=5)
            #Plant
            Label(actualFrame, text=activity.plant.department.name + ' > ' + activity.plant.area.name + ' > '+ activity.plant.name, fg='#444444', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='left').place(x=10, y=10)
            #Name
            Label(actualFrame, text=activity.name, fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=30)
            #Description
            Label(actualFrame, text=activity.description, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=270, justify='left').place(x=10, y=50)
            #Button
            Button(actualFrame, text=' - ',font=("Segoe UI", "9", "bold"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=deleteActivityFromList(self.newMaintenance.activities.index(activity), self)).place(x=260, y=10)

    def eliminarActividadAsignada(self, activity):
        self.newMaintenance.activities.pop(activity)

        self.activitiesTable.clear()
        for activity in self.newMaintenance.activities:
            actualFrame = Frame(self.activitiesTable.scrollableFrame)
            actualFrame.config(bg=colorGray, highlightthickness=0, width=290, height=100)
            actualFrame.pack(pady=5, padx=5)
            #Plant
            Label(actualFrame, text=activity.plant.department + ' > ' + activity.plant.area + ' > '+ activity.plant.name, fg='#444444', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='left').place(x=10, y=10)
            #Name
            Label(actualFrame, text=activity.name, fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=30)
            #Description
            Label(actualFrame, text=activity.description, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=270, justify='left').place(x=10, y=50)
            #Button
            Button(actualFrame, text=' - ',font=("Segoe UI", "9", "bold"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=deleteActivityFromList(self.newMaintenance.activities.index(activity), self)).place(x=260, y=10)

    def nuevoGuardar(self):
        self.newMaintenance.date = datetime.combine(self.cal.selection_get(), datetime.min.time())
        self.newMaintenance.status = self.estado.get()
        self.newMaintenance.responsible = employers.ver()[self.responsible.current()][0]
        self.newMaintenance.description = self.description.get('1.0',END)
        self.newMaintenance.type = maintenances.Preventive
        if (self.varRepeat.get()):
            self.newMaintenance.repeat = self.repeat.get()
        else:
            self.newMaintenance.repeat = None

        self.newMaintenance.save()
        
        texto = f"El mantenimiento ha sido registrado con id {self.newMaintenance.id}."
        messagebox.showinfo(title='Mantenimiento registrado', message=texto)
        self.displayMaintenance(self.newMaintenance.id)

    def programar(self, id=0):
        if id == 0:
            self.noProgramados = maintenances.buscarNoProgramados()
            print(f"Starting to schedule maintenances...")
            for i in self.noProgramados:
                fecha = i[1].split('/')
                fecha = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
                #Duplicar el mantenimiento
                maintenances.nuevo(fecha+timedelta(days=int(i[6])), 'Programado', i[3], i[4], i[5], i[6])
                print(f"    The maintenance was registered with id: {maintenances.ultimoMantenimiento()}")
                #Duplicar actividades
                for j in maintenances.buscarActividades(i[0]):
                    maintenances.agregarActividad(maintenances.ultimoMantenimiento(), j[2])
                    print(f"        Activity added to maintenance")
                maintenances.editar(i[0], fecha, 'Realizado Programado', i[3], i[4], i[5], i[6])
            print(f"{len(self.noProgramados)} maintenances registered succesfully")
            texto = f"Se han programado {len(self.noProgramados)} mantenimientos con éxito."
            messagebox.showinfo(title='Mantenimientos programados', message=texto)    
        else:
            mant = maintenances.Maintenance(id = id)
            nextMaintenance = mant.scheduleNext()
            if nextMaintenance == 1:
                messagebox.showwarning(title='Error', message='El mantenimiento no se puede programar. Consulte la ayuda para más información.')
                return 1
            messagebox.showinfo(title='Matenimiento programado', message=f"El mantenimiento se ha programado correctamente con el ID {nextMaintenance.id}")  
            self.displayMaintenance(nextMaintenance.id) 

    def realizarMantenimiento(self, id):
        if id == '':
            messagebox.showwarning(title='No hay nada seleccionado', message='Seleccione un mantenimiento.')
        else:
            select = maintenances.Maintenance(id = id)
            select.status = maintenances.Done
            select.date = datetime.now()
            select.save()
            messagebox.showinfo(title='Editado con éxito', message='El mantenimiento ha sido modificado correctamente.')
            if messagebox.askyesno(title='¿Programar siguiente?', message='¿Desea programar el siguiente mantenimiento?'):
                self.programar(select.id)

    def cancelarMantenimiento(self, maintenance):
        maintenance.cancel()
        messagebox.showinfo(title='Editado con éxito', message='El mantenimiento ha sido modificado correctamente.')
        self.displayMaintenance(maintenance.id)

    def eliminarMantenimiento(self, maintenance):
        if messagebox.askyesno(title='Eliminar', message='¿En verdad desea eliminar el mantenimiento?'):
            maintenance.delete()
            messagebox.showinfo(title='Eliminado', message='El registro fue eliminado correctamente.')
            self.main()

    def displayMaintenance(self, id):
        global mainFrame
        global root
        mainFrame.destroy()
        mainFrame = Frame(root)
        mainFrame.config(bg="#ffffff",
        width=root.winfo_width(),
        height=root.winfo_height()-50)
        mainFrame.grid(column=0, row=1)

        sel = maintenances.Maintenance(id = id)

        Label(mainFrame, 
            text='Mantenimiento ID '+str(sel.id),
            bg="#ffffff",
            font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        self.info = Frame(mainFrame)
        self.info.config(bg="#ffffff", width=root.winfo_width()*0.2, height=root.winfo_height()-50)
        self.info.place(x=10, y=50)

        #Label fecha y estado de mantenimiento
        if sel.status == 'Programado': 
            text = ' para el '
        elif sel.status == 'Realizado': 
            text = ' el '
        else:
            text = ' el '
        Label(self.info, text=sel.status+text+sel.date.strftime('%d/%m/%Y'),fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=0)
        #Label responsable
        Label(self.info, text='Asignado a '+employers.buscar(sel.responsible)[2],fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=30)
        #Label Tipo de mantenimiento
        Label(self.info, text='Mantenimiento '+sel.type,fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=60)
        if sel.type == 'Preventivo':
            Label(self.info, text='Repetir cada '+str(sel.repeat)+' días',fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=90)
        #Label descripción mantenimiento
        Label(self.info, text=sel.description, bg="#ffffff", font=("Segoe UI", "10", "normal"), wraplength=root.winfo_width()*0.18, justify='left').place(x=0, y=120)
        #Edit Button
        if sel.type == maintenances.Preventive:
            Button(self.info, text='Editar', font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.editPreventiveWindow(sel)).place(x=0, y=root.winfo_height()-200)
        if sel.type == maintenances.Corrective:
            Button(self.info, text='Editar', font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.editCorrectiveWindow(sel)).place(x=0, y=root.winfo_height()-200)    
        #Boton realizar
        if sel.status == 'Programado':
            Button(self.info, text='Realizar', font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.realizarMantenimiento(id)).place(x=0, y=root.winfo_height()-150)
        #Boton Programar
        if sel.status == maintenances.Done and sel.next == None and sel.type == 'Preventivo':
            Button(self.info, text='Programar', font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.programar(id)).place(x=0, y=root.winfo_height()-150)
        #Boton cancelar
        if sel.status != maintenances.Cancelled:
            Button(self.info, text='Cancelar', font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.cancelarMantenimiento(sel)).place(x=70, y=root.winfo_height()-150)
        #Delete Button
        if sel.status == maintenances.Cancelled:
            Button(self.info, text='Eliminar', font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.eliminarMantenimiento(sel)).place(x=0, y=root.winfo_height()-150)
            
        #WorkOrder Button
        Button(self.info, text='Orden de trabajo', font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.maintenanceToWorkOrder(sel)).place(x=140, y=root.winfo_height()-150)

        if sel.type == maintenances.Preventive:
            listActivities = []            
            for activity in sel.activities:
                if len(listActivities) == 0:
                    listActivities.append([])
                    listActivities[0].append(activity)
                else:
                    grouped = False
                    for plant in listActivities:
                        if activity.plant.id == plant[0].plant.id:
                            listActivities[listActivities.index(plant)].append(activity)
                            grouped = True
                    if not grouped:
                        listActivities.append([])
                        listActivities[len(listActivities)-1].append(activity)

            for plant in listActivities:
                framePlant = Frame(mainFrame)
                framePlant.config(bg="#f2f2f2",
                    width=250,
                    height=root.winfo_height()-50)
                framePlant.place(x=root.winfo_width()*0.2+listActivities.index(plant)*250, y=0)
                thisPlant = plants.buscar(plant[0].plant.id)
                area = areas.Area(thisPlant[3])
                #Department
                Label(framePlant, text=area.department.name, fg='#666666', bg="#f2f2f2", font=("Segoe UI", "9", "normal")).place(x=10, y=10)
                #Area
                Label(framePlant, text=area.name, fg='#666666', bg="#f2f2f2", font=("Segoe UI", "9", "bold")).place(x=10+len(area.department.name*10), y=10)
                #Plant
                Label(framePlant, text=thisPlant[1], fg='#000000', bg="#f2f2f2", font=("Segoe UI", "10", "bold")).place(x=10, y=40)
                #Description
                Label(framePlant, text=thisPlant[2], fg='#000000', bg="#f2f2f2", font=("Segoe UI", "9", "normal"), wraplength=180, justify='left').place(x=10, y=70)
                for activity in plant:
                    #Label nombre actividad
                    Label(framePlant, text=activity.name, fg='#111111', bg="#f2f2f2", font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=110+plant.index(activity)*60)
                    #Label descripcion actividad
                    Label(framePlant, text=activity.description, fg='#111111', bg="#f2f2f2", font=("Segoe UI", "8", "normal"), wraplength=180, justify='left').place(x=10, y=130+plant.index(activity)*60)
        else:
            for plant in sel.plants:
                framePlant = Frame(mainFrame)
                framePlant.config(bg="#f2f2f2",
                    width=250,
                    height=root.winfo_height()-50)
                framePlant.place(x=root.winfo_width()*0.2+sel.plants.index(plant)*250, y=0)
                
                Label(framePlant, text=plant.department.name, fg='#666666', bg="#f2f2f2", font=("Segoe UI", "9", "normal")).place(x=10, y=10)
                Label(framePlant, text=plant.area.name, fg='#666666', bg="#f2f2f2", font=("Segoe UI", "9", "bold")).place(x=10+len(plant.department.name*10), y=10)
                Label(framePlant, text=plant.name, fg='#000000', bg="#f2f2f2", font=("Segoe UI", "10", "bold")).place(x=10, y=40)
                Label(framePlant, text=plant.description, fg='#000000', bg="#f2f2f2", font=("Segoe UI", "9", "normal"), wraplength=180, justify='left').place(x=10, y=70)
                
    def maintenanceToWorkOrder(self, maintenance):
        """_summary_

        Args:
            maintenance (_type_): _description_
        """
        workorder = workorders.WorkOrder()
        workorder.date = maintenance.date
        workorder.responsible = employers.Employer(id = maintenance.responsible)
        workorder.comment = maintenance.description
        workorder.maintenances.append(maintenance)
        workorder.save()
        f = asksaveasfile(initialfile=f"Orden de trabajo {workorder.id}.pdf", defaultextension='.pdf', filetypes=[('Portable Document File', '*.pdf'),])
        workorder.generatePDF(f.name)
        
    def statistics(self):
        global mainFrame
        clearMainFrame()
        
        #Tittle
        Label(mainFrame, text='Estadísticas de', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        Label(mainFrame, text='mantenimientos', bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=40)
        
        #InfoFrame
        info = Frame(mainFrame, width=600, height=500, bg=colorWhite)
        info.place(x=20, y=100)
        #Maintenances
        Label(info, text='Mantenimientos totales:', bg="#ffffff", font=("Segoe UI", "11", "bold")).grid(column=0, row=0, sticky='e')
        Label(info, text=str(sql.petition("SELECT COUNT(id) FROM mantenimientos")[0][0]), bg="#ffffff", font=("Segoe UI", "11", "normal")).grid(column=1, row=0, sticky='w')
        #Maintenances predictive
        Label(info, text='Mantenimientos preventivos:', bg="#ffffff", font=("Segoe UI", "11", "bold")).grid(column=0, row=1, sticky='e')
        Label(info, text=str(sql.petition("SELECT COUNT(id) FROM mantenimientos WHERE tipo='Preventivo'")[0][0]), bg="#ffffff", font=("Segoe UI", "11", "normal")).grid(column=1, row=1, sticky='w')
        #Corrective maintenances
        Label(info, text='Mantenimientos correctivos:', bg="#ffffff", font=("Segoe UI", "11", "bold")).grid(column=0, row=2, sticky='e')
        Label(info, text=str(sql.petition("SELECT COUNT(id) FROM mantenimientos WHERE tipo='Correctivo'")[0][0]), bg="#ffffff", font=("Segoe UI", "11", "normal")).grid(column=1, row=2, sticky='w')
        
        #Graphs
        graph = Frame(mainFrame, width=500, height=300)
        graph.place(x=20, y=200)
        fig = Figure(figsize=(5,4), dpi=100)
        plot1 = fig.add_subplot(211)
        rawData = sql.petition("SELECT strftime('%m',fecha) as month ,COUNT(id) as quantity FROM mantenimientos WHERE tipo='Correctivo' GROUP BY strftime('%Y',fecha), strftime('%m',fecha) ORDER BY fecha")
        plot1.set_title("Mantenimientos correctivos por mes")
        plot1.set_xlabel('Mes')
        plot1.set_ylabel('Mantenimientos')
        plot1.bar([row[0] for row in rawData],[row[1] for row in rawData], color='#93C2E4')
        
        plot2 = fig.add_subplot(212)
        rawData = sql.petition("SELECT strftime('%m',fecha) as month ,COUNT(id) as quantity FROM mantenimientos WHERE tipo='Preventivo' GROUP BY strftime('%Y',fecha), strftime('%m',fecha) ORDER BY fecha")
        plot2.set_title("Mantenimientos preventivos por mes")
        plot2.set_xlabel('Mes')
        plot2.set_ylabel('Mantenimientos')
        plot2.bar([row[0] for row in rawData],[row[1] for row in rawData], color='#93C2E4')
        fig.subplots_adjust(hspace=0.6)
        
        canvas = FigureCanvasTkAgg(fig, master=graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, graph)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

def createFunctionToDisplayEmployer(id, object):
    return lambda: object.parent.objetoEmpleados.displayEmployer(id)

class Empleados():
    
    def __init__(self, parent):
        global root
        global mainFrame   
        self.parent = parent    
        self.padre = parent
    
    def main(self):
        clearMainFrame()
        
        #Title
        Label(mainFrame, text='Empleados', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)
        
        employerList = employers.getAll() 
        
        Button(mainFrame, text='Nuevo',font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.newEmployerWindow).place(x=root.winfo_width()-100, y=35)
        
        employerFrame = ScrollableFrame(mainFrame, width=root.winfo_width()-40, height=root.winfo_height()-130, x=10, y=60)
        employerFrame.place(x=10, y=40)
        
        frameQuantity = int((root.winfo_width()-40)/300)
        frameSeparation = int(((root.winfo_width()-40)%300)/(frameQuantity*2))
        
        for employer in employerList:
            actualFrame = Frame(employerFrame.scrollableFrame)
            actualFrame.config(bg=colorGray, highlightthickness=0, width=300, height=200)
            actualFrame.grid(column=employerList.index(employer)%frameQuantity, row=int(employerList.index(employer)/frameQuantity), padx=frameSeparation, pady=10)
            
            #Name
            Label(actualFrame, text=employer.name, fg='#111111', bg=colorGray, font=("Segoe UI", "10", "bold"), wraplength=300, justify='left').place(x=20, y=20)
            
            #Key
            Label(actualFrame, text=employer.key, fg='#444444', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='left').place(x=20, y=40)
            
            #Pending maintenances
            pendingMaintenances = len(maintenances.findPendingMaintenances(employerId= employer.id))
            textColor= colorBlue
            Label(actualFrame, text=pendingMaintenances, fg=textColor, bg=colorGray, font=("Segoe UI", "16", "normal"), wraplength=300, justify='center').place(x=65, y=90, anchor=CENTER)
            Label(actualFrame, text='Mantenimientos\nprogramados', fg='#666666', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='center').place(x=65, y=120, anchor=CENTER)
            
            #Overdue maintenances
            overdueMaintenances = len(maintenances.findOverdueMaintenances(employerId= employer.id))
            if overdueMaintenances == 0: textColor = colorGreen
            elif overdueMaintenances < 3: textColor = colorBlue
            else: textColor = colorRed
            Label(actualFrame, text=overdueMaintenances, fg=textColor, bg=colorGray, font=("Segoe UI", "16", "normal"), wraplength=300, justify='center').place(x=215, y=90, anchor=CENTER)
            Label(actualFrame, text='Mantenimientos\natrasados', fg='#666666', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='center').place(x=215, y=120, anchor=CENTER)
            
            #Button
            Button(actualFrame, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=createFunctionToDisplayEmployer(employer.id, self)).place(x=230, y=160)
            
    def displayEmployer(self, id):
        clearMainFrame()
        
        employer = employers.Employer(id = id)
        
        #Button back
        Button(mainFrame, text=' ← Regresar ',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.main).place(x=20, y=10)
        
        #Edit
        Button(mainFrame, text='Estadísticas',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.statistics(employer)).place(x=root.winfo_width()-120, y=35)
        
        #Title
        Label(mainFrame, text='Empleado', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=40)
        Label(mainFrame, text='ID '+str(employer.id), bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=60)
        #Name
        Label(mainFrame, text='Nombre', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=105)
        Label(mainFrame, text=employer.name, bg='#ffffff', font=("Segoe UI", "11", "normal")).place(x=80, y=105)
        #Key
        Label(mainFrame, text='Clave', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=130)
        Label(mainFrame, text=str(employer.key), bg='#ffffff', font=("Segoe UI", "11", "normal")).place(x=60, y=130)
        
        #Areas
        Label(mainFrame, text='Areas', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=150)
        
        areasFrame = ScrollableFrame(mainFrame, x=10, y=180, width=(root.winfo_width()/2)-40, height=root.winfo_height()-280)
        areasFrame.place(x=10, y=180)
        
        areasList = areas.findByEmployerId(employer.id)
        for area in areasList:
            areaFrame = Frame(areasFrame.scrollableFrame)
            areaFrame.config(bg=colorGray, highlightthickness=0, width=(root.winfo_width()/2)-60, height=100)
            areaFrame.pack(padx=10, pady=10)
            
            #Department
            Label(areaFrame, text=area.department.name, fg='#666666', bg=colorGray, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=20, y=20)
            #Name
            Label(areaFrame, text=area.name, fg='#333333', bg=colorGray, font=("Segoe UI", "11", "bold"), wraplength=300, justify='left').place(x=20, y=50)
        
        #Maintenances
        Label(mainFrame, text='Mantenimientos programados', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=(root.winfo_width()/2)+10, y=150)
        
        maintenancesFrame = ScrollableFrame(mainFrame, x=(root.winfo_width()/2)+10, y=180, width=(root.winfo_width()/2)-40, height=root.winfo_height()-280)
        maintenancesFrame.place(x=(root.winfo_width()/2)+10, y=180)
        
        maintenancesList = maintenances.find(employerId=employer.id, status=maintenances.Programmed)
        for maintenance in maintenancesList:
            mant = Frame(maintenancesFrame.scrollableFrame)
            mant.config(bg=colorGray, highlightthickness=0, highlightbackground="#eeeeee", width=root.winfo_width()/2-100, height=100)
            mant.pack(pady=10, padx=15)
            if maintenance.date < datetime.now():
                actualColor = colorRed
            else:
                actualColor = colorGreen
            Frame(mant, bg=actualColor, height=100, width=3).place(x=0, y=0)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(maintenance.id), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=10)
            #Date
            Label(mant, text=maintenance.date.strftime('%d/%m/%Y'), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
            #Status
            if maintenance.status == 'Realizado' or maintenance.status == 'Realizado Programado':
                color = colorGreen
            elif maintenance.status == 'Programado':
                color = colorBlue
            elif maintenance.status == 'Cancelado':
                color = colorRed
            Label(mant, text=maintenance.status, fg=color, bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, anchor="e", width=20).place(x=root.winfo_width()/2-255, y=10)
            #type
            Label(mant, text='Matenimiento '+maintenance.type, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "bold")).place(x=140, y=30)
            #Descripción
            Label(mant, text=maintenance.description, fg='#333333', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=root.winfo_width()/2-190, justify='left').place(x=10, y=50)
            #Botón
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(maintenance.id, self)).place(x=root.winfo_width()/2-170, y=60)

    def statistics(self, employer):
        global mainFrame
        clearMainFrame()
        
        #Tittle
        Label(mainFrame, text='Estadísticas de', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        Label(mainFrame, text=employer.name, bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=40)
        
        #InfoFrame
        info = Frame(mainFrame, width=600, height=500, bg=colorWhite)
        info.place(x=20, y=100)
        #Maintenances
        Label(info, text='Mantenimientos totales:', bg="#ffffff", font=("Segoe UI", "11", "bold")).grid(column=0, row=0, sticky='e')
        Label(info, text=str(sql.petition(f"SELECT COUNT(id) FROM mantenimientos WHERE responsable = {employer.id}")[0][0]), bg="#ffffff", font=("Segoe UI", "11", "normal")).grid(column=1, row=0, sticky='w')
        #Maintenances predictive
        Label(info, text='Mantenimientos preventivos:', bg="#ffffff", font=("Segoe UI", "11", "bold")).grid(column=0, row=1, sticky='e')
        Label(info, text=str(sql.petition(f"SELECT COUNT(id) FROM mantenimientos WHERE tipo='Preventivo' AND responsable = {employer.id}")[0][0]), bg="#ffffff", font=("Segoe UI", "11", "normal")).grid(column=1, row=1, sticky='w')
        #Corrective maintenances
        Label(info, text='Mantenimientos correctivos:', bg="#ffffff", font=("Segoe UI", "11", "bold")).grid(column=0, row=2, sticky='e')
        Label(info, text=str(sql.petition(f"SELECT COUNT(id) FROM mantenimientos WHERE tipo='Correctivo' AND responsable = {employer.id}")[0][0]), bg="#ffffff", font=("Segoe UI", "11", "normal")).grid(column=1, row=2, sticky='w')
        
        #Graphs
        graph = Frame(mainFrame, width=500, height=300)
        graph.place(x=20, y=200)
        fig = Figure(figsize=(5,4), dpi=100)
        plot1 = fig.add_subplot(211)
        rawData = sql.petition(f"SELECT strftime('%m',fecha) as month ,COUNT(id) as quantity FROM mantenimientos WHERE tipo='Correctivo' AND responsable = {employer.id} GROUP BY strftime('%Y',fecha), strftime('%m',fecha) ORDER BY fecha")
        plot1.set_title("Mantenimientos correctivos por mes en 2022")
        plot1.set_xlabel('Mes')
        plot1.set_ylabel('Mantenimientos')
        plot1.bar([row[0] for row in rawData],[row[1] for row in rawData], color='#93C2E4')
        
        plot2 = fig.add_subplot(212)
        rawData = sql.petition(f"SELECT strftime('%m',fecha) as month ,COUNT(id) as quantity FROM mantenimientos WHERE strftime('%Y',fecha)='2022' AND tipo='Preventivo' AND responsable = {employer.id} GROUP BY strftime('%m',fecha)")
        plot2.set_title("Mantenimientos preventivos por mes en 2022")
        plot2.set_xlabel('Mes')
        plot2.set_ylabel('Mantenimientos')
        plot2.bar([row[0] for row in rawData],[row[1] for row in rawData], color='#93C2E4')
        fig.subplots_adjust(hspace=0.6)
        
        canvas = FigureCanvasTkAgg(fig, master=graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, graph)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def newEmployerWindow(self):
        global mainFrame
        clearMainFrame()
        
        Label(mainFrame, text='Empleado', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=26)
        Label(mainFrame, text='Nuevo', bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=50)
        
        #Var
        nameString = StringVar(mainFrame)
        keyString = StringVar(mainFrame)
        
        #Save
        Button(mainFrame, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveEmployer(nameString, keyString)).place(x=root.winfo_width()-100, y=35)
        
        #Name
        Label(mainFrame, text='Nombre',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=40, y=200)
        Entry(mainFrame, width=20, textvariable=nameString, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=40, y=230)
        
        #Key
        Label(mainFrame, text='Código',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=40, y=300)
        Entry(mainFrame, width=20, textvariable=keyString, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=40, y=330)
        
        
    def saveEmployer(self, name, key):
        """_summary_

        Args:
            name (stringVar): _description_
            key (stringVar): _description_
        """
        newEmployer = employers.Employer()
        newEmployer.name = name.get()
        newEmployer.key = int(key.get())
        newEmployer.save()
        self.displayEmployer(newEmployer.id)

def func_displayRequisition(id, object):
    return lambda event: object.parent.inventory.displayRequisition(id)

def func_displayProduct(id, object):
    return lambda event: object.parent.inventory.displayProduct(id)

def func_removeProductFromRequisition(id, object):
    return lambda: object.parent.inventory.removeProductFromRequisition(id)

class Inventory():
    
    def __init__(self, parent) -> None:
        global root
        self.parent = parent
        
    def inventoryMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        Label(mainFrame, text='Inventario', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)
        productsList = inventory.getProducts()
        
        #Var
        self.searchString = StringVar(mainFrame)
        
        #Search
        search = Frame(mainFrame)
        search.config(bg='#ECECEC', width=(root.winfo_width()/2)-40, height=30)
        search.place(x=200 , y=10)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=95, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#ECECEC', highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventoryFrame)
        
        self.productsFrame = ScrollableFrame(mainFrame, x=10, y=60, width=root.winfo_width()-40, height=root.winfo_height()-120)
        self.productsFrame.place(x=0, y=0)
        
        self.insertProducts(productsList)
            
    def updateInventoryFrame(self, event):
        productsList = inventory.findByName(self.searchString.get())
        self.productsFrame.clear()
        self.insertProducts(productsList)
            
    def insertProducts(self, productsList):
        itemX = int((root.winfo_width()-40)/300)
        itemSeparation = ((root.winfo_width()-40)-(300*itemX))/(itemX+4)
        for product in productsList:
            productNumber = productsList.index(product)
            frame = Frame(self.productsFrame.scrollableFrame)
            frame.config(width=300, height=200, bg=colorGray)
            frame.bind('<Button-1>', func_displayProduct(product.id, self))
            frame.grid(column=productNumber%itemX, row=int(productNumber/itemX), pady=itemSeparation, padx=itemSeparation)
            title = Label(frame, text=product.name, bg=colorGray, fg='#444444',font=("Segoe UI", "10", "bold"), wraplength=180, justify=LEFT)
            title.place(x=10, y=10)
            description = Label(frame, text=product.description, bg=colorGray, fg='#666666', font=("Segoe UI", "9", "normal"), wraplength=180, justify=LEFT)
            description.place(x=10, y=50)
            Label(frame, text=(product.brand if product.brand != None else '')+(' - '+product.model if product.model != None else ''), bg=colorGray,fg='#555555', font=("Segoe UI", "9", "normal"), wraplength=180, justify=LEFT).place(x=10, y=100)
            Label(frame, text=str(product.quantity)+ ' disponible', bg=colorGray,fg=colorRed if product.quantity==0 else colorGreen, font=("Segoe UI", "10", "normal")).place(x=10, y=200-30)
            
    def displayProduct(self, id):
        global mainFrame
        clearMainFrame()
        product = inventory.Product(id = id)
        
        #Tittle
        Label(mainFrame, text='Producto', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        Label(mainFrame, text='ID '+str(product.id), bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=40)
        #Name
        Label(mainFrame, text='Nombre', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=85)
        Label(mainFrame, text=product.name, bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=90, y=85)
        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=110)
        Label(mainFrame, text=product.description, bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=105, y=110)
        #Quantity
        Label(mainFrame, text='Cantidad disponible', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=135)
        Label(mainFrame, text=str(product.quantity), bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=170, y=135)
        #Delivering Time
        Label(mainFrame, text='Tiempo de entrega', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=160)
        Label(mainFrame, text=str(product.deliveringTime().days)+' días', bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=168, y=160)
        #Delivering Time
        Label(mainFrame, text='Tiempo estimado para agotarse', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=250, y=160)
        Label(mainFrame, text=str(product.calculateOutputs().days*product.quantity)+' días', bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=480, y=160)
        #Graph
        Button(mainFrame, text='Graficar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=product.graphMovements).place(x=840, y=35)
        #In
        Button(mainFrame, text='Entrada',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.newInputInventory(product)).place(x=900, y=35)
        #Out
        if product.quantity > 0:    
            Button(mainFrame, text='Salida',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.newOutputInventory(product)).place(x=960, y=35)
            
        #Movements
        Label(mainFrame, text='Movimientos de inventario',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=200)
        
        movementsFrame = ScrollableFrame(mainFrame, width=root.winfo_width()-60, height=root.winfo_height()-300, x=20, y=230)
        movementsFrame.place(x=20, y=230)
        
        for mov in product.movements:
            movNumber = product.movements.index(mov)
            backColor = colorGray if movNumber%2==0 else colorWhite
            productFrame = Frame(movementsFrame.scrollableFrame)
            productFrame.config(bg=backColor, highlightthickness=0, width=root.winfo_width()-80, height=70)
            productFrame.pack(pady=1)
            #Type
            Label(productFrame, image=imgIn if mov.type == inventory.INPUT else imgOut, bd=0, width=40, height=40, bg=backColor).place(x=15, y=15)
            #Date
            Label(productFrame, text=datetime.date(mov.date).strftime('%d/%m/%Y'), fg='#000000', bg=backColor, font=("Segoe UI", "10", "normal")).place(x=65, y=10)
            #Quantity
            Label(productFrame, text='Cantidad: '+str(mov.quantity), fg='#000000', bg=backColor, font=("Segoe UI", "10", "normal")).place(x=65, y=35)
            #Origin
            Label(productFrame, text=(mov.origin+' '+str(mov.origin_id)) if mov.origin != None else 'Movimiento del usuario', fg='#4d4d4d', bg=backColor, font=("Segoe UI", "9", "normal")).place(x=200, y=10)
            #Comment
            Label(productFrame, text=mov.comment, fg='#4d4d4d', bg=backColor, font=("Segoe UI", "9", "normal"), wraplength=600, justify=LEFT).place(x=200, y=35)
            
            
    def newInputInventory(self, product):
        self.window = Toplevel()
        self.window.title('Registrar entrada')
        
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=400, height=500)
        mainframe.pack()
        
        #Var
        inputQuantity = IntVar(mainframe)
        inputComment = StringVar(mainframe)
        inputOrigin = StringVar(mainframe)
        inputOriginId = IntVar(mainframe)
        
        #Tittle
        Label(mainframe, text='Registrar entrada', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        
        #Quantity
        Label(mainframe, text='Cantidad',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=70)
        Entry(mainframe, width=50, textvariable=inputQuantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=100)
        
        #Description
        Label(mainframe, text='Comentario',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=140)
        Entry(mainframe, width=50, textvariable=inputComment, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=170)
        
        #Origin
        Label(mainframe, text='Origen',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=210)
        Entry(mainframe, width=50, textvariable=inputOrigin, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=240)
        
        #Model
        Label(mainframe, text='Id de origen',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=280)
        Entry(mainframe, width=50, textvariable=inputOriginId, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=310)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveInputInventory(product, inputQuantity.get(), inputComment.get(), inputOrigin.get(), inputOriginId.get())).place(x=20, y=380)
        
    def saveInputInventory(self, product, quantity, comment, origin, originId):
        product.addMovement(datetime.now(),inventory.INPUT, quantity, comment, origin if origin != '' else None, originId if origin != '' else None)
        self.window.destroy()
        self.displayProduct(product.id)
    
    def newOutputInventory(self, product):
        self.window = Toplevel()
        self.window.title('Registrar salida')
        
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=400, height=600)
        mainframe.pack()
        
        #Var
        outputQuantity = IntVar(mainframe)
        outputComment = StringVar(mainframe)
        outputOrigin = StringVar(mainframe)
        outputOriginId = IntVar(mainframe)
        
        #Tittle
        Label(mainframe, text='Registrar salida', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        
        #Date
        Label(mainframe, text='Fecha', fg="#777777",  bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=60)
        today = datetime.now()
        cal = Calendar(mainframe, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        cal.place(x=20, y=90)
        
        #Quantity
        Label(mainframe, text='Cantidad',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=270)
        Entry(mainframe, width=50, textvariable=outputQuantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=300)
        
        #Description
        Label(mainframe, text='Comentario',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=330)
        Entry(mainframe, width=50, textvariable=outputComment, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=360)
        
        #Origin
        Label(mainframe, text='Origen',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=390)
        Entry(mainframe, width=50, textvariable=outputOrigin, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=420)
        
        #IDOrigin
        Label(mainframe, text='Id de origen',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=450)
        Entry(mainframe, width=50, textvariable=outputOriginId, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=480)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveOutputInventory(product, outputQuantity.get(), datetime.combine(cal.selection_get(), datetime.min.time()), outputComment.get(), outputOrigin.get(), outputOriginId.get())).place(x=20, y=550)
    
    def saveOutputInventory(self, product, quantity, date, comment, origin, originId):
        product.addMovement(date, inventory.OUTPUT, quantity, comment, origin if origin != '' else None, originId if origin != '' else None)
        self.window.destroy()
        self.displayProduct(product.id)
        
    def requisitionsMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        Label(mainFrame, text='Requisiciones', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)
        requisitionsList = inventory.getRequisitions(quantity=40, order='date')
        
        #New
        Button(mainFrame, text='Nueva',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.newRequisition).place(x=root.winfo_width()-100, y=20)
        
        requisitionsFrame = ScrollableFrame(mainFrame, x=10, y=60, width=root.winfo_width()-40, height=root.winfo_height()-120)
        requisitionsFrame.place(x=0, y=0)
        
        Label(mainFrame, text='Id', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=20, y=40)
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=90, y=40)
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=270, y=40)
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=370, y=40)
        
        for req in requisitionsList:
            reqNumber = requisitionsList.index(req)
            backColor = colorGray if reqNumber%2==0 else colorWhite
            frame = Frame(requisitionsFrame.scrollableFrame)
            frame.config(width=root.winfo_width()-80, height=30, bg=backColor)
            frame.bind('<Button-1>', func_displayRequisition(req.id, self))
            frame.pack(pady=1)
            Label(frame, text=req.id, bg=backColor, font=("Segoe UI", "10", "normal")).place(x=10, y=4)
            Label(frame, text=datetime.date(req.date).strftime("%d %B %Y"), bg=backColor, font=("Segoe UI", "10", "normal")).place(x=80, y=4)
            Label(frame, text=req.status.capitalize(), bg=backColor, font=("Segoe UI", "10", "normal")).place(x=260, y=4)
            Label(frame, text=req.description, bg=backColor, font=("Segoe UI", "10", "normal")).place(x=360, y=4)
    
    def displayRequisition(self, id):
        global mainFrame
        clearMainFrame()
        req = inventory.Requisition(id = id)
        
        #Tittle
        Label(mainFrame, text='Requisición', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        Label(mainFrame, text='ID '+str(req.id), bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=40)
        #Status
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=85)
        Label(mainFrame, text=req.status.capitalize(), bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=75, y=85)
        #Created date
        Label(mainFrame, text='Fecha de creación', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=110)
        Label(mainFrame, text=datetime.date(req.date).strftime("%d / %b /  %Y"), bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=155, y=110)
        #Delivered date
        Label(mainFrame, text='Fecha de recepción', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=285, y=110)
        Label(mainFrame, text=datetime.date(req.deliveredDate).strftime("%d / %b /  %Y") if req.deliveredDate != None else 'Sin fecha', bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=425, y=110)
        #Description
        Label(mainFrame, text='Comentario', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=135)
        Label(mainFrame, text=req.description, bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=110, y=135)
        
        #Edit
        Button(mainFrame, text='Editar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.newRequisition(req)).place(x=880, y=35)
        
        #Save
        Button(mainFrame, text='Guardar en PDF',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveRequisitionPDF(req)).place(x=934, y=35)
        
        #Make requested
        if req.status == inventory.STATUS_DRAFT:    
            Button(mainFrame, text='Marcar solicitada',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.changeStatus(req, inventory.STATUS_REQUESTED)).place(x=1050, y=35)
            
        #Make confirmed
        if req.status == inventory.STATUS_REQUESTED:    
            Button(mainFrame, text='Marcar confirmada',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.changeStatus(req, inventory.STATUS_CONFIRMED)).place(x=1050, y=35)
            
        #Make delivered
        if req.status == inventory.STATUS_CONFIRMED:    
            Button(mainFrame, text='Marcar entregada',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.purchaseDelivered(req)).place(x=1050, y=35)    
        
        #Delete button
        Button(mainFrame, text='Eliminar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.deleteRequisition(req)).place(x=1200, y=35)
            
        #Products
        Label(mainFrame, text='Descripción',fg="#000000", bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=30, y=200)
        Label(mainFrame, text='Cantidad pedidos',fg="#000000", bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=1000, y=200)
        Label(mainFrame, text='Cantidad entregados',fg="#000000", bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=1150, y=200)
        
        self.productsFrame = ScrollableFrame(mainFrame, width=root.winfo_width()-60, height=root.winfo_height()-300, x=20, y=230)
        self.productsFrame.place(x=20, y=230)
        
        for product in req.products:
            productNumber = req.products.index(product)
            backColor = colorGray if productNumber%2==0 else colorWhite
            productFrame = Frame(self.productsFrame.scrollableFrame)
            productFrame.config(bg=backColor, highlightthickness=0, width=root.winfo_width()-80, height=70 if product.comment != None else 40)
            productFrame.pack(pady=1)
            #Description
            name = Label(productFrame, text=product.product.name, fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=450, justify='left')
            name.place(x=10, y=10)
            name.update()
            Label(productFrame, text=str(product.quantity), fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=300, justify='center').place(x=1030, y=10)
            Label(productFrame, text=str(product.deliveredQuantity), fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=300, justify='center').place(x=1180, y=10)
            Label(productFrame, text=product.comment, fg='#4d4d4d', bg=backColor, font=("Segoe UI", "9", "normal"), wraplength=1000, justify='left').place(x=10, y=35)
            productFrame.update()
            
    def changeStatus(self, requisition, status):
        requisition.changeStatus(status)
        self.displayRequisition(requisition.id)
        
    def deleteRequisition(self, requisition):
        if messagebox.askyesno(title='¿Eliminar la requisición?', message=f"¿Desea eliminar la requisición con ID {requisition.id}?"):
            requisition.delete()
            messagebox.showinfo(title='Requisición eliminada', message=f"La requisición ha sido eliminada correctamente")
        self.requisitionsMainWindow()
        
    def saveRequisitionPDF(self, requisition):
        f = asksaveasfile(initialfile=f"Requisicion {requisition.id}.pdf", defaultextension='.pdf', filetypes=[('Portable Document File', '*.pdf'),])
        requisition.generatePDF(f.name)
        
    def purchaseDelivered(self, requisition):
        self.window = Toplevel()
        self.window.title('Procesar entrega')
        
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=800, height=500)
        mainframe.pack()
        
        #Var
        
        #Tittle
        Label(mainframe, text='Procesar entrega', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        
        Label(mainframe, text='Nombre', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=20, y=50)
        Label(mainframe, text='Solicitados', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=580, y=50)
        Label(mainframe, text='Entregados', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=670, y=50)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command= lambda: self.processPurchase(requisition, detailsList)).place(x=720, y=20)
        
        self.productsFrame = ScrollableFrame(mainframe, width=760, height=400, x=10, y=80)
        self.productsFrame.place(x=10, y=80)
        
        detailsList = []
        for detail in requisition.products:
            productFrame = Frame(self.productsFrame.scrollableFrame)
            productFrame.config(bg=colorGray, highlightthickness=0, width=740, height=50)
            productFrame.pack(pady=5, padx=5)
            Label(productFrame, text=detail.product.name, fg='#000000', bg=colorGray, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=10, y=10)
            Label(productFrame, text=detail.quantity, fg='#000000', bg=colorGray, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=570, y=10)
            quantity = IntVar(mainframe)
            Entry(productFrame, textvariable=quantity, width=5, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=660, y=10)
            detailsList.append([detail, quantity])
        
    def processPurchase(self, requisition, detailsList):
        for detail in detailsList:
            detail[0].deliveredQuantity = detail[1].get()
            detail[0].status = inventory.STATUS_DELIVERED
            detail[0].deliveredDate = datetime.now()
            detail[0].save()
            detail[0].product.addMovement(datetime.now(), inventory.INPUT, detail[1].get(), detail[0].comment, inventory.REQUISITION, requisition.id)
        requisition.deliveredDate = datetime.now()
        self.changeStatus(requisition, inventory.STATUS_DELIVERED)
        self.window.destroy()
        self.displayRequisition(requisition.id)
        
    def new(self):
        self.window = Toplevel()
        self.window.title('Crear producto')
        
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=400, height=500)
        mainframe.pack()
        
        #Var
        productName = StringVar(mainframe)
        productDescription = StringVar(mainframe)
        productBrand = StringVar(mainframe)
        productModel = StringVar(mainframe)
        
        #Tittle
        Label(mainframe, text='Nuevo producto', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        
        #Name
        Label(mainframe, text='Nombre',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=70)
        Entry(mainframe, width=50, textvariable=productName, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=100)
        
        #Description
        Label(mainframe, text='Descripción',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=140)
        Entry(mainframe, width=50, textvariable=productDescription, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=170)
        
        #Brand
        Label(mainframe, text='Marca',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=210)
        Entry(mainframe, width=50, textvariable=productBrand, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=240)
        
        #Model
        Label(mainframe, text='Modelo/no. de pieza',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=280)
        Entry(mainframe, width=50, textvariable=productModel, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=310)
        
        #Categories
        Label(mainframe, text='Categoría',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=350)
        categories = inventory.getCategories()
        category = ttk.Combobox(mainframe, values = categories, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, width=47, state="readonly")
        category.place(x=20, y=380)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveProduct(productName.get(), productDescription.get(), productBrand.get(), productModel.get(), categories[category.current()])).place(x=20, y=440)
        
    def saveProduct(self, name, description, brand, model, category):
        newProduct = inventory.Product()
        newProduct.name = name
        newProduct.description = description
        newProduct.brand = brand
        newProduct.model = model
        newProduct.category = category
        newProduct.save()
        try:
            self.window.destroy()
        except:
            pass
        finally:
            messagebox.showinfo(title='Producto registrado', message='El producto se ha registrado correctamente.')
            self.displayProduct(newProduct.id)
        return True
    
    def newCategory(self):
        self.window = Toplevel()
        self.window.title('Crear categoría')
        
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=300, height=200)
        mainframe.pack()
        
        #Var
        categoryName = StringVar(mainframe)
        
        #Tittle
        Label(mainframe, text='Nueva categoría', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        
        #Name
        Label(mainframe, text='Nombre',fg="#777777", bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=70)
        Entry(mainframe, width=37, textvariable=categoryName, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=100)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveCategory(categoryName.get())).place(x=20, y=140)
        
    def saveCategory(self, name):
        newCategory = inventory.Category()
        newCategory.name = name
        newCategory.save()
        try:
            self.window.destroy()
        except:
            pass
        finally:
            messagebox.showinfo(title='Categoría registrada', message='La categoría se ha registrado correctamente.')
        return True
    
    def newRequisition(self, requisition = None):
        self.window = Toplevel()
        self.window.state('zoomed')
        self.window.title('Requisición nueva' if requisition == None else 'Editar requisición')
        
        self.window.update()
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=self.window.winfo_width(), height=self.window.winfo_height())
        mainframe.pack()
        
        #Var
        self.searchString = StringVar(mainframe)
        descriptionString = StringVar(mainframe)
        self.quantity = StringVar(mainframe)
        
        if requisition == None:
            self.requisition = inventory.Requisition()
            self.requisition.date = datetime.now()
            self.requisition.status = inventory.STATUS_DRAFT
        else:
            self.requisition = requisition
        
        #Tittle
        Label(mainframe, text='Requisición', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=26)
        Label(mainframe, text='Nueva' if requisition == None else 'ID '+str(self.requisition.id), bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=50)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.saveRequisition).place(x=root.winfo_width()-100, y=35)
        
        #Search
        search = Frame(mainframe)
        search.config(bg='#ECECEC', width=(root.winfo_width()/2)-40, height=30)
        search.place(x=20 , y=100)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=95, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#ECECEC', highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventorySearch)
        
        #Products table
        tableWidth = int(((root.winfo_width()/2)-40)/4)
        self.productsTable = crearTabla(['Nombre', 'Descripción', 'Marca', 'Modelo'], [1,], [tableWidth,tableWidth,tableWidth,tableWidth], [['','','',''],], mainframe, 4, '' )
        self.productsTable.place(x=20, y=140)
        
        #Coment
        Label(mainframe, text='Comentario',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=20, y=270)
        self.comment = Text(mainframe, width=int(((root.winfo_width()/2)-40)/7), font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=20, y=296)
        
        #Quantity
        Label(mainframe, text='Cantidad',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=20, y=370)
        Entry(mainframe, width=20, textvariable=self.quantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=20, y=392)
        
        #Add product
        Button(mainframe, text='+ Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.addProductToRequisition).place(x=300, y=392)
        
        #Products
        Label(mainframe, text='Productos',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=root.winfo_width()/2, y=100)
        
        self.productsFrame = ScrollableFrame(mainframe, width=int(root.winfo_width()/2-40), height=300, x=root.winfo_width()/2, y=130)
        self.productsFrame.place(x=root.winfo_width()/2, y=130)
        
        #Requisition Comment
        Label(mainframe, text='Comentario',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=20, y=450)
        self.requisitionComment = Text(mainframe, width=int(((root.winfo_width())-40)/7), font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=6)
        self.requisitionComment.place(x=20, y=480)
        
        if requisition != None:
            self.updateProductsFrame()
            self.requisitionComment.insert(INSERT, self.requisition.description)
                
    def updateInventorySearch(self, event):
        productsList = inventory.findByName(self.searchString.get())
        self.productsTable.delete(*self.productsTable.get_children())
        for product in productsList:
            self.productsTable.insert('', 0, id=product.id, text=product.name, values=(product.description, product.brand, product.model))
            
    def addProductToRequisition(self):
        if self.comment.get('1.0',END) == '':
            self.requisition.addProduct(self.productsTable.focus(), self.quantity.get(),None)
        else:
            self.requisition.addProduct(self.productsTable.focus(), self.quantity.get(),self.comment.get('1.0',END))
        self.quantity.set('')
        self.comment.delete("1.0", END)
        self.updateProductsFrame()
        
    def removeProductFromRequisition(self, product):        
        self.requisition.products.pop(self.requisition.products.index(product))
        self.updateProductsFrame()
        
    def updateProductsFrame(self):
        self.productsFrame.clear()
        for product in self.requisition.products:
            productFrame = Frame(self.productsFrame.scrollableFrame)
            productFrame.config(bg=colorGray, highlightthickness=0, width=600, height=70)
            productFrame.pack(pady=5, padx=5)
            #Plant
            name = Label(productFrame, text=product.product.name, fg='#000000', bg=colorGray, font=("Segoe UI", "11", "normal"), wraplength=300, justify='left')
            name.place(x=10, y=10)
            name.update()
            Label(productFrame, text='Cantidad: '+str(product.quantity), fg=colorBlue, bg=colorGray, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=name.winfo_width()+15, y=10)
            Label(productFrame, text=product.comment, fg='#4d4d4d', bg=colorGray, font=("Segoe UI", "9", "normal"), wraplength=600, justify='left').place(x=10, y=35)
            productFrame.update()
            Button(productFrame, text=' X ',font=("Segoe UI", "9", "bold"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=1, relief=FLAT, command= func_removeProductFromRequisition(product, self)).place(x=productFrame.winfo_width()-35, y=10)
    
    def saveRequisition(self):
        self.requisition.description = self.requisitionComment.get('1.0', END)
        if self.requisition.status == inventory.STATUS_DRAFT:
            self.requisition.date = datetime.now()
        self.requisition.save()
        messagebox.showinfo(title='Requisición guardada', message=f"La requisición ha sido guardada con el ID {self.requisition.id}")
        self.window.destroy()
        self.displayRequisition(self.requisition.id)
 
def func_displayWorkOrder(id, object):
    return lambda event: object.parent.workorders.displayWorkOrder(id) 
        
class WorkOrders:
    
    def __init__(self, crm) -> None:
        global root
        self.parent = crm
    
    def mainWindow(self):
        global mainFrame
        clearMainFrame()
        
        Label(mainFrame, text='Ordenes de trabajo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)
        workOrdersList = workorders.getAll(orderby='date', order='DESC')
        
        #New
        Button(mainFrame, text='Nueva',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.newWorkOrder).place(x=root.winfo_width()-100, y=20)
        
        workordersFrame = ScrollableFrame(mainFrame, x=10, y=60, width=root.winfo_width()-40, height=root.winfo_height()-120)
        workordersFrame.place(x=0, y=0)
        
        Label(mainFrame, text='Id', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=20, y=40)
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=90, y=40)
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=270, y=40)
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "bold")).place(x=370, y=40)
        
        for work in workOrdersList:
            reqNumber = workOrdersList.index(work)
            backColor = colorGray if reqNumber%2==0 else colorWhite
            frame = Frame(workordersFrame.scrollableFrame)
            frame.config(width=root.winfo_width()-80, height=30, bg=backColor)
            frame.bind('<Button-1>', func_displayWorkOrder(work.id, self))
            frame.pack(pady=1)
            Label(frame, text=work.id, bg=backColor, font=("Segoe UI", "10", "normal")).place(x=10, y=4)
            Label(frame, text=datetime.date(work.date).strftime("%d %B %Y"), bg=backColor, font=("Segoe UI", "10", "normal")).place(x=80, y=4)
            Label(frame, text=workorders.LANGUAGE[work.status].capitalize(), bg=backColor, font=("Segoe UI", "10", "normal")).place(x=260, y=4)
            Label(frame, text=work.comment, bg=backColor, font=("Segoe UI", "10", "normal")).place(x=360, y=4)
    
    def displayWorkOrder(self, id):
        global mainFrame
        clearMainFrame()
        workorder = workorders.WorkOrder(id = id)
        
        #Tittle
        Label(mainFrame, text='Orden de trabajo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        Label(mainFrame, text='ID '+str(workorder.id), bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=40)
        Label(mainFrame, text=workorders.LANGUAGE[workorder.status].capitalize(), bg="#ffffff", font=("Segoe UI", "16", "normal")).place(x=20, y=80)
        Label(mainFrame, text=datetime.date(workorder.date).strftime("%d / %b /  %Y"), bg="#ffffff", font=("Segoe UI", "14", "normal")).place(x=20, y=120)
        Label(mainFrame, text='Asignada a '+workorder.responsible.name, bg="#ffffff", font=("Segoe UI", "12", "normal")).place(x=200, y=120)
        
        #Save
        Button(mainFrame, text='Guardar en PDF',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveWorkOrderPDF(workorder)).place(x=934, y=35)
        
        #Description
        Label(mainFrame, text=workorder.comment, bg="#ffffff", font=("Segoe UI", "12", "normal")).place(x=20, y=160)
        
        #Make confirmed
        if workorder.status == workorders.STATUS_DRAFT:    
            Button(mainFrame, text='Confirmar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.changeStatus(workorder, workorders.STATUS_CONFIRMED)).place(x=1050, y=35)
            
        #Make in progress
        if workorder.status == workorders.STATUS_CONFIRMED:    
            Button(mainFrame, text='Comenzar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.changeStatus(workorder, workorders.STATUS_IN_PROGRESS)).place(x=1050, y=35)
            
        #Make delivered
        if workorder.status == workorders.STATUS_IN_PROGRESS:    
            Button(mainFrame, text='Terminar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.changeStatus(workorder, workorders.STATUS_DONE)).place(x=1050, y=35)    
        
        #Delete button
        Button(mainFrame, text='Eliminar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.deleteWorkOrder(workorder)).place(x=1200, y=35)
        
        #Activities
        Label(mainFrame, text='Actividades',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=200)
        
        self.activitiesFrame = ScrollableFrame(mainFrame, width=root.winfo_width()-60, height=root.winfo_height()-300, x=20, y=230)
        self.activitiesFrame.place(x=20, y=230)
        
        for maintenance in workorder.maintenances:
            backColor = colorGray
            maintFrame = Frame(self.activitiesFrame.scrollableFrame)
            maintFrame.config(bg=backColor, highlightthickness=0, width=root.winfo_width()-80)
            
            titleFrame = Frame(maintFrame)
            titleFrame.config(bg=backColor, highlightthickness=0, width=root.winfo_width()-80, height=75)
            #Plant
            name = Label(titleFrame, text='Mantenimiento no. '+str(maintenance.id), fg='#000000', bg=backColor, font=("Segoe UI", "11", "bold"), wraplength=300, justify='left')
            name.place(x=10, y=10)
            name.update()
            Label(titleFrame, text='Mantenimiento '+str(maintenance.type), fg=colorBlue, bg=backColor, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=name.winfo_width()+15, y=11)
            Label(titleFrame, text=maintenance.description, fg='#4d4d4d', bg=backColor, font=("Segoe UI", "9", "normal"), wraplength=1000, justify='left').place(x=10, y=35)
            titleFrame.pack(pady=1)
            detailFrame = Frame(maintFrame)
            detailFrame.config(bg=colorWhite, highlightthickness=0, width=root.winfo_width()-100)
            if maintenance.type == maintenances.Corrective:
                for plant in maintenance.plants:
                    plantFrame = Frame(detailFrame)
                    plantFrame.config(bg=colorWhite, highlightthickness=0, width=root.winfo_width()-80, height=70)
                    Label(plantFrame, text=plant.department.name + ' - '+ plant.area.name +' - '+ plant.name, fg='#000000', bg=colorWhite, font=("Segoe UI", "10", "bold"), wraplength=300, justify='left').place(x=10, y=10)
                    plantFrame.pack(pady=1)
                    Label(plantFrame, text=plant.description, fg='#000000', bg=colorWhite, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=10, y=30)
                    plantFrame.pack(pady=1)
            else:
                for plant in maintenance.plants:
                    plantFrame = Frame(detailFrame)
                    plantFrame.config(bg=colorWhite, highlightthickness=0, width=root.winfo_width()-80, height=60)
                    Label(plantFrame, text=plant.department.name + ' - '+ plant.area.name +' - '+ plant.name, fg='#000000', bg=colorWhite, font=("Segoe UI", "10", "bold"), wraplength=300, justify='left').place(x=10, y=0)
                    Label(plantFrame, text=plant.description, fg='#000000', bg=colorWhite, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=10, y=20)
                    plantFrame.pack(pady=1)
                    actFrame = Frame(detailFrame)
                    actFrame.config(bg=colorWhite, highlightthickness=0, width=root.winfo_width()-80)
                    for activity in plant.activities:
                        activityFrame = Frame(actFrame)
                        activityFrame.config(bg=colorWhite, highlightthickness=0, width=root.winfo_width()-80, height=60)
                        Label(activityFrame, text=activity.name, fg='#000000', bg=colorWhite, font=("Segoe UI", "10", "bold"), wraplength=300, justify='left').place(x=40, y=0)
                        Label(activityFrame, text=activity.description, fg='#000000', bg=colorWhite, font=("Segoe UI", "10", "normal"), wraplength=300, justify='left').place(x=40, y=20)
                        activityFrame.pack(pady=1)
                    actFrame.pack(pady=1)
            detailFrame.pack(pady=1)
            maintFrame.pack(pady=1)
    
    def saveWorkOrderPDF(self, workorder):
        f = asksaveasfile(initialfile=f"Orden de trabajo {workorder.id}.pdf", defaultextension='.pdf', filetypes=[('Portable Document File', '*.pdf'),])
        workorder.generatePDF(f.name)
    
    def changeStatus(self, workorder, status):
        workorder.status = status
        workorder.save()
        if status == workorders.STATUS_DONE:
            for maint in workorder.maintenances:
                maint.status = maintenances.Done
                maint.date = datetime.now()
                maint.save()
                if maint.type == maintenances.Preventive:
                    if messagebox.askyesno(title='¿Programas siguiente mantenimiento?', message=f"¿Desea programar el siguiente mantenimiento preventivo con ID {maint.id}?"):
                        maint.scheduleNext()
        self.displayWorkOrder(workorder.id)
        
    def deleteWorkOrder(self, workorder):
        if messagebox.askyesno(title='¿Eliminar la orden de trabajo?', message=f"¿Desea eliminar la orden de trabajo con ID {workorder.id}?"):
            workorder.delete()
            messagebox.showinfo(title='Orden de trabajo eliminada', message=f"La orden de trabajo ha sido eliminada correctamente")
        self.mainWindow()
    
    def newWorkOrder(self):
        self.window = Toplevel()
        self.window.state('zoomed')
        self.window.title('Orden de trabajo nueva')
        self.window.update()
        mainframe = Frame(self.window)
        mainframe.config(bg=colorWhite, width=self.window.winfo_width(), height=self.window.winfo_height())
        mainframe.pack()
        
        #Var
        workorder = workorders.WorkOrder()
        
        #Title
        Label(mainframe, text='Orden de trabajo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=20, y=20)
        Label(mainframe, text='Nueva', bg="#ffffff", font=("Segoe UI", "18", "bold")).place(x=20, y=40)
        
        #Save
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveWorkOrder(workorder)).place(x=root.winfo_width()-100, y=35)
        
        #Date
        Label(mainframe, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=100)
        today = datetime.now()
        self.cal = Calendar(mainframe, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=20, y=130)
        
        #Responsible
        Label(mainframe, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=20, y=340)
        self.responsible = ttk.Combobox(mainframe, state = 'readonly', values = employers.ver('nombre'), foreground="#222222", background=colorGray)
        self.responsible.place(x=20, y=370)
        
        #Comment
        Label(mainframe, text='Comentario',fg="#000000", bg="#ffffff", font=("Segoe UI", "11", "normal")).place(x=20, y=410)
        self.comment = Text(mainframe, width=43, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=20, y=440)
        
        #Maintenances table
        self.productsTable = crearTabla(['Fecha', 'Descripción'], [1,], [100,500], [['',''],], mainframe, 8, '' )
        self.productsTable.place(x=400, y=100)
        for maintenance in maintenances.getMaintenancesToWorkOrders():
            self.productsTable.insert('', 0, id=maintenance.id, text=maintenance.date.strftime('%d/%m/%Y'), values=(maintenance.description,))
            
        #Add
        Button(mainframe, text='Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.addMaintenanceToWorkOrder(workorder, maintenances.Maintenance(id = self.productsTable.focus()))).place(x=1050, y=100)
        
        #Maintenances in work order
        self.maintenancesTable = crearTabla(['Fecha', 'Descripción'], [1,], [100,500], [['',''],], mainframe, 8, '' )
        self.maintenancesTable.place(x=400, y=300)
            
        #Remove
        Button(mainframe, text='Quitar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.removeMaintenanceFromWorkOrder(workorder, maintenances.Maintenance(id = self.maintenancesTable.focus()))).place(x=1050, y=300)
        
    def saveWorkOrder(self, workorder):
        """_summary_

        Args:
            workorder (WorkOrder): _description_
        """
        workorder.date = datetime.combine(self.cal.selection_get(), datetime.min.time())
        workorder.responsible = employers.Employer(id = employers.ver('id')[self.responsible.current()])
        workorder.comment = self.comment.get('1.0', END)
        workorder.save()
        messagebox.showinfo(title='Orden de trabajo creada', message=f"La orden de trabajo se ha creado con el id {workorder.id}")
        self.window.destroy()
        self.displayWorkOrder(workorder.id)
    
    def addMaintenanceToWorkOrder(self, workorder, maintenance):
        if not workorder.hasMaintenance(maintenance):
            workorder.maintenances.append(maintenance)
        self.updateWorkOrderMaintenancesTable(workorder, self.maintenancesTable)
    
    def removeMaintenanceFromWorkOrder(self, workorder, maintenance):
        workorder.removeMaintenance(maintenance)
        self.updateWorkOrderMaintenancesTable(workorder, self.maintenancesTable)
    
    def updateWorkOrderMaintenancesTable(self, workorder, table):
        """_summary_

        Args:
            workorder (WorkOrder Class): _description_
            table (_type_): _description_
        """
        table.delete(*table.get_children())
        for maintenance in workorder.maintenances:
            table.insert('', 0, id=maintenance.id, text=maintenance.date.strftime('%d/%m/%Y'), values=(maintenance.description,))
            
        
if __name__ == '__main__':
    sql.checkDatabase()
    aplicacion = Crm()
    #aplicacion.objetoMantenimientos.statistics()
    root.mainloop()
