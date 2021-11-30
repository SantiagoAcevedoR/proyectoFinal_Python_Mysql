import pymysql
import conexion
from datetime import date

class Factura:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarFacturas()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarFacturas(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM factura")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarFactura(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM factura WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarFactura(self, id_ususario,id_pago):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO factura (id_ususario, id_pago, fecha, estado) 
        VALUES('{}', 'A')'''.format(id_ususario, id_pago, date.today)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n 

    def eliminarFactura(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE factura SET estado='I' WHERE id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    # def modificarFactura(self, id, nombre):
    #     cur = self.cnn.cursor()
    #     sql='''UPDATE factura SET nombre='{}' WHERE id={}'''.format(nombre, id)
    #     cur.execute(sql)
    #     n=cur.rowcount
    #     self.cnn.commit()    
    #     cur.close()
    #     return n