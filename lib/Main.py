# -*- coding: utf-8 -*-

from DB import BaseDatos
from gi.repository import Gtk, Gdk
import gi
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.lib.units import inch





























class Main:

    """Clase principal,donde se cargan todas as vistas"""


    def __init__(self):























        # Inicialización de atributos


        self.bd = BaseDatos()  # Obxeto que  contén a taboa sqlite
        self.treeview = Gtk.TreeView()  # Tabla donde se volcan os resultados da base sqlite
        self.buscar = Gtk  # Buscar Alumno
        self.comprobacion=bool


        self.editar = Gtk  # Editar Alumno guay
        self.insertar = Gtk  # Insertar Alumno
        self.id = Gtk  # Primary key
        self.ventana = Gtk
        self.fillo = None
        self.aux = []
        self.camposIntroducidos = []  # Labels dos arquivos .glade
        # Venta principal

        self.ventana = Gtk.Window()
        self.ventana.connect("delete-event", Gtk.main_quit)
        self.ventana.set_resizable(False)
        self.ventana.set_title("Academia Celia")




        # Caixa donde irá contida a imaxen de fondo
        self.layout =  Gtk.VBox()
        self.ventana.add(self.layout)
        self.banner = Gtk.Image()
        self.banner.set_from_file("../img/arriba.jpg")
        self.layout.add(self.banner)

       #Establecemos un panel donde na parte dereita insertaremos o treeview e na parte esquerda os labels que conforman as accións posibles
        self.panel = Gtk.Paned()
        self.layout.add(self.panel)
        self.label = Gtk.Label("")
        self.label.set_alignment(Gtk.Align.END, 0)
        self.layout.add(self.label)

        # Añadimos a imaxe de fondo do outro lado
        self.bot_banner = Gtk.Image()
        self.bot_banner.set_from_file("../img/abaixo.jpg")
        self.layout.add(self.bot_banner)
        self.layout2 = Gtk.Box()
        self.panel.pack1(self.layout2)

        # Engadimos o toolbar e engadimos unha serie de botons e iconos que veñen predefinidos no GTK



        self.toolbar = Gtk.Toolbar()



        self.toolbar.set_orientation(Gtk.Orientation.VERTICAL)


        self.layout2.pack_start(self.toolbar, True, True, 0)
        self.insertar = Gtk.ToolButton(Gtk.STOCK_NEW)
        self.toolbar.add(self.insertar)


        self.modificar = Gtk.ToolButton(Gtk.STOCK_EDIT)
        self.toolbar.insert(self.modificar, 1)

        self.buscar = Gtk.ToolButton(Gtk.STOCK_FIND)
        self.toolbar.insert(self.buscar, 2)


        self.borrar = Gtk.ToolButton(Gtk.STOCK_REMOVE)
        self.toolbar.insert(self.borrar, 3)


        # Creamos dous scrollwindows.


        self.scrollwidgets = Gtk.ScrolledWindow()
        self.scrollwidgets.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.layout2.pack_end(self.scrollwidgets, True, True, 0)


        self.scrolltree = Gtk.ScrolledWindow()
        self.scrolltree.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.panel.add2(self.scrolltree)
        self.scrolltree.add(self.treeview)

        #Executamos o treeview que contén todo no mesmo inicio do programa
        self.cargar_treeview()

     #Asignamos aos botons da toolbar predefinidos os seus correspondentes eventos
        self.insertar.connect("clicked", self.insertarAl)
        self.borrar.connect("clicked", self.eliminarAl)
        self.modificar.connect("clicked", self.editarAl)
        self.buscar.connect("clicked", self.buscarAl)



        self.ventana.show_all()




    # Lista de funcións e condicións .glade ás que lle asignamos os correspondentes eventos




    #Insertar
    def insertarAl(self, widget):


        """Metodo que inserta alumnos na DB"""


        if self.fillo:
            self.fillo.destroy()
            self.fillo = None

        builder = Gtk.Builder()
        builder.add_from_file("../glade/insertarAlumno.glade")
        self.insertar = builder.get_object("vp1")
        self.fillo = self.insertar
        aplicarCambios = builder.get_object("apply")
        self.bot_banner.set_from_file("../glade/axudaimg/engadir.jpg")






        for i in range (7):
            label = builder.get_object(str(i))
            self.camposIntroducidos.append(label)

        self.scrollwidgets.add(self.insertar)
        signal ={"on_apply_clicked": self.on_apply_clicked}
        builder.connect_signals(signal)

   #Eliminar
    def eliminarAl(self, widget):

        """Metodo que elimina alumnos da DB"""
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.id = model[treeiter][0]
            self.bd.borrarAlumno(self.id)
            self.reloadAlumnos()  # Actualizamos o contido do treeview
            self.bot_banner.set_from_file("../glade/axudaimg/borrar.jpg")
    # Modificar Alumno
    def on_apply_clicked(self, widget):

        """Metodo que modifica valores dun alumno xa insertado na DB"""

        self.verificarAlumno(3, 4)
        if self.comprobacion:
            for texto in self.camposIntroducidos:
                self.aux.append(texto.get_text())
            self.bd.insertarAlumno(self.aux)
            self.reloadAlumnos()
            self.insertar.destroy()
            self.camposIntroducidos.clear()
            self.aux.clear()
    def editarAl(self, widget):
        if self.fillo:
            self.fillo.destroy()
            self.fillo = None

        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.id = model[treeiter][0]
            builder = Gtk.Builder()
            builder.add_from_file("../glade/modificarDatosAlumno.glade")
            self.editar = builder.get_object("vp1")
            self.fillo = self.editar
            modificar = builder.get_object("modify")
            self.bot_banner.set_from_file("../glade/axudaimg/editar.jpg")
            for i in range(6):  # Añadimos los 6 labels que tiene (No tiene el label DNI)
                label = builder.get_object(str(i))
                self.camposIntroducidos.append(label)
            print(self.camposIntroducidos)

            self.scrollwidgets.add(self.editar)
            signal = {"on_modify_clicked": self.on_modify_clicked}
            builder.connect_signals(signal)


    def on_modify_clicked(self, widget):
        for texto in self.camposIntroducidos:
            self.aux.append(texto.get_text())

        self.bd.modificarDatosAlumno(self.id, self.aux)
        self.reloadAlumnos()
        self.editar.destroy()
        self.camposIntroducidos.clear()
        self.aux.clear()

    #Buscar Alumno
    def buscarAl(self, widget):
        """Metodo que busca un alumno na DB segundo o seu ID"""


        if self.fillo:
            self.fillo.destroy()
            self.fillo = None

        builder = Gtk.Builder()
        builder.add_from_file("../glade/buscarAlumno.glade")
        self.buscar = builder.get_object("vp1")
        self.fillo = self.buscar
        find = builder.get_object("find")
        back = builder.get_object("back")
        self.bot_banner.set_from_file("../glade/axudaimg/buscar.jpg")
        label = builder.get_object("0")
        self.camposIntroducidos.append(label)
        print(self.camposIntroducidos)

        self.scrollwidgets.add(self.buscar)
        signal = {"on_find_clicked": self.on_find_clicked,
                  "on_back_clicked": self.on_back_clicked}
        builder.connect_signals(signal)

    def on_find_clicked(self, widget):
        self.model.clear()
        for i in self.camposIntroducidos:
            self.id = i.get_text()
            #Busqueda da fila segundo o seu ID que lle especifiquemos
        datos = self.bd.buscarAlumno(self.id)
        for fila in datos:
            self.model.append(fila)

        self.treeview.set_model(self.model)
        self.camposIntroducidos.clear()
    def on_back_clicked(self, widget):
        self.reloadAlumnos()
        self.buscar.destroy()







#Eventos de interfaz

   #Cargar datos da base
    def cargar_treeview(self):

        """Metodo que carga os datos recollidos na DB"""
        datos = self.bd.verAlumnos()
        self.model = Gtk.ListStore(str, str, str, str, int, str, str)
        for fila in datos:
            self.model.append(fila)

        self.treeview.set_model(self.model)

        for i, column_title in enumerate(
                ["ID", "Nome", "Primeiro apelido", "Segundo apelido", "Teléfono", "Horario", "Observacion"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer,
                                        text=i)  # Engadimos cada titulo á sua correspondente columna
            self.treeview.append_column(column)
    #Manten sempre actualizado o treeview ca taboa dos alumnos
    def reloadAlumnos(self):

        """Metodo que actualiza o treeview para ter a tabla da DB sempre actualizada"""
        self.model.clear()
        datos = self.bd.verAlumnos()
        for fila in datos:
            self.model.append(fila)

        self.treeview.set_model(self.model)
    #Verificanse os datos introducidos para cada alumno
    def verificarAlumno(self, pos1,*pos2):
        """Metodo que verifica que os datos que se introducen son os correctos en cada campo, e asi mesmo, que o ID non esta repetido, xa que e a taboa primaria"""
        self.numero_OK = bool
        self.claveid = int
        for contador, obj in enumerate(
                self.camposIntroducidos):
            texto = obj.get_text()
            if contador == pos1:
                self.claveid = self.bd.coincidenciaClave(texto)

                if self.claveid is not 0:

                    self.erro("Introduciches un ID xa existente     ")

            if contador == pos2:
                self.numero_OK = self.verificar_num(texto, pos2)




        if self.numero_OK == True and self.claveid == 0:
            self.comprobacion = True
        else:
            self.comprobacion = False












#Mensaxe de erro por inconcluencia de tipo de valor en algún campo
    def erro(self, mensaxe):
        vent_emergente = Gtk.Window(title="System Critical Error,Warning,Its explosive")

        vent_emergente.set_resizable(True)
        vent_emergente.set_default_size(200, 90)

        img = Gtk.Image()
        img.set_from_file("../img/error.png")

        caja = Gtk.Box()
        label = Gtk.Label()
        label.set_text("    " + mensaxe)

        vent_emergente.add(caja)

        caja.pack_start(img, False, False, 1)
        caja.add(label)

        vent_emergente.connect("delete-event", vent_emergente.hide)
        vent_emergente.show_all()


Main()
Gtk.main()
