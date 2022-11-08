# -*- coding:utf-8 -*-
try:
    import inventory
except:
    from modules import inventory
try:
    import workorders
except:
    from modules import workorders
try:
    import maintenances
except:
    from modules import maintenances
from math import prod
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

def drawParagraph(page, text, x, y, fontstyle = "Normal", fontsize = 12, width = 68):
    text = text.replace('\n', ' \n')
    description = page.beginText(x, y)
    description.setFont(fontstyle, fontsize)
    paragraph = text.split(' ')
    lines = []
    i = 0
    while i < len(paragraph): 
        count = 0
        line = ''
        while count < width and i < len(paragraph):
            if paragraph[i] == '\n':
                i+=1
                break
            line = line + ' ' + paragraph[i]
            count += len(paragraph[i])
            i += 1
        lines.append(line)
    for line in lines:
        description.textLine(line)
    page.drawText(description)
    return len(lines)

def createRequisitionReport(requisition, filename):
    w, h = letter
    pdfmetrics.registerFont(TTFont('Normal', 'segoeui.ttf'))
    pdfmetrics.registerFont(TTFont('Semibold', 'seguisb.ttf'))
    pdfmetrics.registerFont(TTFont('Bold', 'segoeuib.ttf'))

    page = canvas.Canvas(filename, pagesize=letter)
    page.drawImage("img/logo.jpg", w-180, h-65, width=130, height=37)
    page.setFont("Bold",16)
    page.drawString(50, h - 50, 'Departamento eléctrico') #Draw text
    page.setFont("Semibold",22)
    page.drawString(50, h - 90, 'Requisición de compra') 
    page.setFillColorRGB(0.4, 0.4, 0.4)
    page.setFont("Normal",12)
    page.drawString(50, h - 120, 'Número') 
    page.drawString(115	, h - 120, 'Fecha') 
    page.drawString(50	, h - 143, 'Comentario') 
    page.setFillColorRGB(0,0,0)
    page.setFont("Semibold",12)
    page.drawString(100, h - 120, str(requisition.id)) 
    page.drawString(155	, h - 120, requisition.date.strftime("%d / %m / %Y")) 
    if requisition.description != None:
        requisition.description = requisition.description.replace('\n', ' ')
        description = page.beginText(120, h-143)
        description.setFont("Normal",12)
        paragraph = requisition.description.split(' ')
        lines = []
        i = 0
        while i < len(paragraph): 
            count = 0
            line = ''
            while count < 68 and i < len(paragraph):
                line = line + ' ' + paragraph[i]
                count += len(paragraph[i])
                i += 1
            lines.append(line)
        for line in lines:
            description.textLine(line)
        page.drawText(description)
    page.setStrokeColorRGB(0.6,0.6,0.6)
    page.line(50, h-190, w-50, h-190)
    
    page.setFillColorRGB(0.4, 0.4, 0.4)
    page.setFont("Semibold",11)
    page.drawString(50, h - 210, 'Cant.') 
    page.drawString(90, h - 210, 'Descripción') 
    page.drawString(390 , h - 210, 'Marca') 
    page.drawString(470, h - 210, 'Modelo') 
    
    lastPosition = h-230
    for product in requisition.products:
        productNumber = requisition.products.index(product)
        if(productNumber%2==0):
            page.setFillColorRGB(0.95,0.95,0.95)
            page.rect(50, lastPosition-(12*(int(len(product.product.description)/55)))-6, w-100, (12*(int(len(product.product.description)/55)+1))+6, 0, 1)
        page.setFillColorRGB(0,0,0)
        page.setFont("Normal",10)
        page.drawString(60, lastPosition, str(product.quantity))
        if product.product.description != None:
            product.product.description = product.product.description.replace('\n', ' ')
            description = page.beginText(90, lastPosition)
            description.setFont("Normal",10)
            for line in range(0,int(len(product.product.description)/55)+1,1):
                description.textLine(product.product.description[line*55:(line+1)*55])
            page.drawText(description)
        page.drawString(390, lastPosition, product.product.brand)
        page.drawString(470, lastPosition, product.product.model)
        lastPosition -= 15+(7*(int(len(product.product.description)/55)+1))
        if product.comment != None:
            product.comment = product.comment.replace('\n', ' ')
            page.setFillColorRGB(0.4,0.4,0.4)
            description = page.beginText(50, lastPosition)
            description.setFont("Normal",9)
            for line in range(0,int(len(product.comment)/124)+1,1):
                description.textLine(product.comment[line*124:(line+1)*124])
                lastPosition -= 20
            page.drawText(description)
    
    page.showPage()
    page.save()
    
def createWorkOrder(workOrder, filename):
    """Create a new work order document in pdf.

    Args:
        workOrder (list): The workOrder object to add to the work order.
        filename (string): The filename and the route of the file.
    """
    w, h = letter
    pdfmetrics.registerFont(TTFont('Normal', 'segoeui.ttf'))
    pdfmetrics.registerFont(TTFont('Semibold', 'seguisb.ttf'))
    pdfmetrics.registerFont(TTFont('Bold', 'segoeuib.ttf'))

    page = canvas.Canvas(filename, pagesize=letter)
    page.drawImage("img/logo.jpg", w-180, h-65, width=130, height=37)
    page.setFont("Bold",16)
    page.drawString(50, h - 50, 'Departamento eléctrico') #Draw text
    page.setFont("Semibold",22)
    page.drawString(50, h - 90, 'Orden de trabajo') 
    page.setFillColorRGB(0.4, 0.4, 0.4)
    page.setFont("Normal",12)
    page.drawString(50, h - 120, 'Número') 
    page.drawString(115	, h - 120, 'Fecha') 
    page.drawString(240	, h - 120, 'Asignada a') 
    page.drawString(50	, h - 143, 'Comentario') 
    page.setFillColorRGB(0,0,0)
    page.setFont("Semibold",12)
    page.drawString(100, h - 120, str(workOrder.id)) 
    page.drawString(155	, h - 120, workOrder.date.strftime("%d / %m / %Y")) 
    page.drawString(305, h - 120, str(workOrder.responsible.name)) 
    if workOrder.comment != None:
        workOrder.comment = workOrder.comment.replace('\n', ' ')
        description = page.beginText(120, h-143)
        description.setFont("Normal",12)
        paragraph = workOrder.comment.split(' ')
        lines = []
        i = 0
        while i < len(paragraph): 
            count = 0
            line = ''
            while count < 68 and i < len(paragraph):
                line = line + ' ' + paragraph[i]
                count += len(paragraph[i])
                i += 1
            lines.append(line)
        for line in lines:
            description.textLine(line)
        page.drawText(description)
    page.setStrokeColorRGB(0.6,0.6,0.6)
    page.line(50, h-190, w-50, h-190)
    
    lastPosition = h-215
    for maintenance in workOrder.maintenances:
        page.setFillColorRGB(0.95,0.95,0.95)
        rectHeight = (15 if len(maintenance.description)>0 else 0) + (10*math.ceil(len(maintenance.description)/80))
        page.rect(50, lastPosition-5 -rectHeight, w-100, rectHeight+20, 0, 1)
        page.setFillColorRGB(0,0,0)
        page.setFont("Bold",11)
        page.drawString(60, lastPosition, 'Mantenimiento no. '+str(maintenance.id))
        page.setFont("Normal",11)
        page.drawString(200, lastPosition, 'Mantenimiento '+str(maintenance.type))
        lastPosition -= 20
        lastPosition -= 10*drawParagraph(page, maintenance.description, 60, lastPosition, fontsize=11, width=79)
        lastPosition -= 20
        if lastPosition <= 60:
                    page.showPage()
                    lastPosition = h-60
        if maintenance.type == maintenances.Corrective:
            for plant in maintenance.plants:
                page.rect(60, lastPosition-5, 15, 15, 1, 0)
                page.setFont("Bold",10)
                page.drawString(100, lastPosition, plant.department.name + ' - '+ plant.area.name +' - '+ plant.name)
                lastPosition -= 15
                lastPosition -= 15*drawParagraph(page, plant.description, 97, lastPosition, fontsize=10)
                lastPosition -= 20
                if lastPosition <= 60:
                    page.showPage()
                    lastPosition = h-60
        else:
            for plant in maintenance.plants:
                page.setFont("Bold",10)
                page.drawString(60, lastPosition, plant.department.name + ' - '+ plant.area.name +' - '+ plant.name)
                lastPosition -= 15
                lastPosition -= 15*drawParagraph(page, plant.description, 57, lastPosition, fontsize=10)
                lastPosition -= 10
                if lastPosition <= 60:
                    page.showPage()
                    lastPosition = h-60
                
                for activity in plant.activities:
                    page.rect(60, lastPosition-5, 15, 15, 1, 0)
                    page.setFont("Bold",10)
                    page.drawString(100, lastPosition, activity.name)
                    lastPosition -= 15
                    lastPosition -= 15*drawParagraph(page, activity.description, 97, lastPosition, fontsize=10)
                    lastPosition -= 20
                    if lastPosition <= 60:
                        page.showPage()
                        lastPosition = h-60
                    
    #     if product.product.description != None:
    #         product.product.description = product.product.description.replace('\n', ' ')
    #         description = page.beginText(90, lastPosition)
    #         description.setFont("Normal",10)
    #         for line in range(0,int(len(product.product.description)/55)+1,1):
    #             description.textLine(product.product.description[line*55:(line+1)*55])
    #         page.drawText(description)
    #     page.drawString(390, lastPosition, product.product.brand)
    #     page.drawString(470, lastPosition, product.product.model)
    #     lastPosition -= 15+(7*(int(len(product.product.description)/55)+1))
    #     if product.comment != None:
    #         product.comment = product.comment.replace('\n', ' ')
    #         page.setFillColorRGB(0.4,0.4,0.4)
    #         description = page.beginText(50, lastPosition)
    #         description.setFont("Normal",9)
    #         for line in range(0,int(len(product.comment)/124)+1,1):
    #             description.textLine(product.comment[line*124:(line+1)*124])
    #             lastPosition -= 20
    #         page.drawText(description)
    
    page.showPage()
    page.save()
    
if __name__ == '__main__':
    #createRequisitionReport(inventory.Requisition(id = 12), 'C:/Users/EMMAN/Documents/Compras/Pendientes de solicitar/Prueba.pdf')
    createWorkOrder(workorders.WorkOrder(id = 1), 'prueba.pdf')