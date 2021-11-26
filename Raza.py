import pymysql
import conexion

class raza:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)


    def __str__(self):
        datos=self.consultarRazas()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarRazas(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM raza")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarRaza(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM raza WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarRaza(self, nombre):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO raza (nombre, estado) 
        VALUES('{}', 'A')'''.format(nombre)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarRaza(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE raza SET estado='I' WHERE Id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarRaza(self, id, nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE raza SET nombre='{}' WHERE Id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n