import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ventanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo con check y radio button")

        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        frmMarco = Gtk.Frame(label="Opciones excluyentes")
        caja.pack_start(frmMarco, False, False, 2)
        cajaRbt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        rbtBoton1 = Gtk.RadioButton.new_with_label_from_widget(None, "Botón 1")
        rbtBoton1.connect("toggled", self.on_rbtBoton_toggled, "1")
        cajaRbt.pack_start(rbtBoton1, False, False, 2)

        rbtBoton2 = Gtk.RadioButton.new_from_widget(rbtBoton1)
        rbtBoton2.set_label("Botón 2")
        rbtBoton2.connect("toggled", self.on_rbtBoton_toggled, "2")
        cajaRbt.pack_start(rbtBoton2, False, False, 2)

        rbtBoton3 = Gtk.RadioButton.new_with_mnemonic_from_widget(rbtBoton1, "_Botón 3")
        rbtBoton3.connect("toggled", self.on_rbtBoton_toggled, "3")
        cajaRbt.pack_start(rbtBoton3, False, False, 2)

        frmMarco.add(cajaRbt)

        chkBoton4 = Gtk.CheckButton()
        chkBoton4.set_label("Check 4")
        chkBoton4.connect("toggled", self.on_chkBoton_toggled)
        caja.pack_start(chkBoton4, False, False, 2)

        chkBoton5 = Gtk.CheckButton.new_with_label("Check 5")
        chkBoton5.connect("toggled", self.on_chkBoton_toggled)
        caja.pack_start(chkBoton5, False, False, 2)

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_rbtBoton_toggled(self, boton, numero):
        if boton.get_active():
            print("Botón ", numero, " fue activado")
        else:
            print("Boton ", numero, "fue desactivado")

    def on_chkBoton_toggled(self, boton):
        if boton.get_active():
            print("CheckButton activado: ", boton.get_label())
        else:
            print("CheckButton desactivado: ", boton.get_label())


if __name__ == "__main__":
    ventanaPrincipal()
    Gtk.main()
