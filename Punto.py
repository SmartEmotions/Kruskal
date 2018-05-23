from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class Punto():
    '''
    Clase que implementa la instancia de un punto
    este permite el abstraccion de un punto con su posicion
    el widget y el nombre de ese punto
    '''
    def __init__(self, x, y, nombre):
        '''
        Metodo constructor del objeto Punto
        :x: La posicion x en pixeles del widget valor en tipo entero(int)
        :y: La posicion y en pixeles del widget valor en tipo entero(int)
        :nombre: Nombre del punto
        '''
        self.ubicacion = QPoint(x, y)
        self.nombre = nombre
        self.colorPunto = QBrush(Qt.blue)
        self.RADIO = 10
    
    def ecuacionDeCirculo(self, punto):
        '''
        Metodo que retorna si una posicion punto dado 
        hay ya un punto establecido, 
        :return:si el punto recibido por 
        parametro se encuentra en la ubicacion de este punto se 
        retorna True, por el contrario el False
        :rtype: bool
        '''
        return((((punto.x() - self.ubicacion.x()) *
               (punto.x() - self.ubicacion.x())) +
               ((punto.y() - self.ubicacion.y()) *
               (punto.y() - self.ubicacion.y()))) <=
               (self.RADIO * self.RADIO))
        
    def espacioOcupado(self, punto):
        '''
        Metodo parecido al metodo anterior, la diferencia es que la posicion
        del punto dado con respecto al punto esta expandida en un radio de 50
        Esta funcion se utiliza para cuando se requiere pintar un nuevo punto 
        si el punto dado se encuentra cerca este punto no 
        se podra crear otro punto
        :punto: es el punto de referencia a comparar
        :return: True si se encuentra en el radio de 50, False en caso contrario
        :rtype: bool
        '''
        return((((punto.x() - self.ubicacion.x()) *
               (punto.x() - self.ubicacion.x())) +
               ((punto.y() - self.ubicacion.y()) *
               (punto.y() - self.ubicacion.y()))) <=
               (50 * 50))
               
    def __str__(self):
        return (str(self.nombre) +
                str(self.ubicacion.x()) +
                str(self.ubicacion.y()))
        
    def getUbicacion(self):
        return self.ubicacion
    
    def getNombre(self):
        return self.nombre
    
    def setUbicacion(self, punto):
        self.ubicacion = punto
        
    def getColorPunto(self):
        return self.colorPunto
    
    def setColorPunto(self, colorPunto):
        self.colorPunto = colorPunto
