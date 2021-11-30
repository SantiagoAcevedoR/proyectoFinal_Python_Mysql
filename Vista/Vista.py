from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modelo.TipoUsuario import TipoUsuario
from modelo.Usuario import Usuario
from modelo.Telefono import Telefono
from modelo.Raza import Raza
from modelo.Color import Color
from modelo.Especie import Especie
from modelo.Mascota import Mascota
from modelo.archivo import manejoArchivo

class APP(tk.Tk):
    
    def __init__(self,*args,**kwargs):
      
        super().__init__(*args,**kwargs)
        self.configure(bg = "grey")
        self.title("Veterinaria")
        self.columnconfigure( 0, weight = 1 )
        self.rowconfigure(0, weight = 1)
        contenedor_principal = tk.Frame( self ,bg = "yellow")
        contenedor_principal.grid( padx = 2, pady = 2 , sticky = "nsew")
        self.todos_los_frames = dict()
        for F in (Tipos,InicioSesion, Registro,UsuarioPanel,VeterinarioPanel,AdministradorPanel,Razas,Colores,Especies,MascotasAdmin,TelefonosAdmin,UsuariosAdmin,MascotasUserA):
            frame = F( contenedor_principal , self)
            self.todos_los_frames[F] = frame
            frame.configure(width=700,height=300)
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame( InicioSesion )
    
    def show_frame(self,contenedor_llamado):
        frame = self.todos_los_frames[contenedor_llamado]
        frame.tkraise()

class Tipos(Frame):

    tipo = TipoUsuario()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=300)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=150, height=300)                        
        self.lbl1 = Label(frame2,text="Nombre: ")
        self.lbl1.place(x=3,y=5)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=25,width=90, height=20)                
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=235,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=235,width=60, height=30)      
        frame3 = Frame(self,bg="#d3dde3" )
        frame3.place(x=247,y=0,width=440, height=300)   
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
        if self.txtNombre.get()!="":
            if self.tipo.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","El tipo es incorrecto, escribalo de nuevo")
            else:
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
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")

                      
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

    
class InicioSesion(Frame):
    usuario=Usuario()
    
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#E6F7F5")
        frame1.place(x=0,y=0,width=700, height=300)
        self.img= PhotoImage(file="fotos\logo.png")
        self.imgLbl = Label(frame1,image=self.img)
        self.imgLbl.place(x=0,y=0,width=339)
        self.lbl1 = Label(frame1,text="Usuario: ")
        self.lbl1.place(x=3,y=100)        
        self.txtUsuario=Entry(frame1)
        self.txtUsuario.place(x=100,y=100,width=90, height=30)
        self.lbl2 = Label(frame1,text="Contraseña: ")
        self.lbl2.place(x=3,y=150)        
        self.txtContra=Entry(frame1)
        self.txtContra.place(x=100,y=140,width=90, height=30)         
        self.btnAdmin=Button(frame1,text="Iniciar como Admin",relief="flat",bg="#E6F7F5", command=lambda:controller.show_frame( AdministradorPanel )) 
        self.btnAdmin.place(x=30,y=190,width=130, height=20) 
        self.btnVet=Button(frame1,text="Iniciar como Veterinario",relief="flat",bg="#E6F7F5", command=lambda:controller.show_frame( VeterinarioPanel )) 
        self.btnVet.place(x=30,y=215,width=130, height=20) 
        self.btnUser=Button(frame1,text="Iniciar como Propietario",relief="flat",bg="#E6F7F5", command=lambda:controller.show_frame( UsuarioPanel )) 
        self.btnUser.place(x=30,y=240,width=130, height=20)
        self.img2= PhotoImage(file="fotos\icono.png")
        self.photoimage = self.img2.subsample(7)
        self.btnRegistro=Button(frame1, command=lambda:controller.show_frame( Registro ),relief="flat",bg="#E6F7F5",image=self.photoimage)
        self.btnRegistro.place(x=240,y=210,width=50, height=40)
        self.img3= PhotoImage(file="fotos\check.png")
        self.photoimage2 = self.img3.subsample(25)
        self.btnRegistro=Button(frame1, command=self.verificar,relief="flat",bg="#E6F7F5",image=self.photoimage2)
        self.btnRegistro.place(x=240,y=110,width=50, height=50)
        self.img4= PhotoImage(file="fotos\perro.png") 
        self.imagen_sub=self.img4.subsample(2)
        self.imgLbl2 = Label(frame1,image=self.imagen_sub)
        self.imgLbl2.place(x=340,y=0,width=360,height=300)
        self.habilitarBotonesIniciar("disabled")
        manejoArchivo.elminarArchivo()


    def limpiarCajasTexto(self):
        self.txtUsuario.delete(0,END)
        self.txtContra.delete(0,END)
        self.txtUsuario.focus()
    
    def verificar(self):
        if self.txtUsuario.get()=="" and self.txtContra.get()=="":
            messagebox.showinfo("Insertar datos","Los datos no estan completos")
        else:
            usuario=self.txtUsuario.get()
            contra=self.txtContra.get()
            ver=self.verificarUsuario(usuario)
            ver2=self.verificarContra(usuario)
            if ver=="" or ver2!=contra:
                messagebox.showwarning("Usuario Incorrecto","Usuario incorrecto o contraseña incorrecta")
            elif ver==1:
                self.btnAdmin.configure(state="normal")
                self.btnUser.configure(state="disabled")
                self.btnVet.configure(state="disabled")
                id=self.encontrarId(usuario)
                manejoArchivo.escribirArchivo(id)
            elif ver==2:
                self.btnAdmin.configure(state="disabled")
                self.btnUser.configure(state="disabled")
                self.btnVet.configure(state="normal")
                id=self.encontrarId(usuario)
                manejoArchivo.escribirArchivo(id)
            elif ver==3:
                self.btnAdmin.configure(state="disabled")
                self.btnUser.configure(state="normal")
                self.btnVet.configure(state="disabled")
                id=self.encontrarId(usuario)
                manejoArchivo.escribirArchivo(id)

        self.limpiarCajasTexto()

    def encontrarId(self,usuario):
        aux=""
        dato=self.usuario.buscarNombreUsuario(usuario)
        if dato is None:
            dato=""
            aux=dato
        else:
            aux=dato[0]
        return aux      
    
    def verificarUsuario(self,usuario):
        aux=""
        dato=self.usuario.buscarNombreUsuario(usuario)
        if dato is None:
            dato=""
            aux=dato
        else:
            aux=dato[1]
        return aux

    def verificarContra(self,usuario):
        aux=""
        dato=self.usuario.buscarNombreUsuario(usuario)
        if dato is None:
            dato=""
            aux=dato
        else:
            aux=dato[3]
        return aux

    def habilitarBotonesIniciar(self,estado):
        self.btnAdmin.configure(state=estado)
        self.btnVet.configure(state=estado)
        self.btnUser.configure(state=estado)
  

class Registro(Frame):

    user=Usuario()
    telefono=Telefono()

    def __init__(self, container,controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#E6F7F5")
        frame1.place(x=0,y=0,width=700, height=300)
        self.img= PhotoImage(file="fotos\logoalargado.png")
        self.imgLbl = Label(frame1,image=self.img)
        self.imgLbl.place(x=0,y=0,width=700,height=90)
        self.btnIniciar=Button(frame1,text="Registrarse", command=self.fRegistro)
        self.btnIniciar.place(x=245,y=240,width=90, height=30)
        self.lblNUsuario = Label(frame1,text="Nombre de Usuario: ",bg="#E6F7F5")
        self.lblNUsuario.place(x=10,y=100)        
        self.txtNUsuario=Entry(frame1)
        self.txtNUsuario.place(x=10,y=125,width=90, height=20)     
        self.lblContra = Label(frame1,text="Contraseña: ",bg="#E6F7F5")
        self.lblContra.place(x=170,y=100)        
        self.txtContra=Entry(frame1)
        self.txtContra.place(x=170,y=125,width=90, height=20)  
        self.lblNombre = Label(frame1,text="Nombres: ",bg="#E6F7F5")
        self.lblNombre.place(x=340,y=100)        
        self.txtNombre=Entry(frame1)
        self.txtNombre.place(x=340,y=125,width=90, height=20)
        self.lblApellido = Label(frame1,text="Apellidos: ",bg="#E6F7F5")
        self.lblApellido.place(x=510,y=100)        
        self.txtApellido=Entry(frame1)
        self.txtApellido.place(x=510,y=125,width=90, height=20)
        self.lblNCedula = Label(frame1,text="Cedula: ",bg="#E6F7F5")
        self.lblNCedula.place(x=10,y=160)        
        self.txtNCedula=Entry(frame1)
        self.txtNCedula.place(x=10,y=185,width=90, height=20)     
        self.lblEdad = Label(frame1,text="Edad: ",bg="#E6F7F5")
        self.lblEdad.place(x=170,y=160)        
        self.txtEdad=Entry(frame1)
        self.txtEdad.place(x=170,y=185,width=90, height=20)  
        self.lblTel = Label(frame1,text="Numero de Telefono: ",bg="#E6F7F5")
        self.lblTel.place(x=340,y=160)        
        self.txtTel=Entry(frame1)
        self.txtTel.place(x=340,y=185,width=90, height=20)
        self.lblDirec = Label(frame1,text="Direccion: ",bg="#E6F7F5")
        self.lblDirec.place(x=510,y=160)        
        self.txtDirec=Entry(frame1)
        self.txtDirec.place(x=510,y=185,width=90, height=20) 
        self.img2= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img2.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(InicioSesion),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        self.limpiarCajasTexto()
        
       
    def fRegistro(self):
        if self.txtNUsuario.get()!="" and self.txtContra.get()!="" and self.txtNombre.get()!="" and self.txtApellido.get()!="" and self.txtNCedula.get()!="" and self.txtEdad.get()!="" and self.txtTel.get()!="" and self.txtDirec.get()!="":
            if self.user.validarDato(self.txtEdad.get())==False:
                messagebox.showwarning("Datos erroneos","La edad es incorrecta, escribala de nuevo")
            elif self.user.validarDato(self.txtTel.get())==False:
                messagebox.showwarning("Datos erroneos","El telefono es incorrecto, escribalo de nuevo")
            elif self.user.validarDato(self.txtNCedula.get())==False:
                messagebox.showwarning("Datos erroneos","La cedula es incorrecta, escribala de nuevo")
            elif self.user.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","El nombre es incorrecto, escribalo de nuevo")
            elif self.user.validarDato(self.txtApellido.get())==True:
                messagebox.showwarning("Datos erroneos","El apellido es incorrecto, escribalo de nuevo")
            else:
                usuario=self.txtNUsuario.get()
                contra=self.txtContra.get()
                nombre=self.txtNombre.get()
                apellido=self.txtApellido.get()
                cedula=self.txtNCedula.get()
                edad=self.txtEdad.get()
                tel=self.txtTel.get()
                direc=self.txtDirec.get()
                user=self.user.buscarNombreUsuario(usuario)
                aux=""
                if user is None:
                    user=""
                    aux=user
                else:
                    aux=user[2]

                if aux==usuario:
                    messagebox.showwarning("Cuidado","Ese usuario ya existe, escriba otro")
                else:
                    self.user.insertarUsuario(3,usuario,contra,nombre,apellido,cedula,edad,direc)
                    id=self.user.buscarNombreUsuario(usuario)
                    self.id=id[0]
                    self.telefono.insertarTelefono(self.id,tel)
                    messagebox.showinfo("Insertar","La informacion del usuario ha sido guardada correctamente")
                    self.limpiarCajasTexto()
        else:
            messagebox.showwarning("INFOMRACION","Faltan datos en los campos")


    def limpiarCajasTexto(self):
        self.txtNombre.delete(0,END)
        self.txtNUsuario.delete(0,END)
        self.txtContra.delete(0,END)
        self.txtNombre.delete(0,END)
        self.txtApellido.delete(0,END)
        self.txtNCedula.delete(0,END)
        self.txtEdad.delete(0,END)
        self.txtTel.delete(0,END)
        self.txtDirec.delete(0,END)

class UsuarioPanel(Frame):


    def __init__(self, container,controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#E6F7F5")
        frame1.place(x=0,y=0,width=700, height=300)
        self.img= PhotoImage(file="fotos\perfil.png")
        self.photo = self.img.subsample(1)
        self.imgLbl = Label(frame1,image=self.photo)
        self.imgLbl.place(x=0,y=0,width=700,height=90)
        self.btnMascotas=Button(frame1,text="Agregar Mascota",command=lambda:controller.show_frame(MascotasUserA))
        self.btnMascotas.place(x=260,y=150,width=100, height=30)
        self.btnUsuarios=Button(frame1,text="Ver mascotas")
        self.btnUsuarios.place(x=260,y=200,width=100, height=30)
        self.btnFacturas=Button(frame1,text="Ver perfil")
        self.btnFacturas.place(x=370,y=150,width=100, height=30)
        self.btnTipoUsuario=Button(frame1,text="Modificar usuario")
        self.btnTipoUsuario.place(x=370,y=200,width=100, height=30)

class MascotasUserA(Frame):

    user=Usuario()
    raza=Raza()
    color=Color()
    especie=Especie()

    def __init__(self, container,controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#E6F7F5")
        frame1.place(x=0,y=0,width=700, height=300)
        self.img= PhotoImage(file="fotos\logoalargado.png")
        
        self.imgLbl = Label(frame1,image=self.img)
        self.imgLbl.place(x=0,y=0,width=700,height=90)
        self.gato= PhotoImage(file="fotos\gato.png")
        self.photoimg = self.gato.subsample(3)
        self.imgLbl1 = Label(frame1,image=self.photoimg)
        self.imgLbl1.place(x=350,y=90,width=350,height=210)
        self.btnIniciar=Button(frame1,text="Registrarse", command=self.fRegistro)
        self.btnIniciar.place(x=160,y=240,width=90, height=30)    
        self.lblNombre = Label(frame1,text="Nombre: ",bg="#E6F7F5")
        self.lblNombre.place(x=10,y=100)        
        self.txtNombre=Entry(frame1)
        self.txtNombre.place(x=10,y=125,width=90, height=20)
        self.lblRaza = Label(frame1,text="Raza: ",bg="#E6F7F5")
        self.lblRaza.place(x=10,y=160)        
        self.comboRaza=ttk.Combobox(frame1,state="readonly")
        self.comboRaza['values']=['Seleccione']
        datos= self.raza.consultarNombresRazas()
        for row in datos:
            self.comboRaza['values']=tuple(list(self.comboRaza['values'])+[str(row[0])])
        self.comboRaza.place(x=10,y=185)
        self.comboRaza.current(0)
        self.lblColor = Label(frame1,text="Color: ",bg="#E6F7F5")
        self.lblColor.place(x=170,y=100)        
        self.comboColor=ttk.Combobox(frame1,state="readonly")
        self.comboColor['values']=['Seleccione']
        datos= self.color.consultarNombresColores()
        for row in datos:
            self.comboColor['values']=tuple(list(self.comboColor['values'])+[str(row[0])])
        self.comboColor.place(x=170,y=125)
        self.comboColor.current(0)
        self.lblAnio= Label(frame1,text="Año nacimiento: ",bg="#E6F7F5")
        self.lblAnio.place(x=170,y=160)        
        self.txtAnio=Entry(frame1)
        self.txtAnio.place(x=170,y=185,width=40, height=20)
        self.txtMes=Entry(frame1)
        self.txtMes.place(x=210,y=185,width=25, height=20)
        self.txtDia=Entry(frame1)
        self.txtDia.place(x=235,y=185,width=25, height=20)
        self.img2= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img2.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(InicioSesion),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        self.limpiarCajasTexto()

       
    def fRegistro(self):
        if self.txtNombre.get()!="" and self.txtNombre.get()!="" and self.txtNombre.get()!="" and self.txtApellido.get()!="" and self.txtNCedula.get()!="" and self.txtEdad.get()!="" and self.txtTel.get()!="" and self.txtDirec.get()!="":
            if self.user.validarDato(self.txtEdad.get())==False:
                messagebox.showwarning("Datos erroneos","La edad es incorrecta, escribala de nuevo")
            elif self.user.validarDato(self.txtTel.get())==False:
                messagebox.showwarning("Datos erroneos","El telefono es incorrecto, escribalo de nuevo")
            elif self.user.validarDato(self.txtNCedula.get())==False:
                messagebox.showwarning("Datos erroneos","La cedula es incorrecta, escribala de nuevo")
            elif self.user.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","El nombre es incorrecto, escribalo de nuevo")
            elif self.user.validarDato(self.txtApellido.get())==True:
                messagebox.showwarning("Datos erroneos","El apellido es incorrecto, escribalo de nuevo")
            else:
                usuario=""
                contra=self.txtContra.get()
                nombre=self.txtNombre.get()
                edad=self.txtEdad.get()
                user=self.user.buscarNombreUsuario()
                aux=""
                if user is None:
                    user=""
                    aux=user
                else:
                    aux=user[2]

                if aux==usuario:
                    messagebox.showwarning("Cuidado","Ese usuario ya existe, escriba otro")
                else:
                    self.user.insertarUsuario(3,usuario,contra,nombre,edad)
                    
                    messagebox.showinfo("Insertar","La informacion del usuario ha sido guardada correctamente")
                    self.limpiarCajasTexto()
        else:
            messagebox.showwarning("INFOMRACION","Faltan datos en los campos")


    def limpiarCajasTexto(self):
        self.txtNombre.delete(0,END)
        self.txtAnio.delete(0,END)
        self.txtMes.delete(0,END)
        self.txtDia.delete(0,END)
        

class VeterinarioPanel(Frame):

    def __init__(self, container,controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#E6F7F5")
        frame1.place(x=0,y=0,width=700, height=300)

class AdministradorPanel(Frame):
    def __init__(self, container,controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#E6F7F5")
        frame1.place(x=0,y=0,width=700, height=300)
        self.img= PhotoImage(file="fotos\panelito.png")
        self.photo = self.img.subsample(3)
        self.imgLbl = Label(frame1,image=self.photo)
        self.imgLbl.place(x=0,y=0,width=700,height=90)
        self.btnMascotas=Button(frame1,text="Mascotas",command=lambda:controller.show_frame(MascotasAdmin))
        self.btnMascotas.place(x=70,y=150,width=90, height=30)
        self.btnUsuarios=Button(frame1,text="Usuarios",command=lambda:controller.show_frame(UsuariosAdmin))
        self.btnUsuarios.place(x=70,y=200,width=90, height=30)
        self.btnFacturas=Button(frame1,text="Facturas")
        self.btnFacturas.place(x=170,y=150,width=90, height=30)
        self.btnTipoUsuario=Button(frame1,text="Tipos de usuario",command=lambda:controller.show_frame(Tipos))
        self.btnTipoUsuario.place(x=170,y=200,width=90, height=30)
        self.btnrazas=Button(frame1,text="Razas",command=lambda:controller.show_frame(Razas))
        self.btnrazas.place(x=270,y=150,width=90, height=30)
        self.btnColor=Button(frame1,text="Colores",command=lambda:controller.show_frame(Colores))
        self.btnColor.place(x=270,y=200,width=90, height=30)
        self.btnTel=Button(frame1,text="Telefonos",command=lambda:controller.show_frame(TelefonosAdmin))
        self.btnTel.place(x=370,y=150,width=90, height=30)
        self.btnFPago=Button(frame1,text="Formas de pago")
        self.btnFPago.place(x=370,y=200,width=90, height=30)
        self.btnEspecies=Button(frame1,text="Especies",command=lambda:controller.show_frame(Especies))
        self.btnEspecies.place(x=470,y=150,width=90, height=30)
        self.btnServicio=Button(frame1,text="Servicios")
        self.btnServicio.place(x=470,y=200,width=90, height=30)
        self.img2= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img2.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(InicioSesion),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 

class Razas(Frame):

    raza = Raza()
    especie = Especie()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=300)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=150, height=300)                        
        self.lbl1 = Label(frame2,text="Nombre: ")
        self.lbl1.place(x=3,y=5)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=25,width=90, height=20) 
        self.lbl2 = Label(frame2,text="Especie: ")
        self.lbl2.place(x=3,y=65)        
        self.txtEspecie=Entry(frame2)
        self.txtEspecie.place(x=3,y=85,width=90, height=20)
        self.btnCambiar=Button(frame2,text="Modificar", command=self.fCambiar, bg="light blue", fg="white")
        self.btnCambiar.place(x=10,y=195,width=60, height=30)                  
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=235,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=235,width=60, height=30)      
        frame3 = Frame(self,bg="#d3dde3" )
        frame3.place(x=247,y=0,width=440, height=300)   
        self.tabla = ttk.Treeview(frame3, columns=("col1","col2","col3"))        
        self.tabla.column("#0",width=80, anchor=CENTER)
        self.tabla.column("col1",width=100, anchor=CENTER)
        self.tabla.column("col2",width=130, anchor=CENTER)
        self.tabla.column("col3",width=100, anchor=CENTER)      
        self.tabla.heading("#0", text="Id", anchor=CENTER)
        self.tabla.heading("col1", text="Especie", anchor=CENTER)
        self.tabla.heading("col2", text="nombre", anchor=CENTER)
        self.tabla.heading("col3", text="Estado", anchor=CENTER)      
        self.tabla.pack(side=LEFT, fill=Y)
        sb = Scrollbar(frame3,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        self.tabla.config(yscrollcommand=sb.set)
        sb.config(command=self.tabla.yview)
        self.tabla['selectmode']='browse'
        self.llenarTabla()
        self.habilitarCajasTexto("disabled")
        self.habilitarBotonesOper("normal")
        self.habilitarBotonesGuardar("disabled")
        self.id=-1
        
    
    def habilitarCajasTexto(self, estado):
        self.txtNombre.configure(state=estado)
        self.txtEspecie.configure(state=estado)

    def limpiarCajasTexto(self):
        self.txtNombre.delete(0,END)
        self.txtEspecie.delete(0,END)

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
        datos= self.raza.consultarRazas()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2],row[3]))

    def fNuevo(self):
        self.habilitarCajasTexto("normal")
        self.habilitarBotonesOper("disabled")
        self.habilitarBotonesGuardar("normal")
        self.limpiarCajasTexto()
        self.txtNombre.focus()

    def fCambiar(self):
        if self.txtNombre.get()!="":
            if self.raza.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","La raza es incorrecta, escribala de nuevo")
            else:
                nombre =self.txtNombre.get()
                self.raza.modificarRaza(self.id,nombre)
                messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
                self.id = -1 
                self.limpiarTabla()
                self.llenarTabla() 
                self.limpiarCajasTexto() 
                self.habilitarBotonesGuardar("disabled")      
                self.habilitarBotonesOper("normal")
                self.habilitarCajasTexto("disabled") 
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")

    
        
    def fGuardar(self):
        if self.txtNombre.get()!="" and self.txtEspecie.get()!="":
            if self.raza.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","La raza es incorrecta, escribala de nuevo")
            elif self.raza.validarDato(self.txtEspecie.get())==True:
                messagebox.showwarning("Datos erroneos","La especie es incorrecta, escribala de nuevo")
            else: 
                nombre =self.txtNombre.get()
                especie =self.txtEspecie.get()
                idEspecie=self.verificarEspecie(especie)
                if idEspecie=="":
                    messagebox.showwarning("Datos erroneos","La especie no existe, escribala de nuevo")
                else:
                    if self.id ==-1:       
                        self.raza.insertarRaza(idEspecie,nombre)             
                        messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')
                    else:
                        messagebox.showwarning("Boton Equivocado","Este boton sirve para otra funcion")           
                    self.limpiarTabla()
                    self.llenarTabla() 
                    self.limpiarCajasTexto() 
                    self.habilitarBotonesGuardar("disabled")      
                    self.habilitarBotonesOper("normal")
                    self.habilitarCajasTexto("disabled")
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")
    
    def verificarEspecie(self,especie):
        aux=""
        dato=self.especie.buscarNombreEspecie(especie)
        if dato is None:
            dato=""
            aux=dato
        else:
            aux=dato[0]
        return aux


                      
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
            self.txtNombre.insert(0,valores[1])          
            self.habilitarBotonesOper("disabled")
            self.habilitarBotonesGuardar("normal")
            self.txtEspecie.configure(state="disabled")
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
                self.raza.eliminarRaza(clave)
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

class Colores(Frame):

    color = Color()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=300)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=150, height=300)                        
        self.lbl1 = Label(frame2,text="Nombre: ")
        self.lbl1.place(x=3,y=5)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=25,width=90, height=20)                
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=235,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=235,width=60, height=30)      
        frame3 = Frame(self,bg="#d3dde3" )
        frame3.place(x=247,y=0,width=440, height=300)   
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
        datos= self.color.consultarColores()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2]))

    def fNuevo(self):
        self.habilitarCajasTexto("normal")
        self.habilitarBotonesOper("disabled")
        self.habilitarBotonesGuardar("normal")
        self.limpiarCajasTexto()
        self.txtNombre.focus()
        
    def fGuardar(self): 
        if self.txtNombre.get()!="":
            if self.color.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","El color es incorrecto, escribalo de nuevo")
            else: 
                nombre =self.txtNombre.get()
                if self.id ==-1:       
                    self.color.insertarColor(nombre)             
                    messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')
                else:
                    self.color.modificarColor(self.id,nombre)
                    messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
                    self.id = -1            
                self.limpiarTabla()
                self.llenarTabla() 
                self.limpiarCajasTexto() 
                self.habilitarBotonesGuardar("disabled")      
                self.habilitarBotonesOper("normal")
                self.habilitarCajasTexto("disabled")  
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")
                      
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
                self.color.eliminarColor(clave)
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

class Especies(Frame):

    especie = Especie()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=300)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=150, height=300)                        
        self.lbl1 = Label(frame2,text="Nombre: ")
        self.lbl1.place(x=3,y=5)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=25,width=90, height=20)                
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=235,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=235,width=60, height=30)      
        frame3 = Frame(self,bg="#d3dde3" )
        frame3.place(x=247,y=0,width=440, height=300)   
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
        datos= self.especie.consultarEspecies()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2]))

    def fNuevo(self):
        self.habilitarCajasTexto("normal")
        self.habilitarBotonesOper("disabled")
        self.habilitarBotonesGuardar("normal")
        self.limpiarCajasTexto()
        self.txtNombre.focus()
        
    def fGuardar(self): 
        if self.txtNombre.get()!="":
            if self.especie.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","La especie es incorrecta, escribala de nuevo")
            else: 
                nombre =self.txtNombre.get()
                if self.id ==-1:       
                    self.especie.insertarEspecie(nombre)             
                    messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')
                else:
                    self.especie.modificarEspecie(self.id,nombre)
                    messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
                    self.id = -1            
                self.limpiarTabla()
                self.llenarTabla() 
                self.limpiarCajasTexto() 
                self.habilitarBotonesGuardar("disabled")      
                self.habilitarBotonesOper("normal")
                self.habilitarCajasTexto("disabled")  
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")
                      
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
                self.especie.eliminarEspecie(clave)
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

class MascotasAdmin(Frame):

    mascota = Mascota()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=90, height=300) 
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=590, height=300)                                
        self.tabla = ttk.Treeview(frame2, columns=("col1","col2","col3","col4","col5","col6","col7"))        
        self.tabla.column("#0",width=40, anchor=CENTER)
        self.tabla.column("col1",width=70, anchor=CENTER)
        self.tabla.column("col2",width=70, anchor=CENTER)
        self.tabla.column("col3",width=70, anchor=CENTER) 
        self.tabla.column("col4",width=70, anchor=CENTER) 
        self.tabla.column("col5",width=70, anchor=CENTER)     
        self.tabla.column("col6",width=100, anchor=CENTER) 
        self.tabla.column("col7",width=70, anchor=CENTER) 
        self.tabla.heading("#0", text="Id", anchor=CENTER)
        self.tabla.heading("col1", text="Id Usuario", anchor=CENTER)
        self.tabla.heading("col2", text="nombre", anchor=CENTER) 
        self.tabla.heading("col3", text="Especie", anchor=CENTER)  
        self.tabla.heading("col4", text="Raza", anchor=CENTER)     
        self.tabla.heading("col5", text="Color", anchor=CENTER)  
        self.tabla.heading("col6", text="Año nacimiento", anchor=CENTER)  
        self.tabla.heading("col7", text="Estado", anchor=CENTER)  
        self.tabla.pack(side=LEFT, fill=Y)
        sb = Scrollbar(frame2,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        self.tabla.config(yscrollcommand=sb.set)
        sb.config(command=self.tabla.yview)
        self.tabla['selectmode']='browse'
        self.llenarTabla()
        
        
        
    
    def limpiarTabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
 
    
    def llenarTabla(self):
        datos= self.mascota.consultarMascotas()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
      
    
    def fEliminar(self):
        selected = self.tabla.focus()                               
        clave = self.tabla.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            valores = self.tabla.item(selected,'values')
            data ="id: "+ str(clave) + ", Id usuario: " + valores[0] +", Nombre: " + valores[1] + ", Especie: " + valores[2] +", Raza: " + valores[3] +", Color: " + valores[4] +", Año Nacimiento: " + valores[5] + ", Estado: " + valores[6]
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n" + data)            
            if r == messagebox.YES:
                self.mascota.eliminarMascota(clave)
                messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                self.limpiarTabla()
                self.llenarTabla()
              
class UsuariosAdmin(Frame):

    usuario = Usuario()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=90, height=300) 
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=590, height=300)                                
        self.tabla = ttk.Treeview(frame2, columns=("col1","col2","col3","col4","col5","col6","col7","col8","col9"))        
        self.tabla.column("#0",width=40, anchor=CENTER)
        self.tabla.column("col1",width=70, anchor=CENTER)
        self.tabla.column("col2",width=70, anchor=CENTER)
        self.tabla.column("col3",width=70, anchor=CENTER) 
        self.tabla.column("col4",width=70, anchor=CENTER) 
        self.tabla.column("col5",width=70, anchor=CENTER)     
        self.tabla.column("col6",width=100, anchor=CENTER) 
        self.tabla.column("col7",width=70, anchor=CENTER)
        self.tabla.column("col8",width=70, anchor=CENTER)
        self.tabla.column("col9",width=70, anchor=CENTER) 
        self.tabla.heading("#0", text="Id", anchor=CENTER)
        self.tabla.heading("col1", text="Tipo Usuario", anchor=CENTER)
        self.tabla.heading("col2", text="Usuario", anchor=CENTER) 
        self.tabla.heading("col3", text="Contraseña", anchor=CENTER)  
        self.tabla.heading("col4", text="Nombres", anchor=CENTER)     
        self.tabla.heading("col5", text="Apellidos", anchor=CENTER)  
        self.tabla.heading("col6", text="Cedula", anchor=CENTER)
        self.tabla.heading("col7", text="Edad", anchor=CENTER)
        self.tabla.heading("col8", text="Direccion", anchor=CENTER)  
        self.tabla.heading("col9", text="Estado", anchor=CENTER)  
        self.tabla.pack(side=LEFT, fill=Y)
        sb = Scrollbar(frame2,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        self.tabla.config(yscrollcommand=sb.set)
        sb.config(command=self.tabla.yview)
        self.tabla['selectmode']='browse'
        self.llenarTabla()
        
        
        
    
    def limpiarTabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
 
    
    def llenarTabla(self):
        datos= self.usuario.consultarUsuarios()
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
      
    
    def fEliminar(self):
        selected = self.tabla.focus()                               
        clave = self.tabla.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            valores = self.tabla.item(selected,'values')
            data ="id: "+ str(clave) + ", Id tipo: " + valores[0] +", usuario: " + valores[1] + ", Contraseña: " + valores[2] +", Nombres: " + valores[3] +", Apellidos: " + valores[4] +", Cedula: " + valores[5] +", Edad: " + valores[6] +", Direccion: " + valores[7] + ", Estado: " + valores[8]
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n" + data)            
            if r == messagebox.YES:
                self.usuario.eliminarUsuario(clave)
                messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                self.limpiarTabla()
                self.llenarTabla()
    
class TelefonosAdmin(Frame):

    telefono = Telefono()
    usuario = Usuario()
       
    def __init__(self, container, controller,*args, **kwargs):
        super().__init__(container, *args, **kwargs)
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=300)        
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        self.img= PhotoImage(file="fotos\devolverse.png")
        self.photoimage = self.img.subsample(7)
        self.btnDevolverse=Button(frame1, command=lambda:controller.show_frame(AdministradorPanel),image=self.photoimage, compound = LEFT)
        self.btnDevolverse.place(x=5,y=235,width=40, height=40) 
        frame2 = Frame(self,bg="#d3dde3")
        frame2.place(x=95,y=0,width=150, height=300)                        
        self.lbl1 = Label(frame2,text="Telefono: ")
        self.lbl1.place(x=3,y=5)        
        self.txtNumero=Entry(frame2)
        self.txtNumero.place(x=3,y=25,width=90, height=20) 
        self.lbl2 = Label(frame2,text="Usuario: ")
        self.lbl2.place(x=3,y=65)        
        self.txtNombre=Entry(frame2)
        self.txtNombre.place(x=3,y=85,width=90, height=20)
        self.btnCambiar=Button(frame2,text="Modificar", command=self.fCambiar, bg="light blue", fg="white")
        self.btnCambiar.place(x=10,y=195,width=60, height=30)                  
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=10,y=235,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=80,y=235,width=60, height=30)      
        frame3 = Frame(self,bg="#d3dde3" )
        frame3.place(x=247,y=0,width=440, height=300)   
        self.tabla = ttk.Treeview(frame3, columns=("col1","col2","col3"))        
        self.tabla.column("#0",width=80, anchor=CENTER)
        self.tabla.column("col1",width=100, anchor=CENTER)
        self.tabla.column("col2",width=130, anchor=CENTER)
        self.tabla.column("col3",width=100, anchor=CENTER)      
        self.tabla.heading("#0", text="Id", anchor=CENTER)
        self.tabla.heading("col1", text="Id Usuario", anchor=CENTER)
        self.tabla.heading("col2", text="numero", anchor=CENTER)
        self.tabla.heading("col3", text="Estado", anchor=CENTER)      
        self.tabla.pack(side=LEFT, fill=Y)
        sb = Scrollbar(frame3,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        self.tabla.config(yscrollcommand=sb.set)
        sb.config(command=self.tabla.yview)
        self.tabla['selectmode']='browse'
        self.llenarTabla()
        self.habilitarCajasTexto("disabled")
        self.habilitarBotonesOper("normal")
        self.habilitarBotonesGuardar("disabled")
        self.id=-1
        
    
    def habilitarCajasTexto(self, estado):
        self.txtNombre.configure(state=estado)
        self.txtNumero.configure(state=estado)

    def limpiarCajasTexto(self):
        self.txtNombre.delete(0,END)
        self.txtNumero.delete(0,END)

    def limpiarTabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def habilitarBotonesOper(self,estado):
        self.btnNuevo.configure(state=estado)                
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        
    def habilitarBotonesGuardar(self,estado):
        self.btnCambiar.configure(state=estado)
        self.btnGuardar.configure(state=estado)                
        self.btnCancelar.configure(state=estado)        
    
    def llenarTabla(self):
        datos= self.telefono.consultarTelefonos()
        
        for row in datos:
            self.tabla.insert("",END,text=row[0],values=(row[1],row[2],row[3]))

    def fNuevo(self):
        self.habilitarCajasTexto("normal")
        self.habilitarBotonesOper("disabled")
        self.habilitarBotonesGuardar("normal")
        self.limpiarCajasTexto()
        self.txtNumero.focus()

    def fCambiar(self):
        if self.txtNumero.get()!="":
            if self.telefono.validarDato(self.txtNumero.get())==False:
                messagebox.showwarning("Datos erroneos","El telefono es incorrecto, escribalo de nuevo")
            else:
                num =self.txtNumero.get()
                self.telefono.modificarTelefono(self.id,num)
                messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
                self.id = -1 
                self.limpiarTabla()
                self.llenarTabla() 
                self.limpiarCajasTexto() 
                self.habilitarBotonesGuardar("disabled")      
                self.habilitarBotonesOper("normal")
                self.habilitarCajasTexto("disabled") 
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")

        
    def fGuardar(self):
        if self.txtNombre.get()!="" and self.txtNumero.get()!="":
            if self.telefono.validarDato(self.txtNombre.get())==True:
                messagebox.showwarning("Datos erroneos","El usuario es incorrecto, escribalo de nuevo")
            elif self.telefono.validarDato(self.txtNumero.get())==False:
                messagebox.showwarning("Datos erroneos","El telefono es incorrecto, escribalo de nuevo")
            else: 
                nombre =self.txtNombre.get()
                num =self.txtNumero.get()
                idusuario=self.verificarUsuario(nombre)
                if idusuario=="":
                    messagebox.showwarning("Datos erroneos","El usuario no existe, escribalo de nuevo")
                else:
                    if self.id ==-1:       
                        self.telefono.insertarTelefono(idusuario,num)             
                        messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')    
                    else:
                        messagebox.showwarning("Boton Equivocado","Este boton sirve para otra funcion")      
                    self.limpiarTabla()
                    self.llenarTabla() 
                    self.limpiarCajasTexto() 
                    self.habilitarBotonesGuardar("disabled")      
                    self.habilitarBotonesOper("normal")
                    self.habilitarCajasTexto("disabled")
        else:
            messagebox.showwarning("Campos vacios","El campo esta vacio, por favor llenelo")
    
    
    def verificarUsuario(self,nombre):
        aux=""
        dato=self.usuario.buscarNombreUsuario(nombre)
        if dato is None:
            dato=""
            aux=dato
        else:
            aux=dato[0]
        return aux

                      
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
            self.txtNumero.insert(0,valores[1])          
            self.habilitarBotonesOper("disabled")
            self.habilitarBotonesGuardar("normal")
            self.txtNombre.configure(state="disabled")
            self.txtNumero.focus()             
    
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
                self.telefono.eliminarTelefono(clave)
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
        
    



        

    
    


        