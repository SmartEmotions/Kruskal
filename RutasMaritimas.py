import sys
import copy
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Punto import Punto
from Grafo import Grafo
from Arista import Arista
from AlgoritmoKruskal import AlgoritmoKruskal
from Puertos import*

form_class = uic.loadUiType("RutasGUI.ui")[0]


class Ventana(QMainWindow, form_class):
    '''
    Clase que implementa las ventana principal del programa Rutas Maritimas V 1.0
    esta clase contiene todos los objetos que se heredan de una ventana creada en
    QtDesigner, dentro del proyecto del programa se encuentra el archivo de ventana
    ademas se adicionan otros objetos para las funciones necesarias del programa
    '''
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.numerodenodos = 0
        self.setupUi(self)
        self.lienzoGraphic = LienzoDibujo(self)
        self.lienzoLayout.addWidget(self.lienzoGraphic)
        self.center = QPoint()
        self.mousePunto = QPoint()
        self.textPeso.setValidator(QtGui.QDoubleValidator())


        self.aboutDialog = AboutDialogWindow()
        self.aboutDialog.setHidden = False


        self.about = QAction('Acerca De',self)
        self.saveasTXT = QAction('Guardar Grafo(txt)', self)
        self.saveasBin = QAction('Guardar Grafo(bin)',self)
        self.openTXT = QAction('Abrir Grafo(txt)', self)
        self.openBin = QAction('Abrir Grafo(bin)',self)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Archivo')
        fileMenu.addAction(self.openTXT)
        fileMenu.addAction(self.openBin)
        fileMenu.addAction(self.saveasTXT)
        fileMenu.addAction(self.saveasBin)
        helpMenu = menubar.addMenu('&Ayuda')
        helpMenu.addAction(self.about)


        self.saveasTXT.triggered.connect(self.savetxtDialog)
        self.saveasBin.triggered.connect(self.savebinDialog)
        self.openTXT.triggered.connect(self.opentxtDialog)
        self.openBin.triggered.connect(self.openbinDialog)
        self.about.triggered.connect(self.dialogAbout)

        self.nombrePuerto.addItems(listaPuertos([]))
        self.nombrePuerto.activated['QString'].connect(self.puertoActivado)
        self.costoAnclaje.activated['QString'].connect(self.costoActivado)

        self.costoAnclaje.addItems(['-Vacio-', '1000', '1500', '1200', '1600'])
        self.agregarPuerto.clicked.connect(self.lienzoGraphic.addPunto)
        self.aceptarPeso.clicked.connect(self.lienzoGraphic.addPeso)
        self.aplicarKruskal.clicked.connect(self.lienzoGraphic.appKruskal)
        self.crearPunto.clicked.connect(self.desactivarlinea)
        self.crearArista.clicked.connect(self.someMessage)
        self.nuevoGrafo.clicked.connect(self.limpiarLienzo)
        self.puntoDuo = [None, None]
        self.puntos = []
        self.aristas = []
        self.grafo = Grafo()
        self.contador = 0
        self.cantidad = 0
        self.x = ''
        self.y = ''

    def someMessage(self):
        self.labelMessage.setText('Seleccione un punto con click izquierdo')

    def dialogAbout(self):
        '''
        Metodo que muestra el dialogo de en la ventana, este metodo inicia
        una ventana de dialogo con la informacion de los creadores del proyecto
        '''
        showFrame = AboutDialogWindow().exec_()

    def getGrafo(self):
        return self.grafo

    def desactivarlinea(self):
        '''
        Este metodo desactiva las acciones de pintar recta
        cuando el usuario repentinamente selecciona otras opciones
        '''
        if self.puntoDuo[0] is not None:
            self.puntoDuo[0].setColorPunto(QBrush(Qt.blue))
            self.puntoDuo[0] = None
        if self.puntoDuo[1] is not None:
            self.puntoDuo[1].setColorPunto(QBrush(Qt.blue))
            self.puntoDuo[1] = None
        self.lienzoGraphic.puntoenable = False
        self.lienzoGraphic.repaint()
        self.widgetPeso.setEnabled(False)
        self.labelMessage.setText('Presione click derecho en el lienzo ')

    def unabled(self, doThis):
        '''
        Este metodo habilita y deshabilita los widgets de opciones
        de usuario, dependiendo de las acciones que se requiere
        se habilitaran los widgets
        '''
        self.widgetPeso.setEnabled(doThis)
        self.widgetPunto.setEnabled(doThis)
        self.widgetMenu.setEnabled(doThis)
        self.lienzoLayout.setEnabled(doThis)
        self.aplicarKruskal.setEnabled(doThis)
        self.labelMessage.setText('')

    def puertoActivado(self, text):
        '''
        Metodo para el QComboBox de Nombre del puerto
        si el usuario selecciona un puerto de la lista
        se agregara un item o nombre del pais al que pertenece
        el puerto selecionado
        '''

        self.paisPuerto.clear()
        self.costoAnclaje.clear()
        if text != '-Vacio-':
            self.labelMessage.setText('Seleccione un costo de anclaje')
            self.paisPuerto.addItems([paispuerto(self.nombrePuerto.currentText())])
            self.costoAnclaje.addItems(['-Vacio-', '1000', '1500', '1200', '1600'])
            self.costoAnclaje.setEnabled(True)
            if self.agregarPuerto.isEnabled():
                self.agregarPuerto.setEnabled(False)

    def costoActivado(self, text):
        '''
        Metodo de seleccion de costo de anclaje en la opcion de adcionar
        punto, si el usuario selecciona un costo, el boton de adicionar punto
        se activa
        '''
        if text != '-Vacio-':
            self.labelMessage.setText('Presione Agregar Punto')
            self.agregarPuerto.setEnabled(True)
            self.paisPuerto.setEnabled(True)

    def savetxtDialog(self):
        '''
        Metodo que guarda todo la informacion del grafo Rutas Maritimas
        se escribe un archivo de texto con la cantidad de puntos que
        haya en el grafo, luego se escriben las cordenadas de los punto,
        el nombre de los puntos, y finalizado de guardar los
        puntos se ecriben las aristas, con las cordenadas de sus extremos
        y el peso de la arista como tal, el usuario debera digitar el
        nombre del archivo a guardarse, y la extension .txt o .bin
        '''
        nameTree = QFileDialog.getSaveFileName(self,
                                                     "Guardar fichero",
                                                     "/home/carlos/Escritorio",
                                                     "(*.txt)")
        if nameTree:
            writeTree = open(nameTree, 'w') # Indicamos el valor 'w'.
            writeTree.write(str(len(self.puntos)) + '\n')
            for punto in self.puntos:
                writeTree.write(str(punto.ubicacion.x()) + "|" +
                                str(punto.ubicacion.y()) + "|" +
                                str(punto.nombre) + '\n')
            for arista in self.aristas:
                writeTree.write(str(arista.puntoA.ubicacion.x()) + '|' +
                                str(arista.puntoA.ubicacion.y()) + '|' +
                                str(arista.puntoB.ubicacion.x()) + '|' +
                                str(arista.puntoB.ubicacion.y()) + '|' +
                                str(arista.peso) + '|' +
                                str(arista.puntoA.nombre) + '|' +
                                str(arista.puntoB.nombre) + '\n')
            writeTree.close()
            self.labelMessage.setText('El grafo se guardo satisfactoriamente')

    def savebinDialog(self):
        '''
        Metodo que guarda todo la informacion del grafo Rutas Maritimas
        se escribe un archivo de texto con la cantidad de puntos que
        haya en el grafo, luego se escriben las cordenadas de los punto,
        el nombre de los puntos, y finalizado de guardar los
        puntos se ecriben las aristas, con las cordenadas de sus extremos
        y el peso de la arista como tal, el usuario debera digitar el
        nombre del archivo a guardarse, y la extension .txt o .bin
        '''
        nameTree = QFileDialog.getSaveFileName(self,
                                                     "Guardar fichero",
                                                     "/home/carlos/Escritorio",
                                                     "(*.bin)")
        if nameTree:
            writeTree = open(nameTree, 'wb') # Indicamos el valor 'w'.
            writeTree.write(str(len(self.puntos)) + '\n')
            for punto in self.puntos:
                writeTree.write(str(punto.ubicacion.x()) + "|" +
                                str(punto.ubicacion.y()) + "|" +
                                str(punto.nombre) + '\n')
            for arista in self.aristas:
                writeTree.write(str(arista.puntoA.ubicacion.x()) + '|' +
                                str(arista.puntoA.ubicacion.y()) + '|' +
                                str(arista.puntoB.ubicacion.x()) + '|' +
                                str(arista.puntoB.ubicacion.y()) + '|' +
                                str(arista.peso) + '|' +
                                str(arista.puntoA.nombre) + '|' +
                                str(arista.puntoB.nombre) + '\n')
            writeTree.close()
            self.labelMessage.setText('El grafo se guardo satisfactoriamente')


    def opentxtDialog(self):
        '''
        Funcion que permite abrir un archivo de texto
        con formato del programa Rutas Maritimas, el metodo
        permite cargar un archivo de tipos *txt o *bin  cuando
        se carga un archivo, el grafo que se haya trabajado
        hasta el momento se eliminara, y solamente aparecera el nuevo grafo
        con el que se podra seguir trabajando normalmente
         '''
        filename = QFileDialog.getOpenFileName(self,
                                                     'Abrir archivo',
                                                     '/home',
                                                     "(*.txt)")
        if filename:
            self.limpiarLienzo()
            regTree = open(filename, "r")
            self.numerodenodos = regTree.readline()
            self.numerodenodos = int(self.numerodenodos.replace('\n', ''))
            i = 1
            for line in regTree:
                line = line.replace("\n", "")
                if line != '':
                    line = line.split("|")
                    if i <= self.numerodenodos + 1:
                        if len(line) == 3:
                            x = int(line[0])
                            y = int(line[1])
                            nombre = line[2]
                            punto = Punto(x + 5, y + 5, nombre)
                            self.grafo.ingresarNodo(nombre)
                            self.puntos.append(punto)

                    if self.numerodenodos < i:
                        x1 = int(line[0])
                        y1 = int(line[1])
                        x2 = int(line[2])
                        y2 = int(line[3])
                        peso = float(line[4])
                        nombre1 = line[5]
                        nombre2 = line[6]
                        punto1 = Punto(x1 + 5, y1 + 5, nombre1)
                        punto2 = Punto(x2 + 5, y2 + 5, nombre2)
                        arista = Arista(punto1, punto2, peso)
                        self.aristas.append(arista)
                        self.grafo.adicionarEnlace(nombre1, nombre2, peso)
                i = i + 1
            regTree.close()
            self.labelMessage.setText('Grafo abierto correctamente')
            self.nombrePuerto.clear()
            nuevalista = listaPuertos([])
            for n in self.puntos:
                if n.nombre in nuevalista:
                    del nuevalista[nuevalista.index(n.nombre)]
            self.nombrePuerto.addItems(nuevalista)

        self.lienzoGraphic.repaint()
        self.aplicarKruskal.setEnabled(True)
        if len(self.puntos) > 1:
            self.crearArista.setEnabled(True)
        self.nuevoGrafo.setEnabled(True)

    def openbinDialog(self):
        '''
        Funcion que permite abrir un archivo de texto
        con formato del programa Rutas Maritimas, el metodo
        permite cargar un archivo de tipos *txt o *bin  cuando
        se carga un archivo, el grafo que se haya trabajado
        hasta el momento se eliminara, y solamente aparecera el nuevo grafo
        con el que se podra seguir trabajando normalmente
         '''
        filename = QFileDialog.getOpenFileName(self,
                                                     'Abrir archivo',
                                                     '/home',
                                                     "(*.bin)")
        if filename:
            self.limpiarLienzo()
            regTree = open(filename, "rb")
            self.numerodenodos = regTree.readline()
            self.numerodenodos = int(self.numerodenodos.replace('\n', ''))
            i = 1
            for line in regTree:
                line = line.replace("\n", "")
                if line != '':
                    line = line.split("|")
                    if i <= self.numerodenodos + 1:
                        if len(line) == 3:
                            x = int(line[0])
                            y = int(line[1])
                            nombre = line[2]
                            punto = Punto(x, y, nombre)
                            self.grafo.ingresarNodo(nombre)
                            self.puntos.append(punto)
                    if self.numerodenodos < i:
                        x1 = int(line[0])
                        y1 = int(line[1])
                        x2 = int(line[2])
                        y2 = int(line[3])
                        peso = float(line[4])
                        nombre1 = line[5]
                        nombre2 = line[6]
                        punto1 = Punto(x1, y1, nombre1)
                        punto2 = Punto(x2, y2, nombre2)
                        arista = Arista(punto1, punto2, peso)
                        self.aristas.append(arista)
                        self.grafo.adicionarEnlace(nombre1, nombre2, peso)
                i = i + 1
            regTree.close()
            self.labelMessage.setText('Grafo abierto correctamente')
            self.nombrePuerto.clear()
            nuevalista = listaPuertos([])
            for n in self.puntos:
                if n.nombre in nuevalista:
                    del nuevalista[nuevalista.index(n.nombre)]
            self.nombrePuerto.addItems(nuevalista)

        self.lienzoGraphic.repaint()
        self.aplicarKruskal.setEnabled(True)
        if len(self.puntos) > 1:
            self.crearArista.setEnabled(True)
        self.nuevoGrafo.setEnabled(True)

    def limpiarLienzo(self):
        '''
        Metodo implementado para limpiar el
        grafo que se encuetre en el lienzo
        esto permitira crer nuevos grafos desde el principio
        '''
        self.puntos = []
        self.aristas = []
        self.grafo.nombres = []
        self.grafo.nodos = []
        self.grafo.aristas = []
        self.lienzoGraphic.neo = []
        self.lienzoGraphic.repaint()


class LienzoDibujo(QWidget):
    '''
    Clase que implementa el lienzo en donde se grafica los puntos y aristas
    del grafo, es un objeto de tipo Widget, el cual contiene metodos para
    los eventos de acciones de usuario con el mouse, este objeto tiene referencia
    del la ventana principal, lo que permite la interaccion con la interfaz externa
    '''
    def __init__(self, ventana):
        '''
        Metodo para iniciar el widget, aqui se instancian, puntos de referencia
        de las acciones del mouse, se inicia un graficador de tipo QPainter y algunas otras
        variables necesarioas
        :ventana: es la referencia de venta principal es de tipo QWindow
        '''
        QWidget.__init__(self)
        self.nodisponible = 0
        self.espacioOcupado = 0
        self.copyGrafo = Grafo()
        self.lienzo = ventana
        self.lienzo.unabled(False)
        self.lienzo.crearArista.setEnabled(False)
        self.lienzo.widgetMenu.setEnabled(True)
        self.painter = QPainter()
        self.hayArista = 0
        self.puntoenable = False
        self.pesoenable = False
        self.estado = False
        self.punto = QPoint()
        self.puntoDuo = [None, None]
        self.puntoA = QPoint()
        self.puntoB = QPoint()
        self.colorPunto = QBrush(Qt.blue)
        self.neo = []
        self.x = 1
        self.y = 1


    def paintEvent(self, event):
        '''
        Metodo que pinta los objetos creados por el usuario, tambien este
        detecta los eventos del raton en caso de pintar arista
        Aqui se dibuja Puntos con sus respectivos nombre, Aristas con
        los respectivos pesos, y en caso de aplicar Kruskal tambien
        dibuja el arbol de axpansion minima
        '''
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setPen(QPen(QBrush(Qt.red), 1, Qt.DashLine))
        if self.puntoenable:
            self.painter.setPen(QPen(Qt.blue))
            self.painter.drawLine(self.puntoA.x(), self.puntoA.y(), self.puntoB.x(), self.puntoB.y())

        if not self.estado:
            for arista in self.lienzo.aristas:
                inicial = arista.puntoA.ubicacion
                terminal = arista.puntoB.ubicacion
                self.painter.setPen(QPen(Qt.blue))
                self.painter.drawLine(inicial.x(), inicial.y(), terminal.x(), terminal.y())
                self.painter.setPen(QPen(Qt.red))
                self.painter.drawText((inicial.x() + terminal.x()) / (2), (inicial.y() + terminal.y())/ (2), str(arista.peso))
        else:
            for arista in self.lienzo.aristas:
                inicial = arista.puntoA.ubicacion
                terminal = arista.puntoB.ubicacion
                self.painter.setPen(QPen(Qt.red))
                self.painter.drawLine(inicial.x(), inicial.y(), terminal.x(), terminal.y())
                self.painter.setPen(QPen(Qt.red))
                self.painter.drawText((inicial.x() + terminal.x()) / (2), (inicial.y() + terminal.y())/ (2), str(arista.peso))

        if self.estado:
            costoTotal = 0
            for i in self.neo:
                for n in self.lienzo.aristas:
                    if n == i:
                        inicial = n.puntoA.ubicacion
                        terminal = n.puntoB.ubicacion
                        self.painter.setPen(QPen(QBrush(Qt.green), 5, Qt.DashLine))
                        self.painter.drawLine(inicial.x(), inicial.y(), terminal.x(), terminal.y())
                        self.painter.setPen(QPen(Qt.green))
                        self.painter.drawLine(inicial.x(), inicial.y(), terminal.x(), terminal.y())
                        self.painter.setPen(QPen(Qt.black))
                        self.painter.drawText((inicial.x() + terminal.x()) / (2), (inicial.y() + terminal.y())/ (2), str(n.peso))
                        costoTotal = costoTotal + n.peso
            self.lienzo.labelMessage.setText('El valor de arbol expansion minima es  ' + str(costoTotal) + 'u')
            self.lienzo.grafo = self.copyGrafo
            self.neo = []
            self.copyGrafo = Grafo()
            self.estado = False

        for puntos in self.lienzo.puntos:
            point = puntos.getUbicacion()
            name = puntos.getNombre()
            self.painter.setPen(QPen(Qt.black))
            self.painter.drawText(point.x() - 30,
                                  point.y() - 11,
                                  name)
            self.painter.setPen(QPen(puntos.colorPunto, 3, Qt.DashLine))
            self.painter.drawEllipse(point, 9, 9)
        self.painter.end()

    def mousePressEvent(self, event):
        '''
        Metodo que captura la acciones de los botones del mouse
        cuando se quiere crear un punto aqui se guarda el punto en
        donde si ha clikeado, pero este punto debe estar fuera de algo de los
        puntos si es que ya existe mas puntos, si se clumplen las condiciones
        se habilita las opciones para cargar el nombre del puerto
        que sera el nombre del punto
        Para crer arista, se camptura las acciones del boton izquierdo del mouse
        y si se ha clikeado en alguno de los puntos, se guarda el punto
        como punto inicial
        '''
        if self.lienzo.crearPunto.isChecked() and event.buttons() == QtCore.Qt.RightButton:
            if len(self.lienzo.puntos) == 0:
                 self.lienzo.unabled(False)
                 self.lienzo.widgetPunto.setEnabled(True)
                 self.lienzo.costoAnclaje.setEnabled(False)
                 self.lienzo.agregarPuerto.setEnabled(False)
                 self.lienzo.paisPuerto.setEnabled(False)
                 self.setEnabled(False)
                 self.punto = event.pos()
                 self.lienzo.labelMessage.setText('Seleccione un puerto')
            if len(self.lienzo.puntos) > 0:
                for n in self.lienzo.puntos:
                    if n.espacioOcupado(event.pos()):
                        self.espacioOcupado = self.espacioOcupado + 1
                if self.espacioOcupado == 0:
                    self.lienzo.unabled(False)
                    self.lienzo.widgetPunto.setEnabled(True)
                    self.lienzo.costoAnclaje.setEnabled(False)
                    self.lienzo.agregarPuerto.setEnabled(False)
                    self.lienzo.paisPuerto.setEnabled(False)
                    self.setEnabled(False)
                    self.punto = event.pos()
                    self.lienzo.labelMessage.setText('Seleccione un puerto')
                else:
                    self.lienzo.labelMessage.setText('Hay un punto cerca de este espacio')
            self.espacioOcupado = 0
        if self.lienzo.crearArista.isChecked() and event.buttons() == QtCore.Qt.LeftButton:

            if self.lienzo.puntoDuo[0] is not None:
                self.lienzo.puntoDuo[0].setColorPunto(QBrush(Qt.blue))
            if self.lienzo.puntoDuo[1] is not None:
                self.lienzo.puntoDuo[1].setColorPunto(QBrush(Qt.blue))
            for n in self.lienzo.puntos:
                if n.ecuacionDeCirculo(event.pos()):
                    n.setColorPunto(QBrush(Qt.red))
                    auxp = n.getUbicacion()
                    self.lienzo.x = auxp.x()
                    self.lienzo.y = auxp.y()
                    self.lienzo.puntoDuo[0] = n
                    self.lienzo.labelMessage.setText('Arrastre el mouse hasta un punto')
                    if self.lienzo.puntoDuo[1] is not None:
                        self.lienzo.puntoDuo[1] = None

    def mouseMoveEvent(self, event):
        '''
        Metodo que captura las acciones de movimiento del mouse
        cuando se esta creando una arista este metodo colecta
        la informacion del mousePressEvent mas los movimientos
        del mouse cuando el click izquierdo o derecho esta sostenido
        si los movimientos escuentran a un punto diferente al que ya se
        guardo se activa la opcion de digitar peso para la
        nueva arista
        '''
        self.lienzo.contador = 0

        if self.lienzo.crearArista.isChecked() and event.buttons() == QtCore.Qt.LeftButton:
            for n in self.lienzo.puntos:
                if n != self.lienzo.puntoDuo[0]:
                    if n.ecuacionDeCirculo(event.pos()):
                        self.lienzo.puntoDuo[1] = n
                        self.lienzo.puntoDuo[1].setColorPunto(QBrush(Qt.red))
                        #Prueba mover
            for n in self.lienzo.puntos:
                if n != self.lienzo.puntoDuo[0] and n.ecuacionDeCirculo(event.pos()):
                    self.lienzo.contador = self.lienzo.contador + 1
            if self.lienzo.puntoDuo[0] is not None and self.lienzo.puntoDuo[1] is not None:
                for m in self.lienzo.aristas:
                    if (str(m.puntoA) == str(self.lienzo.puntoDuo[0]) and
                        str(m.puntoB) == str(self.lienzo.puntoDuo[1]) or
                        str(m.puntoB) == str(self.lienzo.puntoDuo[0]) and
                        str(m.puntoA) == str(self.lienzo.puntoDuo[1])):
                        self.hayArista = self.hayArista + 1

            if self.lienzo.contador > 0 and self.lienzo.puntoDuo[0] is not None:
                if self.hayArista == 0:
                    self.lienzo.widgetPeso.setEnabled(True)
                    self.lienzo.textPeso.setModified(True)
                    self.lienzo.labelMessage.setText('Digite peso de la nueva arista')
                else:
                    self.lienzo.labelMessage.setText('Ya hay una arista con este punto')
            else:
                if self.lienzo.puntoDuo[0] is not None:
                    self.lienzo.widgetPeso.setEnabled(False)
                    self.lienzo.labelMessage.setText('Arrastre el mouse hasta un punto')
                if self.lienzo.puntoDuo[1] is not None:
                    self.lienzo.puntoDuo[1].setColorPunto(QBrush(Qt.blue))


            if self.lienzo.puntoDuo[0] != None:
                self.puntoA = QPoint(self.lienzo.x, self.lienzo.y)
                self.puntoB = event.pos()
                self.puntoenable = True

                self.repaint()
            self.lienzo.contador = 0
            self.hayArista = 0
        self.repaint()

    def cambiarGrafo(self, nuevo):
        '''
        Metodd secundario que se utiliza para la funcion de aplicarKruskal
        esta funcion agrega las aristas que tienen el camino mas corto
        y seran las que posteriormente se graficaran, ya que la varible estado para
        a ser True en este metodo
        :nuevo: es el grafo creado con el algoritmo
        ya que este grafo solo contendra las aristas indicadas
        '''
        for n in self.lienzo.aristas:
            aux = n.getArista()
            if nuevo.buscarArista(aux) == True:
                n.setColor(QPen(Qt.green))
                self.neo.append(n)
        self.estado = True
        self.repaint()

    def addPunto(self):
        '''
        Metodo para adicionar puntos en el lienzo
        este metodo se ejecuta con la accion del boton AgregarPunto
        el cual insancia un objeto de tipo Punto
        con la ubicacion y el nombre del punto, y aqui tambien
        se agrega un nodo al grafo
        '''
        punto = Punto(self.punto.x(),
                      self.punto.y(),
                      self.lienzo.nombrePuerto.currentText())
        self.lienzo.grafo.ingresarNodo(self.lienzo.nombrePuerto.currentText())
        self.lienzo.puntos.append(punto)
        self.lienzo.unabled(False)
        self.lienzo.widgetMenu.setEnabled(True)
        self.setEnabled(True)
        if len(self.lienzo.puntos) >= 2:
            self.lienzo.crearArista.setEnabled(True)
            self.lienzo.aplicarKruskal.setEnabled(True)
        else:
            self.lienzo.crearArista.setEnabled(False)
            self.lienzo.aplicarKruskal.setEnabled(False)
        self.lienzo.nombrePuerto.removeItem(self.lienzo.nombrePuerto.currentIndex())
        self.lienzo.costoAnclaje.clear()
        self.lienzo.paisPuerto.clear()
        self.lienzo.nombrePuerto.setCurrentIndex(0)
        self.lienzo.labelMessage.setText('Se adiciono un punto')
        self.repaint()

    def addPeso(self):
        '''
        Metodo que permite ingresar una arista, cuando se tiene referenciados
        dos puntos en el widget se podra digitar el peso, solo si se clickea en el boton
        aceptar la arista sera guardada, por lo cual, aqui se instacia
        un objeto de tipo Arista, y se adiciona un enlace en el grafo
        '''
        if self.lienzo.textPeso.text() != '0' and self.lienzo.textPeso.text() != '':
            peso = float(self.lienzo.textPeso.text())
            if peso > 0:
                arista = Arista(self.lienzo.puntoDuo[0],
                                self.lienzo.puntoDuo[1],
                                peso)
                self.lienzo.aristas.append(arista)
                self.lienzo.grafo.adicionarEnlace(
                                     self.lienzo.puntoDuo[0].getNombre(),
                                     self.lienzo.puntoDuo[1].getNombre(),
                                     float(peso))
                self.lienzo.puntoDuo[1].setColorPunto(QBrush(Qt.blue))
                self.lienzo.textPeso.setText('')
                self.lienzo.widgetPeso.setEnabled(False)
                self.lienzo.contador = 0
                self.lienzo.puntoDuo[0].setColorPunto(QBrush(Qt.blue))
                self.lienzo.puntoDuo[1].setColorPunto(QBrush(Qt.blue))
                self.puntoenable = False
                self.lienzo.puntoDuo[0] = None
                self.lienzo.puntoDuo[1] = None
                self.repaint()
                self.lienzo.labelMessage.setText('Se adiciono una arista')
            else:
               self.lienzo.labelMessage.setText('Digite valores mayores a cero')
        else:
            self.lienzo.labelMessage.setText('No deje el espacio de peso en blanco')

    def appKruskal(self):
        '''
        Accion ejecutada cuando se presiona aplicar kruskal
        aqui se guarda primero el antiguo grafo
        para volverlo a copiar cuando las acciones del
        usuario continuen, luego se instancia una nuevo Grafo
        y se le envia el grafo contenido hasta el momento del
        grafo principal
        '''
        for i in self.lienzo.puntos:
            self.copyGrafo.ingresarNodo(i.getNombre())
        for i in self.lienzo.aristas:
            self.copyGrafo.adicionarEnlace(i.puntoA.getNombre(),
                                           i.puntoB.getNombre(),
                                           i.peso)
        kruskal = AlgoritmoKruskal()
        grafokruskal = Grafo()
        grafokruskal = kruskal.aplicarKruskal(self.lienzo.grafo)
        self.cambiarGrafo(grafokruskal)


class AboutDialogWindow(QDialog):
    def __init__(self, parent=None):
        '''
        Metodo y clase para crear el widget de About, se muestra aqui
        la informacion sobre los desarrolladores
        '''
        QDialog.__init__(self, parent)
        self.setFixedSize(600, 400)
        self.setWindowTitle('About')
        contenedor = QVBoxLayout()
        self.setLayout(contenedor)
        self.setLayout(contenedor)
        self.painter = QPainter()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("AboutImage.jpg")))
        self.setPalette(palette)
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        contenedor.addWidget(QLabel())
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(18)

        labelCarlos = QLabel('Carlos Hernan Guadir Aza')
        labelDario = QLabel('Dario Fernando Criollo')
        labelInfo = QLabel('Telf: 3185622909/3157415315')
        labelUn = QLabel('Ingenieria de Sistemas - UDENAR')
        labelTime = QLabel('2015 - 2016')
        labelCarlos.setAlignment(QtCore.Qt.AlignCenter)
        labelDario.setAlignment(QtCore.Qt.AlignCenter)
        labelInfo.setAlignment(QtCore.Qt.AlignCenter)
        labelUn.setAlignment(QtCore.Qt.AlignCenter)
        labelTime.setAlignment(QtCore.Qt.AlignCenter)

        labelCarlos.setFont(font)
        labelDario.setFont(font)
        labelInfo.setFont(font)
        labelUn.setFont(font)
        labelTime.setFont(font)
        contenedor.addWidget(labelDario)
        contenedor.addWidget(labelCarlos)
        contenedor.addWidget(labelInfo)
        contenedor.addWidget(labelUn)
        contenedor.addWidget(labelTime)


if __name__ == "__main__":
    '''
    Inicio principal de la ventana y las clases para la ejecucion del programa
    '''
    app = QApplication(sys.argv)
    MyWindow = Ventana(None)
    MyWindow.setWindowTitle(('Rutas Maritimas').center(150, " "))
    screen = QDesktopWidget().screenGeometry()
    size = MyWindow.geometry()
    MyWindow.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
    MyWindow.show()
    app.exec_()
