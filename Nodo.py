from Enlace import Enlace
class Nodo():
    def __init__(self, nombre):
        self.nombre = nombre
        self.enlacesExistentes = -1
        self.enlaces = []
        
    def getEnlaces(self):
        return self.enlaces
    
    def getEnlacesExistentes(self):
        return self.enlacesExistentes
    
    def getNombre(self):
        return self.nombre
    
    def agregarEnlace(self, enlazar, peso):
        if self.enlacesExistentes == -1:
            self.enlaces.append(Enlace(enlazar, peso))
            self.enlacesExistentes = self.enlacesExistentes + 1
        else:
            posicion = self.existeEnlace(enlazar)
            if posicion == -1:
                self.enlaces.append(Enlace(enlazar, peso))
                self.enlacesExistentes = self.enlacesExistentes + 1
    
    def existeEnlace(self, enlazar):
        i = 0
        for enlaces in self.enlaces:
            if enlaces.getDestino() == enlazar:
                return i
            i = i + 1
        return -1
    
    def enlacePosicion(self, posicion):
        miEnlace = self.enlaces[posicion]
        return miEnlace.getPeso()
    
    def nodoPosicion(self, posicion):
        miEnlace = self.enlaces[posicion]
        return miEnlace.getDestino()
    
    def eliminarEnlace(self, posicion):
        if posicion >= 0 and posicion <= len(self.enlaces):
            del self.enlaces[posicion]
            self.enlacesExistentes = self.enlacesExistentes - 1
            return True
    
