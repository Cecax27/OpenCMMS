from cgitb import text
from msilib.schema import ComboBox
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from turtle import width
import empleados
import equipos
import actividades
import areas
import mantenimientos
from tkcalendar import Calendar
from datetime import datetime
from datetime import date
from datetime import timedelta
from modules.ui.scrollableFrame import *
from modules import inventory
import locale

#locale.setlocale(locale.LC_ALL, 'es-ES')

#Constantes-----
colorGreen = '#37c842'
colorRed = '#c83737'
colorBlue = '#37abc8'
colorGray = '#f2f2f2'
colorDarkGray = '#dadada'
colorWhite = "#ffffff"

#Funciones--------
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

def getPlant(activity):
    return activity.plant.department

def clearMainFrame():
    global mainFrame
    global root
    
    global imgCorrective
    global imgPreventive
    imgCorrective = PhotoImage(file='img/corrective.png').subsample(8)
    imgPreventive = PhotoImage(file='img/preventive.png').subsample(8)
    
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
            text='Actividades',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.actividades
            ).place(x=2.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Departamentos',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.departamentos
            ).place(x=3.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Areas',
            font=("Segoe UI", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.areas
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

        self.objetoMantenimientos.main()

    def actividades(self):
        self.mainframe.destroy()
        self.mainframe = Frame(self.root, relief=RIDGE, borderwidth=2)
        self.mainframe.grid(column=0, row=1)

        lblMain = Label(self.mainframe, text='Actividades')
        lblMain.grid(column=0, row=0)

        listaActividades = actividades.ver()
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
        listaEmpleados = empleados.ver()
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
        codigo = empleados.buscar(self.responsable.get())[0][1]
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
        menuEquipos.add_command(label='Editar equipo', 
            command= lambda:padre.objetoEquipos.editar())
        menuEquipos.add_command(label='Eliminar equipo', 
            command= lambda:padre.objetoEquipos.eliminar())

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
        #menuMantenimientos.add_command(label='Editar actividad', command= lambda:padre.objetoActividades.editar())
        #menuMantenimientos.add_command(label='Eliminar actividad', command= lambda:padre.objetoActividades.eliminar())

        #Inventory menu------------------------
        productMenu = Menu(self.menubar, tearoff=0)
        productMenu.add_command(label='Crear producto', command= lambda:padre.inventory.new())
        
        categoryMenu = Menu(self.menubar, tearoff=0)
        categoryMenu.add_command(label='Crear categoría', command= lambda:padre.inventory.newCategory())
        
        inventoryMenu = Menu(self.menubar, tearoff=0)
        inventoryMenu.add_cascade(label='Productos', menu=productMenu)
        inventoryMenu.add_cascade(label='Categorías', menu=categoryMenu)
        
        
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
        help(Button)
        Button(frameBotones, text='Guardar', command= self.guardar).grid(column=0, row=3,pady=5, padx=5, sticky='w e')
        Button(frameBotones, text='Cancelar', command=self.ventana.destroy).grid(column=1, row=3,pady=5, padx=5, sticky='w e') 

    def editarActualizar(self, event):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        resultado = areas.buscarDepartamento(text) 
        #print(resultado)
        self.nombre.delete(0, "end")
        self.nombre.insert(0, resultado[0][1])

    def guardar(self):
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        resultado = areas.buscarDepartamento(text) 
        areas.modificarDepartamento(resultado[0][0], self.nombre.get())
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
        self.listaEmpleados = empleados.ver()
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
        codigo = empleados.buscar(self.dictEmpleado[self.responsable.get()])[1]
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
        self.listaEmpleados = empleados.ver()
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
        codigo = empleados.buscar(self.responsable.get())[0][1]
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
        select = list(equipos.buscar(self.tabla.focus()))
        selectMantenimientos = mantenimientos.buscarPorEquipo(self.tabla.focus())
        select[3] = areas.buscar(select[3])[1]

        #Labels principales
        Label(self.info, text=select[1], bg=colorGray, font=("Segoe UI", "10", "bold"), wraplength=400, justify='left').place(x=10, y=10)
        Label(self.info, text=select[2], bg=colorGray, font=("Segoe UI", "9", "normal"), wraplength=400, justify='left').place(x=10, y=40)

        #Ultimo mantenimiento realizado
        Label(self.info, text="Último mantenimiento", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=10, y=80)
        text = mantenimientos.ultimoMantenimientoRealizado(select[0])
        if text == None:
            text = 'No se ha hecho ninguno'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Segoe UI", "9", "bold")).place(x=140, y=80)

        #Ultimo mantenimiento programado
        Label(self.info, text="Siguiente mantenimiento programado", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=400, y=80)
        text = mantenimientos.ultimoMantenimientoProgramado(select[0])
        if text == None:
            text = 'No hay mantenimiento programado'
        else:
            text = text[1]
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
            #mant.place(x=10+selectMantenimientos.index(i)*260, y=0)
            mant.pack(pady=5, padx=5, side=LEFT)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i[0]), fg='#111111', bg=colorDarkGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=10)
            Label(mant, text=i[1], fg='#111111', bg=colorDarkGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
            Label(mant, text=i[2], fg='#111111', bg=colorDarkGray, font=("Segoe UI", "8", "normal"), wraplength=120, justify='right').place(x=100, y=30)
            #Descripción
            Label(mant, text='Matenimiento '+i[5], fg='#333333', bg=colorDarkGray, font=("Segoe UI", "8", "bold")).place(x=10, y=60)
            Label(mant, text=i[4], fg='#333333', bg=colorDarkGray, font=("Segoe UI", "8", "normal"), wraplength=230, justify='left').place(x=10, y=80)
            #Botón
            Button(mant, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i[0], self)).place(x=180, y=200)

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
        equipos.new(nombre, descripcion, area)

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
        select = list(equipos.buscar(self.tabla.focus()))
        selectMantenimientos = mantenimientos.buscarPorEquipo(self.tabla.focus())
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
        text = mantenimientos.ultimoMantenimientoRealizado(select[0])
        if text == None:
            text = 'No se ha hecho ninguno'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Segoe UI", "9", "bold")).place(x=140, y=80)

        #Ultimo mantenimiento programado
        Label(self.info, text="Siguiente mantenimiento programado", fg='#666666', bg=colorGray, font=("Segoe UI", "9", "normal")).place(x=400, y=80)
        text = mantenimientos.ultimoMantenimientoProgramado(select[0])
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
        equipoActual = equipos.buscar(id)
        equipos.modificar(id, nombre,  descripcion, equipoActual[3])
        texto = 'El equipo ' + nombre + ' ha sido modificado.'
        messagebox.showinfo(title='Equipo modificada', message=texto)
        self.actualizarInformacion()

    def editarActualizarEquipos(self, *event):
        #print(self.verTodos.get())
        if self.verTodos.get() == 1:
            self.listaEquipos = equipos.ver()
        elif not hasattr(self, 'listaAreas'):
            self.listaEquipos = [[' ','Seleccione un area',' ']]
        else:
            self.listaEquipos = equipos.buscarPorArea( self.listaAreas[self.area.current()][0])
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
        nombre = equipos.buscar(id)[1]
        texto = '¿En verdad desea eliminar el equipo ' + nombre +'? Esta eliminación será permantente'
        if messagebox.askyesno(title='¿Eliminar el equipo?', message=texto):
            equipos.eliminar(id)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Equipo eliminada', message=texto)

    def asignarActividades(self, id, mantFrame):
        #Limpiar el frame
        mantFrame.destroy()
        #Variables

        #Tabla de actividades para asignar--------------
        Label(self.info, text='Actividades disponibles',fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=180, justify='left').place(x=10, y=150)
        lista = actividades.ver()
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
        lista = actividades.buscarPorEquipo(id)
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
        self.listaActividadesAsignadas = actividades.buscarPorEquipo(id)
        if len(self.listaActividadesAsignadas) < 1:
            self.listaActividadesAsignadas =(['','Equipo sin actividades','',''],)
        self.tablaActividadesAsignadas.delete(*self.tablaActividadesAsignadas.get_children())        
        for x in self.listaActividadesAsignadas:
            #print(x)
            self.tablaActividadesAsignadas.insert('', 0, values = (x[1],x[2],x[3]), text = x[0],tags=("mytag",))

    def asignarActividad(self, idActividad, idEquipo):
        actividad = actividades.buscar(idActividad)
        actividades.nuevaActividadAsignada(actividad[1], actividad[2], actividad[3], idEquipo)
        texto = 'La actividad ' + actividad[1] + ' ha sido asignada al equipo.'
        messagebox.showinfo(title='Actividad asignada', message=texto)


    def eliminarActividadAsignada(self, idActividad):
        actividad = actividades.buscarActividadAsignada(idActividad)
        actividades.eliminarActividadAsignada(idActividad)
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
        actividades.new(self.nombre.get(), self.descripcion.get(),int(self.tiempo.get()))
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

        lista = actividades.ver()
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
        resultado = actividades.buscar(text) 
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
        actividades.modificar(text, self.nombre.get(),  self.descripcion.get(), self.tiempo.get())
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

        lista = actividades.ver()
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
            actividades.eliminar(clave)
            texto = 'El equipo ' + nombre + ' ha sido eliminado permantente.'
            messagebox.showinfo(title='Actividad eliminada', message=texto)
        self.ventana.destroy()

class Mantenimientos(Crm):
    def __init__(self, padre):
        self.padre = padre
        global mainFrame
        
    def main(self):
        global mainFrame
        global root
        
        clearMainFrame()

        #Title
        Label(mainFrame, text='Mantenimientos', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Buttons
        Button(mainFrame, text='+ Mantenimiento preventivo',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.nuevo).place(x=10, y=40)

        Button(mainFrame, text='+ Mantenimiento correctivo',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.newCorrective).place(x=200, y=40)

        #Show all maintenances
        lista = mantenimientos.getAll()[0:10]
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
            Label(mant, text=i.date.strftime("%a %d %B %Y"), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=45, y=30)
            #Status
            if i.status == 'Realizado' or i.status == 'Realizado Programado':
                color = colorGreen
            elif i.status == 'Programado':
                color = colorBlue
            elif i.status == 'Cancelado':
                color = colorRed
            Label(mant, text=i.status, fg=color, bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, anchor="e", width=20).place(x=root.winfo_width()/2-255, y=10)
            #type
            if i.type == mantenimientos.Corrective:
                Label(mant, image = imgCorrective, bd=0, width=25, height=25).place(x=10, y=15)
            elif i.type == mantenimientos.Preventive:
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
        
        lista = mantenimientos.getProgrammed()
        
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
            if i.date < datetime.date(datetime.now()):
                actualColor = colorRed
            else:
                actualColor = colorGreen
            Frame(mant, bg=actualColor, height=100, width=3).place(x=0, y=0)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i.id), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=10)
            #Date
            Label(mant, text=i.date.strftime("%a %d %B %Y"), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
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

    def ActualizarAreas(self, event):
        #print(self.departamento2.current())
        self.listaAreas = areas.buscarPorDepartamento( self.listaDepartamentos[self.departamento.current()][0])
        self.listaNombresAreas=[]
        for x in self.listaAreas:
            self.listaNombresAreas.append(x[1])
        #print(self.listaNombresAreas)
        self.area["values"]=self.listaNombresAreas

    def ActualizarEquipos(self, *event):
        self.listaEquipos = equipos.buscarPorArea( self.listaAreas[self.area.current()][0])
        if len(self.listaEquipos) == 0:
            self.listaEquipos = [[' ','Area sin equipos']]
        self.tabla.delete(*self.tabla.get_children())
        #print(self.listaAreas[self.area.current()][0])
        
        for x in self.listaEquipos:
            self.tabla.insert('', 0,id=x[0], text = x[1], values =x[2], tags=("mytag","color"))

    def actualizarActividades(self, *event):
        id = self.tabla.focus()
        self.listaActividadesAsignadas = actividades.buscarPorEquipo(id)
        if len(self.listaActividadesAsignadas) < 1:
            self.listaActividadesAsignadas =(['','Equipo sin actividades'],)
        self.tablaActividadesAsignadas.delete(*self.tablaActividadesAsignadas.get_children())        
        for x in self.listaActividadesAsignadas:
            self.tablaActividadesAsignadas.insert('', 0, id= x[0], values = x[2], text = x[1])

    def nuevo(self):
        global mainFrame
        clearMainFrame()
        
        self.varRepeat = IntVar()
        
        self.newMaintenance = mantenimientos.Maintenance(type=mantenimientos.Preventive)
        
        #Tittle
        Label(mainFrame, text='Mantenimiento preventivo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),bg="#ffffff", selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')))
        self.cal.place(x=10, y=70)

        #Estado------------
        self.listaEstados=[mantenimientos.Done, mantenimientos.Programmed]
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=280)
        self.estado = ttk.Combobox(mainFrame, state='readonly',values=self.listaEstados)
        self.estado.place(x=10, y=310)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=340)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = empleados.ver('nombre'))
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

        self.selectedPlants = []

        #Tittle
        Label(mainFrame, text='Mantenimiento correctivo', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Segoe UI", "9", "normal"),bg="#ffffff", selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')))
        self.cal.place(x=10, y=70)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=280)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = empleados.ver('nombre'))
        self.responsible.place(x=10, y=310)

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=10, y=350)
        self.description = Text(mainFrame, width=40, height=13, font=("Segoe UI", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.place(x=10, y=380)

        Button(mainFrame, text='Guardar',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.saveCorrective).place(x=root.winfo_width()-100, y=10)

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
            ''
        )
        self.tabla.place(x=400, y=110)

        Button(mainFrame, text='Seleccionar equipo',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.selectPlant).place(x=400, y=350)

        #Plants table
        Label(mainFrame, text='Equipos seleccionados', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=800, y=80)
        self.selectedPlantsTable = crearTabla(
            ['Nombre', 'Descripción'],
            [1,],
            [120, 150],
            [('','Aún no hay nada seleccionado'),],
            mainFrame,
            10, 
            ''
        )
        self.selectedPlantsTable.place(x=800, y=110)

        Button(mainFrame, text='Deseleccionar equipo',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.deselectPlant).place(x=800, y=350)

    def selectPlant(self):
        plantId = self.tabla.focus()
        plantData = equipos.buscar(plantId)
        if not plantData in self.selectedPlants:
            self.selectedPlants.append(plantData)
            print(f"Plant with id {plantId} added to the maintenance")
        self.selectedPlantsTable.delete(*self.selectedPlantsTable.get_children())
        if len(self.selectedPlants) == 0:
            self.selectedPlantsTable.insert('', 0, id = 0, values = 'Aún no hay nada seleccionado', text = '',tags=("mytag",))
            return
        for x in self.selectedPlants:
            self.selectedPlantsTable.insert('', 0, id = x[0], values = x[2], text = x[1],tags=("mytag",))
        

    def deselectPlant(self):
        plantId = self.selectedPlantsTable.focus()
        plantData = equipos.buscar(plantId)
        if plantData in self.selectedPlants:
            self.selectedPlants.pop(self.selectedPlants.index(plantData))
            print(f"Plant with id {plantId} removed to the maintenance")
        self.selectedPlantsTable.delete(*self.selectedPlantsTable.get_children())
        if len(self.selectedPlants) == 0:
            self.selectedPlantsTable.insert('', 0, id = 0, values = 'Aún no hay nada seleccionado', text = '',tags=("mytag",))
            return
        for x in self.selectedPlants:
            self.selectedPlantsTable.insert('', 0, id = x[0], values = x[2], text = x[1],tags=("mytag",))

    def saveCorrective(self):
        maintenanceData = mantenimientos.Maintenance(type = 'corrective')
        maintenanceData.date = self.cal.selection_get()
        maintenanceData.responsible = empleados.ver('id')[self.responsible.current()]
        maintenanceData.description = self.description.get('1.0', END)
        maintenanceData.plants = self.selectedPlants
        
        maintenanceData.save()

        texto = f"El mantenimiento ha sido registrado con id {maintenanceData.id}."
        messagebox.showinfo(title='Mantenimiento registrado', message=texto)
        self.displayMaintenance(maintenanceData.id)

    def asignarActividad(self):
        #Get activity
        newActivity = actividades.Activity(id = self.tablaActividadesAsignadas.focus(), assigned= True)
        if newActivity not in self.newMaintenance.activities:
            self.newMaintenance.activities.append(newActivity)
            self.newMaintenance.activities.sort(key=getPlant)

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
        self.newMaintenance.date = self.cal.selection_get()
        self.newMaintenance.status = self.estado.get()
        self.newMaintenance.responsible = empleados.ver()[self.responsible.current()][0]
        self.newMaintenance.description = self.description.get('1.0',END)
        self.newMaintenance.type = mantenimientos.Preventive
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
            self.noProgramados = mantenimientos.buscarNoProgramados()
            print(f"Starting to schedule maintenances...")
            for i in self.noProgramados:
                fecha = i[1].split('/')
                fecha = date(int(fecha[2]), int(fecha[1]), int(fecha[0]))
                #Duplicar el mantenimiento
                mantenimientos.nuevo(fecha+timedelta(days=int(i[6])), 'Programado', i[3], i[4], i[5], i[6])
                print(f"    The maintenance was registered with id: {mantenimientos.ultimoMantenimiento()}")
                #Duplicar actividades
                for j in mantenimientos.buscarActividades(i[0]):
                    mantenimientos.agregarActividad(mantenimientos.ultimoMantenimiento(), j[2])
                    print(f"        Activity added to maintenance")
                mantenimientos.editar(i[0], fecha, 'Realizado Programado', i[3], i[4], i[5], i[6])
            print(f"{len(self.noProgramados)} maintenances registered succesfully")
            texto = f"Se han programado {len(self.noProgramados)} mantenimientos con éxito."
            messagebox.showinfo(title='Mantenimientos programados', message=texto)    
        else:
            mant = mantenimientos.Maintenance()
            mant.findById(id)
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
            select = mantenimientos.Maintenance()
            select.findById(id)
            select.status = mantenimientos.Done
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

        sel = mantenimientos.Maintenance(id = id)

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
        Label(self.info, text='Asignado a '+empleados.buscar(sel.responsible)[2],fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=30)
        #Label Tipo de mantenimiento
        Label(self.info, text='Mantenimiento '+sel.type,fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=60)
        if sel.type == 'Preventivo':
            Label(self.info, text='Repetir cada '+str(sel.repeat)+' días',fg='#666666', bg="#ffffff", font=("Segoe UI", "10", "normal")).place(x=0, y=90)
        #Label descripción mantenimiento
        Label(self.info, text=sel.description, bg="#ffffff", font=("Segoe UI", "10", "normal"), wraplength=root.winfo_width()*0.18, justify='left').place(x=0, y=120)
        #Boton realizar
        if sel.status == 'Programado':
            Button(self.info, text='Realizar', font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.realizarMantenimiento(id)).place(x=0, y=root.winfo_height()-150)
        #Boton Programar
        if sel.status == mantenimientos.Done and sel.next == None and sel.type == 'Preventivo':
            Button(self.info, text='Programar', font=("Segoe UI", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.programar(id)).place(x=0, y=root.winfo_height()-150)
        #Boton cancelar
        if sel.status != mantenimientos.Cancelled:
            Button(self.info, text='Cancelar', font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.cancelarMantenimiento(sel)).place(x=70, y=root.winfo_height()-150)
        #Delete Button
        if sel.status == mantenimientos.Cancelled:
            Button(self.info, text='Eliminar', font=("Segoe UI", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.eliminarMantenimiento(sel)).place(x=0, y=root.winfo_height()-150)

        if sel.type == mantenimientos.Preventive:
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
                thisPlant = equipos.buscar(plant[0].plant.id)
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
        
        employerList = empleados.getAll() 
        
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
            pendingMaintenances = len(mantenimientos.findPendingMaintenances(employerId= employer.id))
            textColor= colorBlue
            Label(actualFrame, text=pendingMaintenances, fg=textColor, bg=colorGray, font=("Segoe UI", "16", "normal"), wraplength=300, justify='center').place(x=65, y=90, anchor=CENTER)
            Label(actualFrame, text='Mantenimientos\nprogramados', fg='#666666', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='center').place(x=65, y=120, anchor=CENTER)
            
            #Overdue maintenances
            overdueMaintenances = len(mantenimientos.findOverdueMaintenances(employerId= employer.id))
            if overdueMaintenances == 0: textColor = colorGreen
            elif overdueMaintenances < 3: textColor = colorBlue
            else: textColor = colorRed
            Label(actualFrame, text=overdueMaintenances, fg=textColor, bg=colorGray, font=("Segoe UI", "16", "normal"), wraplength=300, justify='center').place(x=215, y=90, anchor=CENTER)
            Label(actualFrame, text='Mantenimientos\natrasados', fg='#666666', bg=colorGray, font=("Segoe UI", "8", "normal"), wraplength=300, justify='center').place(x=215, y=120, anchor=CENTER)
            
            #Button
            Button(actualFrame, text='Ver más',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=createFunctionToDisplayEmployer(employer.id, self)).place(x=230, y=160)
            
    def displayEmployer(self, id):
        clearMainFrame()
        
        #Title
        Label(mainFrame, text='Empleados', bg="#ffffff", font=("Segoe UI", "11", "bold")).place(x=10, y=10)
        
        employer = empleados.Employer(id = id)
        
        #Button back
        Button(mainFrame, text=' ← Regresar ',font=("Segoe UI", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.main).place(x=10, y=40)
        
        #Name
        Label(mainFrame, text=employer.name, fg='#444444', bg='#ffffff', font=("Segoe UI", "16", "normal"), wraplength=300, justify='left').place(x=10, y=80)
        #Key
        Label(mainFrame, text='Clave: '+str(employer.key), fg='#777777', bg='#ffffff', font=("Segoe UI", "12", "normal"), wraplength=300, justify='left').place(x=10, y=120)
        
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
        
        maintenancesList = mantenimientos.find(employerId=employer.id, status=mantenimientos.Programmed)
        for maintenance in maintenancesList:
            mant = Frame(maintenancesFrame.scrollableFrame)
            mant.config(bg=colorGray, highlightthickness=0, highlightbackground="#eeeeee", width=root.winfo_width()/2-100, height=100)
            mant.pack(pady=10, padx=15)
            if maintenance.date < datetime.date(datetime.now()):
                actualColor = colorRed
            else:
                actualColor = colorGreen
            Frame(mant, bg=actualColor, height=100, width=3).place(x=0, y=0)
            #Titular
            Label(mant, text='Mantenimiento ID '+str(maintenance.id), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "bold"), wraplength=300, justify='left').place(x=10, y=10)
            #Date
            Label(mant, text=maintenance.date.strftime("%a %d %B %Y"), fg='#111111', bg=colorGray, font=("Segoe UI", "8", "normal")).place(x=10, y=30)
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

class Inventory():
    
    def __init__(self, parent) -> None:
        global root
        self.parent = parent
        
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
        
if __name__ == '__main__':
    aplicacion = Crm()
    root.mainloop()
