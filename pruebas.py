from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

requisitionNumber = 1
date = datetime.now()



w, h = letter
pdfmetrics.registerFont(TTFont('Normal', 'segoeui.ttf'))
pdfmetrics.registerFont(TTFont('Semibold', 'seguisb.ttf'))
pdfmetrics.registerFont(TTFont('Bold', 'segoeuib.ttf'))

page = canvas.Canvas('prueba.pdf', pagesize=letter)
page.drawImage("img/logo.png", w-180, h-65, width=130, height=37)
page.setFont("Bold",16)
page.drawString(50, h - 50, 'Departamento eléctrico') #Draw text
page.setFont("Semibold",22)
page.drawString(50, h - 90, 'Requisición de compra') 
page.setFillColorRGB(0.4, 0.4, 0.4)
page.setFont("Normal",12)
page.drawString(50, h - 170, 'Número') 
page.drawString(115	, h - 170, 'Fecha') 
page.setFillColorRGB(0,0,0)
page.setFont("Semibold",12)
page.drawString(100, h - 170, str(requisitionNumber)) 
page.drawString(155	, h - 170, date.strftime("%d / %m / %Y")) 
page.setStrokeColorRGB(0.6,0.6,0.6)
page.line(50, h-190, w-50, h-190)
page.showPage()
page.save()