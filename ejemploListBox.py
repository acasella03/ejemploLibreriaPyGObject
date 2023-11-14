import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FilaListBoxConDatos(Gtk.ListBoxRow):
    def __init__(self, palabra):
        super().__init__()
        self.palabra = palabra
        self.add(Gtk.Label(label=palabra))


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo ListBox")

        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        listbox = Gtk.ListBox()
        caja.pack_start(listbox, True, True, 0)

        elementos = "Esta es una cadena para ordenar en ListBox, para el ListBox".split()
        for palabra in elementos:
            listbox.add(FilaListBoxConDatos(palabra))

        def funcion_ordenar(fila1, fila2):
            return fila1.palabra.lower() > fila2.palabra.lower()

        def funcion_filtrar(fila):
            return False if fila.palabra == "ListBox" else True

        listbox.set_sort_func(funcion_ordenar)
        listbox.set_filter_func(funcion_filtrar)
        listbox.connect("row-activated", self.on_row_activated)


        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_row_activated(self,listBox,fila):
        print (fila.palabra)


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
