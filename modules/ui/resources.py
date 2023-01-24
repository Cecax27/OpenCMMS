from tkinter import *

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