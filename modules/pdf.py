try:
    import inventory
except:
    from modules import inventory
from math import prod
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

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
        description = page.beginText(120, h-143)
        description.setFont("Normal",12)
        for line in range(0,int(len(requisition.description)/77)+1,1):
            description.textLine(requisition.description[line*77:(line+1)*77])
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
            page.rect(50, lastPosition-5, w-100, 17, 0, 1)
        page.setFillColorRGB(0,0,0)
        page.setFont("Normal",10)
        page.drawString(50, lastPosition, str(product.quantity))
        page.drawString(90, lastPosition, product.product.description)
        page.drawString(390, lastPosition, product.product.brand)
        page.drawString(470, lastPosition, product.product.model)
        lastPosition -= 20
        if product.comment != None:
            page.setFillColorRGB(0.4,0.4,0.4)
            description = page.beginText(50, lastPosition)
            description.setFont("Normal",9)
            for line in range(0,int(len(product.comment)/124)+1,1):
                description.textLine(product.comment[line*124:(line+1)*124])
                lastPosition -= 20
            page.drawText(description)
    
    page.showPage()
    page.save()