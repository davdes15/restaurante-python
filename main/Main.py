'''
Created on 19/12/2018

@author: a16daviddss
'''

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import BDCA,BDres
import Comprobaciones
import hashlib
from re import sub
from decimal import Decimal
import datetime
import sacarpdf
import os
from gi.repository import Gdk
from os.path import abspath, dirname, join


WHERE_AM_I = abspath(dirname(__file__))

class Restaurante():
    def __init__(self):
        b = Gtk.Builder()
        b.add_from_file("restaurante.glade")
        self.venprincipal = b.get_object("venprincipal")
        self.venlogin = b.get_object("venlogin")
        self.venerrlog = b.get_object("venerrlog")
        
        #self.venres = b.get_object("venreservas")
        
        self.user = None
        self.idcamarero = None
        self.entdni = b.get_object("entdni")
        self.entnom =b.get_object("entnom")
        self.entapel = b.get_object("entapel")
        self.entdir = b.get_object("entdir")
        self.entus =b.get_object("entus")
        self.entps=b.get_object("entps")
        self.entserv =b.get_object("entserv")
        self.entprec = b.get_object("entprec")
        self.lblcamarero = b.get_object("lblcamarero")
        self.lblmesa = b.get_object("lblmesa")
        self.entud = b.get_object("entud")
        self.entservicio = b.get_object("entservicio")
        self.servicio = 0
        self.id = 0
        self.pagada = 0
        self.idmesa = 0
        
        
        self.comboprov = b.get_object("comboprov")
        self.combomun =b.get_object("combomun")
        self.listprov = b.get_object("listprov")
        self.listmun = b.get_object("listmun")
        
        self.treeclientes = b.get_object("treeclientes")
        self.listclientes = b.get_object("listclientes")
        self.treeserv = b.get_object("treeserv")
        self.listserv = b.get_object("listserv")
        self.treemesas = b.get_object("treemesas")
        self.listmesas = b.get_object("listmesas")
        self.treefact = b.get_object("treefact")
        self.listfact = b.get_object("listfact")
        self.treecom = b.get_object("treecom")
        self.listcom = b.get_object("listcom")
        
        self.btn41 = b.get_object("btn41")
        self.btn42 = b.get_object("btn42")
        self.btn43 = b.get_object("btn43")
        self.btn44 = b.get_object("btn44")
        self.btn81 = b.get_object("btn81")
        self.btn82 = b.get_object("btn82")
        self.btn101 = b.get_object("btn101")
        self.btn102 = b.get_object("btn102")
        self.mesaant = self.btn41
        self.btnactual = self.btn41
        
    
        
        dict ={"on_venlogin_destroy":self.salir,"on_venprincipal_destroy":self.salir,"on_btncanc_clicked":self.salir,
               "on_btn41_clicked":self.reserva,"on_btn42_clicked":self.reserva,"on_btn43_clicked":self.reserva,
               "on_btn44_clicked":self.reserva,"on_btn81_clicked":self.reserva,"on_btn82_clicked":self.reserva,
               "on_btn101_clicked":self.reserva,"on_btn102_clicked":self.reserva,"on_comboprov_changed":self.updatemun,
               "on_btnalta_clicked":self.altacli,"on_btnacceder_clicked":self.login,
               "on_btnadd_clicked":self.altaprod,"on_treeclientes_cursor_changed":self.selectcli,"on_treeserv_cursor_changed":self.selectprod,
               "on_btnacerr_clicked":self.hide,"on_btnocupar_clicked":self.ocupar,"on_treemesas_cursor_changed":self.verfact,
               "on_treefact_cursor_changed":self.verlineas,"on_btnaddlinea_clicked":self.addlineaf,"on_entps_key_press_event":self.evtlog
               ,"on_btnpagar_clicked":self.pagar}
        
        #relaciona cada boton con el id de la mesa en la base de datos
        self.dictmesas={1:self.btn41,2:self.btn42,3:self.btn81,4:self.btn43,5:self.btn44,6:self.btn82,7:self.btn101,8:self.btn102}
        self.dictidmesa={self.btn41:1,self.btn42:2,self.btn81:3,self.btn43:4,self.btn44:5,self.btn82:6,self.btn101:7,self.btn102:8}
        
        b.connect_signals(dict)
        self.venerrlog.connect('delete-event', lambda w, e: w.hide() or True)
        #self.venprincipal.show()
        #self.venprincipal.maximize()
        self.venlogin.show()
        BDCA.cargarCombo(self.listprov)
        BDres.cargarCli(self.listclientes,self.treeclientes)
        BDres.cargaserv(self.listserv,self.treeserv)
        BDres.cargamesas(self.dictmesas,self.treemesas,self.listmesas)
        self.set_style()
       # sacarpdf.genfact()
       # self.comboprov.set_entry_text_column(1)

    def salir(self,widget,data=None):
        Gtk.main_quit()
        
    def hide(self,widget):
        self.venerrlog.hide()
        
    def evtlog(self,window,event):
        
        if event.keyval == 65293:
            self.login(window)
    
    def login(self,widget,data=None):
        user = self.entus.get_text()
        ps = self.entps.get_text()
        res = BDres.login(user,ps)
        if res[0]:
            self.venprincipal.show()
            self.venprincipal.maximize()
            self.venlogin.hide()
            self.user = user
            self.idcamarero = res[1]
            self.lblcamarero.set_text(user)
        else:
            self.venerrlog.show()

    def reserva(self,widget,data=None):
        self.btnactual = widget
        
        if not BDres.checkOcupada(self.dictidmesa[self.mesaant]):
            self.mesaant.set_sensitive(True)
            if self.mesaant == self.btn41:
                self.mesaant.get_image().set_from_file("./mesa4vacia.png")
                
            elif self.mesaant == self.btn42:
                self.mesaant.get_image().set_from_file("./mesa4vacia.png")
                
            elif self.mesaant == self.btn81:
                self.mesaant.get_image().set_from_file("./mesa8vaciav2.png")
                
            elif self.mesaant == self.btn43:
                self.mesaant.get_image().set_from_file("./mesa4vacia.png")
              
            elif self.mesaant == self.btn44:
                self.mesaant.get_image().set_from_file("./mesa4vacia.png")
                
            elif self.mesaant == self.btn82:
                self.mesaant.get_image().set_from_file("./mesa8vaciav2.png")
             
            elif self.mesaant == self.btn101:
                self.mesaant.get_image().set_from_file("./mesa10vacia.png")
                
            else:
                self.mesaant.get_image().set_from_file("./mesa10vacia.png")   
        self.mesaant = widget
        self.lblmesa.set_text(str(self.dictidmesa[widget]))
        if widget == self.btn41:
            widget.get_image().set_from_file("./mesa4oc.png")
            widget.set_sensitive(False)
        elif widget == self.btn42:
            widget.get_image().set_from_file("./mesa4oc.png")
            widget.set_sensitive(False)
        elif widget == self.btn81:
            widget.get_image().set_from_file("./mesa8ocv2.png")
            widget.set_sensitive(False)
        elif widget == self.btn43:
            widget.get_image().set_from_file("./mesa4oc.png")
            widget.set_sensitive(False)
        elif widget == self.btn44:
            widget.get_image().set_from_file("./mesa4oc.png")
            widget.set_sensitive(False)
        elif widget == self.btn82:
            widget.get_image().set_from_file("./mesa8ocv2.png")
            widget.set_sensitive(False)
        elif widget == self.btn101:
            widget.get_image().set_from_file("./mesa10oc.png")
            widget.set_sensitive(False)
        else:
            widget.get_image().set_from_file("./mesa10oc.png")
            widget.set_sensitive(False)
        
        #self.venres.show()
        #self.combomun.set_sensitive(False)
      
    def updatemun(self,widget,data=None):
        
       
        prov = self.comboprov.get_active()
        BDCA.cargarmun(self.listmun,prov)
    
    def altacli(self,widget,data=None):
        dni = self.entdni.get_text()
        nom = self.entnom.get_text()
        apel = self.entapel.get_text()
        dir = self.entdir.get_text()
        if Comprobaciones.calcularDNI(dni):
            if nom is not None and apel is not None and dir is not None:
                index = self.comboprov.get_active_iter()
                if index is not None:
                    mod = self.comboprov.get_model()
                    prov = mod[index][:2][0]
                    index = self.combomun.get_active_iter()
                    if index is not None:
                        mod = self.combomun.get_model()
                        mun = mod[index][:2][0]
                        
                        fila =(dni,nom,apel,dir,prov,mun)
                        BDres.altaCliente(self.listclientes,self.treeclientes,fila)
                        self.cleanCli()
                    else:
                        print("No seleccionado el municipio")
                else:
                    print("No seleccionada la provincia")
                
            else:
                #cambiar por popup
                print("debes cubrir todos los campos")
        else:
            print("error")
            
            
            #para reactivar los botones
            #self.btnactual.set_sensitive(True)
            #self.cambiobtn(self.btnactual)
            
            #para guardar la contraseña
            #import hashlib

            #sh = hashlib.sha1()
            #sh.update('password')
            #hash_value = sh.hexdigest()
            
    def cleanCli(self):
        self.entdni.set_text("")
        self.entapel.set_text("")
        self.entdir.set_text("")
        self.entnom.set_text("")
        self.comboprov.set_active(-1)
        self.combomun.set_active(-1)
        self.combomun.set_sensitive(False)
            
    def cleanProd(self):
        self.entserv.set_text("")
        self.entprec.set_text("")
            
    def altaprod(self,widget,data=None):
        prod = self.entserv.get_text()
        prec = float(self.entprec.get_text())
        row = (prod,prec)
        BDres.altaserv(self.listserv,self.treeserv,row)
        self.cleanProd()
        
    
    def selectcli(self,widget):
        sel = self.treeclientes.get_selection()
        (tm,ti) =sel.get_selected()
        dni= tm.get_value(ti,0)
        nombre = tm.get_value(ti,1)
        apel = tm.get_value(ti,2)
        dir = tm.get_value(ti,3)
        self.entdni.set_text(dni)
        self.entapel.set_text(apel)
        self.entdir.set_text(dir)
        self.entnom.set_text(nombre)
        
    def selectprod(self,widget):
        sel = self.treeserv.get_selection()
        (tm,ti) =sel.get_selected()
        prod = tm.get_value(ti,1)
        prec = Decimal(sub(r'[^\d.]','',tm.get_value(ti,2)))/100
        self.servicio = tm.get_value(ti,0)
        self.entserv.set_text(prod)
        self.entservicio.set_text(prod)
        self.entprec.set_text(str(prec))
        
    
    def cambiobtn(self,widget):
        if widget == self.btn41:
            widget.get_image().set_from_file("./mesa4vacia.png")
          
        elif widget == self.btn42:
            widget.get_image().set_from_file("./mesa4vacia.png")
         
        elif widget == self.btn81:
            widget.get_image().set_from_file("./mesa8vaciav2.png")
          
        elif widget == self.btn43:
            widget.get_image().set_from_file("./mesa4vacia.png")
           
        elif widget == self.btn44:
            widget.get_image().set_from_file("./mesa4vacia.png")
       
        elif widget == self.btn82:
            widget.get_image().set_from_file("./mesa8vaciav2.png")
       
        elif widget == self.btn101:
            widget.get_image().set_from_file("./mesa10vacia.png")
          
        else:
            widget.get_image().set_from_file("./mesa10vacia.png")
           
    #metodo para ocupar la mesa
    def ocupar(self,widget,data=None):
        sel = self.treeclientes.get_selection()
        (tm,ti) =sel.get_selected()
        cliente = "anonimo"
        if ti is not None:
            cliente = tm.get_value(ti,0)
        mesa = self.lblmesa.get_text()
        if mesa is not None:
            fila=(cliente,self.idcamarero,mesa,datetime.date.today())
            BDres.insmesa(self.dictmesas,self.treemesas,self.listmesas,fila)
            
    def verfact(self,widget):
        sel = self.treemesas.get_selection()
        self.listcom.clear()
        self.entud.set_editable(False)
        (tm,ti) = sel.get_selected()
        if ti is not None:
            self.idmesa = tm.get_value(ti,0)
            BDres.checkfacturas(self.treefact,self.listfact,self.idmesa)
            
    def verlineas(self,widget,data=None):
        self.entud.set_editable(True)
        sel = self.treefact.get_selection()
        (tm,ti) = sel.get_selected()
        if ti is not None:
            self.id = tm.get_value(ti,0)
            self.pagada = 1 if tm.get_value(ti,5) == "SI" else 0
            BDres.verlineas(self.treecom,self.listcom,self.id)
            
    def addlineaf(self,widget):
        unidades = int(self.entud.get_text())
        fila = (int(self.id),int(self.servicio),unidades)
        BDres.addlinea(self.treecom,self.listcom,fila)
        self.entud.set_text("")
        self.entservicio.set_text("")
        
    def pagar(self,widget):
        sacarpdf.genfact(self.id,self.user)
        dir = os.getcwd()
        os.system('/usr/bin/xdg-open ' + dir + '/factura_'+str(self.id)+'.pdf')
        if self.pagada==0:
            BDres.pagar(self.id,self.idmesa,self.listfact,self.treefact,self.listcom)
            BDres.cargamesas(self.dictmesas,self.treemesas,self.listmesas)
            
    def set_style(self):
        """
        Change Gtk+ Style
        """
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-theme-name", "Adwaita")
        settings.set_property("gtk-application-prefer-dark-theme", True)


if __name__ == '__main__':
    main = Restaurante()
    Gtk.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    