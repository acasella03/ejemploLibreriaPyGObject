import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
import sqlite3 as dbapi  # para imprimir los datos del SQLite


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Treeview Filtrado y Ordenado")
        self.set_default_size(250, 100)
        self.set_border_width(10)
        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        self.filtradoGenero = "None"
        modelo = Gtk.ListStore(str, str, int, str, bool)
        modelo_filtrado = modelo.filter_new()
        modelo_filtrado.set_visible_func(self.filtro_usuarios_genero)

        # Conexión a la base de datos
        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
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

        # tryDatosUsuarios = Gtk.TreeView(model=modelo)  # creamos el TreeView
        tryDatosUsuarios = Gtk.TreeView(model=modelo_filtrado)
        seleccion = tryDatosUsuarios.get_selection()  # creamos la selección

        for i, tituloColumna in enumerate(["Dni", "Nome"]):  # creamos las columnas
            celda = Gtk.CellRendererText()  # creamos la celda
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i)  # creamos la columna
            tryDatosUsuarios.append_column(columna)  # añadimos la columna al TreeView

        celda = Gtk.CellRendererProgress()  # para la barra de progreso
        columna = Gtk.TreeViewColumn("Edade", celda,
                                     value=2)  # creamos la columna con una variable columna distinta a la anterior que nada tiene que ver
        tryDatosUsuarios.append_column(columna)

        modeloCombo = Gtk.ListStore(str)  # para el combo
        modeloCombo.append(("Home",))  # añadimos los valores al combo
        modeloCombo.append(("Muller",))  # añadimos los valores al combo
        modeloCombo.append(("Outro",))  # añadimos los valores al combo
        celda = Gtk.CellRendererCombo()  # creamos la celda
        celda.set_property("editable", True)  # prpiedad para que se pueda editar
        celda.props.model = modeloCombo  # propiedad donde pasamos el modelo, para que sepa que valores tiene que mostrar
        celda.set_property("text-column", 0)  # propiedad para que sepa que columna tiene que mostrar
        celda.set_property("has-entry", False)  # propiedad para que se pueda escribir
        celda.connect("edited", self.on_celdaGenero_edited, modelo_filtrado, 3)

        columna = Gtk.TreeViewColumn("Xenero", celda, text=3)
        tryDatosUsuarios.append_column(columna)

        caja.pack_start(tryDatosUsuarios, True, True, 2)

        cajaH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        caja.pack_start(cajaH, True, True, 0)

        rbtHombre = Gtk.RadioButton(label="Home")
        rbtMujer = Gtk.RadioButton.new_with_label_from_widget(rbtHombre, label="Muller")
        rbtOtro = Gtk.RadioButton.new_with_label_from_widget(rbtHombre, label="Outro")
        cajaH.pack_start(rbtHombre, True, True, 2)
        cajaH.pack_start(rbtMujer, True, True, 2)
        cajaH.pack_start(rbtOtro, True, True, 2)
        rbtHombre.connect("toggled", self.on_genero_toggled, "Home", modelo_filtrado)
        rbtMujer.connect("toggled", self.on_genero_toggled, "Muller", modelo_filtrado)
        rbtOtro.connect("toggled", self.on_genero_toggled, "Outro", modelo_filtrado)

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_celdaGenero_edited(self, celda, fila, texto, modelo, columna):
        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute("UPDATE usuarios SET xenero=? WHERE dni=?",
                           (texto, modelo[fila][0]))
            bbdd.commit()
        except dbapi.Error as e:
            print(e)
        except dbapi.DatabaseError as e:
            print("Error al cargar la base de datos")
        finally:
            cursor.close()
            bbdd.close()

        modelo[fila][columna] = texto
        modelo.refilter()

    def on_genero_toggled(self, botonSeleccionado, genero, modelo):
        if botonSeleccionado.get_active():
            self.filtradoGenero = genero
            modelo.refilter()

    def filtro_usuarios_genero(self, modelo, fila, datos):
        if self.filtradoGenero is None or self.filtradoGenero == "None":
            return True
        else:
            return modelo[fila][3] == self.filtradoGenero


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
