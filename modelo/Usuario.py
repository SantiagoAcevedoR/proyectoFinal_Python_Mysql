
import pymysql
import conexion

class Usuario:
    
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)



    def __str__(self):
        datos=self.consultarUsuarios()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
        
    def consultarUsuarios(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM usuario WHERE estado ='A'")
        datos = cur.fetchall()
        cur.close()
        return datos 

    def buscarUsuario(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM usuario WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def buscarNombreUsuario(self, nombre_usuario):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM usuario WHERE nombre_usuario = '{}';".format(nombre_usuario)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos


    def buscarIdUsuario(self, nombre_usuario):
        cur = self.cnn.cursor()
        sql = "SELECT id FROM usuario WHERE nombre_usuario = '{}';".format(nombre_usuario)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarUsuario(self,id_tipo,nombre_usuario,contrasenia,nombres,apellidos,numero_cedula,edad,direccion):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO usuario (id_tipo, nombre_usuario, contrasenia, nombres, apellidos, numero_cedula, edad, direccion, estado) 
        VALUES('{}','{}', '{}', '{}', '{}', '{}','{}', '{}', 'A')'''.format(id_tipo,nombre_usuario,contrasenia,nombres,apellidos,numero_cedula,edad,direccion)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarUsuario(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE usuario SET estado='I' WHERE id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def consultarNombresUsuarios(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT nombre_usuario FROM usuario WHERE estado ='A' and id_tipo=3")
        datos = cur.fetchall()
        cur.close()
        return datos


    def modificarUsuario(self, id,nombres,apellidos,numero_cedula,edad,direccion):
        cur = self.cnn.cursor()
        sql='''UPDATE usuario SET nombres='{}',apellidos='{}',numero_cedula='{}',edad='{}',direccion='{}'  WHERE id={}'''.format(nombres,apellidos,numero_cedula,edad,direccion, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n

    def validarDato(self,string):
        return string.isdigit()
