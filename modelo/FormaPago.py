import pymysql
import conexion

class Pago:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarFormasPago()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarFormasPago(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM formapago")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarFormaPago(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM formapago WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarFormaPago(self, nombre):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO formapago (nombre, estado) 
        VALUES('{}', 'A')'''.format(nombre)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarFormaPago(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE formapago SET estado='I' WHERE id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarFormaPago(self, id, nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE formapago SET nombre='{}' WHERE id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n