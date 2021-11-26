import pymysql
import conexion

class especie:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)


    def __str__(self):
        datos=self.consultarEspecies()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarEspecies(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM especie")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarEspecie(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM especie WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarEspecie(self, nombre):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO especie (nombre, estado) 
        VALUES('{}', 'A')'''.format(nombre)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarEspecie(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE especie SET estado='I' WHERE Id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarTipo(self, id, nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE especie SET nombre='{}' WHERE Id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n
