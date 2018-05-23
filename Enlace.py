class Enlace():
    def __init__(self, destino, peso):
		
        self.destino = destino   
        self.peso = peso
    
    def modificar(self, peso):
        self.peso = peso
    
    def getDestino(self):
        return self.destino
    
    def getPeso(self):
        return self.peso
