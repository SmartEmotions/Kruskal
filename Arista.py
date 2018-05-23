from Arco import Arco
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class Arista():
    def __init__(self, puntoA, puntoB, peso):
        self.arista = Arco(puntoA.nombre, puntoB.nombre, peso)
        self.puntoA = puntoA
        self.puntoB = puntoB
        self.peso = peso
        self.color = QBrush(Qt.green)
        self.auxiliar = QBrush(Qt.red)
        
    def __eq__(self, other):
        return (self.puntoA.ubicacion.x() == other.puntoA.ubicacion.x() and
                self.puntoB.ubicacion.y() == other.puntoB.ubicacion.y() and
                self.puntoA.ubicacion.y() == other.puntoA.ubicacion.y() and
                self.puntoB.ubicacion.x() == other.puntoB.ubicacion.x())
                
    def getArista(self):
        return self.arista
    
    def setColor(self, color):
        if color == QBrush(Qt.blue):
            self.auxiliar = QBrush(Qt.red)
        else:
            self.auxiliar = QBrush(Qt.blue)
        self.color = color  
