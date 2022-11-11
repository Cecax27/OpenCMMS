"""Module to hand work orders.
"""

try:
    import sql
except:
    from modules import sql
try:
    import employers
except:
    from modules import employers
try:
    from modules import maintenances
except:
    import maintenances
from datetime import date
from datetime import datetime
from datetime import timedelta
from pickle import NONE
try:
    import pdf
except:
    from modules import pdf
#Const-----
STATUS_DRAFT = 'draft'
STATUS_CONFIRMED = 'confirmed'
STATUS_IN_PROGRESS = 'in progress'
STATUS_DONE = 'done'

#Dictionarys
ESP = {STATUS_DRAFT:'borrador',
       STATUS_CONFIRMED: 'confirmada',
       STATUS_IN_PROGRESS: 'en progreso',
       STATUS_DONE: 'realizada'}
ESP_ENG = {'borrador':STATUS_DRAFT,
       'confirmada':STATUS_CONFIRMED,
       'en progreso':STATUS_IN_PROGRESS,
       'realizada':STATUS_DONE}

LANGUAGE = ESP


#Classes------

class WorkOrder():
    """_summary_
    """
    
    def __init__(self, id = None) -> None:
        """_summary_
        """
        if id != None:
            self.findById(id)
            return
        self.id = None
        self.date = None
        self.status = STATUS_DRAFT
        self.responsible = None
        self.comment = None
        self.maintenances = []
        
    def __repr__(self) -> str:
        return f"Work Order with Id {self.id}:\n\tDescription: {self.comment}\n"
        
    def findById(self, id):
        """Find in the database.

        Args:
            id (int): The work order id.

        Returns:
            bool: 0 if error, 1 if not.
        """
        rawData = sql.petition(f"SELECT * FROM workorders WHERE id = {id}")[0]
        if(len(rawData) == 0):
            print('Error. Work Order id not found.')
            return 0
        self.id = rawData[0]
        self.date = rawData[1] 
        self.status = rawData[2]
        self.responsible = employers.Employer(id = rawData[3])
        self.comment = rawData[4]
        rawData = sql.petition(f"SELECT * FROM workorders_detail WHERE workorder_id = {id}")
        self.maintenances = []
        for line in rawData:
            self.maintenances.append(maintenances.Maintenance(id = line[2]))
        return 1
    
    def save(self):
        """Save in the database.
        """
        if self.id == None:
            sql.petitionWithParam(f"INSERT INTO workorders VALUES (NULL, ?, ?, ?, ?)", (self.date, self.status, self.responsible.id, self.comment))
            self.id = sql.peticion(f"SELECT MAX(id) as id FROM workorders")[0][0]
            if len(self.maintenances) > 0:
                for maintenance in self.maintenances:
                    sql.petition(f"INSERT INTO workorders_detail VALUES (NULL, {self.id}, {maintenance.id})")
        else:
            sql.petitionWithParam(f"UPDATE workorders SET date=?, status=?, responsible=?, comment = ? WHERE id = {self.id}", (self.date, self.status, self.responsible.id, self.comment))
            sql.petition(f"DELETE FROM workorders_detail WHERE workorder_id = {self.id}")
            if len(self.maintenances) > 0:
                for maintenance in self.maintenances:
                    sql.petition(f"INSERT INTO workorders_detail VALUES (NULL, {self.id}, {maintenance.id})")
                    
    def delete(self):
        """Delete from database.
        """
        sql.petition(f"DELETE FROM workorders_detail WHERE workorder_id = {self.id}")
        sql.petition(f"DELETE FROM workorders WHERE id = {self.id}")
        
    def generatePDF(self, filename):
        pdf.createWorkOrder(self, filename)
    
def getAll(orderby = 'id', order = 'ASC'):
    """_summary_

    Args:
        orderby (str, optional): _description_. Defaults to 'id'.
        order (str, optional): 'DESC' or 'ASC'. Defaults to 'ASC'.

    Returns:
        _type_: _description_
    """
    list = []
    for id in sql.petition(f"SELECT id FROM workorders ORDER BY {orderby} {order}"):
        list.append(WorkOrder(id = id[0]))
    return list
    
if __name__ == '__main__':
    # work = WorkOrder()
    # work.date = datetime.now()
    # work.responsible = employers.Employer(id = 13)
    # work.comment = 'Primera prueba.'
    # work.maintenances.append(maintenances.Maintenance(id = 143))
    # work.save()
    # work = WorkOrder(id = 1)
    #work.maintenances.append(maintenances.Maintenance(id = 109))
    #work.save()
    #work.generatePDF('prueba.pdf')
    print(getAll())