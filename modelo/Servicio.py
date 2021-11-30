import pymysql
import conexion

class Servicio:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)


    def __str__(self):
        datos=self.consultarServicios()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarServicios(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM servicio")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarServicio(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM servicio WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarServicio(self, nombre, valor, cantidad):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO servicio (nombre, valor, cantidad, estado) 
        VALUES('{}', '{}', '{}', 'A')'''.format(nombre, valor, cantidad)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n

    def eliminarServicio(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE servicio SET estado='I' WHERE Id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarServicio(self, id, nombre, valor, cantidad):
        cur = self.cnn.cursor()
        sql='''UPDATE servicio SET nombre='{}', valor='{}',cantitad='{}' WHERE id={}'''.format(nombre, valor, cantidad , id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n