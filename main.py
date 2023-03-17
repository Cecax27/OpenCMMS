from cgitb import text
from math import prod
from msilib.schema import ComboBox
import textwrap
from tkinter import *
import customtkinter
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
from modules.ui import resources
from modules import inventory
from modules import sql
from modules import workorders
import locale
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

#locale.setlocale(locale.LC_ALL, 'es-ES')

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

#Constantes-----
colorGreen = '#37c842'
colorRed = '#c83737'
colorBlue = '#37abc8'
colorGray = '#e6e6e6'
colorDarkGray = '#dadada'
colorWhite = "#ffffff"
colorBlack = "#454545"
colorBackground = "#f2f2f2"

previousWindow = []
previousWindowTemp = None

#Functios--------
def goBack():
    """Go to the back window
    """
    global previousWindow, previousWindowTemp
    previousWindowTemp = previousWindow.pop()
    previousWindowTemp()
    
def goNext(command):
    """Go to the next window uses the back function.

    Args:
        command (function): The next command to execute.
    """
    global previousWindowTemp, previousWindow
    if previousWindowTemp != None:
        previousWindow.append(previousWindowTemp)
    previousWindowTemp = command
    command()

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

def deleteActivityFromList(activity, objeto):
    return lambda:objeto.padre.objetoMantenimientos.eliminarActividadAsignada(activity)

def clearMainFrame():
    global mainFrame
    global root
    
    global imgCorrective, imgPreventive, imgIn, imgOut, imgDate, imgPerson, imgDescription, imgMaintenance, imgPlant, imgPreventive2, imgRepeat, imgTask, imgStatus, imgQuantity, imgTime
    imgCorrective = PhotoImage(file='img/corrective.png').subsample(8)
    imgPreventive = PhotoImage(file='img/preventive.png').subsample(8)
    imgIn = PhotoImage(file='img/in.png')
    imgOut = PhotoImage(file='img/out.png')
    imgDate = PhotoImage(file='img/date.png').subsample(3)
    imgPerson = PhotoImage(file="img/person.png").subsample(3)
    imgDescription = PhotoImage(file="img/description.png").subsample(3)
    imgMaintenance = PhotoImage(file="img/maintenance.png").subsample(3)
    imgPlant = PhotoImage(file="img/plant.png").subsample(3)
    imgPreventive2 = PhotoImage(file="img/preventive_2.png").subsample(3)
    imgRepeat = PhotoImage(file="img/repeat.png").subsample(3)
    imgTask = PhotoImage(file="img/task.png").subsample(3)
    imgStatus = PhotoImage(file="img/status.png").subsample(3)
    imgQuantity = PhotoImage(file="img/quantity.png").subsample(3)
    imgTime = PhotoImage(file="img/time.png").subsample(3)
  
    mainFrame.destroy()
    mainFrame = customtkinter.CTkFrame(master = root, corner_radius=0, fg_color='transparent')
    mainFrame.grid(column=1, row=0, columnspan=2, rowspan=3, padx=(20,20), pady=(20,20), sticky='nsew')
    mainFrame.grid_columnconfigure(0, weight=1)
    mainFrame.grid_rowconfigure(2, weight=1)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Root----------------------
        self.title('Gestión de Mantenimiento Emman')
        self.state('zoomed') #abrir maximizado
        icon = PhotoImage(file = "img/maintenance.png")
        self.iconphoto(True, icon)
        
        global root
        root = self
        
        #Configure grid layout--------------
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Objetos--------
        self.objetoDepartamentos = Departamentos()
        self.objetoAreas = Areas()
        self.objetoEquipos = Plants(self)
        self.objetoActividades = Actividades()
        self.objetoMantenimientos = Maintenances(self)
        self.objetoEmpleados = Empleados(self)
        self.inventory = Inventory(self)
        self.workorders = WorkOrders(self)

        #Menu---------------------
        self.menu = resources.Menu(self) 

        self.menu.addButton("Mantenimientos", lambda: self.select_frame_by_name('Mantenimientos'))
        self.menu.addButton("Inventario", lambda: self.select_frame_by_name('Inventario'))
        self.menu.addButton("Empleados", lambda: self.select_frame_by_name('Empleados'))

        global barraMenu
        barraMenu = BarraMenu(self)

        global mainFrame
        mainFrame = customtkinter.CTkFrame(self)

        self.mainframe = mainFrame
        clearMainFrame()
        
        self.select_frame_by_name('Mantenimientos')
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        for index, button in enumerate(self.menu.buttons):
            button.configure(fg_color=("gray75", "gray25") if name == self.menu.buttons_names[index] else "transparent")
        if name == 'Mantenimientos':    
            goNext(self.objetoMantenimientos.maintenancesMainWindow)
        elif name == 'Inventario':
            goNext(self.inventory.inventoryMainWindow)
        elif name == 'Empleados':
            goNext(self.objetoEmpleados.employersMainWindow)
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

        btGuardar = Button(self.frame, text='Guardar', command= self.empleadosGuardar).grid(column=0, row=6)
        btCancelar = Button(self.frame, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=6)

theme = 'light'
def change_appearance_mode_event():
    global theme
    customtkinter.set_appearance_mode('dark' if theme == 'light' else 'light')
    theme = 'dark' if theme == 'light' else 'light'

class BarraMenu(App):

    def __init__(self, padre):

        self.menubar = Menu(padre)
        padre.config(menu=self.menubar)

        #Objetos menu
        filemenu = Menu(self.menubar)
        
        editmenu = Menu(self.menubar)
        
        editmenu_preferences = Menu(self.menubar, tearoff= 0)
        editmenu_preferences.add_command(label='Tema oscuro/claro', command = change_appearance_mode_event)
        
        editmenu.add_cascade(label='Preferencias', menu=editmenu_preferences)

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
        productMenu.add_command(label='Recalcular cantidades', command= lambda:padre.inventory.recalculateInventory())
        
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

def func_displayPlant(id, object, previous):
    return lambda event: goNext(lambda: object.parent.objetoEquipos.displayPlant(id))

class Plants(App):

    def __init__(self, padre):
        self.parent = padre
        self.root = padre

    def plantsMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Mantenimientos", "Por equipo")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Nuevo equipo", lambda: goNext(self.nuevo), colorGreen)
        
        #Var
        self.searchString = StringVar(mainFrame)
        self.verTodos = IntVar()
        self.verTodos.set(0)
        
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        self.listaNombresAreas=[]
        
        searchBar = resources.SearchBar(mainFrame)
        searchBar.addSearchBar(self.searchString, self.updatePlantsWindow)
        self.departamento2 = searchBar.addFilter("Departamento", self.listaNombresDepartamentos, self.updatePlantsWindow)
        self.area = searchBar.addFilter("Área", self.listaNombresAreas, self.updatePlantsWindow)
        
        self.plantsFrame = ScrollableFrame(mainFrame, x=10, y=200, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-220, bg=colorBackground)
        self.plantsFrame.place(0,0)
        
        self.updatePlantsWindow()
        
    def updatePlantsWindow(self, *event):
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento2.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
        self.area["values"]=self.listaNombresAreas
        if self.searchString.get() == "" and self.departamento2.current() == -1 and self.area.current() == -1:
            self.plantsList = plants.get(all = True)
        else:
            self.plantsList = plants.get(name=self.searchString.get(), department=self.listaDepartamentos[self.departamento2.current()][0] if self.departamento2.current() != -1 else -1,area=self.listaAreas[self.area.current()][0] if self.area.current() != -1 else -1)
            
        self.plantsFrame.clear()
        itemX = int((mainFrame.winfo_width()-40)/250)
        itemSeparation = ((mainFrame.winfo_width()-40)-(250*itemX))/(itemX+4)
        for plant in self.plantsList:
            plantNumber = self.plantsList.index(plant)
            frame = Frame(self.plantsFrame.scrollableFrame)
            frame.config(width=250, height=150, bg=colorDarkGray, cursor='hand2')
            frame.bind('<Button-1>', func_displayPlant(plant.id, self, self.plantsMainWindow))
            frame.grid(column=plantNumber%itemX, row=int(plantNumber/itemX), pady=10, padx=itemSeparation)
            Label(frame, text=plant.name, bg=colorDarkGray, fg='#444444',font=("Segoe UI", "10", "bold"), wraplength=230, justify=LEFT).place(x=10, y=10)
            Label(frame, text=plant.description, bg=colorDarkGray, fg='#666666', font=("Segoe UI", "9", "normal"), wraplength=230, justify=LEFT).place(x=10, y=50)
            Label(frame, text=plant.area.name, bg=colorDarkGray,fg='#555555', font=("Segoe UI", "9", "normal"), wraplength=180, justify=LEFT).place(x=10, y=90)
            Label(frame, text=plant.department.name, bg=colorDarkGray,fg='#555555', font=("Segoe UI", "9", "normal")).place(x=10, y=120)

    def displayPlant(self, id):
        global mainFrame
        clearMainFrame()
        plant = plants.Plant(id)
        
        resources.AddTittle(mainFrame, plant.name, plant.description)
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Asignar actividades", lambda: goNext(lambda: self.assignActivitiesWindow(plant)))
        menu.addButton("Editar", lambda: goNext(lambda:self.editar(plant.id)))
        menu.addButton("Eliminar", lambda:self.eliminar(plant.id), colorRed)

        global imgPlant, imgDescription, imgTime
        info = resources.sectionInfo(mainFrame)
        info.addData("ID", plant.id, imgPlant)
        info.addData("Área", plant.area.name, imgDescription)
        info.addData("Departamento", plant.department.name, imgDescription)
        info.addData("Último mantenimiento realizado", plant.getLastMaintenance().date.strftime('%d/%m/%Y') if plant.getLastMaintenance() else "No se ha hecho ninguno", imgTime)
        
        selectMantenimientos = plant.getMaintenances()

        mainFrame.update()
        maintenancesFrame = ScrollableFrame(mainFrame, bg=colorBackground, x=20, y=200, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-220)
        maintenancesFrame.place()
        
        for maint in selectMantenimientos:
            frame = Frame(maintenancesFrame.scrollableFrame)
            frame.config(width=mainFrame.winfo_width()-80, height=130, bg=colorGray, cursor='hand2')
            frame.bind('<Button-1>', func_displayMaintenance(maint.id, self, lambda: self.displayPlant(plant.id)))
            frame.pack(pady=10, padx=10)
            Frame(frame, bg=colorRed if maint.date < datetime.now() and maint.status == maintenances.Programmed else colorGreen, height=130, width=3).place(x=0, y=0)
            #Titular
            global imgTask, imgDate, imgStatus, imgMaintenance
            info = resources.Info(frame, colorGray)
            info.addData("ID", maint.id, imgTask)
            info.addData("", maint.date.strftime('%d/%m/%Y'), imgDate)
            info.addData("", maint.status, imgStatus)
            info.addData("", maint.type, imgMaintenance)
            info.addData("", maint.description, imgDescription, large=True)

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
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
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

        Button(self.info, text='Asignar actividades',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command = lambda: self.assignActivitiesWindow(select[0], mantFrame)).place(x=root.winfo_width()-380, y=10)

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
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command= func_displayMaintenance(i[0], self, lambda: self.editar(idEquipo))).place(x=180, y=200)

        v.config(command=mantFrame.xview)

    def editarGuardar(self, id, nombre, descripcion):
        equipoActual = plants.buscar(id)
        plants.modificar(id, nombre,  descripcion, equipoActual[3])
        texto = 'El equipo ' + nombre + ' ha sido modificado.'
        messagebox.showinfo(title='Equipo modificada', message=texto)
        self.actualizarInformacion()

    def editarActualizarEquipos(self, *event):
        if self.verTodos.get() == 1:
            self.listaEquipos = plants.ver()
        elif not hasattr(self, 'listaAreas'):
            self.listaEquipos = [[' ','Seleccione un area',' ']]
        else:
            self.listaEquipos = plants.buscarPorArea( self.listaAreas[self.area.current()][0])
            if len(self.listaEquipos) == 0:
                self.listaEquipos = [[' ','Area sin equipos',' ']]
        self.tabla.delete(*self.tabla.get_children())
        
        for x in self.listaEquipos:
            self.tabla.insert('', 0, id=x[0], values = (x[2],), text = x[1], tags=('mytag',))

    def editarActualizarAreas(self, event):
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento2.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
        self.area["values"]=self.listaNombresAreas

    def eliminar(self, id):
        nombre = plants.buscar(id)[1]
        texto = '¿En verdad desea eliminar el equipo ' + nombre +'? Esta eliminación será permantente'
        if messagebox.askyesno(title='¿Eliminar el equipo?', message=texto):
            plants.eliminar(id)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Equipo eliminada', message=texto)

    def assignActivitiesWindow(self, plant):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, plant.name, "Asignar actividades")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Guardar", lambda: self.displayPlant(plant.id))
        
        #Tabla de actividades para asignar--------------
        Label(mainFrame, text='Actividades disponibles',fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=20, y=150)
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
            mainFrame,
            10,
            ''
        )
        self.tablaActividades.place(x=10, y=180)

        #Botón para asignar actividad
        Button(mainFrame, text='Asignar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = lambda:self.asignarActividad(self.tablaActividades.focus(),plant.id)).place(x=10, y=420)

        #Tabla de actividades asignadas-------------
        Label(mainFrame, text='Actividades asignadas',fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=root.winfo_width()/2-150, y=150)
        lista = activities.buscarPorEquipo(plant.id)
        listaIds = []
        for activity in lista:
            listaIds.append(activity[0])
            lista[lista.index(activity)] = [lista[lista.index(activity)][1], lista[lista.index(activity)][2]]
        self.tablaActividadesAsignadas = crearTabla(
            ['Nombre', 'Descripción'],
            listaIds,
            [200,300],
            lista,
            mainFrame,
            10,
            ''
        )
        self.tablaActividadesAsignadas.place(x=root.winfo_width()/2-150, y=180)

        #Botón para eliminar actividad asignada
        Button(mainFrame, text='Eliminar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = lambda:self.eliminarActividadAsignada(self.tablaActividadesAsignadas.focus())).place(x=root.winfo_width()/2-150, y=420)
   
    def actualizarActividades(self, *event):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        self.listaActividadesAsignadas = activities.buscarPorEquipo(id)
        if len(self.listaActividadesAsignadas) < 1:
            self.listaActividadesAsignadas =(['','Equipo sin actividades','',''],)
        self.tablaActividadesAsignadas.delete(*self.tablaActividadesAsignadas.get_children())        
        for x in self.listaActividadesAsignadas:
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

def func_displayMaintenance(id, object, previous = None):
    return lambda event = None: goNext(lambda: object.parent.objetoMantenimientos.displayMaintenance(id) )

class Maintenances(App):
    def __init__(self, padre):
        self.padre = padre
        self.parent = padre
        global mainFrame
        
    def maintenancesMainWindow(self):
        global root
        global mainFrame
    
        resources.AddTittle(mainFrame, "Mantenimientos")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Ordenes de trabajo", lambda: goNext(self.parent.workorders.workOrdersMainWindow))
        menu.addButton("+ Mantenimiento preventivo", lambda: goNext(self.newPreventiveWindow), colorGreen)
        menu.addButton("+ Mantenimiento correctivo", lambda: goNext(self.newCorrective), colorGreen)
        menu.addButton("Ver todos", lambda: goNext(self.allMaintenancesWindow))
        menu.addButton("Ver por equipos", lambda: goNext(self.parent.objetoEquipos.plantsMainWindow))
        menu.addButton("Estadísticas", lambda: goNext(self.statistics))

        #Programmed maintenances
        frame = customtkinter.CTkScrollableFrame(mainFrame, fg_color='transparent')
        frame.grid(column=0, row=2, padx=(20, 20), pady=(20, 20),sticky='nswe')
        frame.grid_columnconfigure((0,1), weight=1)
        
        programmed_maintenances = customtkinter.CTkFrame(frame)
        programmed_maintenances.grid(column = 0, row = 0, pady=10, padx=10)
        resources.Title(programmed_maintenances, text = 'Mantenimientos programados').grid(column=0, row=0, pady=10, padx=10)
        resources.Metric(programmed_maintenances, text = sql.petition('SELECT COUNT(id) FROM mantenimientos WHERE estado = "Programado"'), text_color=(colorBlue, colorBlue)).grid(column=0, row=2, pady=(0,10), padx=10)
        
        overdue_maintenances = customtkinter.CTkFrame(frame)
        overdue_maintenances.grid(column = 1, row = 0, pady=10, padx=10)
        resources.Title(overdue_maintenances, text = 'Mantenimientos atrasados').grid(column=0, row=0, pady=10, padx=10)
        resources.Metric(overdue_maintenances, text = sql.petition('SELECT COUNT(id) FROM mantenimientos WHERE estado = "Programado" AND fecha < date("now")'), text_color=(colorRed, colorRed)).grid(column=0, row=2, pady=(0,10), padx=10)
        
        

    def allMaintenancesWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Mantenimientos", "Todos")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        
        maintenancesTotal = maintenances.count()
        
        Label(mainFrame, text='Id', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=20, y=120)
        Label(mainFrame, text='Fecha', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=90, y=120)
        Label(mainFrame, text='Estado', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=270, y=120)
        Label(mainFrame, text='Descripción', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=370, y=120)
        
        self.maintenancesFrame = ScrollableFrame(mainFrame, x=20, y=150, width=mainFrame.winfo_width()-40, height=root.winfo_height()-210, bg=colorBackground)
        self.maintenancesFrame.place(x=0, y=0)
        
        navigation = resources.sectionNavigation(mainFrame, int(maintenancesTotal/10), lambda: self.updateAllMaintenancesWindow(navigation.page.get()), "Atrás", "Siguiente")
        
        self.updateAllMaintenancesWindow(navigation.page.get())
        
    def updateAllMaintenancesWindow(self, page):
        maintenancesList = maintenances.getAll(10, (page*10))
        self.maintenancesFrame.clear()
        self.maintenancesFrame.set(0)
        
        for maint in maintenancesList:
            frame = Frame(self.maintenancesFrame.scrollableFrame)
            frame.config(width=mainFrame.winfo_width()-80, height=130, bg=colorGray, cursor='hand2')
            frame.bind('<Button-1>', func_displayMaintenance(maint.id, self, self.allMaintenancesWindow))
            frame.pack(pady=10, padx=10)
            Frame(frame, bg=colorRed if maint.date < datetime.now() and maint.status == maintenances.Programmed else colorGreen, height=130, width=3).place(x=0, y=0)
            #Titular
            global imgTask, imgDate, imgStatus, imgMaintenance, imgDescription
            info = resources.Info(frame, colorGray)
            info.addData("ID", maint.id, imgTask)
            info.addData("", maint.date.strftime('%d/%m/%Y'), imgDate)
            info.addData("", maint.status, imgStatus)
            info.addData("", maint.type, imgMaintenance)
            info.addData("", maint.description, imgDescription, large=True)
    
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

    def newPreventiveWindow(self, maintenance = None):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Mantenimiento preventivo")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Guardar", self.nuevoGuardar, colorGreen)
        
        self.varRepeat = IntVar()
        
        if not maintenance:
            self.newMaintenance = maintenances.Maintenance(type=maintenances.Preventive)
        else:
            self.newMaintenance = maintenance
            self.varRepeat.set(1) if self.newMaintenance.repeat != None else self.varRepeat.set(0)

        #Date
        customtkinter.CTkLabel(mainFrame, text='Fecha', font=("Segoe UI", 14, "normal")).place(x=10, y=130)
        today = datetime.now() if not maintenance else maintenance.date
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorBackground, selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=10, y=160)

        #Estado------------
        self.listaEstados=[maintenances.Done, maintenances.Programmed]
        customtkinter.CTkLabel(mainFrame, text='Estado').place(x=10, y=340)
        self.estado = customtkinter.CTkOptionMenu(mainFrame,values=self.listaEstados)
        self.estado.place(x=10, y=370)

        #Responsible
        customtkinter.CTkLabel(mainFrame, text='Responsable').place(x=10, y=400)
        self.responsible = customtkinter.CTkOptionMenu(mainFrame, values = employers.ver('nombre'))
        self.responsible.place(x=10, y=430)

        #Repeat
        self.repeatOn = customtkinter.CTkSwitch(mainFrame, text="Repetir cada", variable=self.varRepeat, onvalue=1, offvalue=0)
        self.repeatOn.place(x=10, y=460)
        self.repeat = customtkinter.CTkEntry(mainFrame, width=10)
        self.repeat.place(x=140, y=460)
        customtkinter.CTkLabel(mainFrame, text='días').place(x=180, y=460)

        #Description
        customtkinter.CTkLabel(mainFrame, text='Descripción').place(x=10, y=490)
        self.description = customtkinter.CTkTextbox(mainFrame, width=200, height=200)
        self.description.place(x=10, y=520)

        #Department
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=400, y=30)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=400, y=60)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=600, y=30)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=60)

        #Plants table
        Label(mainFrame, text='Equipos', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=400, y=100)
        self.tabla = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('','Seleccione un area y departamento'),],
            mainFrame,
            10,
            self.actualizarActividades
        )
        self.tabla.place(x=400, y=130)

        #Activities table
        Label(mainFrame, text='Actividades', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=400, y=360)
        self.tablaActividadesAsignadas = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('',''),],
            mainFrame,
            10,
            ''
        )

        self.tablaActividadesAsignadas.place(x=400, y=390)

        #Botón para asignar actividad
        Button(mainFrame, text=' + ',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = self.asignarActividad).place(x=650, y=620)

        #Tabla de equipos
        self.activitiesTable = ScrollableFrame(mainFrame, x=800, y=30, width=300, height=mainFrame.winfo_height()-60, bg=colorBackground)
        self.activitiesTable.place()
        
        if maintenance:
            self.estado.set(self.newMaintenance.status)
            self.responsible.set(employers.Employer(id=self.newMaintenance.responsible).name)
            self.description.insert(INSERT, self.newMaintenance.description)
            self.repeat.insert(INSERT, self.newMaintenance.repeat)
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

    def newCorrective(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Nuevo", "Mantenimiento correctivo")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Guardar", self.saveCorrective, colorGreen)
        
        #Var
        self.newMaintenance = maintenances.Maintenance(type = maintenances.Corrective)
        self.searchString = StringVar(mainFrame)
        self.quantity = StringVar(mainFrame)

        self.selectedPlants = []

        #Date
        Label(mainFrame, text='Fecha', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=20, y=150)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorWhite, selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=20, y=180)

        #Responsible
        Label(mainFrame, text='Responsable', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=300, y=150)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = employers.ver('nombre'))
        self.responsible.place(x=300, y=180)

        #Description
        Label(mainFrame, text='Descripción', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=300, y=210)
        self.description = Text(mainFrame, width=120, height=4, font=("Segoe UI", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.place(x=300, y=240)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=450, y=150)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=450, y=180)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=600, y=150)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=180)
        
        #Status
        self.statusList=[maintenances.Done, maintenances.Programmed]
        Label(mainFrame, text='Estado', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=750, y=150)
        self.status = ttk.Combobox(mainFrame, state='readonly',values=self.statusList)
        self.status.place(x=750, y=180)

        #Plants table
        Label(mainFrame, text='Equipos', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=20, y=380)
        self.tabla = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [200, 200],
            [('','Seleccione un area y departamento'),],
            mainFrame,
            5, 
            ''
        )
        self.tabla.place(x=20, y=410)

        Button(mainFrame, text='+',font=("Segoe UI", "11", "normal"), bg=colorBlue, fg=colorBackground, highlightthickness=0, borderwidth=2, relief=FLAT, command=self.selectPlant).place(x=430, y=420)

        #Plants table
        Label(mainFrame, text='Equipos seleccionados', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=20, y=550)
        self.selectedPlantsTable = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [200, 200],
            [('','Aún no hay nada seleccionado'),],
            mainFrame,
            5, 
            ''
        )
        self.selectedPlantsTable.place(x=20, y=580)

        Button(mainFrame, text='-',font=("Segoe UI", "11", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.deselectPlant).place(x=430, y=590)

        #Search
        Label(mainFrame, text='Productos usados', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=500, y=330)
        search = Frame(mainFrame)
        search.config(bg='#ECECEC', width=400, height=30)
        search.place(x=500 , y=360)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=50, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#ECECEC', highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventorySearch)
        
        #Products table
        self.productsTable = crearTabla(['Nombre', 'Descripción', 'Marca', 'Modelo'], [1,], [100,100,100,100], [['','','',''],], mainFrame, 4, '' )
        self.productsTable.place(x=500, y=400)
        
        #Coment
        Label(mainFrame, text='Comentario',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "normal")).place(x=500, y=530)
        self.comment = Text(mainFrame, width=43, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=590, y=530)
        
        #Quantity
        Label(mainFrame, text='Cantidad',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "normal")).place(x=500, y=600)
        Entry(mainFrame, width=20, textvariable=self.quantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT).place(x=590, y=600)
        
        #Add product
        Button(mainFrame, text='+ Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg=colorBackground, highlightthickness=0, borderwidth=2, relief=FLAT, command=self.addProductToMaintenance).place(x=820, y=630)
        
        #Products
        Label(mainFrame, text='Productos',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "bold")).place(x=950, y=330)
        
        self.productsFrame = ScrollableFrame(mainFrame, width=380, height=200, x=950, y=360)
        self.productsFrame.place()
    
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
        maintenanceExists = True if self.newMaintenance.id else False
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
        
        #texto = f"El mantenimiento ha sido registrado con id {self.newMaintenance.id}."
        #messagebox.showinfo(title='Mantenimiento registrado', message=texto)
        goBack()
        if not maintenanceExists: goNext(lambda: self.displayMaintenance(self.newMaintenance.id)) 

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
            if select.type == maintenances.Preventive:
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
            global previousWindow
            previousWindow()

    def displayMaintenance(self, id):
        global mainFrame
        global root
        global previousWindow
        clearMainFrame()

        global imgDate
        global imgPerson
        global imgDescription
        global imgMaintenance
        global imgPlant
        global imgPreventive2
        global imgRepeat
        global imgTask
        
        sel = maintenances.Maintenance(id = id)
        resources.AddTittle(mainFrame, f"Mantenimiento {sel.type}", f"ID {sel.id}")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Editar", lambda: goNext(lambda: self.newPreventiveWindow(sel) if sel.type == maintenances.Preventive else lambda: self.editCorrectiveWindow(sel)))
        if sel.status == 'Programado':
            menu.addButton("Realizar", lambda: self.realizarMantenimiento(id))
        if sel.status == maintenances.Done and sel.next == None and sel.type == 'Preventivo':
            menu.addButton("Programar", lambda: self.programar(id))
        if sel.status != maintenances.Cancelled:
            menu.addButton("Cancelar", lambda: self.cancelarMantenimiento(sel), colorRed)
        if sel.status == maintenances.Cancelled:
            menu.addButton("Eliminar", lambda: self.eliminarMantenimiento(sel), colorRed)
        menu.addButton("Orden de trabajo", lambda: goNext(lambda: self.maintenanceToWorkOrder(sel)), colorGreen)

        #Label fecha y estado de mantenimiento
        info = resources.sectionInfo(mainFrame)
        info.addData("", sel.date.strftime('%d/%m/%Y'), imgDate)
        info.addData("", employers.buscar(sel.responsible)[2], imgPerson)
        info.addData("", 'Mantenimiento '+sel.type, imgMaintenance)
        if sel.type == 'Preventivo':
            info.addData("", str(sel.repeat)+' días', imgRepeat)
        info.addData("", sel.description, imgDescription, True)        

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
                framePlant.config(bg=colorBackground,
                    width=250,
                    height=root.winfo_height()-50)
                framePlant.place(x=listActivities.index(plant)*250+15, y=220)
                thisPlant = plants.buscar(plant[0].plant.id)
                area = areas.Area(thisPlant[3])
                #Department
                Label(framePlant, text=area.department.name, fg='#666666', bg=colorBackground, font=("Segoe UI", "9", "normal")).place(x=10, y=10)
                #Area
                Label(framePlant, text=area.name, fg='#666666', bg=colorBackground, font=("Segoe UI", "9", "bold")).place(x=10+len(area.department.name*10), y=10)
                #Plant
                Label(framePlant, text=thisPlant[1], fg='#000000', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=10, y=40)
                #Description
                Label(framePlant, text=thisPlant[2], fg='#000000', bg=colorBackground, font=("Segoe UI", "9", "normal"), wraplength=180, justify='left').place(x=10, y=70)
                for activity in plant:
                    #Label nombre actividad
                    Label(framePlant, text=activity.name, fg='#111111', bg=colorBackground, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=110+plant.index(activity)*60)
                    #Label descripcion actividad
                    Label(framePlant, text=activity.description, fg='#111111', bg=colorBackground, font=("Segoe UI", "8", "normal"), wraplength=180, justify='left').place(x=10, y=130+plant.index(activity)*60)
        else:
            for plant in sel.plants:
                framePlant = Frame(mainFrame)
                framePlant.config(bg=colorBackground,
                    width=250,
                    height=root.winfo_height()-50)
                framePlant.place(x=15+sel.plants.index(plant)*250, y=220)
                
                Label(framePlant, text=plant.department.name, fg='#666666', bg=colorBackground, font=("Segoe UI", "9", "normal")).place(x=10, y=10)
                Label(framePlant, text=plant.area.name, fg='#666666', bg=colorBackground, font=("Segoe UI", "9", "bold")).place(x=10+len(plant.department.name*10), y=10)
                Label(framePlant, text=plant.name, fg='#000000', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=10, y=40)
                Label(framePlant, text=plant.description, fg='#000000', bg=colorBackground, font=("Segoe UI", "9", "normal"), wraplength=180, justify='left').place(x=10, y=70)
                
    def maintenanceToWorkOrder(self, maintenance):
        """_summary_

        Args:
            maintenance (_type_): _description_
        """
        # global previousWindow
        # previousWindow = self.displayMaintenance(maintenance.id)
        self.parent.workorders.newWorkOrder(employers.Employer(maintenance.responsible), (maintenance,))
        
    def statistics(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Mantenimientos", "Estadísticas")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        
        global imgDescription
        info = resources.sectionInfo(mainFrame)
        info.addData("Mantenimientos totales", str(sql.petition("SELECT COUNT(id) FROM mantenimientos")[0][0]), imgDescription)
        info.addData("Mantenimientos preventivos", str(sql.petition("SELECT COUNT(id) FROM mantenimientos WHERE tipo='Preventivo'")[0][0]), imgDescription)
        info.addData("Mantenimientos correctivos", str(sql.petition("SELECT COUNT(id) FROM mantenimientos WHERE tipo='Correctivo'")[0][0]), imgDescription)

        #Graphs
        graph = Frame(mainFrame, width=500, height=300, bg=colorBackground)
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
    return lambda event = None: goNext(lambda: object.parent.objetoEmpleados.displayEmployer(id))

class Empleados():
    
    def __init__(self, parent):
        global root
        global mainFrame   
        self.parent = parent    
        self.padre = parent
    
    def employersMainWindow(self):
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Empleados")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Nuevo", lambda: goNext(self.newEmployerWindow), colorGreen)
        
        employerList = employers.getAll() 
        
        employerFrame = ScrollableFrame(mainFrame, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-150, x=20, y=130, bg=colorBackground)
        employerFrame.place(x=10, y=40)
        
        frameQuantity = int((mainFrame.winfo_width()-40)/300)
        frameSeparation = int(((mainFrame.winfo_width()-40)%300)/(frameQuantity*2))
        
        for employer in employerList:
            actualFrame = Frame(employerFrame.scrollableFrame)
            actualFrame.config(bg=colorGray, highlightthickness=0, width=300, height=200)
            actualFrame.bind('<Button-1>', createFunctionToDisplayEmployer(employer.id, self))
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
            
    def displayEmployer(self, id):
        clearMainFrame()
        
        employer = employers.Employer(id = id)
        resources.AddTittle(mainFrame, employer.name, "Empleado")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Estadísticas", lambda: goNext(lambda: self.statistics(employer)))
        menu.addButton("Mantenimientos asignados", lambda: goNext(lambda: self.assignedMaintenancesWindow(employer)))
        
        global imgPerson, imgTask
        info = resources.sectionInfo(mainFrame)
        info.addData("ID", employer.id, imgPerson)
        info.addData("Clave", employer.key, imgTask)
        
        #Areas
        Label(mainFrame, text='Areas', bg=colorBackground, font=("Segoe UI", "11", "bold")).place(x=10, y=150)
        
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

    def statistics(self, employer):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, employer.name, "Estadísticas")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        
        global imgDescription
        info = resources.sectionInfo(mainFrame)
        info.addData("Mantenimientos totales", str(sql.petition(f"SELECT COUNT(id) FROM mantenimientos WHERE responsable = {employer.id}")[0][0]), imgDescription)
        info.addData("Mantenimientos preventivos", str(sql.petition(f"SELECT COUNT(id) FROM mantenimientos WHERE tipo='Preventivo' AND responsable = {employer.id}")[0][0]), imgDescription)     
        info.addData("Mantenimientos correctivos", str(sql.petition(f"SELECT COUNT(id) FROM mantenimientos WHERE tipo='Correctivo' AND responsable = {employer.id}")[0][0]), imgDescription)
        
        #Graphs
        employer.stats()
        
        graph = Frame(mainFrame, width=500, height=300, bg=colorBackground)
        graph.place(x=20, y=200)
        fig = Figure(figsize=(5,4), dpi=100)
        plot1 = fig.add_subplot(211)
        rawData = sql.petition(f"SELECT strftime('%m',fecha) as month ,COUNT(id) as quantity FROM mantenimientos WHERE tipo='Correctivo' AND responsable = {employer.id} GROUP BY strftime('%Y',fecha), strftime('%m',fecha) ORDER BY fecha")
        plot1.set_title("Mantenimientos correctivos por mes")
        plot1.set_xlabel('Mes')
        plot1.set_ylabel('Mantenimientos')
        plot1.bar([row[0] for row in rawData],[row[1] for row in rawData], color='#93C2E4')
        
        plot2 = fig.add_subplot(212)
        rawData = sql.petition(f"SELECT strftime('%m',fecha) as month ,COUNT(id) as quantity FROM mantenimientos WHERE tipo='Preventivo' AND responsable = {employer.id} GROUP BY strftime('%Y',fecha), strftime('%m',fecha) ORDER BY fecha")
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

    def assignedMaintenancesWindow(self, employer):
        clearMainFrame()
        resources.AddTittle(mainFrame, employer.name, "Mantenimientos asignados")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Crear orden de trabajo", lambda: goNext(lambda:self.parent.workorders.newWorkOrder(responsible = employer, maintenancesList = list(filter(lambda x: selectList[maintenancesList.index(x)].get() == 1, maintenancesList)))))
        
        maintenancesFrame = ScrollableFrame(mainFrame, x=20, y=150, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-170, bg=colorBackground)
        maintenancesFrame.place(x=0, y=0)
        
        maintenancesList = maintenances.find(employerId=employer.id, status=maintenances.Programmed, order="fecha")
        selectList = [IntVar() for i in maintenancesList]
        for maintenance in maintenancesList:
            mant = Frame(maintenancesFrame.scrollableFrame)
            mainFrame.update()
            mant.config(bg=colorGray, highlightthickness=0, highlightbackground="#eeeeee", width=mainFrame.winfo_width()-100, height=130, cursor='hand2')
            mant.bind('<Button-1>', func_displayMaintenance(maintenance.id, self, lambda: self.assignedMaintenancesWindow(employer)))
            mant.pack(pady=10, padx=15)
            Frame(mant, bg=colorRed if maintenance.date < datetime.now() else colorGreen, height=130, width=3).place(x=0, y=0)
            #Titular
            global imgTask, imgDate, imgStatus, imgMaintenance, imgDescription
            info = resources.Info(mant, colorGray)
            info.addData("ID", maintenance.id, imgTask)
            info.addData("", maintenance.date.strftime('%d/%m/%Y'), imgDate)
            info.addData("", maintenance.status, imgStatus)
            info.addData("", maintenance.type, imgMaintenance)
            info.addData("", maintenance.description, imgDescription, large=True)
            Checkbutton(mant, cursor='hand2', variable=selectList[maintenancesList.index(maintenance)], bg=colorGray, width=1, height=1).place(x=5, y=5)

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
    return lambda event: goNext(lambda: object.parent.inventory.displayRequisition(id))

def func_displayProduct(id, object):
    return lambda event: goNext(lambda: object.parent.inventory.displayProduct(id))

def func_removeProductFromRequisition(id, object):
    return lambda: object.parent.inventory.removeProductFromRequisition(id)

class Inventory():
    
    def __init__(self, parent) -> None:
        global root
        self.parent = parent
        
    def inventoryMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Inventario")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Productos", lambda: goNext(self.productsMainWindow)) 
        menu.addButton("Requisiciones", lambda: goNext(self.requisitionsMainWindow))  
        menu.addButton("Proveedores", lambda:goNext(self.suppliersMainWindow))     
        
    def productsMainWindow(self):
        global mainFrame
        clearMainFrame()
    
        resources.AddTittle(mainFrame, "Productos")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Nuevo producto", self.newProduct, colorGreen)
        menu.addButton("Exportar inventario", self.exportInventory)
        
        #Var
        self.searchString = StringVar(mainFrame)
        productsList = inventory.getProducts()
        
        #Search
        search = Frame(mainFrame)
        search.config(bg='#fafafa', width=(root.winfo_width()/2)-40, height=30)
        search.place(x=20 , y=120)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=95, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#fafafa', highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventoryFrame)
        
        mainFrame.update()  
        self.productsFrame = ScrollableFrame(mainFrame, x=10, y=160, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-180,bg=colorBackground)
        self.productsFrame.place(x=0, y=0)
        
        self.insertProducts(productsList)
            
    def updateInventoryFrame(self, event):
        productsList = inventory.findByName(self.searchString.get())
        self.productsFrame.clear()
        self.insertProducts(productsList)
            
    def insertProducts(self, productsList):
        itemX = int((mainFrame.winfo_width()-40)/250)
        itemSeparation = ((mainFrame.winfo_width()-40)-(250*itemX))/(itemX+4)
        for product in productsList:
            productNumber = productsList.index(product)
            frame = Frame(self.productsFrame.scrollableFrame)
            frame.config(width=250, height=150, bg=colorDarkGray)
            frame.bind('<Button-1>', func_displayProduct(product.id, self))
            frame.grid(column=productNumber%itemX, row=int(productNumber/itemX), pady=10, padx=itemSeparation)
            Label(frame, text=product.name, bg=colorDarkGray, fg='#444444',font=("Segoe UI", "10", "bold"), wraplength=230, justify=LEFT).place(x=10, y=10)
            Label(frame, text=product.description, bg=colorDarkGray, fg='#666666', font=("Segoe UI", "9", "normal"), wraplength=230, justify=LEFT).place(x=10, y=50)
            Label(frame, text=(product.brand if product.brand != None else '')+(' - '+product.model if product.model != None else ''), bg=colorDarkGray,fg='#555555', font=("Segoe UI", "9", "normal"), wraplength=180, justify=LEFT).place(x=10, y=90)
            Label(frame, text=str(product.quantity)+ ' disponible', bg=colorDarkGray,fg=colorRed if product.quantity==0 else colorGreen, font=("Segoe UI", "9", "normal")).place(x=10, y=120)
            
    def exportInventory(self):
        f = asksaveasfile(initialfile=f"Inventario - {datetime.now().strftime('%d-%m-%Y')}.pdf", defaultextension='.pdf', filetypes=[('Portable Document File', '*.pdf'),])
        inventory.generatePDF(f.name)
    
    def displayProduct(self, id):
        global mainFrame
        clearMainFrame()
        product = inventory.Product(id = id)
        product.findMovements()
        
        #Tittle
        resources.AddTittle(mainFrame, product.name, product.description)
        menu = resources.sectionMenu(mainFrame)
        global previousWindow
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Editar", lambda: self.newProduct(product))
        menu.addButton("Graficar", product.graphMovements)
        menu.addButton("Registrar entrada", lambda: goNext(lambda: self.newInputInventory(product)), colorGreen)
        if product.quantity > 0: 
            menu.addButton("Registrar salida", lambda: goNext(lambda: self.newOutputInventory(product)), colorRed)
        
        global imgQuantity, imgTime, imgDescription
        info = resources.sectionInfo(mainFrame)
        info.addData("Cantidad disponible", product.quantity, imgQuantity)
        info.addData("Tiempo de entrega", str(product.deliveringTime().days)+' días', imgTime)
        info.addData("Tiempo estimado para agotarse", str(product.calculateOutputs()*product.quantity)+' días', imgTime)
        info.addData("Marca", product.brand, imgDescription)
        info.addData("Modelo", product.model, imgDescription)
        
            
        #Movements
        Label(mainFrame, text='Movimientos de inventario',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "bold")).place(x=20, y=220)
        
        movementsFrame = ScrollableFrame(mainFrame, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-200, x=20, y=250, bg=colorBackground)
        movementsFrame.place(x=20, y=230)
        
        for mov in product.movements:
            movNumber = product.movements.index(mov)
            backColor = colorGray if movNumber%2==0 else colorDarkGray
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
        goBack()
    
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
        goBack()
        
    def requisitionsMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Requisiciones")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Nueva requisición", lambda: goNext(self.newRequisition), colorGreen)
        menu.addButton("Productos pendientes", lambda: goNext(self.pendingProductsWindow))
        
        requisitionsList = inventory.getRequisitions(quantity=40, order='date')
        
        requisitionsFrame = ScrollableFrame(mainFrame, x=20, y=150, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-180, bg=colorBackground)
        requisitionsFrame.place(x=0, y=0)
        
        Label(mainFrame, text='Id', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=20, y=120)
        Label(mainFrame, text='Fecha', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=90, y=120)
        Label(mainFrame, text='Estado', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=270, y=120)
        Label(mainFrame, text='Descripción', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=370, y=120)
        
        for req in requisitionsList:
            reqNumber = requisitionsList.index(req)
            backColor = colorGray if reqNumber%2==0 else colorDarkGray
            frame = Frame(requisitionsFrame.scrollableFrame)
            frame.config(width=mainFrame.winfo_width()-60, height=30, bg=backColor)
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
        resources.AddTittle(mainFrame, "Requisición", f"ID {req.id}")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Editar", lambda: goNext(lambda: self.newRequisition(req)))
        menu.addButton("Guardar en PDF", lambda: self.saveRequisitionPDF(req))
        if req.status == inventory.STATUS_DRAFT: 
            menu.addButton("Marcar solicitada", lambda: self.changeStatus(req, inventory.STATUS_REQUESTED))  
        elif req.status == inventory.STATUS_REQUESTED:   
            menu.addButton("Marcar confirmada", lambda: self.changeStatus(req, inventory.STATUS_CONFIRMED))
        elif req.status == inventory.STATUS_CONFIRMED or req.status == inventory.STATUS_PARTIAL_DELIVERED: 
            menu.addButton("Registrar entrega", lambda: goNext(lambda: self.purchaseDelivered(req)))  
        menu.addButton("Eliminar", lambda: self.deleteRequisition(req), colorRed)

        global imgStatus, imgDate, imgDescription
        info = resources.sectionInfo(mainFrame)
        info.addData("",req.status.capitalize(),imgStatus)
        info.addData("Fecha de creación", datetime.date(req.date).strftime("%d / %b /  %Y"), imgDate)
        if req.deliveredDate != None:
            info.addData("Fecha de recepción", datetime.date(req.deliveredDate).strftime("%d / %b /  %Y"), imgDate)
        info.addData("", req.description, imgDescription, True)
        
        #Products
        Label(mainFrame, text='Descripción',fg="#000000", bg=colorBackground, font=("Segoe UI", "10", "bold"), justify="center").place(x=(mainFrame.winfo_width()-40)*0.3+20, y=220)
        Label(mainFrame, text='Cantidad pedidos',fg="#000000", bg=colorBackground, font=("Segoe UI", "10", "bold"), justify="center").place(x=(mainFrame.winfo_width()-40)*0.65+20, y=220)
        Label(mainFrame, text='Cantidad entregados',fg="#000000", bg=colorBackground, font=("Segoe UI", "10", "bold"), justify="center").place(x=(mainFrame.winfo_width()-40)*0.85+20, y=220)
        
        self.productsFrame = ScrollableFrame(mainFrame, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-270, x=20, y=250, bg=colorBackground)
        self.productsFrame.place(x=20, y=250)
        
        for product in req.products:
            productNumber = req.products.index(product)
            backColor = colorGray if productNumber%2==0 else colorDarkGray
            productFrame = Frame(self.productsFrame.scrollableFrame)
            productFrame.config(bg=backColor, highlightthickness=0, width=mainFrame.winfo_width()-50, height=70 if product.comment != None else 40)
            productFrame.bind('<Button-1>', func_displayProduct(product.product.id, self))
            productFrame.pack(pady=1)
            #Description
            name = Label(productFrame, text=product.product.name, fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=450, justify='left')
            name.place(x=10, y=10)
            name.update()
            Label(productFrame, text=str(product.quantity), fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=300, justify='center').place(x=(mainFrame.winfo_width()-40)*0.65+20, y=10)
            Label(productFrame, text=str(product.deliveredQuantity), fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=300, justify='center').place(x=(mainFrame.winfo_width()-40)*0.85+20, y=10)
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
        clearMainFrame()
        #Tittle
        resources.AddTittle(mainFrame, "Requisición", f"ID {requisition.id}")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Cancelar", goBack, "#555555")
        menu.addButton("Guardar como entrega total", lambda: self.processPurchase(requisition, detailsList), colorGreen)
        menu.addButton("Guardar como entrega parcial", lambda: self.processPurchase(requisition, detailsList, partial = True), colorGreen)
        
        global imgStatus, imgDate, imgDescription
        info = resources.sectionInfo(mainFrame)
        info.addData("",requisition.status.capitalize(),imgStatus)
        info.addData("Fecha de creación", datetime.date(requisition.date).strftime("%d / %b /  %Y"), imgDate)
        if requisition.deliveredDate != None:
            info.addData("Fecha de recepción", datetime.date(requisition.deliveredDate).strftime("%d / %b /  %Y"), imgDate)
        info.addData("", requisition.description, imgDescription, True)
        
        #Products
        Label(mainFrame, text='Descripción',fg="#000000", bg=colorBackground, font=("Segoe UI", "10", "bold"), justify="center").place(x=(mainFrame.winfo_width()-40)*0.3+20, y=220)
        Label(mainFrame, text='Cantidad pedidos',fg="#000000", bg=colorBackground, font=("Segoe UI", "10", "bold"), justify="center").place(x=(mainFrame.winfo_width()-40)*0.65+20, y=220)
        Label(mainFrame, text='Cantidad entregados',fg="#000000", bg=colorBackground, font=("Segoe UI", "10", "bold"), justify="center").place(x=(mainFrame.winfo_width()-40)*0.85+20, y=220)
        
        self.productsFrame = ScrollableFrame(mainFrame, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-270, x=20, y=250, bg=colorBackground)
        self.productsFrame.place(x=20, y=250)
        
        detailsList = []
        for product in requisition.products:
            productNumber = requisition.products.index(product)
            backColor = colorGray if productNumber%2==0 else colorDarkGray
            productFrame = Frame(self.productsFrame.scrollableFrame)
            productFrame.config(bg=backColor, highlightthickness=0, width=mainFrame.winfo_width()-50, height=70 if product.comment != None else 40)
            productFrame.pack(pady=1)
            #Description
            Label(productFrame, text=product.product.name, fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=450, justify='left').place(x=10, y=10)
            Label(productFrame, text=str(product.quantity), fg='#000000', bg=backColor, font=("Segoe UI", "11", "normal"), wraplength=300, justify='center').place(x=(mainFrame.winfo_width()-40)*0.65+20, y=10)
            quantity = IntVar(mainFrame)
            Entry(productFrame, textvariable=quantity, width=5, font=("Segoe UI", "10", "normal"), foreground="#000000", background=colorWhite, highlightthickness=0, relief=FLAT).place(x=(mainFrame.winfo_width()-40)*0.85+20, y=10)
            detailsList.append([product, quantity])
            Label(productFrame, text=product.comment, fg='#4d4d4d', bg=backColor, font=("Segoe UI", "9", "normal"), wraplength=1000, justify='left').place(x=10, y=35)
            productFrame.update()
        
    def processPurchase(self, requisition, detailsList, partial = False):
        for detail in detailsList:
            detail[0].deliveredQuantity = detail[1].get()
            if not partial or (partial and detail[0].deliveredQuantity != 0):
                detail[0].status = inventory.STATUS_DELIVERED
                detail[0].deliveredDate = datetime.now()
                detail[0].save()
                detail[0].product.addMovement(datetime.now(), inventory.INPUT, detail[1].get(), detail[0].comment, inventory.REQUISITION, requisition.id)
        requisition.deliveredDate = datetime.now()
        if partial:
            self.changeStatus(requisition, inventory.STATUS_PARTIAL_DELIVERED)
        else:
            self.changeStatus(requisition, inventory.STATUS_DELIVERED)
        self.displayRequisition(requisition.id)
        
    def newProduct(self, product = None):
        self.window = Toplevel()
        self.window.title("Editar producto" if product else 'Crear producto')
        
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
        Button(mainframe, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.saveProduct(productName.get(), productDescription.get(), productBrand.get(), productModel.get(), categories[category.current()], product.id if product else None)).place(x=20, y=440)
        if product:
            productName.set(product.name)
            productDescription.set(product.description)
            productBrand.set(product.brand)
            productModel.set(product.model)
            category.current(categories.index(list(filter(lambda x: x.id == product.category.id, categories))[0]))
        
    def saveProduct(self, name, description, brand, model, category, id = None):
        newProduct = inventory.Product() if not id else inventory.Product(id)
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
            if not id:
                goNext(lambda: self.displayProduct(newProduct.id))
            else:
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
        mainframe.config(bg=colorBackground, width=self.window.winfo_width(), height=self.window.winfo_height())
        mainframe.pack()
        
        resources.AddTittle(mainframe, "Requisición", "nueva" if requisition == None else requisition.id)
        menu = resources.sectionMenu(mainframe)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Guardar", self.saveRequisition)
        menu.addButton("Nuevo producto", self.newProduct, colorGreen)
        
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
        
        
        
        #Search
        search = Frame(mainframe)
        search.config(bg=colorWhite, width=(root.winfo_width()/2)-40, height=30)
        search.place(x=20 , y=130)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(search, image = searchImg, bd=0, width=12, heigh=12).place(x=12, y=9)
        searchEntry = Entry(search, width=95, textvariable=self.searchString, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorWhite, highlightthickness=0, relief=FLAT)
        searchEntry.place(x=30, y=4)
        searchEntry.bind('<Key>', self.updateInventorySearch)
        
        #Products table
        tableWidth = int(((root.winfo_width()/2)-40)/4)
        self.productsTable = crearTabla(['Nombre', 'Descripción', 'Marca', 'Modelo'], [1,], [tableWidth,tableWidth,tableWidth,tableWidth], [['','','',''],], mainframe, 4, '' )
        self.productsTable.place(x=20, y=170)
        
        #Coment
        Label(mainframe, text='Comentario',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "normal")).place(x=20, y=290)
        self.comment = Text(mainframe, width=int(((root.winfo_width()/2)-40)/7), font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorWhite, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=20, y=320)
        
        #Quantity
        Label(mainframe, text='Cantidad',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "normal")).place(x=20, y=400)
        Entry(mainframe, width=20, textvariable=self.quantity, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorWhite, highlightthickness=0, relief=FLAT).place(x=20, y=430)
        
        #Add product
        Button(mainframe, text='+ Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.addProductToRequisition).place(x=300, y=420)
        
        #Products
        Label(mainframe, text='Productos',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "bold")).place(x=root.winfo_width()/2, y=100)
        
        self.productsFrame = ScrollableFrame(mainframe, width=int(root.winfo_width()/2-40), height=300, x=root.winfo_width()/2, y=130, bg=colorBackground)
        self.productsFrame.place(x=root.winfo_width()/2, y=130)
        
        #Requisition Comment
        Label(mainframe, text='Comentario',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "normal")).place(x=20, y=480)
        self.requisitionComment = Text(mainframe, width=int(((root.winfo_width())-40)/7), font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorWhite, highlightthickness=0, relief=FLAT, height=6)
        self.requisitionComment.place(x=20, y=510)
        
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
        
    def recalculateInventory(self):
        for product in inventory.getProducts():
            product.recalculateQuantity()
    
    def pendingProductsWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Requisiciones", "Productos pendientes de entrega")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        
        mainFrame.update()  
        productsFrame = ScrollableFrame(mainFrame, x=20, y=160, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-180,bg=colorBackground)
        productsFrame.place()
        productsList = inventory.getPendingProducts()
        global imgDescription, imgQuantity, imgDate
        
        for product in productsList:
            frame = Frame(productsFrame.scrollableFrame)
            frame.config(width=mainFrame.winfo_width()-60, height=150, bg=colorDarkGray)
            frame.bind('<Button-1>', func_displayRequisition(product.requisitionId, self))
            frame.pack(pady=10)
            info = resources.Info(frame, colorDarkGray)
            info.addData("", product.product.name, imgDescription)
            info.addData("", (product.product.brand if product.product.brand != None else '')+(' - '+product.product.model if product.product.model != None else ''), imgDescription)
            info.addData("Cantidad pendiente", product.quantity, imgQuantity)
            info.addData("Requisición", product.requisitionId, imgDescription)
            info.addData("", inventory.Requisition(product.requisitionId).date.strftime("%d/%m/%Y"), imgDate)
       
    def suppliersMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Proveedores")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Nuevo proveedor", lambda: goNext(self.newSupplierWindow), colorGreen)
        
    def newSupplierWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Nuevo proveedor")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
            
def func_displayWorkOrder(id, object, previous = None):
    return lambda event: goNext(lambda: object.parent.workorders.displayWorkOrder(id)) 
        
class WorkOrders:
    
    def __init__(self, App) -> None:
        global root
        self.parent = App
    
    def workOrdersMainWindow(self):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Ordenes de trabajo")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Nueva", lambda: goNext(self.newWorkOrder), colorGreen)
        
        workOrdersList = workorders.getAll(orderby='date', order='DESC')
        
        workordersFrame = ScrollableFrame(mainFrame, x=20, y=180, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-180, bg=colorBackground)
        workordersFrame.place(x=0, y=0)
        
        Label(mainFrame, text='Id', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=20, y=150)
        Label(mainFrame, text='Fecha', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=90, y=150)
        Label(mainFrame, text='Estado', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=270, y=150)
        Label(mainFrame, text='Descripción', bg=colorBackground, font=("Segoe UI", "10", "bold")).place(x=370, y=150)
        
        for work in workOrdersList:
            reqNumber = workOrdersList.index(work)
            backColor = colorGray if reqNumber%2==0 else colorDarkGray
            frame = Frame(workordersFrame.scrollableFrame)
            frame.config(width=root.winfo_width()-80, height=30, bg=backColor, cursor='hand2')
            frame.bind('<Button-1>', func_displayWorkOrder(work.id, self, self.workOrdersMainWindow))
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
        resources.AddTittle(mainFrame, "Orden de trabajo", f"ID {workorder.id}")
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Editar", lambda: goNext(lambda: self.newWorkOrder(workorder = workorder)))
        menu.addButton("Guardar PDF", lambda: self.saveWorkOrderPDF(workorder))
        if workorder.status == workorders.STATUS_DRAFT:
            menu.addButton("Confirmar", lambda: self.changeStatus(workorder, workorders.STATUS_CONFIRMED))    
        if workorder.status == workorders.STATUS_CONFIRMED:   
            menu.addButton("Comenzar", lambda: self.changeStatus(workorder, workorders.STATUS_IN_PROGRESS)) 
        if workorder.status == workorders.STATUS_IN_PROGRESS:  
            menu.addButton("Terminar", lambda: self.changeStatus(workorder, workorders.STATUS_DONE))  
        menu.addButton("Eliminar", lambda: self.deleteWorkOrder(workorder), colorRed)
        
        global imgStatus, imgDate, imgPerson, imgDescription
        
        info = resources.sectionInfo(mainFrame)
        info.addData("", workorders.LANGUAGE[workorder.status].capitalize(), imgStatus)
        info.addData("", datetime.date(workorder.date).strftime("%d / %b /  %Y"), imgDate)
        info.addData("", workorder.responsible.name, imgPerson)
        info.addData("", workorder.comment, imgDescription)
        
        self.activitiesFrame = ScrollableFrame(mainFrame, width=mainFrame.winfo_width()-40, height=mainFrame.winfo_height()-250, x=20, y=230, bg=colorBackground)
        self.activitiesFrame.place(x=20, y=230)
        
        for maint in workorder.maintenances:
            frame = Frame(self.activitiesFrame.scrollableFrame)
            frame.config(width=mainFrame.winfo_width()-80, height=130, bg=colorGray, cursor='hand2')
            frame.bind('<Button-1>', func_displayMaintenance(maint.id, self, lambda: self.displayWorkOrder(workorder.id)))
            frame.pack(pady=10, padx=10)
            Frame(frame, bg=colorRed if maint.date < datetime.now() and maint.status == maintenances.Programmed else colorGreen, height=130, width=3).place(x=0, y=0)
            #Titular
            global imgTask, imgMaintenance
            info = resources.Info(frame, colorGray)
            info.addData("ID", maint.id, imgTask)
            info.addData("", maint.date.strftime('%d/%m/%Y'), imgDate)
            info.addData("", maint.status, imgStatus)
            info.addData("", maint.type, imgMaintenance)
            info.addData("", maint.description, imgDescription, large=True)
    
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
        self.workOrdersMainWindow()
    
    def newWorkOrder(self, responsible = None, maintenancesList = None, workorder = None):
        global mainFrame
        clearMainFrame()
        
        resources.AddTittle(mainFrame, "Orden de trabajo", f"ID {workorder.id}" if workorder else "Nueva")
        
        menu = resources.sectionMenu(mainFrame)
        menu.addButton("Atrás", goBack, "#555555")
        menu.addButton("Guardar", lambda: self.saveWorkOrder(workorder), colorGreen)
        
        #Var
        if not workorder:
            workorder = workorders.WorkOrder()
        
        #Date
        Label(mainFrame, text='Fecha', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=20, y=130)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),background=colorBackground, selectmode='day', year= int(workorder.date.strftime('%Y')) if workorder.id else int(today.strftime('%Y')), month = int(workorder.date.strftime('%m')) if workorder.id else int(today.strftime('%m')), day = int(workorder.date.strftime('%d')) if workorder.id else int(today.strftime('%d')), showweeknumbers=False, foreground= colorBlack, bordercolor=colorWhite, headersbackground=colorWhite, headersforeground= colorBlack, selectbackground=colorBlue, weekendbackground=colorWhite, weekendforeground=colorBlack, selectforeground=colorGray, normalbackground=colorWhite, normalforeground=colorBlack, othermonthbackground=colorGray, othermonthweforeground=colorBlack)
        self.cal.place(x=20, y=160)
        
        #Responsible
        Label(mainFrame, text='Responsable', bg=colorBackground, font=("Segoe UI", "10", "normal")).place(x=20, y=340)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = employers.ver('nombre'), foreground="#222222", background=colorGray)
        if responsible:
            self.responsible.current((employers.ver('nombre').index(responsible.name)))
        elif workorder.id:
            self.responsible.current((employers.ver('nombre').index(workorder.responsible.name)))
        self.responsible.place(x=20, y=370)
        
        #Comment
        Label(mainFrame, text='Comentario',fg="#000000", bg=colorBackground, font=("Segoe UI", "11", "normal")).place(x=20, y=410)
        self.comment = Text(mainFrame, width=43, font=("Segoe UI", "10", "normal"), foreground="#222222", background=colorGray, highlightthickness=0, relief=FLAT, height=3)
        self.comment.place(x=20, y=440)
        if workorder.id:
            self.comment.insert(END, workorder.comment)
        
        #Maintenances table
        self.productsTable = crearTabla(['Fecha', 'Descripción'], [1,], [100,500], [['',''],], mainFrame, 8, '' )
        self.productsTable.place(x=400, y=100)
        for maintenance in maintenances.getMaintenancesToWorkOrders():
            self.productsTable.insert('', 0, id=maintenance.id, text=maintenance.date.strftime('%d/%m/%Y'), values=(maintenance.description,))
            
        #Add
        Button(mainFrame, text='Agregar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.addMaintenanceToWorkOrder(workorder, maintenances.Maintenance(id = self.productsTable.focus()))).place(x=1050, y=100)
        
        #Maintenances in work order
        self.maintenancesTable = crearTabla(['Fecha', 'Descripción'], [1,], [100,500], [['',''],], mainFrame, 8, '' )
        self.maintenancesTable.place(x=400, y=300)
        
        if maintenancesList:
            workorder.maintenances = maintenancesList
        self.updateWorkOrderMaintenancesTable(workorder, self.maintenancesTable)
            
        #Remove
        Button(mainFrame, text='Quitar',font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.removeMaintenanceFromWorkOrder(workorder, maintenances.Maintenance(id = self.maintenancesTable.focus()))).place(x=1050, y=300)
        
    def saveWorkOrder(self, workorder):
        """Save a workorder

        Args:
            workorder (WorkOrder): _description_
        """
        workorder.date = datetime.combine(self.cal.selection_get(), datetime.min.time())
        workorder.responsible = employers.Employer(id = employers.ver('id')[self.responsible.current()])
        workorder.comment = self.comment.get('1.0', END)
        workorder.save()
        messagebox.showinfo(title='Orden de trabajo creada', message=f"La orden de trabajo se ha creado con el id {workorder.id}")
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
    
    app = App()
    app.mainloop()
