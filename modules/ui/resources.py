from tkinter import *
import tkinter.ttk as ttk
# Botón
#Button(mainFrame, text='+ Agregar equipo',font=("Noto Sans", "9", "normal"), bg=colorBlue, fg="#ffffff", highlightthickness=0, borderwidth=2, relief=FLAT, command=self.nuevo).place(x=10, y=450)

class Menu:
    
    def __init__(self, root, backgroundColor = "#555555", foregroundColor = "#eeeeee") -> None:
        
        root.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(root.winfo_width()*0.11)
        self.backgroundFrame = Frame(root)
        self.backgroundFrame.config(width=self.width, height=root.winfo_height(), bg=self.backgroundColor)
        self.backgroundFrame.grid(column=0, row=0, sticky='nswe')
        self.menuFrame = Frame(self.backgroundFrame, bg=self.backgroundColor)
        self.menuFrame.pack(fill = 'both', expand=True)
        self.buttons = []
        
    def addButton(self, text, command,):

        self.buttons.append(Button(self.menuFrame, 
            text=text,
            font=("Segoe UI", "10", "bold"),
            bg=self.backgroundColor,
            fg=self.foregroundColor, activeforeground= self.foregroundColor,
            bd=0, activebackground= self.backgroundColor,
            highlightthickness=0,
            borderwidth=5,
            relief=FLAT,
            command=command,
            anchor="w", cursor='hand2'
            ))
        self.buttons[len(self.buttons)-1].grid(column = 0, row = len(self.buttons)-1, sticky = 'ew', pady=5)
        
class sectionMenu:
    def __init__(self, master, backgroundColor = "#f2f2f2", foregroundColor = "#f2f2f2") -> None:
        master.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(master.winfo_width()-40)
        self.backgroundFrame = Frame(master)
        self.backgroundFrame.config(width=self.width, height=70, bg=self.backgroundColor)
        self.backgroundFrame.place(x=20, y=80)
        #self.menuFrame = Frame(self.backgroundFrame, bg=self.backgroundColor)
        #self.menuFrame.pack(fill = 'both', expand=True)
        self.buttons = []
        
    def addButton(self, text, command, backgroundColor = "#37abc8"):

        self.buttons.append(Button(self.backgroundFrame, 
            text=text,
            font=("Segoe UI", "10", "normal"),
            bg=backgroundColor,
            fg=self.foregroundColor, activeforeground= self.foregroundColor,
            bd=0, activebackground= backgroundColor,
            highlightthickness=0,
            borderwidth=2,
            relief=FLAT,
            command=command, padx=10, cursor='hand2'
            ))
        self.buttons[len(self.buttons)-1].grid(row = 0, column = len(self.buttons)-1, padx=5)
        
class sectionNavigation:
    def __init__(self, master, pages, command, textLeft, textRight, backgroundColor = "#f2f2f2", foregroundColor = "#f2f2f2") -> None:
        master.update()
        self.backgroundColor = backgroundColor
        self.foregroundColor = foregroundColor
        self.width = int(master.winfo_width()-40)
        self.backgroundFrame = Frame(master)
        self.backgroundFrame.config(width=self.width, height=40, bg=self.backgroundColor)
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
        
def AddTittle(mainFrame, tittleText, subtittleText = None) -> None:
    Label(mainFrame, text=tittleText, bg="#f2f2f2", font=("Segoe UI", "12", "bold")).place(x=20, y=20)
    if(subtittleText):
        Label(mainFrame, text=subtittleText, bg="#f2f2f2", font=("Segoe UI", "10", "bold")).place(x=20, y=50)