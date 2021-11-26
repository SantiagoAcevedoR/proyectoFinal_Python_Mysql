import pymysql
import conexion

class Color:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarColores()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarColores(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM color")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarColor(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM color WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarColor(self, nombre):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO color (nombre, estado) 
        VALUES('{}', 'A')'''.format(nombre)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarColor(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE color SET estado='I' WHERE Id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarColor(self, id, nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE color SET nombre='{}' WHERE Id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n