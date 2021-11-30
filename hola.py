import tkinter as tk
from tkinter import ttk

def boton_aumentar():
	etiqueta.config(image=imagen_zoom)
def boton_reducir():
	etiqueta.config(image=imagen_sub)
def boton_original():
	etiqueta.config(image=imagen)
	
ventana=tk.Tk()
ventana.title("Ajuste de imagen")
ventana.geometry("600x500")

imagen=tk.PhotoImage(file="perro.png")
#Aumenta las dimensiones de la imagen en un (2 * ancho_imagen)
imagen_zoom=imagen.zoom(2)
#Reduce las dimensiones de la imagen en un (ancho_imagen / 2)
imagen_sub=imagen.subsample(2)
etiqueta=ttk.Label(image=imagen)
etiqueta.place(x=130, y=20)

boton_zoom=ttk.Button(text="Aumentar(200%)", command=boton_aumentar)
boton_zoom.place(x=20, y=20, width=100)
boton_ori=ttk.Button(text="Original  (100%)", command=boton_original)
boton_ori.place(x=20, y=50, width=100)
boton_sub=ttk.Button(text="Reducir    (50%)", command=boton_reducir)
boton_sub.place(x=20, y=80, width=100)

ventana.mainloop()