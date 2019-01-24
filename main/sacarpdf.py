'''
Created on 23/01/2019

@author: a16daviddss
'''

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
import BDres
import locale



def genfact(id=6,camarero="a"):
    infofact = BDres.getfact(id)
    c = canvas.Canvas("factura_"+str(id)+".pdf",pagesize=A4)
    c.setFont("Helvetica", 10)
    c.line(30, 750, 565, 750)
    #c.drawString(30, 765, "Factura")
    c.drawCentredString(297.5, 765,"Restaurante David")
    c.drawString(30, 710, "Camarero: " + camarero)
    c.drawString(30, 730, "Nº de factura: "+str(id))
    c.drawRightString(560, 730, "Fecha de factura: "+infofact[4])
    c.drawString(30, 640, "Producto")
    c.drawRightString(305, 640, "Cantidad")
    c.drawRightString(565, 640, "Precio")
    c.setDash(6,3)
    
    c.line(30, 625, 565, 625)
    total = 0
    ciclo = 2
    locale.setlocale(locale.LC_ALL, '')
    lineas = BDres.getlineas(id)
    for linea in lineas:
        producto = linea[2]
        cantidad = linea[3]
        info = BDres.getnompre(producto)
        subtotal = cantidad*info[1]
        total = total + subtotal
        c.drawString(30, 640-(ciclo*20),info[0].title())
        c.drawRightString(305, 640-(ciclo*20),str(cantidad))
        c.drawRightString(565, 640-(ciclo*20),locale.currency(subtotal))
        ciclo = ciclo+1
    c.line(30, 645-(ciclo*20), 565, 645-(ciclo*20))
    c.drawRightString(565, 640-((ciclo+1)*20), "TOTAL:   " + locale.currency(total))
    c.showPage()
    c.save()
    





