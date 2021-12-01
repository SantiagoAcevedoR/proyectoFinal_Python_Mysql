import pymysql
import conexion

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

    def consultarFacturasConDetalle(self):
        cur = self.cnn.cursor()
        cur.execute("select j.id_factura, sum(j.cantidad), sum(j.subtotal), sum(j.iva), sum(j.total), r.fecha from  facturadetalle j, factura r where j.id_factura = r.id  and j.estado ='A' group by j.id_factura;")
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

    def insertarFactura(self,id,id_usuario,id_pago,fecha):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO factura (id,id_usuario, id_pago, fecha, estado) 
        VALUES('{}','{}','{}','{}','A')'''.format(id, id_usuario, id_pago, fecha)
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