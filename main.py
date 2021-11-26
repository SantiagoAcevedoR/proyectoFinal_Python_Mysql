from tkinter import *
from Vista import *


def main():
    root = Tk()
    root.wm_title("Veterinaria")
    screenWidth = root.winfo_screenwidth()  # Obtenga el ancho del área de visualización
    screenHeight = root.winfo_screenheight()  # Obtenga la altura del área de visualización
    width = 680  # Establecer ancho de ventana
    height = 280  # Establecer altura de ventana
    left = (screenWidth - width) / 2
    top = (screenHeight - height) / 2
    root.geometry("%dx%d+%d+%d" % (width, height, left, top))
    app = Ventana(root)
    app.mainloop()

if __name__ == "__main__":
    main()