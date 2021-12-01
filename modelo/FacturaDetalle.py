import pymysql
import conexion

class FacturaDetalle:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarFacturasDetalle()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarFacturasDetalle(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM facturadetalle")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarColorFacturaDetalle(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM facturadetalle WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarFacturaDetalle(self, id_factura,id_servicio):
        cur = self.cnn.cursor()
        sql = "SELECT valor FROM servicio WHERE id = {}".format(id_servicio)
        cur.execute(sql)
        st = cur.fetchone()
        sub=int(st[0])
        subtotal=sub*1
        iva= subtotal*0.19
        total=subtotal+iva
        sql2 ='''INSERT INTO facturadetalle (id_factura,id_servicio,cantidad,subtotal,iva,total,estado) 
        VALUES('{}','{}','{}','{}','{}','{}','A')'''.format(id_factura,id_servicio,1,subtotal,iva,total)
        cur.execute(sql2)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarFacturaDetalle(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE facturadetalle SET estado='I' WHERE id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarFacturaDetalle(self, id, nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE facturadetalle SET nombre='{}' WHERE id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n