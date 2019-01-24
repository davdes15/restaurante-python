'''
Created on 19/12/2018

@author: a16daviddss
'''

import sqlite3


# este bloque de codigo nos conecta a la base de datos
try:
    bd = 'Provincias'
    conex = sqlite3.connect(bd)
    cur = conex.cursor()
    print('Conectado a la base de datos')
except sqlite3.OperationalError as e:
    print(e)
    

def cargarCombo(list):
    try:
        cur.execute("select provincia from Provincias")
        res = cur.fetchall()
        list.clear()
        for row in res:
            
            list.append(row)
    except sqlite3.OperationalError as e:
        print(e)
    
def cargarmun(listmun,prov):
    try:
        cur.execute("select municipio from municipios where provincia_id = "+str(prov+1)+"")
        res = cur.fetchall()
        listmun.clear()
        for row in res:
           
            listmun.append(row)
    except sqlite3.OperationalError as e:
        print(e)
        
