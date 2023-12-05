import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
import sqlite3 as dbapi #para imprimir los datos del SQLite

class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Treeview Filtrado y Ordenado")
        self.set_default_size(250, 100)
        self.set_border_width(10)
        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        modelo=Gtk.ListStore(str, str, int, str, bool)

        #Conexión a la base de datos
        try:
            bbdd= dbapi.connect("baseDatos2.dat")
            cursor=bbdd.cursor()
            cursor.execute("SELECT * FROM usuarios")
            for fila in cursor:
                modelo.append(fila)
        except dbapi.Error as e:
            print(e)
        except dbapi.DatabaseError as e:
            print("Error al cargar la base de datos")
        finally:
            cursor.close()
            bbdd.close()

        tryDatosUsuarios = Gtk.TreeView(model=modelo) #creamos el TreeView
        seleccion= tryDatosUsuarios.get_selection() #creamos la selección

        for i, tituloColumna in enumerate(["Dni", "Nome"]): #creamos las columnas
            celda = Gtk.CellRendererText() #creamos la celda
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i) #creamos la columna
            tryDatosUsuarios.append_column(columna) #añadimos la columna al TreeView

        celda=Gtk.CellRendererProgress() #para la barra de progreso
        columna=Gtk.TreeViewColumn("Edade", celda, value=2) #creamos la columna con una variable columna distinta a la anterior que nada tiene que ver
        tryDatosUsuarios.append_column(columna)

        modeloCombo=Gtk.ListStore(str) #para el combo
        modeloCombo.append(("Home",)) #añadimos los valores al combo
        modeloCombo.append(("Muller",)) #añadimos los valores al combo
        modeloCombo.append(("Outro",)) #añadimos los valores al combo
        celda=Gtk.CellRendererCombo() #creamos la celda
        celda.set_property("editable", True) # prpiedad para que se pueda editar
        celda.props.model=modeloCombo #propiedad donde pasamos el modelo, para que sepa que valores tiene que mostrar
        celda.set_property("text-column", 0) #propiedad para que sepa que columna tiene que mostrar
        celda.set_property("has-entry", False) #propiedad para que se pueda escribir

        columna=Gtk.TreeViewColumn("Xenero", celda, text=3)
        tryDatosUsuarios.append_column(columna)

        caja.pack_start(tryDatosUsuarios, True, True, 2)



        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()