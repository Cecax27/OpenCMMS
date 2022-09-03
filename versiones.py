def displayMaintenance(self, id):
        global mainFrame
        global root
        mainFrame.destroy()
        mainFrame = Frame(root)
        mainFrame.config(bg="#ffffff",
        width=root.winfo_width(),
        height=root.winfo_height()-50)
        mainFrame.grid(column=0, row=1)

        sel = mantenimientos.buscar(id)

        Label(mainFrame, 
            text='Mantenimiento ID '+str(sel[0]),
            bg="#ffffff",
            font=("Noto Sans", "11", "bold")).place(x=10, y=10)

        self.info = Frame(mainFrame)
        self.info.config(bg="#ffffff", width=root.winfo_width()*0.2, height=root.winfo_height()-50)
        self.info.place(x=10, y=50)

        #Label fecha y estado de mantenimiento
        if sel[2] == 'Programado': 
            text = ' para el '
        elif sel[2] == 'Realizado': 
            text = ' el '
        else:
            text = ' el '
        Label(self.info, text=sel[2]+text+sel[1],fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=0)
        #Label responsable
        Label(self.info, text='Asignado a '+empleados.buscar(sel[3])[2],fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=30)
        #Label Tipo de mantenimiento
        Label(self.info, text='Mantenimiento '+sel[5],fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=60)
        if sel[5] == 'Preventivo':
            Label(self.info, text='Repetir cada '+str(sel[6])+' días',fg='#666666', bg="#ffffff", font=("Noto Sans", "10", "normal")).place(x=0, y=90)
        #Label descripción mantenimiento
        Label(self.info, text=sel[4], bg="#ffffff", font=("Noto Sans", "11", "normal"), wraplength=root.winfo_width()*0.18, justify='left').place(x=0, y=120)
        #Boton realizar
        if sel[2] == 'Programado':
            Button(self.info, text='Realizar', font=("Noto Sans", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.realizarMantenimiento(id)).place(x=0, y=root.winfo_height()-150)
        #Boton Programar
        if sel[2] == mantenimientos.Done and sel[8] == None and sel[5] == 'Preventivo':
            Button(self.info, text='Programar', font=("Noto Sans", "9", "normal"), bg=colorGreen, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.programar(id)).place(x=0, y=root.winfo_height()-150)
        #Boton cancelar
        Button(self.info, text='Cancelar', font=("Noto Sans", "9", "normal"), bg=colorRed, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=lambda: self.cancelarMantenimiento(id)).place(x=70, y=root.winfo_height()-150)
        

        selActivities = mantenimientos.buscarActividades(id)
        listActivities = []
        for activity in selActivities:
            selActivities[selActivities.index(activity)] = actividades.buscarActividadAsignada(activity[2])
            
        for activity in selActivities:
            if len(listActivities) == 0:
                listActivities.append([])
                listActivities[0].append(activity)
            else:
                grouped = False
                for plant in listActivities:
                    if activity[4] == plant[0][4]:
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
            
            thisPlant = equipos.buscar(plant[0][4])
            area = areas.buscar(thisPlant[3])
            Label(framePlant, text=area[4], fg='#666666', bg="#f2f2f2", font=("Noto Sans", "9", "normal")).place(x=10, y=10)
            Label(framePlant, text=area[1], fg='#666666', bg="#f2f2f2", font=("Noto Sans", "9", "bold")).place(x=10+len(area[4]*10), y=10)
            Label(framePlant, text=thisPlant[1], fg='#000000', bg="#f2f2f2", font=("Noto Sans", "10", "bold")).place(x=10, y=40)
            Label(framePlant, text=thisPlant[2], fg='#000000', bg="#f2f2f2", font=("Noto Sans", "9", "normal"), wraplength=180, justify='left').place(x=10, y=70)
            for activity in plant:
                #Label nombre actividad
                Label(framePlant, text=activity[1], fg='#111111', bg="#f2f2f2", font=("Noto Sans", "8", "bold"), wraplength=180, justify='left').place(x=10, y=110+plant.index(activity)*60)
                #Label descripcion actividad
                Label(framePlant, text=activity[2], fg='#111111', bg="#f2f2f2", font=("Noto Sans", "8", "normal"), wraplength=180, justify='left').place(x=10, y=130+plant.index(activity)*60)
                


        # for i in selActivities:
        #     frameActivity = Frame(mainFrame, borderwidth=5)
        #     frameActivity.place(x=500, y=selActivities.index(i)*80)
        #     activity = actividades.buscarActividadAsignada(i[2])
        #     plant = equipos.buscar(activity[4])
        #     area = areas.buscar(plant[3])
        #     Label(frameActivity, text=area[4]+'>'+area[1]+'>'+str(plant[1])).grid(column=0, row = 0)
        #     Label(frameActivity, text=activity[1]).grid(column=0, row=1)
        #     Label(frameActivity, text=activity[2]).grid(column=0, row=2)