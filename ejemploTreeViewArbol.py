import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango


class VentanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo Treeview en forma de arbol")
        self.set_default_size(250, 100)
        self.set_border_width(10)
        caja = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)

        modelo=Gtk.TreeStore(str,int)

        for abuelo in range (5):
            punteroAbuelo=modelo.append(None, ['Abuelo %i  '% (abuelo,),abuelo])
            for padre in range(4):
                punteroPadre=modelo.append(punteroAbuelo,['Padre %i del Abuelo %i '% (padre,abuelo),padre])
                for hijo in range(3):
                    punteroHijo=modelo.append(punteroPadre,['Hijo %i del Padre %i del Abuelo %i '% (hijo,padre,abuelo),hijo])
                    for nieto in range(2):
                        modelo.append(punteroHijo,['Nieto %i del Hijo %i del Padre %i del Abuelo %i '% (nieto,hijo,padre,abuelo),nieto])

        treeView = Gtk.TreeView(model=modelo)
        trvColumna=Gtk.TreeViewColumn("Parentesco")
        treeView.append_column(trvColumna)
        celda = Gtk.CellRendererText()
        trvColumna.pack_start(celda,True)
        trvColumna.add_attribute(celda,'text',0)

        trvColumna = Gtk.TreeViewColumn("Orden")
        treeView.append_column(trvColumna)
        celda = Gtk.CellRendererText()
        trvColumna.pack_start(celda, True)
        trvColumna.add_attribute(celda, 'text', 1)

        caja.pack_start(treeView,True,True,0)

        self.add(caja)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
