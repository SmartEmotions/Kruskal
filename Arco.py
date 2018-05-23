class Arco():
    '''
    Clase que contiene un Arco el nombre del nodo inicial y el nombre del nodo
    terminal, y tambien contiene el peso de ese enlace, esta clase utiliza para
    la aplicacion de AlgoritmoKruskal
    '''
    def __init__(self, inicial, terminal, peso):
        '''
        Metodo de inicio del objeto Arco
        :inicial:nombre del nodo inicial
        :terminal:nombre del nodo terminal
        :peso:peso del arco entre el nodo inicial y terminal
        '''
        self.inicial = inicial
        self.terminal = terminal
        self.peso = peso
        
    def getPeso(self):
        '''
        Metodo para retornar el peso del Arco
        '''
        return self.peso
    
    def getInicial(self):
        '''
        Metodo que retorna el nombre del nodo inicial del arco
        '''
        return self.inicial
        
    def getTerminal(self):
        '''
        Metodo que retorna el nombre del nodo terminal del arco
        '''
        return self.terminal
        
        
    
    def setTerminal(self, terminal):
        self.terminal = terminal
        
    def setPeso(self, peso):
        self.peso = peso
    
    def setInicial(self, inicial):
        self.inicial = inicial
