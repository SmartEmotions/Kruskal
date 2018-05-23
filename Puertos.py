'''
Created on 14/06/2015

@author: dario
'''

EEUU = ['Miami', 'Los Angeles', 'New Orleans', 'San Diego']
Canada = ['Halifax', 'Montreal', 'Toronto',
          'Vancouyer']
Mexico  = ['Altamira', 'Veracruz', 'Tampico', 'Acapulco']
Argentina = ['Bahiha', 'Delta Dock', 'Ushuaia']
Brazil = ['Rio Cubatao', 'Rio Grande',
          'Rio de Janeiro']
Chile = ['San Antonio', 'Valparaiso']
Colombia = ['Cartagena', "Santa Martha"]
Ecuador = ['Guayaquil']
Peru = ['Callao', 'Hilo']
Costa_Rica = ['P. Limon']
Panama = ['Cristobal', 'Canal De Panama']
Alemania = ['Dormund', 'Hamburg']
Espana = ['Barcelona', 'Bilbao', 'La coruna', 'Las Palmas', 'Sevilla']
Francia = ['Bresty']
Gran_Bretana = ['Liverpool', 'Londres']
Holanda = ['Amsterdam', 'Roterrdam']
Italia = ['Salerno', 'Venecia']
Grecia = ['Limassol Larnaca']
Rusia = ['San Petesburg']
China = ['Shangal', 'Xiamen International']
India = ['Cochin', 'Mumbai']
Japon = ['Kobe', 'Osaka', 'Yokohama']
Tailandia = ['Bangkok']
Emiratos_Arabes_Unidos = ['Dubai']
Egipto = ['Alexandria']
Marruecos = ['Tanger']
Sudafrica = ['Ciudad del Cabo']
Australia = ['Newcastle',
             'Sydney']

listaNombrePaises = ['EEUU', 'Canada', 'Mexico', 'Argentina', 'Brazil',
                    'Chile', 'Colombia', 'Ecuador', 'Peru', 'Costa Rica',
                    'Panama', 'Alemania', 'Espana', 'Franci', 'Gran Bretana',
                    'Holanda', 'Italia', 'Grecia', 'Rusica', 'China', 'India',
                    'Japon', 'Tailandia', 'Emiratos Arabes', 'Egipto', 'Marruecos',
                    'Sudafrica', 'Australia']

listaNombresPuertos = [EEUU, Canada, Mexico, Argentina, Brazil, Chile,
                       Colombia, Ecuador, Peru, Costa_Rica, Panama,
                       Alemania, Espana, Francia, Gran_Bretana, Holanda,
                       Italia, Grecia, Rusia, China, India, Japon,
                       Tailandia, Emiratos_Arabes_Unidos, Egipto,
                       Marruecos, Sudafrica, Australia]
def listaPuertos(lista):
	for n in listaNombresPuertos:
		for i in n:
			lista.append(i)
	lista.insert(0, '-Vacio-')
	return lista

def paispuerto(puerto):
	i = 0
	for n in listaNombresPuertos:
		if puerto in n:
			return listaNombrePaises[i]
		i = i + 1
