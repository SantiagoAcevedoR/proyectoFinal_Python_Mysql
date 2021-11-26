from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from TipoUsuario import *


    

class Ventana(Frame):

    tipo = TipoUsuario()
       
    def __init__(self, master=None):
        super().__init__(master,width=680, height=260)
        self.master = master
        self.pack()
        self.create_widgets()
        self.llenarTabla()
        self.habilitarCajasTexto("disabled")
        self.habilitarBotonesOper("normal")
        self.habilitarBotonesGuardar("disabled")
        self.id=-1
    
    def habilitarCajasTexto(self, estado):
        self.txtNombre.configure(state=estado)

    def limpiarCajasTexto(self):
        self.txtNombre.delete(0,END)

    def limpiarTabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def habilitarBotonesOper(self,estado):
        self.btnNuevo.configure(state=estado)                
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        
    def habilitarBotonesGuardar(self,estado):
        self.btnGuardar.configure(state=estado)                
        self.btnCancelar.configure(state=estado)        
    
    def llenarTabla(self):
        datos= self.tipo.consultarTipos()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2]))

    def fNuevo(self):
        self.habilitarCajasTexto("normal")
        self.habilitarBotonesOper("disabled")
        self.habilitarBotonesGuardar("normal")
        self.limpiarCajasTexto()
        self.txtNombre.focus()
        
    
    def fGuardar(self): 
        nombre =self.txtNombre.get()
        if self.id ==-1:       
            self.tipo.insertarTipo(nombre)             
            messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')
        else:
            self.tipo.modificarTipo(self.id,nombre)
            messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
            self.id = -1            
        self.limpiarTabla()
        self.llenarTabla() 
        self.limpiarCajasTexto() 
        self.habilitarBotonesGuardar("disabled")      
        self.habilitarBotonesOper("normal")
        self.habilitarCajasTexto("disabled")  
        
                 
    def fModificar(self):
        selected = self.tabla.focus()                               
        clave = self.tabla.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Modificar", 'Debes seleccionar un elemento.')            
        else:            
            self.id= clave  
            self.habilitarCajasTexto("normal")                         
            valores = self.tabla.item(selected,'values')
            self.limpiarCajasTexto()           
            self.txtNombre.insert(0,valores[0])          
            self.habilitarBotonesOper("disabled")
            self.habilitarBotonesGuardar("normal")
            self.txtNombre.focus()        
        
    
    def fEliminar(self):
        selected = self.tabla.focus()                               
        clave = self.tabla.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            valores = self.tabla.item(selected,'values')
            data ="id: "+ str(clave) + ", Nombre: " + valores[0] + ", Estado: " + valores[1]
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n" + data)            
            if r == messagebox.YES:
                self.tipo.eliminarTipo(clave)
                messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                self.limpiarTabla()
                self.llenarTabla()
        
        

    def fCancelar(self):
        r = messagebox.askquestion("Calcelar", "Esta seguro que desea cancelar la operación actual")
        if r == messagebox.YES:
            self.limpiarCajasTexto() 
            self.habilitarBotonesGuardar("disabled")      
            self.habilitarBotonesOper("normal")
            self.habilitarCajasTexto("disabled")

    def create_widgets(self):
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=259)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)    


        frame2 = Frame(self,bg="#d3dde3" )
        frame2.place(x=95,y=0,width=150, height=259)                        
        lbl1 = Label(frame2,text="Nombre: ")
        lbl1.place(x=3,y=5)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=25,width=90, height=20)                
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=210,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=210,width=60, height=30)      

        frame3 = Frame(self,bg="#d3dde3" )
        frame3.place(x=247,y=0,width=420, height=259)   
        self.tabla = ttk.Treeview(frame3, columns=("col1","col2"))        
        self.tabla.column("#0",width=120, anchor=CENTER)
        self.tabla.column("col1",width=150, anchor=CENTER)
        self.tabla.column("col2",width=130, anchor=CENTER)    
        self.tabla.heading("#0", text="Id", anchor=CENTER)
        self.tabla.heading("col1", text="nombre", anchor=CENTER)
        self.tabla.heading("col2", text="Estado", anchor=CENTER)    
        self.tabla.pack(side=LEFT, fill=Y)
        sb = Scrollbar(frame3,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        self.tabla.config(yscrollcommand=sb.set)
        sb.config(command=self.tabla.yview)
        self.tabla['selectmode']='browse'


        