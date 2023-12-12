import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio
import pathlib


class primeraVentana(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Explorador de archivos en arbol")

        self.set_default_size(250, 100)
        self.set_border_width(10)

        self.modelo = Gtk.TreeStore(str)
        arbol = Gtk.TreeView(model=self.modelo)

        celdaTexto = Gtk.CellRendererText()
        trvColumna = Gtk.TreeViewColumn("Text",celdaTexto, text=0)
        arbol.append_column(trvColumna)

        self.explorarDirectorio('.', None)

        self.add(arbol)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    def explorarDirectorio(self,ruta, punteroPadre):
        contenido = pathlib.Path(ruta)
        for entrada in contenido.iterdir():
            punteroHijo = self.modelo.append(punteroPadre,(entrada.name,))
            if entrada.is_dir():
                self.explorarDirectorio(ruta+'/'+entrada.name, punteroHijo) #Las barras son para que no se junten las rutas


if __name__ =="__main__":
    primeraVentana()
    Gtk.main()