from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import empleados
import equipos
import actividades
import areas
import mantenimientos
from tkcalendar import Calendar
from datetime import datetime
from datetime import date
from datetime import timedelta

#Constantes-----
colorGreen = '#37c842'
colorRed = '#c83737'
colorBlue = '#37abc8'
colorGray = '#f2f2f2'

#Funciones--------
def crearTabla(encabezados, ids, anchos, matriz, lugar, altura, funcion):
    """Crea una tabla con un Treeview de Tkinter.
    Parámetros: matriz = matriz de la tabla,
    lugar = widget padre de Tkinter,
    altura = altura de la tabla"""

    if len(matriz) == 0:
        return Label(text='No hay datos')

    nuevaTabla = ttk.Treeview(lugar, height = altura, columns = encabezados[1:], selectmode = 'browse')
    nuevaTabla.tag_configure("color", background = "#ffffff", font=("Noto Sans", "9", "normal"))
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

def clearMainFrame():
    global mainFrame
    global root

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
        self.root.title('Gestión de Mantenimiento GMAO Emman')

        #Objetos--------
        self.objetoDepartamentos = Departamentos()
        self.objetoAreas = Areas()
        self.objetoEquipos = Equipos(self)
        self.objetoActividades = Actividades()
        self.objetoMantenimientos = Mantenimientos(self)

        #Menu---------------------
        root.update()
        global menuFrame
        menuFrame = Frame(root)
        menuFrame.config(width=root.winfo_width(), height=50, bg="#37abc8")
        menuFrame.grid(column=0, row=0)

        colorButton = "#37abc8"

        Button(menuFrame, 
            text='Mantenimientos',
            font=("Noto Sans", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.mantenimientos
            ).place(x=0.25*root.winfo_width()/6, y=4)

        Button(menuFrame, 
            text='Equipos',
            font=("Noto Sans", "11", "normal"),
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
            font=("Noto Sans", "11", "normal"),
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
            font=("Noto Sans", "11", "normal"),
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
            font=("Noto Sans", "11", "normal"),
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
            font=("Noto Sans", "11", "normal"),
            bg=colorButton,
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            width=12,
            borderwidth=5,
            relief=FLAT,
            command=self.empleados
            ).place(x=5.25*root.winfo_width()/6, y=4)

        global barraMenu
        barraMenu = BarraMenu(self)

        global mainFrame
        mainFrame = Frame(self.root)
        mainFrame.config(bg="#ffffff",
        width=root.winfo_width(),
        height=root.winfo_height()-50)
        mainFrame.grid(column=0, row=1)

        self.mainframe = mainFrame

        Label(self.mainframe, 
            text=datetime.now().strftime('%d/%m/%Y'),
            bg="#ffffff",
            font=("Noto Sans", "11", "normal")).place(x=root.winfo_width()-100, y=10)
             

    def mantenimientos(self):
        global mainFrame
        
        clearMainFrame()

        #Título
        Label(mainFrame, text='Mantenimientos', bg="#ffffff", font=("Noto Sans", "11", "bold")).place(x=10, y=10)

        #Botones
        Button(mainFrame, text='+ Mantenimiento preventivo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.objetoMantenimientos.nuevo).place(x=10, y=40)

        Button(mainFrame, text='+ Mantenimiento correctivo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=self.objetoMantenimientos.newCorrective).place(x=200, y=40)

        Button(mainFrame, text='Eliminar',command=lambda: self.objetoMantenimientos.eliminarMantenimiento(self.tabla.focus())).place(x=100, y=800)

        Button(mainFrame, text='Ver más', command=lambda: self.objetoMantenimientos.displayMaintenance(tabla.focus())).place(x=200, y=800)

        lista = mantenimientos.getAll()

        allMaintenances = Frame(mainFrame, highlightthickness=1, bg="#ffffff")
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
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i.id), fg='#111111', bg=colorGray, font=("Noto Sans", "8", "bold"), wraplength=300, justify='left').place(x=10, y=10)
            #Date
            Label(mant, text=i.date.strftime("%a %d %B %Y"), fg='#111111', bg=colorGray, font=("Noto Sans", "8", "normal")).place(x=10, y=30)
            #Status
            if i.status == 'Realizado' or i.status == 'Realizado Programado':
                color = colorGreen
            elif i.status == 'Programado':
                color = colorBlue
            elif i.status == 'Cancelado':
                color = colorRed
            Label(mant, text=i.status, fg=color, bg=colorGray, font=("Noto Sans", "8", "normal"), wraplength=300, anchor="e", width=20).place(x=root.winfo_width()/2-255, y=10)
            #type
            Label(mant, text='Matenimiento '+i.type, fg='#333333', bg=colorGray, font=("Noto Sans", "8", "bold")).place(x=140, y=30)
            #Descripción
            Label(mant, text=i.description, fg='#333333', bg=colorGray, font=("Noto Sans", "8", "normal"), wraplength=root.winfo_width()/2-190, justify='left').place(x=10, y=50)
            #Botón
            Button(mant, text='Ver más',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i.id, self.objetoMantenimientos)).place(x=root.winfo_width()/2-170, y=60)

        canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        lista = mantenimientos.buscarAtrasados(date.today())
        listaId = []
        for mantenimiento in lista:
            lista[lista.index(mantenimiento)] = [mantenimiento[4], mantenimiento[1], mantenimiento[2], empleados.buscar(mantenimiento[3])[2]]
            listaId.append(mantenimiento[0])

        Label(mainFrame, text='Mantenimientos programados para hoy:', bg="#ffffff", font=("Noto Sans", "11", "normal")).place(x=500, y=30)

        if len(lista) == 0:
            Label(mainFrame, text='No hay mantenimientos pendientes.', fg="#aad400" ,bg="#ffffff", font=("Noto Sans", "11", "normal")).place(x=700, y=60)
        else:
            tabla2 = crearTabla(['Descripción','Fecha','Estado','Responsable'],listaId,[200, 70, 100, 100], lista, mainFrame, 10, '')
            tabla2.place(x=700, y=60)

            Button(mainFrame, text='Marcar como realizado', command=lambda: objetoMantenimientos.realizarMantenimiento(self.tabla.focus())).place(x=700, y=300)

            Button(mainFrame, text='Marcar como cancelado', command=lambda: self.cancelarMantenimiento(self.tabla.focus())).place(x=900, y=300)

            Button(mainFrame, text='Ver más',command=lambda: self.objetoMantenimientos.displayMaintenance(tabla2.focus())).place(x=1100, y=300)

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

    def empleados(self):
        self.mainframe.destroy()
        self.mainframe = Frame(self.root, relief=RIDGE, borderwidth=2)
        self.mainframe.grid(column=0, row=1)

        lblMain = Label(self.mainframe, text='Empleados')
        lblMain.grid(column=0, row=0)

        listaEmpleados = empleados.ver()
        self.tabla = ttk.Treeview(self.mainframe, height = 10, columns = 2, selectmode = 'browse')
        self.tabla.grid(row = 2, column = 0, columnspan = 3)
        self.tabla.heading('#0', text='Código', anchor=CENTER)
        self.tabla.heading('#1', text='Nombre', anchor=CENTER)
        for x in listaEmpleados:
            self.tabla.insert('', 0, values = (x[2],), text = x[1])

        self.btnuevo =  Button(self.mainframe, text='Nuevo',command=self.empleadosNuevo)
        self.btnuevo.grid(column=0,row=3)

        self.bteditar =  Button(self.mainframe, text='Editar',command=self.empleadosEditar)
        self.bteditar.grid(column=1,row=3)

        self.btborrar =  Button(self.mainframe, text='Eliminar',command=self.empleadosBorrar)
        self.btborrar.grid(column=2,row=3)

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

    def empleadosEditar(self):
        self.root2 = Tk()

    def empleadosBorrar(self):
        pass

    def empleadosGuardar(self):
         empleados.new(self.clave.get(), self.nombre.get())
         self.ventana.destroy()
         self.empleados()



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

        helpmenu = Menu(self.menubar)



        #Etiquetas
        self.menubar.add_cascade(label="Archivo", menu=filemenu)
        self.menubar.add_cascade(label="Editar", menu=editmenu)
        self.menubar.add_cascade(label="Departamentos y areas", menu=menuAreas)
        self.menubar.add_cascade(label="Equipos", menu=menuEquipos)
        self.menubar.add_cascade(label="Actividades", menu=menuActividades)
        self.menubar.add_cascade(label="Mantenimientos", menu=menuMantenimientos)
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
        self.nombre.insert(0, resultado[0][1])
        #Descripcion
        self.descripcion.delete(0, "end")
        self.descripcion.insert(0, resultado[0][2])
        #Responsable
        self.responsable.current(self.listaNombres.index(resultado[0][3]))
        #Departamento
        self.departamento.current(self.listaNombresDepartamentos.index(resultado[0][4]))

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

        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Noto Sans", "11", "bold")).place(x=10, y=10)

        #Departamento------------
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        
        Label(mainFrame, text='Departamento', fg='#666666', bg='#ffffff', font=("Noto Sans", "10", "normal")).place(x=10, y=40)
        self.departamento2 = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento2.bind("<<ComboboxSelected>>", self.editarActualizarAreas)
        self.departamento2.place(x=10, y=70)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', fg='#666666', bg='#ffffff', font=("Noto Sans", "10", "normal")).place(x=10, y=110)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.editarActualizarEquipos)
        self.area.place(x=10, y=140)

        #Tabla de equipos-----------------------
        Label(mainFrame, text='Equipos', fg='#666666', bg='#ffffff', font=("Noto Sans", "10", "normal")).place(x=10, y=180)
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

        Button(mainFrame, text='+ Agregar equipo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.nuevo).place(x=10, y=450)

        self.info = Frame(mainFrame)
        self.info.config(bg=colorGray, width=root.winfo_width()-250, height=root.winfo_height()-50)
        self.info.place(x=250, y=0)

        Label(self.info, text='No se ha seleccionado ningún equipo', bg=colorGray, font=("Noto Sans", "11", "bold")).place(x=10, y=10)

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
        Label(self.info, text=select[1], bg=colorGray, font=("Noto Sans", "10", "bold"), wraplength=400, justify='left').place(x=10, y=10)
        Label(self.info, text=select[2], bg=colorGray, font=("Noto Sans", "9", "normal"), wraplength=400, justify='left').place(x=10, y=40)

        #Ultimo mantenimiento realizado
        Label(self.info, text="Último mantenimiento", fg='#666666', bg=colorGray, font=("Noto Sans", "9", "normal")).place(x=10, y=80)
        text = mantenimientos.ultimoMantenimientoRealizado(select[0])
        if text == None:
            text = 'No se ha hecho ninguno'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Noto Sans", "9", "bold")).place(x=140, y=80)

        #Ultimo mantenimiento programado
        Label(self.info, text="Siguiente mantenimiento programado", fg='#666666', bg=colorGray, font=("Noto Sans", "9", "normal")).place(x=400, y=80)
        text = mantenimientos.ultimoMantenimientoProgramado(select[0])
        if text == None:
            text = 'No hay mantenimiento programado'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Noto Sans", "9", "bold")).place(x=620, y=80)

        #Botones
        Button(self.info, text='Editar',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.editar(select[0])).place(x=root.winfo_width()-500, y=10)

        Button(self.info, text='Eliminar',font=("Noto Sans", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.eliminar(select[0])).place(x=root.winfo_width()-445, y=10)

        Button(self.info, text='Asignar actividades',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command = lambda: self.asignarActividades(select[0], mantFrame)).place(x=root.winfo_width()-380, y=10)

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
            #mant.place(x=10+selectMantenimientos.index(i)*260, y=0)
            mant.pack()
            #Titular
            Label(mant, text='Mantenimiento ID '+str(i[0]), fg='#111111', bg=colorGray, font=("Noto Sans", "8", "bold"), wraplength=180, justify='left').place(x=10, y=10)
            Label(mant, text=i[1], fg='#111111', bg=colorGray, font=("Noto Sans", "8", "normal")).place(x=10, y=30)
            Label(mant, text=i[2], fg='#111111', bg=colorGray, font=("Noto Sans", "8", "normal"), wraplength=120, justify='right').place(x=100, y=30)
            #Descripción
            Label(mant, text='Matenimiento '+i[5], fg='#333333', bg=colorGray, font=("Noto Sans", "8", "bold")).place(x=10, y=60)
            Label(mant, text=i[4], fg='#333333', bg=colorGray, font=("Noto Sans", "8", "normal"), wraplength=230, justify='left').place(x=10, y=80)
            #Botón
            Button(mant, text='Ver más',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i[0], self)).place(x=180, y=200)

        v.config(command=mantFrame.xview)

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
        nombre = Entry(self.info, font=("Noto Sans", "10", "bold"), bg='#ffffff', fg="#000000", highlightthickness=0, borderwidth=2, relief=FLAT, width=30)
        nombre.insert(0,select[1])
        nombre.place(x=10, y=10)

        #Descripcion-------------
        descripcion = Entry(self.info, font=("Noto Sans", "9", "normal"), bg='#ffffff', fg="#000000", highlightthickness=0, borderwidth=2, relief=FLAT, width=100)
        descripcion.insert(0,select[2])
        descripcion.place(x=10, y=40)

        #Ultimo mantenimiento realizado
        Label(self.info, text="Último mantenimiento", fg='#666666', bg=colorGray, font=("Noto Sans", "9", "normal")).place(x=10, y=80)
        text = mantenimientos.ultimoMantenimientoRealizado(select[0])
        if text == None:
            text = 'No se ha hecho ninguno'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Noto Sans", "9", "bold")).place(x=140, y=80)

        #Ultimo mantenimiento programado
        Label(self.info, text="Siguiente mantenimiento programado", fg='#666666', bg=colorGray, font=("Noto Sans", "9", "normal")).place(x=400, y=80)
        text = mantenimientos.ultimoMantenimientoProgramado(select[0])
        if text == None:
            text = 'No hay mantenimiento programado'
        else:
            text = text[1]
        Label(self.info, text=text, fg='#666666', bg=colorGray, font=("Noto Sans", "9", "bold")).place(x=620, y=80)

        #Botones
        Button(self.info, text='Guardar',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.editarGuardar(idEquipo,nombre.get(), descripcion.get())).place(x=root.winfo_width()-510, y=10)

        Button(self.info, text='Eliminar',font=("Noto Sans", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=lambda:self.eliminar(select[0])).place(x=root.winfo_width()-445, y=10)

        Button(self.info, text='Asignar actividades',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command = lambda: self.asignarActividades(select[0], mantFrame)).place(x=root.winfo_width()-380, y=10)

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
            Label(mant, text='Mantenimiento ID '+str(i[0]), fg='#111111', bg=colorGray, font=("Noto Sans", "8", "bold"), wraplength=180, justify='left').place(x=10, y=10)
            Label(mant, text=i[1], fg='#111111', bg=colorGray, font=("Noto Sans", "8", "normal")).place(x=10, y=30)
            Label(mant, text=i[2], fg='#111111', bg=colorGray, font=("Noto Sans", "8", "normal"), wraplength=120, justify='right').place(x=100, y=30)
            #Descripción
            Label(mant, text='Matenimiento '+i[5], fg='#333333', bg=colorGray, font=("Noto Sans", "8", "bold")).place(x=10, y=60)
            Label(mant, text=i[4], fg='#333333', bg=colorGray, font=("Noto Sans", "8", "normal"), wraplength=230, justify='left').place(x=10, y=80)
            #Botón
            Button(mant, text='Ver más',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT,command=crearFuncion(i[0], self)).place(x=180, y=200)

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
        Label(self.info, text='Actividades disponibles',fg='#111111', bg=colorGray, font=("Noto Sans", "8", "bold"), wraplength=180, justify='left').place(x=10, y=150)
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
        Button(self.info, text='Asignar',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = lambda:self.asignarActividad(self.tablaActividades.focus(),id)).place(x=10, y=420)

        #Tabla de actividades asignadas-------------
        Label(self.info, text='Actividades asignadas',fg='#111111', bg=colorGray, font=("Noto Sans", "8", "bold"), wraplength=180, justify='left').place(x=root.winfo_width()/2-150, y=150)
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
        Button(self.info, text='Eliminar',font=("Noto Sans", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command = lambda:self.eliminarActividadAsignada(self.tablaActividadesAsignadas.focus())).place(x=root.winfo_width()/2-150, y=420)
   
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
            self.tabla.insert('', 0,id=x[0], text = x[1], values =x[2])

    def actualizarActividades(self, *event):
        print("Llegue aqui")
        id = self.tabla.focus()
        self.listaActividadesAsignadas = actividades.buscarPorEquipo(id)
        print(self.listaActividadesAsignadas)
        if len(self.listaActividadesAsignadas) < 1:
            self.listaActividadesAsignadas =(['','Equipo sin actividades'],)
        self.tablaActividadesAsignadas.delete(*self.tablaActividadesAsignadas.get_children())        
        for x in self.listaActividadesAsignadas:
            print(x)
            self.tablaActividadesAsignadas.insert('', 0, id= x[0], values = x[2], text = x[1])

    def nuevo(self):
        global mainFrame
        clearMainFrame()
        
        #Tittle
        Label(mainFrame, text='Mantenimiento preventivo', bg="#ffffff", font=("Noto Sans", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Noto Sans", "9", "normal"),bg="#ffffff", selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')))
        self.cal.place(x=10, y=70)

        #Estado------------
        self.listaEstados=[mantenimientos.Done, mantenimientos.Programmed]
        Label(mainFrame, text='Estado', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=280)
        self.estado = ttk.Combobox(mainFrame, state='readonly',values=self.listaEstados)
        self.estado.place(x=10, y=310)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=340)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = empleados.ver('nombre'))
        self.responsible.place(x=10, y=370)

        #Repeat
        self.repeatOn = Checkbutton(mainFrame, bg="#ffffff", text="Repetir cada", font=("Noto Sans", "10", "normal"))
        self.repeatOn.place(x=10, y=400)
        self.repeat = Entry(mainFrame, width=5, highlightthickness=2)
        self.repeat.place(x=120, y=400)
        Label(mainFrame, text='días', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=160, y=400)

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=430)
        self.description = Text(mainFrame, width=40, height=9, font=("Noto Sans", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.place(x=10, y=460)

        Button(mainFrame, text='Guardar',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.saveCorrective).place(x=root.winfo_width()-100, y=10)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=400, y=10)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=400, y=40)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=600, y=10)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=40)

        #Plants table
        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=400, y=80)
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
        Label(mainFrame, text='Actividades', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=400, y=340)
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
        #Button(self.frameA, text='+', command = self.asignarActividad).grid(row=1, column=7)

        #Botón para eliminar actividad asignada
        #Button(self.frameA, text='-', command = self.eliminarActividadAsignada).grid(row=2, column=7)

        #Tabla de equipos
        # self.tablaEquipos = ttk.Treeview(self.frameA, height = 10, columns = ('nombre','descripcion'), selectmode = 'browse')
        # self.tablaEquipos.heading('#0', text='Id', anchor=CENTER)
        # self.tablaEquipos.heading('#1', text='Nombre', anchor=CENTER)
        # self.tablaEquipos.heading('#2', text='Descripción', anchor=CENTER)
        # self.tablaEquipos.column('#0', minwidth=0, width=40)
        # self.tablaEquipos.column('#1', minwidth=0, width=120)
        # self.tablaEquipos.column('#2', minwidth=0, width=120)

        # lista = [('','Seleccione un area y departamento','','','')]
        # for x in lista:
        #     self.tabla.insert('', 0, values = (x[1],x[4]), text = x[0],tags=("mytag",))

        # self.tablaEquipos.grid(row=0, column=8, pady=5, padx=5, rowspan=3)
        # self.listaEquiposSeleccionados = []
        # self.listaActividadesSeleccionadas = []

    def newCorrective(self):
        global mainFrame
        clearMainFrame()

        self.selectedPlants = []

        #Tittle
        Label(mainFrame, text='Mantenimiento correctivo', bg="#ffffff", font=("Noto Sans", "11", "bold")).place(x=10, y=10)

        #Date
        Label(mainFrame, text='Fecha', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=40)
        today = datetime.now()
        self.cal = Calendar(mainFrame, font=("Noto Sans", "9", "normal"),bg="#ffffff", selectmode='day', year=int(today.strftime('%Y')), month = int(today.strftime('%m')), day = int(today.strftime('%d')))
        self.cal.place(x=10, y=70)

        #Responsible
        Label(mainFrame, text='Responsable', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=280)
        self.responsible = ttk.Combobox(mainFrame, state = 'readonly', values = empleados.ver('nombre'))
        self.responsible.place(x=10, y=310)

        #Description
        Label(mainFrame, text='Descripción', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=10, y=350)
        self.description = Text(mainFrame, width=40, height=13, font=("Noto Sans", "9", "normal"), borderwidth=2, relief=FLAT, highlightbackground="#777777", highlightthickness=1)
        self.description.place(x=10, y=380)

        Button(mainFrame, text='Guardar',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.saveCorrective).place(x=root.winfo_width()-100, y=10)

        #Departamento
        self.listaDepartamentos = areas.getDepartamentos()
        self.listaNombresDepartamentos=[]
        for x in self.listaDepartamentos:
            self.listaNombresDepartamentos.append(x[1])
        Label(mainFrame, text='Departamento', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=400, y=10)
        self.departamento = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresDepartamentos)
        self.departamento.bind("<<ComboboxSelected>>", self.ActualizarAreas)
        self.departamento.place(x=400, y=40)

        #Area
        self.listaNombresAreas=[]
        Label(mainFrame, text='Área', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=600, y=10)
        self.area = ttk.Combobox(mainFrame, state='readonly',values=self.listaNombresAreas)
        self.area.bind("<<ComboboxSelected>>", self.ActualizarEquipos)
        self.area.place(x=600, y=40)

        #Plants table
        Label(mainFrame, text='Equipos', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=400, y=80)
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

        Button(mainFrame, text='Seleccionar equipo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.selectPlant).place(x=400, y=350)

        #Plants table
        Label(mainFrame, text='Equipos seleccionados', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=800, y=80)
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

        Button(mainFrame, text='Deseleccionar equipo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.deselectPlant).place(x=800, y=350)

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
        #Obtener equipo
        id = self.tabla.focus()
        text = self.tabla.item(id, option='text')
        equipoNuevo = equipos.buscar(text)
        if not equipoNuevo in self.listaEquiposSeleccionados:
            self.listaEquiposSeleccionados.append(equipoNuevo)

        #Obtener actividad
        id = self.tablaActividadesAsignadas.focus()
        text = self.tablaActividadesAsignadas.item(id, option='text')
        actividadNueva = actividades.buscarActividadAsignada(text)
        if not actividadNueva in self.listaActividadesSeleccionadas:
            self.listaActividadesSeleccionadas.append(actividadNueva)

        #Actualizar tabla
        if len(self.listaEquiposSeleccionados) == 0:
            self.listaEquiposSeleccionados = [[' ','Sin equipos',' ']]
        self.tablaEquipos.delete(*self.tablaEquipos.get_children())
        
        for x in self.listaEquiposSeleccionados:
            item = self.tablaEquipos.insert('', 0, values = (x[1],x[2]), text = x[0],tags=("mytag",))
            #print(self.listaActividadesSeleccionadas)
            for y in self.listaActividadesSeleccionadas:
                if y[4] == x[0]:
                    self.tablaEquipos.insert(item, 0, text=y[0], values=(y[1],y[2]), iid=y[0])

    def eliminarActividadAsignada(self):
        id = self.tablaEquipos.focus()
        actividadBorrar = actividades.buscarActividadAsignada(id)[0]
        self.listaActividadesSeleccionadas.pop(self.listaActividadesSeleccionadas.index(actividadBorrar))

        #Actualizar tabla
        if len(self.listaEquiposSeleccionados) == 0:
            self.listaEquiposSeleccionados = [[' ','Sin equipos',' ']]
        self.tablaEquipos.delete(*self.tablaEquipos.get_children())
        
        for x in self.listaEquiposSeleccionados:
            item = self.tablaEquipos.insert('', 0, values = (x[1],x[2]), text = x[0],tags=("mytag",))
            #print(self.listaActividadesSeleccionadas)
            for y in self.listaActividadesSeleccionadas:
                if y[4] == x[0]:
                    self.tablaEquipos.insert(item, 0, text=y[0], values=(y[1],y[2]), iid=y[0])

    def nuevoGuardar(self):
        fecha = self.cal.selection_get()
        responsable = self.listaEmpleados[self.responsable.current()][0]
        mantenimientos.nuevo(fecha, self.estado.get(), responsable, self.comentario.get('1.0',END), self.tipo.get(), self.tiempo.get())
        id = mantenimientos.ultimoMantenimiento()
        for x in self.listaActividadesSeleccionadas:
            mantenimientos.agregarActividad(id, x[0])
        texto = 'El mantenimiento ha sido registrado.'
        messagebox.showinfo(title='Mantenimiento registrado', message=texto)
        self.ventana.destroy()

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

    def cancelarMantenimiento(self, id):
        if id == '':
            messagebox.showwarning(title='No hay nada seleccionado', message='Seleccione un mantenimiento.')
        else:
            select = mantenimientos.buscar(id)
            fechaMant = select[1].split('/')
            fechaMant = date(int(fechaMant[2]), int(fechaMant[1]), int(fechaMant[0]))
            mantenimientos.editar(id, fechaMant, 'Cancelado', select[3], select[4], select[5], select[6])
            messagebox.showinfo(title='Editado con éxito', message='El mantenimiento ha sido modificado correctamente.')

    def eliminarMantenimiento(self, id):
        if id == '':
            messagebox.showwarning(title='No hay nada seleccionado', message='Seleccione un mantenimiento.')
        else:
            select = mantenimientos.buscar(id)[0]
            if messagebox.askyesno(title='Eliminar', message='¿En verdad desea eliminar el mantenimiento?'):
                actividades = mantenimientos.buscarActividades(id)
                for i in actividades:
                    mantenimientos.eliminarActividad(i[0])
                mantenimientos.eliminar(id)
                messagebox.showinfo(title='Eliminado', message='El registro fue eliminado correctamente.')

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
            font=("Noto Sans", "11", "bold")).place(x=10, y=10)

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
        Label(self.info, text=sel.status+text+sel.date.strftime('%d/%m/%Y'),fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=0)
        #Label responsable
        Label(self.info, text='Asignado a '+empleados.buscar(sel.responsible)[2],fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=30)
        #Label Tipo de mantenimiento
        Label(self.info, text='Mantenimiento '+sel.type,fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=60)
        if sel.type == 'Preventivo':
            Label(self.info, text='Repetir cada '+str(sel.repeat)+' días',fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=90)
        #Label descripción mantenimiento
        Label(self.info, text=sel.description, bg="#ffffff", font=("Noto Sans", "11", "normal"), wraplength=root.winfo_width()*0.18, justify='left').place(x=0, y=120)
        #Boton realizar
        if sel.status == 'Programado':
            Button(self.info, text='Realizar', font=("Noto Sans", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.realizarMantenimiento(id)).place(x=0, y=root.winfo_height()-150)
        #Boton Programar
        if sel.status == mantenimientos.Done and sel.next == None and sel.type == 'Preventivo':
            Button(self.info, text='Programar', font=("Noto Sans", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.programar(id)).place(x=0, y=root.winfo_height()-150)
        #Boton cancelar
        Button(self.info, text='Cancelar', font=("Noto Sans", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.cancelarMantenimiento(id)).place(x=70, y=root.winfo_height()-150)

        if sel.type == mantenimientos.Preventive:
            listActivities = []            
            for activity in sel.activities:
                if len(listActivities) == 0:
                    listActivities.append([])
                    listActivities[0].append(activity)
                else:
                    grouped = False
                    for plant in listActivities:
                        if activity.plant == plant[0].plant:
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
                
                thisPlant = equipos.buscar(plant[0].plant)
                area = areas.buscar(thisPlant[3])
                Label(framePlant, text=area[4], fg='#666666', bg="#f2f2f2", font=("Noto Sans", "9", "normal")).place(x=10, y=10)
                Label(framePlant, text=area[1], fg='#666666', bg="#f2f2f2", font=("Noto Sans", "9", "bold")).place(x=10+len(area[4]*10), y=10)
                Label(framePlant, text=thisPlant[1], fg='#000000', bg="#f2f2f2", font=("Noto Sans", "10", "bold")).place(x=10, y=40)
                Label(framePlant, text=thisPlant[2], fg='#000000', bg="#f2f2f2", font=("Noto Sans", "9", "normal"), wraplength=180, justify='left').place(x=10, y=70)
                for activity in plant:
                    #Label nombre actividad
                    Label(framePlant, text=activity.name, fg='#111111', bg="#f2f2f2", font=("Noto Sans", "8", "bold"), wraplength=180, justify='left').place(x=10, y=110+plant.index(activity)*60)
                    #Label descripcion actividad
                    Label(framePlant, text=activity.description, fg='#111111', bg="#f2f2f2", font=("Noto Sans", "8", "normal"), wraplength=180, justify='left').place(x=10, y=130+plant.index(activity)*60)
                


        # for i in selActivities:
        #     frameActivity = Frame(mainFrame, borderwidth=5)
        #     frameActivity.place(x=500, y=selActivities.index(i)*80)
        #     activity = actividades.buscarActividadAsignada(i[2])
        #     plant = equipos.buscar(activity[4])
        #     area = areas.buscar(plant[3])
        #     Label(frameActivity, text=area[4]+'>'+area[1]+'>'+str(plant[1])).grid(column=0, row = 0)
        #     Label(frameActivity, text=activity[1]).grid(column=0, row=1)
        #     Label(frameActivity, text=activity[2]).grid(column=0, row=2)

        

if __name__ == '__main__':
    aplicacion = Crm()
    root.mainloop()
