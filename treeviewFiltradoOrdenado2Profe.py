import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk
import sqlite3 as dbapi

class ventanaPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Ejemplo de TreeView Filtrado")

        self.set_default_size(250, 100)
        self.set_border_width(10)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('estilo.css')
        contexto = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        contexto.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        cajaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        cajaPrincipal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        cajaPrincipal.pack_start(cajaV, True, True, 0)

        # Parte TREEVIEW
        self.filtradoXenero = "None"
        modelo = Gtk.ListStore(str, str, int, str, bool)
        modelo_filtrado = modelo.filter_new()
        modelo_filtrado.set_visible_func(self.filtro_usuarios_xenero)

        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute("select * from usuarios")
            for fila in cursor:
                modelo.append(fila)
        except dbapi.DatabaseError as e:
            print("Erro insertando usuarios: " + e)
        finally:
             cursor.close()
             bbdd.close()


        #trvDatosUsarios = Gtk.TreeView(model=modelo)
        ventanaScroll = Gtk.ScrolledWindow()
        ventanaScroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        ventanaScroll.set_size_request(300, 150)
        trvDatosUsarios = Gtk.TreeView(model=modelo_filtrado)  # Ver commits para entender cuando he usado un modelo y cuando otro.
        seleccion = trvDatosUsarios.get_selection()
        ventanaScroll.add(trvDatosUsarios)

        for i, tituloColumna in enumerate(["Dni", "Nome"]):#Aqui pongo las columnas que quiero que se muestren. La i es la posicion de la columna en la tupla y el titulo es el nombre de la columna.
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(tituloColumna, celda, text=i)# Para la columna necesito el titulo, la celda y el texto. El texto es la posicion de la columna en la tupla.
            trvDatosUsarios.append_column(columna)

            celda = Gtk.CellRendererProgress()
            columna = Gtk.TreeViewColumn("Edade", celda, value=2)
            trvDatosUsarios.append_column(columna)

        # Combo con un modelo
        modeloCombo = Gtk.ListStore(str)
        modeloCombo.append(("Home",))# Fijarme en que pongo una coma al final. Es una tupla de un elemento.
        modeloCombo.append(("Muller",))
        modeloCombo.append(("Outro",))
        celda = Gtk.CellRendererCombo()# Para la barra de combo del porcentaje
        celda.set_property("editable", True)
        celda.props.model = modeloCombo
        #celda.set_property("model", modeloCombo)# Es lo mismo que la linea de arriba
        celda.set_property("text-column", 0)# La columna que quiero que se muestre es la 0, la primera.
        celda.set_property("has-entry", False)# Para que no se pueda escribir en el combo
        celda.connect("edited", self.on_celdaXenero_edited, modelo_filtrado, 3)

        columna = Gtk.TreeViewColumn("Xenero", celda, text=3)
        trvDatosUsarios.append_column(columna)
        cajaV.pack_start(ventanaScroll, True, True, 2)

        cajaH = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=2)
        cajaV.pack_start(cajaH, True, True, 0)

        rbtHome = Gtk.RadioButton( label ="Home")
        rbtMuller = Gtk.RadioButton.new_with_label_from_widget(rbtHome, label = "Muller")
        rbtOutros = Gtk.RadioButton.new_with_label_from_widget(rbtHome, label ="Outro")
        cajaH.pack_start(rbtHome, True, True, 2)
        cajaH.pack_start(rbtMuller, True, True, 2)
        cajaH.pack_start(rbtOutros, True, True, 2)
        rbtHome.connect("toggled", self.on_xenero_toggled,"Home", modelo_filtrado)
        rbtMuller.connect("toggled", self.on_xenero_toggled, "Muller",  modelo_filtrado)
        rbtOutros.connect("toggled", self.on_xenero_toggled, "Outro", modelo_filtrado)

        # Parte GRID
        grid = Gtk.Grid()
        cajaPrincipal.pack_start(grid, True, True, 0)
        self.lblNome = Gtk.Label(label="Nome")
        self.txtNome = Gtk.Entry()
        self.lblDni = Gtk.Label(label="Dni")
        self.txtDni = Gtk.Entry()
        self.lblEdade = Gtk.Label(label="Edade")
        self.txtEdade = Gtk.Entry()
        self.lblXenero = Gtk.Label(label="Xenero")
        self.cmbXenero = Gtk.ComboBox()
        self.cmbXenero.set_model(modeloCombo)# Le asigno el modelo que cree antes
        celda = Gtk.CellRendererText()  # Para la barra de combo del porcentaje
        #celda.set_property("editable", False)# Digo que no quiero que sea editable
        self.cmbXenero.pack_start(celda, True)
        self.cmbXenero.add_attribute(celda, "text", 0)# La columna que quiero que se muestre es la 0, la primera.
        self.chkFalecido = Gtk.CheckButton(label="Falecido")
        self.btnNovo = Gtk.Button(label="Novo")
        self.btnNovo.connect("clicked", self.on_btnNovo_clicked)
        self.btnEditar = Gtk.Button(label="Editar")
        self.btnEditar.connect("clicked", self.on_btnEditar_clicked, seleccion)
        self.btnAceptar = Gtk.Button(label="Aceptar")
        self.btnAceptar.connect("clicked", self.on_btnAceptar_clicked, modelo, seleccion)
        self.btnCancelar = Gtk.Button(label="Cancelar")
        self.btnCancelar.connect("clicked", self.on_btnCancelar_clicked)
        self.deshabilitarControles()

        grid.add(self.lblNome)# Con add
        grid.attach(self.txtNome,1,0,3,1)# Pongo 3 en width porque quiero que ocupe 3 columnas y sea mas larga la caja de texto.
        grid.attach_next_to(self.lblDni, self.lblNome, Gtk.PositionType.BOTTOM, 1, 1)# Con attach_next_to es el widget, el widget al que se pone al lado, la posicion, el numero de columnas y el numero de filas.
        grid.attach_next_to(self.txtDni, self.lblDni, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.lblEdade, self.txtDni, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtEdade, self.lblEdade, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.lblXenero, self.lblDni, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.cmbXenero, self.lblXenero, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.chkFalecido, self.txtEdade, Gtk.PositionType.BOTTOM, 2, 1)
        cajaH2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=5)
        cajaH2.pack_start(self.btnNovo, True, True, 1)# Diferencia entre False, True que True, True
        cajaH2.pack_start(self.btnEditar, True, True, 1)
        cajaH2.pack_start(self.btnAceptar, True, True, 1)
        cajaH2.pack_start(self.btnCancelar, True, True, 1)
        grid.attach_next_to(cajaH2, self.lblXenero, Gtk.PositionType.BOTTOM, 4, 1)# Pongo la caja horizontal 2, que tiene los botones, debajo de la etiqueta de xenero



        self.add(cajaPrincipal)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    def on_celdaXenero_edited(self, celda, fila, texto, modelo, columna):# Para cambiar el valor de la columna xenero. Es un comboBox.
        try:
            bbdd = dbapi.connect("baseDatos2.dat")
            cursor = bbdd.cursor()
            cursor.execute("UPDATE usuarios set xenero = ? where dni = ?", (texto, modelo[fila][0]))
            bbdd.commit()
        except dbapi.DatabaseError as e:
            print("Erro insertando usuarios: " + e)
        finally:
            cursor.close()
            bbdd.close()
        modelo[fila][columna] = texto
        modelo.refilter()

    def on_xenero_toggled(self, botonSeleccionado, xenero, modelo):
        if botonSeleccionado.get_active():
            self.filtradoXenero = xenero
            modelo.refilter()


    def filtro_usuarios_xenero(self, modelo, fila, datos):
        if self.filtradoXenero is None or self.filtradoXenero == "None":
            return True
        else:
            return modelo[fila][3] == self.filtradoXenero


    def on_btnNovo_clicked(self, control): # Control es el boton que se pulso y que se pasa como parametro automaticamente.
        self.operacion = "Novo"
        self.habilitarControles()
        self.btnEditar.set_sensitive(False)
        self.btnNovo.set_sensitive(False)

    def on_btnCancelar_clicked(self, control):
        self.operacion = None
        self.limpiarControles()
        self.deshabilitarControles()
        self.btnEditar.set_sensitive(True)
        self.btnNovo.set_sensitive(True)

    def on_btnAceptar_clicked(self, control, modelo, seleccion):
        nome= self.txtNome.get_text()
        dni = self.txtDni.get_text()
        edade = self.txtEdade.get_text()
        idXenero = self.cmbXenero.get_active()
        modeloXenero=self.cmbXenero.get_model()
        xenero = modeloXenero[idXenero][0]
        falecido = self.chkFalecido.get_active()
        if self.datosCorrectos(dni,edade):

            datos = (dni, nome, int(edade), xenero, falecido)
            try:
                bbdd = dbapi.connect("baseDatos2.dat")
                cursor = bbdd.cursor()
                if self.operacion == "Novo":
                    modelo.append(datos)
                    cursor.execute("insert into usuarios values(?,?,?,?,?)",datos)
                if self.operacion == "Editar":
                    modelo, fila= seleccion.get_selected()
                    dniAnt= modelo[fila][0]
                    modelo[fila][0] = dni
                    modelo[fila][1] = nome
                    modelo[fila][2] = int(edade)
                    modelo[fila][3] = xenero
                    modelo[fila][4] = falecido
                    datosUp=(dni, nome, int(edade), xenero, falecido, dniAnt)
                    cursor.execute("UPDATE usuarios set dni=?, nome = ?, edade = ?, xenero = ?, falecido = ? where dni = ?",datosUp)
                bbdd.commit()
            except dbapi.DatabaseError as e:
                print("Erro insertando usuarios: " + e)
            finally:
                cursor.close()
                bbdd.close()
                self.limpiarControles()
                self.deshabilitarControles()
                self.btnEditar.set_sensitive(True)
                self.btnNovo.set_sensitive(True)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('estilo.css')
        contexto = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        contexto.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_btnEditar_clicked(self, control, seleccion):
        self.operacion = "Editar"
        self.habilitarControles()
        self.btnNovo.set_sensitive(False)
        self.btnEditar.set_sensitive(False)
        modelo,fila = seleccion.get_selected()
        self.txtDni.set_text(modelo[fila][0])
        self.txtNome.set_text(modelo[fila][1])
        self.txtEdade.set_text(str(modelo[fila][2]))
        xen=modelo[fila][3]
        modeloXenero = self.cmbXenero.get_model()
        for i, elemento in enumerate(modeloXenero):
            if elemento[0] == xen:
                self.cmbXenero.set_active(i)
                break
        self.chkFalecido.set_active(modelo[fila][4])


    def limpiarControles(self):
        self.txtNome.set_text("")
        self.txtDni.set_text("")
        self.txtEdade.set_text("")
        self.cmbXenero.set_active(-1)
        self.chkFalecido.set_active(False)

    def habilitarControles(self):
        self.lblNome.set_sensitive(True)
        self.txtNome.set_sensitive(True)
        self.lblDni.set_sensitive(True)
        self.txtDni.set_sensitive(True)
        self.lblEdade.set_sensitive(True)
        self.txtEdade.set_sensitive(True)
        self.lblXenero.set_sensitive(True)
        self.cmbXenero.set_sensitive(True)
        self.chkFalecido.set_sensitive(True)
        self.btnAceptar.set_sensitive(True)
        self.btnCancelar.set_sensitive(True)
        self.chkFalecido.set_sensitive(True)

    def deshabilitarControles(self):
        self.lblNome.set_sensitive(False)
        self.txtNome.set_sensitive(False)
        self.lblDni.set_sensitive(False)
        self.txtDni.set_sensitive(False)
        self.lblEdade.set_sensitive(False)
        self.txtEdade.set_sensitive(False)
        self.lblXenero.set_sensitive(False)
        self.cmbXenero.set_sensitive(False)
        self.chkFalecido.set_sensitive(False)
        self.btnAceptar.set_sensitive(False)
        self.btnCancelar.set_sensitive(False)
        self.chkFalecido.set_sensitive(False)

    def datosCorrectos(self, dni, edade):
        correctos=True
        if edade.isdigit():
            if int(edade)>0 and int(edade)<200:
                self.txtEdade.set_name("edade")
            else:
                correctos=False
                self.txtEdade.set_name("edadeErro")
        else:
            correctos=False
            self.txtEdade.set_name("edadeErro")
        return correctos

if __name__ =="__main__":
    ventanaPrincipal()
    Gtk.main()