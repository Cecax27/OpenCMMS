##añadir herramientas

import csv

def abrirCsv(ruta):
    with open(ruta, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter= ',', quotechar='"')
        datos = []
        for row in spamreader:
            linea = []
            for valor in row:
                linea.append(valor)
            datos.append(linea)
    return datos

def escribirCsv(ruta, baseDeDatos):
    with open(ruta, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in baseDeDatos:
            spamwriter.writerow(row)
    
