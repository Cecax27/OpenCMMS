try:
    import sql
except:
    from modules import sql
from datetime import date
from datetime import datetime
from datetime import timedelta

#Const-----
INPUT = "input"
OUTPUT = 'output'

MAINTENANCE = 'maintenance'
REQUISITION = 'requisition'

#Classes------
class Category():
    
    def __init__(self, id = 0) -> None:
        if id != 0:
            self.id = id
            self.findById(self.id)
            return
        self.name = None
        
    def __repr__(self) -> str:
        return f"{self.name}"
        
    def findById(self, id):
        rawData = sql.peticion(f"SELECT * FROM category WHERE id = {id}")[0]
        self.name = rawData[1]
        return 1
        

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
        rawData = sql.peticiontres(f"SELECT id FROM inventory_detail WHERE product_id = {self.id}")
        if len(rawData) == 0:
            print('No movements found.')
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
        newMovement.origin_id = origin_id
        newMovement.save()
        self.movements.append(newMovement)
        self.recalculateQuantity()
        
    def save(self):
        if self.id == 0:
            sql.peticion(f"INSERT INTO inventory VALUES(NULL, '{self.name}', {self.category.id}, '{self.description}', '{self.brand}', '{self.model}', {self.quantity})")
            self.id = sql.peticion(f"SELECT MAX(id) as id FROM inventory")[0][0]
        else:
            sql.peticion(f"UPDATE inventory SET name = '{self.name}', category =  {self.category.id}, description = '{self.description}', brand = '{self.brand}', model = '{self.model}', quantity = {self.quantity} WHERE id = {self.id}")

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
        
        
#Functions------
def checkDatabase():
    return sql.peticion('''CREATE TABLE IF NOT EXISTS "inventory_detail" (
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

#Test------

if __name__ == '__main__':
    # checkDatabase()
    # myproduct = Product()
    # myproduct.name = 'Tubo LED T8/18W Led Concept'
    # myproduct.category = 5
    # myproduct.description = 'Tubo LED T8/18W Led Concept'
    # myproduct.brand = 'Led Concept'
    # myproduct.model = 'T8/18W'
    # myproduct.save()
    #myproduct = Product(id = 2)
    #myproduct.addMovement(datetime.now(), INPUT, 5, 'Esto es una prueba.', REQUISITION, 1)
    #print(type(myproduct.movements[0].date))
    #myproduct.movements[0].save()
    #myproduct = Product(id = 2)
    #print(type(myproduct.movements[0].date))
    print(getCategories())