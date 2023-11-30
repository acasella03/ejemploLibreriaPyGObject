import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

columnas = ("Nombre", "Apellido", "Número de teléfono") # Nombres de las columnas
agendaTelf= (("Juan", "Pérez", "605 568 478"),
             ("Ana", "Sánchez", "986 120 967"),
             ("José", "López", "689 552 123"),
             ("Manuel", "García", "602 405 633")) # Datos de la agenda telefónica
class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo listin telefónico con Treeview")
        self.set_default_size(250, 100)
        self.set_border_width(10)

        modelo=Gtk.ListStore(str, str, str) # Creo una tabla (modelo) con 3 columnas de tipo texto

        for usuario in agendaTelf: # Recorremos la agenda telefónica
            modelo.append(usuario) # Añadimos cada usuario a la tabla, solo admite un parámetro tipo tupla o lista

        trvVista= Gtk.TreeView(model=modelo) # Creo una vista de la tabla
        objetoSeleccion=trvVista.get_selection() # Creo un objeto de selección de la tabla
        objetoSeleccion.connect("changed", self.on_objetoSeleccion_changed)

        for i, nomColumna in enumerate(columnas): # Recorremos las columnas
            celda=Gtk.CellRendererText() # Creo una celda de tipo texto
            if i==0:
                celda.props.weight_set=True # Si es la primera columna, la hago negrita
                celda.props.weight=Pango.Weight.BOLD
            columnaTabla=Gtk.TreeViewColumn(nomColumna, celda, text=i) # Creo una columna de la tabla con la celda anterior y el texto de la columna correspondiente de la tabla
            trvVista.append_column(columnaTabla) # Añado la columna a la vista de la tabla

        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        caja.pack_start(trvVista, True, True, 0)




        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_objetoSeleccion_changed(self, seleccion):
        modelo, punteroFila = seleccion.get_selected()
        print("El usuario seleccionado es: ", modelo[punteroFila][0], modelo[punteroFila][1], modelo[punteroFila][2])

if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()