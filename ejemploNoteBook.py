import gi



gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from boxConBotones import BoxConBotones

class ventanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo de NoteBook Gtk")

        notebook= Gtk.Notebook()

        pagina1= Gtk.Box()
        pagina1.set_border_width(10)
        pagina1.add(Gtk.Label(label="Página por defecto"))
        notebook.append_page(pagina1,Gtk.Label(label="Título de la página"))

        pagina2=Gtk.Box()
        pagina2.set_border_width(5)
        pagina2.add(Gtk.Label(label="Página con una imagen"))
        notebook.append_page(pagina2,Gtk.Image.new_from_icon_name("help-about",Gtk.IconSize.MENU))

        notebook.append_page(BoxConBotones(), Gtk.Label(label="Box con botones"))

        self.add(notebook)
        self.connect("delete-event",Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    ventanaPrincipal()
    Gtk.main()
