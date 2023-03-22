try:
    from modules import sql, pdf
except:
    import sql, pdf
from datetime import date
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

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
        self.movements = [InventoryMovement(id = x[0]) for x in sql.petition(f"SELECT id FROM inventory_detail WHERE product_id = {self.id} ORDER BY date DESC")]
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
        self.recalculateQuantity()
        
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
    
    #With ML    
    """ def graphMovements(self):
        self.findMovements()
        time = []
        quantity = []
        time.append(self.movements[-1].date-timedelta(days=10))
        quantity.append(0)
        purchasesTimes = []
        purchasesQuantity = []
        for mov in reversed(self.movements):
            time.append(mov.date)
            if len(quantity) == 1:
                quantity.append(mov.quantity)
            else:
                quantity.append(quantity[-1]+mov.quantity if mov.type == INPUT else quantity[-1]-mov.quantity)
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
        ax.plot(time, quantity, label='Real', color='#475CA7',drawstyle='steps-post', linewidth=2)
        
        data = sql.petition(f"SELECT inventory_detail.date, inventory_detail.quantity FROM inventory_detail WHERE inventory_detail.type = 'output' AND inventory_detail.product_id = {self.id} ORDER BY inventory_detail.date")
        #dates = np.array([i[0].timetuple().tm_yday+(365 if i[0].year == 2023 else 0) for i in data][0:-1], dtype=float)
        dates = np.array([to_integer(i[0]) for i in data][0:-1], dtype=float)
        quantities = np.array([quantity[1] for quantity in data][0:-1], dtype=float)
        results = np.array([to_integer(i[0]) for i in data][1:], dtype=float)
        
        oculta1 = tf.keras.layers.Dense(units=60, input_shape=[2])
        oculta2 = tf.keras.layers.Dense(units=50)
        oculta3 = tf.keras.layers.Dense(units=50)
        salida = tf.keras.layers.Dense(units=1)
        modelo = tf.keras.Sequential([oculta1, oculta2, oculta3, salida])
        
        modelo.compile(
            optimizer=tf.keras.optimizers.Adam(0.1),
            loss='mean_squared_error'
        )
        
        historial = modelo.fit(np.stack([ dates, quantities ], axis=1), results, epochs=1000, verbose=False)
        
        # plt.xlabel("# Epoca")
        # plt.ylabel("Magnitud de pérdida")
        # plt.plot(historial.history["loss"])
        
        time = []
        quantity = []
        time.append(self.movements[-1].date-timedelta(days=10))
        quantity.append(0)
        inputs = iter(list(filter(lambda i: i.type == INPUT, reversed(self.movements))))
        actualmov = next(inputs)
        time.append(actualmov.date)
        quantity.append(actualmov.quantity)
        actualmov = next(inputs)
        
        while(quantity[-1] != 0 or actualmov.date != datetime.strptime('2100 1', '%Y %j')):
            #prediction = int(modelo.predict(np.stack([[time[-1].timetuple().tm_yday+(365*2 if time[-1].year == 2024 else ( 365 if time[-1].year == 2023 else 0 ) )],[1]], axis=1))[0][0])
            #predictiondate = datetime.strptime(f"{2024 if prediction > (365 * 2) else ( 2023 if prediction > 365 else 2022 )} { prediction - ( (365 * 2) if prediction > (365 * 2) else ( 365 if prediction > 365 else 0 ) ) }", '%Y %j')
            predictiondate = to_dt( modelo.predict( np.stack( [ [ to_integer( time[-1] ) ], [1] ], axis=1 ) )[0][0] )
            if predictiondate < actualmov.date:
                time.append(predictiondate)
                if quantity[-1] == 0:
                    quantity.append(0)
                else:
                    quantity.append(quantity[-1]-1)
            else:
                time.append(actualmov.date)
                quantity.append(quantity[-1]+actualmov.quantity)
                try:
                    actualmov = next(inputs)
                except StopIteration: 
                    actualmov.date = datetime.strptime('2100 1', '%Y %j')
        
        #time = [datetime.now(), datetime.now()+self.calculateOutputs()]
        #quantity = [quantity[len(quantity)-1], quantity[len(quantity)-1]]
        #while quantity[len(quantity)-1] != 0:
        #    time.append(time[len(time)-1]+self.calculateOutputs())
        #    quantity.append(quantity[len(quantity)-1]-1)
        ax.plot(time, quantity, label='IA', color='#916AAD',drawstyle='steps-post', linewidth=2, linestyle='dotted')
        ax.plot(purchasesTimes, purchasesQuantity, label='Compras', color='#475CA7', marker='o', linewidth=0)
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
        
        plt.show() """
        
    def graphMovements(self):
        self.findMovements()
        time = []
        quantity = []
        time.append(self.movements[-1].date-timedelta(days=10))
        quantity.append(0)
        purchasesTimes = []
        purchasesQuantity = []
        for mov in reversed(self.movements):
            time.append(mov.date)
            if len(quantity) == 1:
                quantity.append(mov.quantity)
            else:
                quantity.append(quantity[-1]+mov.quantity if mov.type == INPUT else quantity[-1]-mov.quantity)
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
        ax.plot(time, quantity, label='Real', color='#475CA7',drawstyle='steps-post', linewidth=2)
        
        distance = self.calculateOutputs()
        
        time = []
        quantity = []
        time.append(self.movements[-1].date-timedelta(days=10))
        quantity.append(0)
        inputs = iter(list(filter(lambda i: i.type == INPUT, reversed(self.movements))))
        actualmov = next(inputs)
        time.append(actualmov.date)
        quantity.append(actualmov.quantity)
        actualmov = next(inputs)
        
        while(quantity[-1] != 0 or actualmov.date != datetime.strptime('2100 1', '%Y %j')):
            predictiondate = time[-1] + timedelta(seconds = distance * 84600)
            if predictiondate < actualmov.date:
                time.append(predictiondate)
                if quantity[-1] == 0:
                    quantity.append(0)
                else:
                    quantity.append(quantity[-1]-1)
            else:
                time.append(actualmov.date)
                quantity.append(quantity[-1]+actualmov.quantity)
                try:
                    actualmov = next(inputs)
                except StopIteration: 
                    actualmov.date = datetime.strptime('2100 1', '%Y %j')
        
        ax.plot(time, quantity, label='predictions', color='#916AAD',drawstyle='steps-post', linewidth=2, linestyle='dotted')
        ax.plot(purchasesTimes, purchasesQuantity, label='Compras', color='#475CA7', marker='o', linewidth=0)
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
        
        plt.show()
        
    def calculateOutputs(self):
        outputs = []
        for x in sql.petition('''SELECT date(date), sum(quantity) FROM inventory_detail
        WHERE product_id = {} AND type = 'output'
        GROUP BY date(date)
        ORDER BY date desc'''.format(self.id)):
            newMov = InventoryMovement()
            newMov.date = date.fromisoformat(x[0])
            newMov.quantity = x[1]  
            outputs.append(newMov)
        distances = []
        for i, mov in enumerate(outputs):
            if len(outputs) > i+1:
                distance = (mov.date - outputs[i+1].date) / mov.quantity
                for x in range(mov.quantity):
                    distances.append(distance)
        df_movements = pd.DataFrame({
            'days':[i.total_seconds() / 86400 for i in distances]})
        return df_movements.days.median()
    
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
            if status != STATUS_PARTIAL_DELIVERED:
                for detail in self.products:
                    detail.status = status
                    detail.save()
            
    def generatePDF(self, filename):
        pdf.createRequisitionReport(self, filename)
        
class RequisitionDetail():
    
    def __init__(self, productId = 0, quantity = 0, id = None, comment = None, status = STATUS_DRAFT, requisitionId = 0, deliveredQuantity = None, deliveredDate = None) -> None:
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
    return [Product(id = x[0]) for x in sql.peticion(f"SELECT id FROM inventory ORDER BY {order} {'' if quantity == 0 else 'LIMIT '+str(quantity)}")]

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
    
def generatePDF(filename):
    pdf.createInventory(filename, [Product(x[0]) for x in sql.petition("SELECT id FROM inventory WHERE quantity > 0")])

def getPendingProducts():
    """Get the pending products to delivering.

    Returns:
        list: List of RequisitionDetail objects.
    """
    return [RequisitionDetail(id = id[0]) for id in sql.petition("SELECT requisitions_detail.id FROM requisitions_detail LEFT JOIN requisitions ON requisitions_detail.requisition_id = requisitions.id WHERE requisitions_detail.status = 'solicitada' OR requisitions_detail.status = 'confirmada' OR (requisitions_detail.status = 'entregada' AND requisitions_detail.deliveredQuantity = 0 AND requisitions.status = 'entregada parcialmente') ORDER BY requisitions.date ASC")]
  
def to_integer(dt_time):
    dt_delta = dt_time - datetime(2020,1,1)
    total = datetime(2030,1,1) - datetime(2000,1,1)
    return dt_delta.days

def to_dt(integer):
    total = datetime(2030,1,1) - datetime(2020,1,1)
    dt_time = datetime(2020,1,1) + timedelta(int(integer))
    return dt_time
    
if __name__ == '__main__':
    #checkDatabase()
    #print((datetime(2030,1,1) - datetime(2000,1,1)).days)
    #print(to_integer(datetime.now()))
    #print(to_dt(to_integer(datetime.now())))
    Product(1).graphMovements()
    
    """ data = sql.petition("SELECT inventory_detail.date, inventory_detail.quantity FROM inventory_detail WHERE inventory_detail.type = 'output' AND inventory_detail.product_id = 19 ORDER BY inventory_detail.date")
    
    dates = np.array([i[0].timetuple().tm_yday+(365 if i[0].year == 2023 else 0) for i in data][0:-1], dtype=float)
    quantities = np.array([quantity[1] for quantity in data][0:-1], dtype=float)
    results = np.array([i[0].timetuple().tm_yday+(365 if i[0].year == 2023 else 0) for i in data][1:], dtype=float)
    
    oculta1 = tf.keras.layers.Dense(units=8, input_shape=[2])
    oculta2 = tf.keras.layers.Dense(units=4)
    salida = tf.keras.layers.Dense(units=1)
    modelo = tf.keras.Sequential([oculta1, oculta2, salida])
    
    modelo.compile(
        optimizer=tf.keras.optimizers.Adam(0.1),
        loss='mean_squared_error'
    )
    
    print("Comenzando entrenamiento...")
    historial = modelo.fit(np.stack([dates,quantities], axis=1), results, epochs=100, verbose=False)
    print("Modelo entrenado!")
    
    import matplotlib.pyplot as plt
    plt.xlabel("# Epoca")
    plt.ylabel("Magnitud de pérdida")
    plt.plot(historial.history["loss"])
    
    
    resultado = modelo.predict(np.stack([[287, 299, 309, 309, 319, 326, 326, 333, 335, 343, 357, 361, 388, 395],[1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 4, 2]], axis=1))
    print(resultado)
    
    print(datetime.strptime(f"2023 {406-365}", '%Y %j')) """
#else:
#    map(lambda x: x.recalculateQuantity, getProducts())
    