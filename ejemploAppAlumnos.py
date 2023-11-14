import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo expediente académico")

        # Primero hay que observar que disposición general tienen los elementos para saber si ponemos primero vertical u horizontal

        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        cajaAlumno = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        caja.pack_start(cajaAlumno, True, True, 0)
        lblAlumno = Gtk.Label(label="Alumno")
        cajaAlumno.pack_start(lblAlumno, False, False, 2)
        self.txtNombre = Gtk.Entry()
        cajaAlumno.pack_start(self.txtNombre, True, False, 2)
        self.txtApellidos = Gtk.Entry()
        cajaAlumno.pack_start(self.txtApellidos, True, False, 2)

        listBox = Gtk.ListBox()
        caja.pack_start(listBox, True, True, 0)

        fila = Gtk.ListBoxRow()

        cajaVFila = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        fila.add(cajaVFila)

        cajaHFila1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        lblModulo = Gtk.Label(label="COD")
        cajaHFila1.pack_start(lblModulo, False, False, 2)
        self.chkBilingueCod = Gtk.CheckButton()
        self.chkBilingueCod.set_label("Bilingüe")
        cajaHFila1.pack_start(self.chkBilingueCod, False, False, 2)

        cajaHFila2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        lblNota = Gtk.Label(label="Nota")
        cajaHFila2.pack_start(lblNota, False, False, 2)
        self.txtNotaCod = Gtk.Entry()
        cajaHFila2.pack_start(self.txtNotaCod, False, False, 2)
        cajaVFila.pack_start(cajaHFila1, True, True, 0)
        cajaVFila.pack_start(cajaHFila2, True, True, 0)

        listBox.add(fila)

        fila = Gtk.ListBoxRow()

        cajaVFila = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        fila.add(cajaVFila)

        cajaHFila1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        lblModulo = Gtk.Label(label="PROG")
        cajaHFila1.pack_start(lblModulo, False, False, 2)
        self.chkBilingueProg = Gtk.CheckButton()
        self.chkBilingueProg.set_label("Bilingüe")
        cajaHFila1.pack_start(self.chkBilingueProg, False, False, 2)

        cajaHFila2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        lblNota = Gtk.Label(label="Nota")
        cajaHFila2.pack_start(lblNota, False, False, 2)
        self.txtNotaProg = Gtk.Entry()
        cajaHFila2.pack_start(self.txtNotaProg, False, False, 2)
        cajaVFila.pack_start(cajaHFila1, True, True, 0)
        cajaVFila.pack_start(cajaHFila2, True, True, 0)

        listBox.add(fila)

        btnGuardar = Gtk.Button(label="Guardar")
        caja.pack_start(btnGuardar, False, False, 4)
        btnGuardar.connect("clicked", self.on_btnGuardar_clicked)

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_btnBoton_clicked(self, boton,
                            etiqueta):  # boton: cualquier nombre para recoger una referencia o control que generó la señal
        # etiqueta: es la referencia de lblEtiqueta
        etiqueta.set_text("Ola alumnos de Gtk")

    def on_txtSaludo_activate(self, cuadroTexto, etiqueta):
        etiqueta.set_text(cuadroTexto.get_text())

    def on_btnGuardar_clicked(self, boton):
        lista = list()  # lista = [] --->también puede ponerse así
        lista.append(self.txtNombre.get_text())
        lista.append(self.txtApellidos.get_text())
        modulo = list()
        modulo.append("COD")
        modulo.append(float(self.txtNotaCod.get_text()))
        modulo.append(self.chkBilingueCod.get_active())
        lista.append(modulo)
        modulo = list()
        modulo.append("PROG")
        modulo.append(float(self.txtNotaProg.get_text()))
        modulo.append(self.chkBilingueProg.get_active())
        lista.append(modulo)
        print(lista)
        return lista


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
