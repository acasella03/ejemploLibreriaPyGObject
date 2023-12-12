import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk



class primeraVentana(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo de TreeView con CellRendererPixbuf")

        self.set_default_size(250, 100)
        self.set_border_width(10)

        cajaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        modelo = Gtk.ListStore(str, str)
        modelo.append(("Nuevo", "document-new"))
        modelo.append(("Abrir", "document-open"))
        modelo.append(("Guardar", "document-save"))

        treeView = Gtk.TreeView(model=modelo)

        celdaTexto = Gtk.CellRendererText()
        col_texto = Gtk.TreeViewColumn("Texto",celdaTexto, text=0)
        treeView.append_column(col_texto)

        celdaImagen = Gtk.CellRendererPixbuf()
        col_imagen = Gtk.TreeViewColumn("Imagen",celdaImagen, icon_name=1)
        treeView.append_column(col_imagen)

        cajaV.pack_start(treeView, True, True, 0)


        self.add(cajaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ =="__main__":
    primeraVentana()
    Gtk.main()