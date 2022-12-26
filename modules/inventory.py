try:
    import sql
except:
    from modules import sql
from datetime import date
from datetime import datetime
from datetime import timedelta
try:
    from modules import pdf
except:
    import pdf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

#Const-----
INPUT = "input"
OUTPUT = 'output'

MAINTENANCE = 'maintenance'
REQUISITION = 'requisition'

STATUS_DRAFT = 'borrador'
STATUS_REQUESTED = 'solicitada'
STATUS_CONFIRMED = 'confirmada'
STATUS_PARTIAL_DELIVERED = 'entregada parcialmente'
STATUS_DELIVERED = 'entregada'

#Classes------
class Category():
    
    def __init__(self, id = 0) -> None:
        if id != 0:
            self.id = id
            self.findById(self.id)
            return
        self.id = 0
        self.name = None
        
    def __repr__(self) -> str:
        return f"{self.name}"
        
    def findById(self, id):
        rawData = sql.peticion(f"SELECT * FROM category WHERE id = {id}")[0]
        self.name = rawData[1]
        return 1
    
    def save(self):
        if self.id == 0:
            sql.peticion(f"INSERT INTO category VALUES(NULL, '{self.name}')")
            self.id = sql.peticion(f"SELECT MAX(id) as id FROM category")[0][0]
        else:
            sql.peticion(f"UPDATE category SET name = '{self.name}' WHERE id = {self.id}")     

class Product():
    
    def __init__(self, id = 0) -> None:
        if id != 0:
            self.id = id
            self.findById(self.id)
            return
        self.id = 0
        self.name = ''
        self.category = 0
        self.description = ''
        self.brand = ''
        self.model = ''
        self.quantity = 0
        self.movements = []
        
    def __repr__(self) -> str:
        return f"Product ID {self.id}:\n\tName: {self.name}\n\tDescription: {self.description}\n\tQuantity: {self.quantity}\n"
    
    def findById(self, id):
        rawData = sql.peticion(f"SELECT * FROM inventory WHERE id = {id}")[0]
        if(len(rawData) == 0):
            print('Error. Product id not found.')
            return 0
        self.name = rawData[1]
        self.category = Category(id = rawData[2])
        self.description = rawData[3]
        self.brand = rawData[4]
        self.model = rawData[5]
        self.quantity = rawData[6]
        #self.recalculateQuantity()
        self.findMovements()
        return 1
    
    def recalculateQuantity(self):
        if self.findMovements() == 1:
            self.quantity = 0
            for movement in self.movements:
                if movement.type == INPUT:
                    self.quantity += movement.quantity
                elif movement.type == OUTPUT:
                    self.quantity -= movement.quantity
            sql.peticion(f"UPDATE inventory SET quantity = {self.quantity} WHERE id = {self.id}")
            
    def findMovements(self):
        if self.id == 0:
            print('Error. The product has not id.')
            return 0
        self.movements = []
        rawData = sql.peticiontres(f"SELECT id FROM inventory_detail WHERE product_id = {self.id} ORDER BY date")
        if len(rawData) == 0:
            #print('No movements found.')
            return 0
        for movement in rawData:
            self.movements.append(InventoryMovement(id = movement[0]))
        return 1

    def addMovement(self, date, type, quantity, comment, origin, origin_id):
        newMovement = InventoryMovement()
        newMovement.date = date
        newMovement.type = type
        newMovement.product = self.id
        newMovement.quantity = quantity
        newMovement.comment = comment
        newMovement.origin = origin
        newMovement.origin_id = origin_id if origin != None else None
        newMovement.save()
        self.movements.append(newMovement)
        #self.recalculateQuantity()
        
    def save(self):
        if self.id == 0:
            sql.peticion(f"INSERT INTO inventory VALUES(NULL, '{self.name}', {self.category.id}, '{self.description}', '{self.brand}', '{self.model}', {self.quantity})")
            self.id = sql.peticion(f"SELECT MAX(id) as id FROM inventory")[0][0]
        else:
            sql.peticion(f"UPDATE inventory SET name = '{self.name}', category =  {self.category.id}, description = '{self.description}', brand = '{self.brand}', model = '{self.model}', quantity = {self.quantity} WHERE id = {self.id}")

    def deliveringTime(self):
        rawData = sql.petition(f"SELECT requisitions.date, requisitions_detail.deliveredDate FROM requisitions LEFT JOIN requisitions_detail ON requisitions.id = requisitions_detail.requisition_id WHERE product_id = {self.id}")
        if len(rawData) == 0:
            return timedelta()
        times = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        for purchase in rawData:
            if(purchase[0] == None or purchase[1] == None):
                continue
            times += purchase[1] - purchase[0]
        times = times / len(rawData)
        return times
        
    def graphMovements(self):
        time = []
        quantity = []
        time.append(self.movements[0].date-timedelta(days=10))
        quantity.append(0)
        purchasesTimes = []
        purchasesQuantity = []
        for mov in self.movements:
            time.append(mov.date)
            if len(quantity) == 1:
                quantity.append(mov.quantity)
            else:
                quantity.append(quantity[len(quantity)-1]+mov.quantity if mov.type == INPUT else quantity[len(quantity)-1]-mov.quantity)
            if mov.type == INPUT and mov.origin == REQUISITION:
                purchasesTimes.append(mov.date)
                purchasesQuantity.append(mov.quantity)
        time.append(datetime.now())
        quantity.append(self.quantity)
        fig, ax = plt.subplots()
        ax.set_title(f"Gráfico de {self.name}")
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cantidad')
        ax.grid(True, color="#cccccc", linestyle='dashed')
        ax.plot(time, quantity, label='Cantidad de productos', color='#475CA7',drawstyle='steps-post', linewidth=2)
        time = [datetime.now()]
        quantity = [quantity[len(quantity)-1]]
        while quantity[len(quantity)-1] != 0:
            time.append(time[len(time)-1]+self.calculateOutputs())
            quantity.append(quantity[len(quantity)-1]-1)
        ax.plot(time, quantity, label='Proyección', color='#916AAD',drawstyle='steps', linewidth=2, linestyle='dotted')
        ax.plot(purchasesTimes, purchasesQuantity, label='Compras', color='#475CA7', marker='o', linewidth=2)
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
        
        plt.show()
        
    def calculateOutputs(self):
        self.findMovements()
        distances = []
        suma = timedelta()
        for mov in self.movements:
            if mov.type == OUTPUT:
                distance = mov.date-self.movements[self.movements.index(mov)-1].date
                distances.append(distance)
                suma += abs(distance)
        if len(distances) == 0:
            return timedelta()
        prom = suma/len(distances)
        return prom
    
    def buy(self):
        timeToDontHave = self.calculateOutputs() * self.quantity
        if timeToDontHave <= self.deliveringTime():
            return True
        else:
            return False

class InventoryMovement():
    
    def __init__(self, id = 0) -> None:
        if id != 0:
            self.id = id
            self.findById(self.id)
            return
        self.id = 0
        self.date = None
        self.type = None
        self.product = None
        self.quantity = None
        self.comment = None
        self.origin = None
        self.origin_id = None
        
    def __repr__(self) -> str:
        return f"Inventory Movement ID {self.id}:\n\tDate: {self.date}\n\tProduct: {self.product}\n\tType: {self.type}\n\tQuantity: {self.quantity}\n"
    
    def findById(self, id):
        rawData = sql.peticiontres(f"SELECT * FROM inventory_detail WHERE id = {id}")[0]
        if(len(rawData) == 0):
            print('Error. Movement id not found.')
            return 0
        self.date = rawData[1] #WIP
        self.type = rawData[2]
        self.product = rawData[3]
        self.quantity = rawData[4]
        self.comment = rawData[5]
        self.origin = rawData[6]
        self.origin_id = rawData[7]
        return 1
        
    def save(self):
        if self.id == 0:
            sql.petitionWithParam(f"INSERT INTO inventory_detail VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (self.date, self.type, self.product, self.quantity, self.comment, self.origin, self.origin_id))
            self.id = sql.peticion(f"SELECT MAX(id) as id FROM inventory_detail")[0][0]
        else:
            sql.petitionWithParam(f"UPDATE inventory_detail SET 'date' = (?) WHERE id = {self.id}", (self.date,))
        
class Requisition():
    
    def __init__(self, id = 0) -> None:
        if id != 0:
            self.id = id
            self.findById(self.id)
            return
        self.id = 0
        self.date = None
        self.status = None
        self.description = None
        self.deliveredDate = None
        self.products = []
    
    def __repr__(self) -> str:
        return f"Requisition Id {self.id}:\n\tDate: {self.date}\n\tStatus: {self.status}\n\tDescription: {self.description}\n"
    
    def findById(self, id):
        rawData = sql.peticiontres(f"SELECT * FROM requisitions WHERE id = {id}")[0]
        if len(rawData) == 0:
            return 0
        self.date = rawData[1]
        self.status = rawData[2]
        self.description = rawData[3]
        self.deliveredDate = rawData[4]
        self.products = []
        idList = sql.peticion(f"SELECT id FROM requisitions_detail WHERE requisition_id = {id}")
        for id in idList:
            self.products.append(RequisitionDetail(id = id[0]))
        
    def addProduct(self, productId, quantity, comment = None, status = STATUS_DRAFT):
        self.products.append(RequisitionDetail(productId = productId, quantity = quantity, comment = comment, status = status, requisitionId = self.id))
        
    def save(self):
        if self.id == 0:
            sql.petitionWithParam("INSERT INTO requisitions VALUES (NULL, ?, ?, ?, ?)",(self.date, self.status, self.description, self.deliveredDate))
            self.id = sql.peticion("SELECT MAX(id) as id FROM requisitions")[0][0]
        else:
            sql.petitionWithParam(f"UPDATE requisitions SET date = ?, status = ?, description = ?, delivered = ? WHERE id = {self.id}", (self.date, self.status, self.description, self.deliveredDate))
            sql.petition(f"DELETE FROM requisitions_detail WHERE requisition_id = {self.id}")
    
        for product in self.products:
            product.requisitionId = self.id
            product.id = None
            product.save()
            
    def delete(self):
        for product in self.products:
            product.delete()
        sql.peticion(f"DELETE FROM requisitions WHERE id = {self.id}")
    
    def changeStatus(self, status, save = True):
        self.status = status
        if save == True:
            self.save()
            for detail in self.products:
                detail.status = status
                detail.save()
            
    def generatePDF(self, filename):
        pdf.createRequisitionReport(self, filename)
        
class RequisitionDetail():
    
    def __init__(self, productId = 0, quantity = 0, id = None, comment = None, status = STATUS_DRAFT, requisitionId = 0, deliveredQuantity = 0, deliveredDate = None) -> None:
        if id != None:
            self.id = id
            self.findById(self.id)
            return
        self.id = None
        if productId == 0:
            self.product = Product()
        else:
            self.product = Product(id = productId)
        self.quantity = quantity
        self.deliveredQuantity = deliveredQuantity
        self.deliveredDate = deliveredDate
        self.comment = comment if comment!='\n' else None
        self.status = status
        self.requisitionId = requisitionId
        
    def __repr__(self) -> str:
        return f"\tDetail Id {self.id}:\n\t\tProduct:{self.product.name}\n\t\tQuantity: {self.quantity}\n\t\tStatus: {self.status}\n\t\tComment: {self.comment}\n"
        
    def findById(self, id):
        rawData = sql.peticion(f"SELECT * FROM requisitions_detail WHERE id = {id}")[0]
        self.requisitionId = rawData[1]
        self.product = Product(id = rawData[2])
        self.quantity = rawData[3]
        self.comment = rawData[4]
        self.status = rawData[5]
        self.deliveredQuantity = rawData[6]
        self.deliveredDate = rawData[7]
        
    def save(self):
        if self.id == None:
            sql.petitionWithParam("INSERT INTO requisitions_detail VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (self.requisitionId, self.product.id, self.quantity, self.comment, self.status, self.deliveredQuantity, self.deliveredDate))
            self.id = sql.peticion("SELECT MAX(id) AS id FROM requisitions_detail")[0][0]
        else:
            sql.petitionWithParam(f"UPDATE requisitions_detail SET quantity = ?, comment = ?, status = ?, deliveredQuantity = ?, deliveredDate = ? WHERE id = {self.id}", (self.quantity, self.comment, self.status, self.deliveredQuantity, self.deliveredDate))
    
    def delete(self):
        sql.peticion(f"DELETE FROM requisitions_detail WHERE id = {self.id}")
        self.id = None
            
#Functions------
def checkDatabase():
    sql.peticion('''CREATE TABLE IF NOT EXISTS "requisitions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	TIMESTAMP NOT NULL,
	"status"	TEXT NOT NULL,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')
    
    sql.peticion('''CREATE TABLE IF NOT EXISTS "requisitions_detail" (
	"id"	INTEGER NOT NULL UNIQUE,
	"requisition_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"comment"	TEXT,
	"status"	TEXT NOT NULL,
	FOREIGN KEY("requisition_id") REFERENCES "requisitions"("id"),
	FOREIGN KEY("product_id") REFERENCES "inventory"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);''')
    
    sql.peticion('''CREATE TABLE IF NOT EXISTS "inventory_detail" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	BLOB NOT NULL,
	"type"	TEXT NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"comment"	TEXT,
	"origin"	TEXT,
	"origin_id"	INTEGER,
	FOREIGN KEY("product_id") REFERENCES "inventory"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);''')

def getCategories():
    list = []
    for id in sql.peticion("SELECT id FROM category"):
        list.append(Category(id = id[0]))
    return list

def findByName(name):
    return [Product(id = x[0]) for x in sql.peticion(f"SELECT id FROM inventory WHERE name LIKE '%{name}%'")]

def getProducts(order = 'name', quantity = 0):
    list = []
    for id in sql.peticion(f"SELECT id FROM inventory ORDER BY {order} {'' if quantity == 0 else 'LIMIT '+str(quantity)}"):
        list.append(Product(id = id[0]))
    return list

def getRequisitions(lastest = True, quantity = 0, order = 'id'):
    list = []
    for id in sql.peticion(f"SELECT id FROM requisitions ORDER BY {order} {'DESC' if lastest else 'ASC'} {'' if quantity == 0 else 'LIMIT '+str(quantity)}"):
        list.append(Requisition(id = id[0]))
    return list
    

    #Test------

def crearRequisiion():
    newRequisition = Requisition()
    newRequisition.date = datetime(year=2022,month=9,day=5)
    newRequisition.status = STATUS_DELIVERED
    newRequisition.description = 'Requisición antigua'
    
    newRequisition.addProduct(23, 100, comment='')
    newRequisition.addProduct(22, 10, comment='Para almacenar como refacción.')
    print(newRequisition)
    print(newRequisition.products[0])
    newRequisition.save()
    
if __name__ == '__main__':
    #checkDatabase()
    product = Product(id=39)
    print(product.calculateOutputs()*product.quantity)
    print(product.buy())
    product.graphMovements()