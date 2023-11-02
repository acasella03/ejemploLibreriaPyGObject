import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class CajaConObjetoColor(Gtk.Box):
    def __init__(self):
        super().__init__()

        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        cajaV1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        cajaV1.pack_start(self.boton_con_color("red"), True, True, 2)
        cajaV1.pack_start(self.boton_con_color("yellow"), True, True, 2)
        cajaV1.pack_start(self.boton_con_color("purple"), True, True, 2)
        self.pack_start(cajaV1, True, True, 2)

        self.pack_start(self.boton_con_color("green"), True, True, 2)

        cajaV2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        cajaV2.pack_start(self.boton_con_color("blue"), True, True, 2)
        cajaV2.pack_start(self.boton_con_color("orange"), True, True, 2)
        self.pack_start(cajaV2, True, True, 2)
    def on_dibuja(self, control, cr, datos):
        contexto = control.get_style_context()
        ancho = control.get_allocated_width()
        alto = control.get_allocated_height()
        Gtk.render_background(contexto, cr, 0, 0, ancho, alto)

        r, g, b, a = datos["color"]
        cr.set_source_rgba(r, g, b, a)
        cr.rectangle(0, 0, ancho, alto)
        cr.fill()

    def boton_con_color(self, color):
        rgba = Gdk.RGBA()
        rgba.parse(color)

        boton = Gtk.Button()
        area = Gtk.DrawingArea()
        area.set_size_request(32, 24)
        area.connect("draw", self.on_dibuja, {"color": rgba})
        boton.add(area)
        return boton

class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Stack Layout con Gtk")

        cajaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        tarjetas = Gtk.Stack()
        tarjetas.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        tarjetas.set_transition_duration(1000)

        chekPulsame = Gtk.CheckButton(label="Púlsame")
        tarjetas.add_titled(chekPulsame, "pulsame", "Check pulsame")

        lblEtiqueta = Gtk.Label()
        lblEtiqueta.set_markup("<big>Esta és uan etiqueta elegante</big>")
        tarjetas.add_titled(lblEtiqueta, "etiqueta", "Una etiqueta")

        cajaConContenido=CajaConObjetoColor()
        tarjetas.add_titled(cajaConContenido,"caja","Caja con contenido")

        botonesTarjetas = Gtk.StackSwitcher()
        botonesTarjetas.set_stack(tarjetas)
        cajaV.pack_start(botonesTarjetas, True, True, 0)
        cajaV.pack_start(tarjetas, True, True, 0)

        self.add(cajaV)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
