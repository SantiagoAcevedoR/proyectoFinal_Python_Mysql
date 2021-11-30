import os

class manejoArchivo():
    def escribirArchivo(palabra):
        file = open("archivos/filename.txt", "w")
        file.write(str(palabra) + os.linesep)
        file.close()

    def leerArchivo():
        f = open ("archivos/filename.txt","r")
        mensaje = f.read()
        f.close()
        return mensaje

    def elminarArchivo():
        f = open("archivos/filename.txt","w")
        f.close()


