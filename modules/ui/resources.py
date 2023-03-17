from tkinter import *
import tkinter.ttk as ttk
import customtkinter
# Botón
#Button(mainFrame, text='+ Agregar equipo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.nuevo).place(x=10, y=450)



class Menu:
    
    def __init__(self, root) -> None:
        self.sidebar_frame = customtkinter.CTkFrame(root, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Emman", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.buttons = []
        self.buttons_names = []
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
    def addButton(self, text, command):

        self.buttons.append(customtkinter.CTkButton(
            master = self.sidebar_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            fg_color='transparent',
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w", 
            text = text,
            command=command,
            ))
        self.buttons_names.append(text)
        self.buttons[len(self.buttons)-1].grid(column = 0, row = len(self.buttons), sticky='ew')
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
class sectionMenu:
    def __init__(self, master, backgroundColor = "#f2f2f2", foregroundColor = "#f2f2f2") -> None:
        self.backgroundFrame = customtkinter.CTkFrame(master)
        self.backgroundFrame.grid(column = 0, row=1, pady=(0,0), padx=(20,20), sticky='new')
        self.buttons = []
        
    def addButton(self, text, command, backgroundColor = "#37abc8"):
        newButton = customtkinter.CTkButton(
            master = self.backgroundFrame, 
            text=text,
            font=("Segoe UI", 12),
            #bg=backgroundColor,
            #fg=self.foregroundColor, activeforeground= self.foregroundColor,
            #bd=0, activebackground= backgroundColor,
            #highlightthickness=0,
            #borderwidth=2,
            #relief=FLAT,
            command=command, 
            #padx=10, 
            cursor='hand2'
            )
        if backgroundColor != "#37abc8":
            newButton.configure(fg_color = backgroundColor)
        self.buttons.append(newButton)
        self.buttons[len(self.buttons)-1].grid(row = 0, column = len(self.buttons)-1, padx=10, pady=10, sticky='nsw')
        
class sectionNavigation:
    def __init__(self, master, pages, command, textLeft, textRight, backgroundColor = "#f2f2f2", foregroundColor = "#f2f2f2") -> None:
        master.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(master.winfo_width()-40)
        self.backgroundFrame = customtkinter.CTkFrame(master)
        self.backgroundFrame.configure(width=self.width, height=40)
        self.backgroundFrame.place(x=20, y=master.winfo_height()-40)
        self.buttons = []
        self.page = IntVar(master)
        self.page.set(0)
        self.pages = pages
        self.addButton(textLeft, command, left=True)
        self.addButton(textRight, command, right=True)
        self.actualPage = Label(self.backgroundFrame, text = f"1/{pages+1}", font=("Segoe UI", "10", "normal"))
        self.actualPage.grid(row = 0, column = 2)
        
    def addButton(self, text, command, backgroundColor = "#37abc8", left = None, right = None):

        self.buttons.append(Button(self.backgroundFrame, 
            text=text,
            font=("Segoe UI", "10", "normal"),
            bg=backgroundColor,
            fg=self.foregroundColor, activeforeground= self.foregroundColor,
            bd=0, activebackground= backgroundColor,
            highlightthickness=0,
            borderwidth=2,
            relief=FLAT,
            command=(lambda: self.clickButtonLeft(command)) if left else (lambda: self.clickButtonRight(command)), padx=10, cursor='arrow' if left else 'hand2',
            state='disabled' if left else 'normal'
            ))
        self.buttons[len(self.buttons)-1].grid(row = 0, column = len(self.buttons)-1, padx=5)
        
    def clickButtonLeft(self, command):
        if self.page.get() > 0:
            self.page.set(self.page.get()-1)
            self.actualPage.config(text = f"{self.page.get()+1}/{self.pages+1}")
            if self.page.get() == 0:
                self.buttons[0].config(state = 'disabled', cursor = 'arrow')
            self.buttons[1].config(state = 'normal', cursor = 'hand2')
        command()
        
    def clickButtonRight(self, command):
        if self.page.get() < self.pages:
            self.page.set(self.page.get()+1)
            self.actualPage.config(text = f"{self.page.get()+1}/{self.pages+1}")
            if self.page.get() == self.pages:
                self.buttons[1].config(state = 'disabled', cursor='arrow')
            self.buttons[0].config(state = 'normal', cursor='hand2')
        command()
        
        
class sectionInfo:
    def __init__(self, master, backgroundColor = "#f2f2f2", foregroundColor = "#000000") -> None:
        master.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(master.winfo_width()-40)
        self.backgroundFrame = Frame(master)
        self.backgroundFrame.config(width=self.width, bg = self.backgroundColor)
        self.backgroundFrame.place(x=0, y=120)
        self.data = []

    def addData(self, tittle, data, image, large = False):
        dataFrame = Frame(self.backgroundFrame)
        dataFrame.config(width=self.width/2, bg=self.backgroundColor)
        if large:
            self.data.append(True)
            dataFrame.grid(row=int(len(self.data)/2), column=0,columnspan=2,  sticky='wne', pady=1, padx=20)
        else:
            dataFrame.grid(row=int(len(self.data)/2), column=int(len(self.data)%2), sticky='wne', pady=1, padx=20)
        Label(dataFrame, image=image, width=25, height=25, anchor='n', bg=self.backgroundColor).grid(column=0, row=0, sticky='n')
        Label(dataFrame, text=tittle, bg=self.backgroundColor, font=("Segoe UI", "11", "bold")).grid(column=1, row=0)
        Label(dataFrame, text=data, bg=self.backgroundColor, font=("Segoe UI", "11", "normal")).grid(column=2, row=0)
        self.data.append(dataFrame)
        
class SearchBar:
    def __init__(self, master, backgroundColor = "#f2f2f2", foregroundColor = "#000000") -> None:
        master.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(master.winfo_width()-40)
        self.backgroundFrame = Frame(master)
        self.backgroundFrame.config(width=self.width, bg = self.backgroundColor)
        self.backgroundFrame.place(x=20, y=120)
        self.filters=[]
        
    def addSearchBar(self, variable, command):
        searchFrame = Frame(self.backgroundFrame)
        searchFrame.config(bg='#ffffff', width=self.width, height=30)
        searchFrame.grid(row=0, column=0, columnspan=4)
        frame = Frame(searchFrame)
        frame.config(bg='#ffffff', width=self.width, height=30)
        frame.place(x=0, y=0)
        global searchImg 
        searchImg= PhotoImage(file='img/search.png')
        Label(frame, image = searchImg, bd=0, width=12, heigh=12).grid(column=0, row=0, padx=5, pady=5)
        searchEntry = Entry(frame, width=int(self.width/6)-40, textvariable=variable, font=("Segoe UI", "10", "normal"), foreground="#222222", background='#ffffff', highlightthickness=0, relief=FLAT)
        searchEntry.grid(column=1, row=0, padx=5, pady=5)
        searchEntry.bind('<Key>', command)
        
    def addFilter(self, tittle, values, command, image = None):
        filterFrame = Frame(self.backgroundFrame)
        filterFrame.config(width=self.width/4, bg=self.backgroundColor)
        filterFrame.grid(row=int(len(self.filters)/4)+1, column=int(len(self.filters)%4), sticky='wne', pady=10, padx=20)
        if image:
            Label(filterFrame, image=image, width=25, height=25, anchor='n', bg=self.backgroundColor).grid(column=0, row=0, sticky='n')
        Label(filterFrame, text=tittle, bg=self.backgroundColor, font=("Segoe UI", "11", "bold")).grid(column=1, row=0)
        combobox = ttk.Combobox(filterFrame, state='readonly',values=values)
        combobox.bind("<<ComboboxSelected>>", command)
        combobox.grid(column=2, row=0)
        self.filters.append(filterFrame)
        return combobox
        
class Info(sectionInfo):
    def __init__(self, master, backgroundColor="#f2f2f2", foregroundColor="#000000") -> None:
        master.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(master.winfo_width()-40)
        self.backgroundFrame = Frame(master)
        self.backgroundFrame.config(width=self.width, bg = self.backgroundColor)
        self.backgroundFrame.place(x=20, y=20)
        self.data = []
   
class Title(customtkinter.CTkLabel):
    def __init__(self, master, **kwargs):   
        super().__init__(master, **kwargs)
        self.configure(font = customtkinter.CTkFont(family = "Segoe UI", size = 16, weight = 'bold'))
        
class Metric(customtkinter.CTkLabel):
    def __init__(self, master, **kwargs):   
        super().__init__(master, **kwargs)
        self.configure(font = customtkinter.CTkFont(family = "Segoe UI", size = 36))
        
        
def AddTittle(mainFrame, tittleText, subtittleText = None) -> None:
    frame = customtkinter.CTkFrame(mainFrame)
    frame.grid(column=0, row=0, padx=(20,20), pady=(20,10), sticky='new')
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure((0, 1), weight=1)
    customtkinter.CTkLabel(master = frame, text=tittleText,
                           font=("Segoe UI Bold", 16, "bold")
                           ).grid(row=0, column=1, padx=(20,0), pady=(10,10), sticky='nws')
    if(subtittleText):
        customtkinter.CTkLabel(frame, text=subtittleText, font=("Segoe UI", "10", "bold")).grid(row=1, column=1, padx=(20,0), pady=(20,20), sticky='nws')