import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ventanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Primera Ventana con Gtk")

        caja = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)



        imagen = Gtk.Image()
        imagen.set_from_file("gatito.png")
        caja.pack_start(imagen, True, True, 5)
        lblEtiqueta = Gtk.Label(label="Hola a todos!!!!")
        caja.pack_start(lblEtiqueta, True, True, 5)
        txtSaludo = Gtk.Entry()
        txtSaludo.connect("activate", self.on_txtSaludo_activate, lblEtiqueta)
        caja.pack_start(txtSaludo, True,False, 5)
        btnBoton = Gtk.Button(label="Click")
        btnBoton.connect("clicked", self.on_btnBoton_clicked, lblEtiqueta)
        caja.pack_start(btnBoton, False, False, 5)
        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_btnBoton_clicked(self, boton, etiqueta):
        etiqueta.set_text("Hola alumnos del GTK")

    def on_txtSaludo_activate(self, cuadroTexto, etiqueta):
        etiqueta.set_text(cuadroTexto.get_text())

if __name__ == "__main__":
    ventanaPrincipal()
    Gtk.main()
