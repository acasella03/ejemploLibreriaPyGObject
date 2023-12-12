import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio
import pathlib



class primeraVentana(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Explorador de archivos")

        self.set_default_size(250, 100)
        self.set_border_width(10)

        area = Gtk.FlowBox()
        contenidoCarpeta = pathlib.Path('.')

        for elemento in contenidoCarpeta.iterdir():
            caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            tipo ="folder" if elemento.is_dir() else "text-x-generic"
            icono = Gio.ThemedIcon(name=tipo)
            imagen = Gtk.Image.new_from_gicon(icono, Gtk.IconSize.MENU)
            caja.pack_start(imagen, True,True, 0)
            caja.pack_start(Gtk.Label(label=elemento.name), True,True, 0)
            area.add(caja)


        self.add(area)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ =="__main__":
    primeraVentana()
    Gtk.main()