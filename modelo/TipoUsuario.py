import pymysql
import conexion

class TipoUsuario:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarTipos()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
        
    def consultarTipos(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM tipousuario WHERE estado ='A'")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarTipo(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM tipousuario WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarTipo(self, nombre):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO tipousuario (nombre, estado) 
        VALUES('{}', 'A')'''.format(nombre)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarTipo(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE tipousuario SET estado='I' WHERE id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarTipo(self, id, nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE tipousuario SET nombre='{}' WHERE id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n


    def validarDato(self,string):
        return string.isdigit()




 

    
