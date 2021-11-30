import pymysql
import conexion

class Telefono:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarTelefonos()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux

    def consultarTelefonos(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM telefono WHERE estado = 'A'")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarTelefono(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM telefono WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarTelefono(self, idUsuario, telefono):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO telefono (id_usuario, numero_telefono, estado) 
        VALUES('{}','{}', 'A')'''.format(idUsuario,telefono)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarTelefono(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE telefono SET estado='I' WHERE Id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarTelefono(self, id, telefono):
        cur = self.cnn.cursor()
        sql='''UPDATE telefono SET numero_telefono='{}' WHERE Id={}'''.format(telefono, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n

    def validarDato(self,string):
        return string.isdigit()

