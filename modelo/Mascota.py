import pymysql
import conexion

class Mascota:
    def __init__(self):
        self.cnn = pymysql.connect(host=conexion.host, user=conexion.user,password=conexion.password, database=conexion.database)

    def __str__(self):
        datos=self.consultarMascotas()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
        
    def consultarMascotas(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM mascota WHERE estado ='A'")
        datos = cur.fetchall()
        cur.close()
        return datos

    def consultarMascotasPorId(self,id):
        cur = self.cnn.cursor()
        sql="SELECT * FROM mascota WHERE id_usuario ={}".format(id)
        cur.execute(sql)
        datos = cur.fetchall()
        cur.close()
        return datos  

    def buscarMascota(self, id):
        cur = self.cnn.cursor()
        sql = "SELECT * FROM mascota WHERE id = {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertarMascota(self, id_usuario,nombre,id_especie,id_raza,id_color,anio):
        cur = self.cnn.cursor()
        sql ='''INSERT INTO mascota (id_usuario, nombre, id_especie, id_raza, id_color, anio_nacimiento, estado) 
        VALUES('{}','{}', '{}', '{}', '{}', '{}', 'A')'''.format(id_usuario,nombre,id_especie,id_raza,id_color,anio)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n 

    def eliminarMascota(self, id):
        cur = self.cnn.cursor()
        sql ='''UPDATE mascota SET estado='I' WHERE id={}'''.format(id)  
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n  

    def modificarMascota(self, id,nombre):
        cur = self.cnn.cursor()
        sql='''UPDATE mascota SET nombre='{}' WHERE id={}'''.format(nombre, id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n
