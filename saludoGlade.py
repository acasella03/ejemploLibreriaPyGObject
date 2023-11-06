import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Aplicacion():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("saludoGlade.glade")

        wndVentanaPrincipal = builder.get_object("wndVentanaPrincipal")
        self.lblEtiqueta = builder.get_object("lblEtiqueta")
        self.txtNombre = builder.get_object("txtNombre")
        self.btnSaludo = builder.get_object("btnSaludo")
        senales = {
            "on_btnSaludo_clicked": self.on_btnBoton_clicked,
            "on_txtNombre_activate": self.on_txtNombre_activate
        }
        builder.connect_signals(senales)

    def on_btnBoton_clicked(self, boton):
        self.lblEtiqueta.set_text("Hola "+ self.txtNombre.get_text())

    def on_txtNombre_activate(self, cuadroTexto):
        self.lblEtiqueta.set_text("Hola " + cuadroTexto.get_text())


if __name__ == "__main__":
    Aplicacion()
    Gtk.main()
