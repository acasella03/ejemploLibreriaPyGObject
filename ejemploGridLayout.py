import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Grid Layout con Gtk")

        boton1 = Gtk.Button(label="Botón 1")
        boton2 = Gtk.Button(label="Botón 2")
        boton3 = Gtk.Button(label="Botón 3")
        boton4 = Gtk.Button(label="Botón 4")
        boton5 = Gtk.Button(label="Botón 5")
        boton6 = Gtk.Button(label="Botón 6")

        red = Gtk.Grid()
        red.add(boton1)
        red.attach(boton2,1,0,2,1)
        red.attach(boton3,0,1,1,2)
        red.attach_next_to(boton4,boton3,Gtk.PositionType.RIGHT,2,1)
        red.attach_next_to(boton5,boton4,Gtk.PositionType.BOTTOM,1,1)
        red.attach_next_to(boton6,boton5,Gtk.PositionType.RIGHT,1,1)


        self.add(red)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
