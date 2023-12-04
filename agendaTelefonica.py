import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
import sqlite3 as dbapi #para imprimir los datos del SQLite

columnas = ("Nombre", "Apellido", "Número de teléfono") # Nombres de las columnas
'''agendaTelf= (("Juan", "Pérez", "605 568 478"),
             ("Ana", "Sánchez", "986 120 967"),
             ("José", "López", "689 552 123"),
             ("Manuel", "García", "602 405 633")) # Datos de la agenda telefónica'''
class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo listin telefónico con Treeview")
        self.set_default_size(250, 100)
        self.set_border_width(10)

        modelo=Gtk.ListStore(str, str, str) # Creo una tabla (modelo) con 3 columnas de tipo texto

        try:
            bbdd= dbapi.connect("bdListinTelefonico.dat")
            c = bbdd.cursor()
            c.execute("""select * from listaTelefonos""")
            for datos in c:
                modelo.append(datos)
            c.close()
            bbdd.close()
        except dbapi.DatabaseError as e:
            print (e)

        trvVista= Gtk.TreeView(model=modelo) # Creo una vista de la tabla
        objetoSeleccion=trvVista.get_selection() # Creo un objeto de selección de la tabla
        objetoSeleccion.connect("changed", self.on_objetoSeleccion_changed) # Conecto la señal de cambio de selección con el método on_objetoSeleccion_changed

        for i, nomColumna in enumerate(columnas): # Recorremos las columnas
            celda=Gtk.CellRendererText() # Creo una celda de tipo texto
            if i==0: # Si es la primera columna, la hago negrita
                celda.props.weight_set=True # Si es la primera columna, la hago negrita
                celda.props.weight=Pango.Weight.BOLD
            if i==2: # Si es la tercera columna, la hago editable
                celda.props.editable=True # Si es la tercera columna, la hago editable
                celda.connect("edited", self.on_celda_telefono_edited,modelo,i) # Conecto la señal de edición de la celda con el método on_celda_edited
            columnaTabla=Gtk.TreeViewColumn(nomColumna, celda, text=i) # Creo una columna de la tabla con la celda anterior y el texto de la columna correspondiente de la tabla
            trvVista.append_column(columnaTabla) # Añado la columna a la vista de la tabla

        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        caja.pack_start(trvVista, True, True, 0)

        grid= Gtk.Grid()
        caja.pack_start(grid, True, True, 0)
        lblNombre=Gtk.Label(label="Nombre:")
        lblApellido=Gtk.Label(label="Apellido:")
        lblTelefono=Gtk.Label(label="Teléfono:")
        self.txtNombre=Gtk.Entry()
        self.txtApellido=Gtk.Entry()
        self.txtTelefono=Gtk.Entry()
        btnIngresar=Gtk.Button(label="Añadir")
        btnBorrar=Gtk.Button(label="Borrar")
        grid.add(lblNombre)
        grid.attach_next_to(self.txtNombre, lblNombre, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(lblApellido, self.txtNombre, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(self.txtApellido, lblApellido, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(lblTelefono, lblNombre, Gtk.PositionType.BOTTOM,1,1)
        grid.attach_next_to(self.txtTelefono, lblTelefono, Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(btnIngresar, self.txtTelefono, Gtk.PositionType.RIGHT,2, 1)
        grid.attach_next_to(btnBorrar, btnIngresar, Gtk.PositionType.BOTTOM,2, 1)
        btnIngresar.connect("clicked", self.on_btnIngresar_clicked, modelo)
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked, objetoSeleccion)


        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_objetoSeleccion_changed(self, seleccion): # Método que se ejecuta cuando cambia la selección de la tabla
        modelo, punteroFila = seleccion.get_selected()
        print("El usuario seleccionado es: ", modelo[punteroFila][0], modelo[punteroFila][1], modelo[punteroFila][2])

    def on_celda_telefono_edited(self, celda, fila, texto, modelo, columna): # Método que se ejecuta cuando se edita la celda
        modelo[fila][columna]=texto # Cambio el valor de la celda en el modelo de la tabla


    def on_btnIngresar_clicked(self, boton, modelo):
        elemento=list() # Creo una lista vacía
        if self.txtNombre.get_text()!="" and self.txtApellido.get_text()!="" and self.txtTelefono.get_text()!="":
            elemento=[self.txtNombre.get_text(), self.txtApellido.get_text(), self.txtTelefono.get_text()]

        modelo.append(elemento) # Añado una fila al modelo de la tabla
        self.txtNombre.set_text("")
        self.txtApellido.set_text("")
        self.txtTelefono.set_text("")
        try:
            bbdd= dbapi.connect("bdListinTelefonico.dat")
            c = bbdd.cursor()
            c.execute("""insert into listaTelefonos values(?,?,?)""",elemento) # Añado una fila a la base de datos
            bbdd.commit() # Guardo los cambios
            c.close()
            bbdd.close()
        except dbapi.Error as e:
            print (e)
        except dbapi.DatabaseError as e:
            print (e)

    def on_btnBorrar_clicked(self, boton, objetoSeleccion):
        (modelo,fila)=objetoSeleccion.get_selected() # Obtengo el modelo y la fila seleccionada
        try:
            bbdd= dbapi.connect("bdListinTelefonico.dat")
            c = bbdd.cursor()
            c.execute("""delete from listaTelefonos where telefono=?""", (modelo[fila][2],)) # Borro la fila seleccionada de la base de datos
            bbdd.commit() # Guardo los cambios
            c.close()
            bbdd.close()
        except dbapi.Error as e:
            print (e)
        except dbapi.DatabaseError as e:
            print (e)
        modelo.remove(fila) # Borro la fila seleccionada del modelo de la tabla


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()