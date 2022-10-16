from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Foco:
    '''
    Cada Foco es único y es identificado por un índice.
    '''

    _initialFoco = GL_LIGHT0

    def __init__(self, index, luzdifusa=(0.0, 0.0, 0.0, 0.1), luzambiente=(0.0, 0.0, 0.0, 1.0), luzspecular=(0.0, 0.0, 0.0, 1.0), posicion=(0, 0, 1, 0)):
        '''
        ## Foco
        Constructor de la clase Foco.

        ### Parámetros:
        - index: Número del foco generado en orden de aparición dentro del archivo de configuración .json cargado. Es un valor entero en el rango de 0 (inclusive) a 7 (inclusive).
        - luzdifusa: Lista de 4 valores doubles para representar la luz difusa.
        - luzambiente: Lista de 4 valores doubles para representar la luz ambiente.
        - luzspecular: Lista de 4 valores doubles para representar la luz especular.
        - posicion: Lista de 4 valores doubles para posicionar al foco.

        ### Otros atributos:
        - name: Nombre del foco. Se genera siguiendo el siguiente patrón: GL_LIGHT seguido del índice. P.ej: GL_LIGHT2
        - glTarget: Código numérico usado internamente por OpenGL para representar al foco de luz.
        '''
        if index in range(0, 8):
            if index == 0:
                luzdifusa = (1.0, 1.0, 1.0, 1.0)
                luzspecular = (1.0, 1.0, 1.0, 1.0)
            self.luzdifusa = luzdifusa
            self.luzambiente = luzambiente
            self.luzspecular = luzspecular
            self.posicion = posicion
            self.name = "GL_LIGHT{}".format(index)
            self.glTarget = Foco._initialFoco + index
            print(f"{self.name} creado con valor {self.glTarget}")
        else:
            raise Exception(f"No se puede crear un foco con el indice {index}")

    def __activarFoco__(self):
        '''
        ## Método privado
        No deberías de usar este método.

        ### Funcionamiento
        Activa el foco utilizando la propiedad glTarget mediante el uso de las primitivas de OpenGL "glEnable" y "glLightfv".
        
        Coloca las propiedades definidas por el foco para GL_DIFFUSE, GL_AMBIENT, GL_SPECULAR y GL_POSITION.
        '''
        glEnable(self.glTarget)
        glLightfv(self.glTarget, GL_DIFFUSE, self.luzdifusa)
        glLightfv(self.glTarget, GL_AMBIENT, self.luzambiente)
        glLightfv(self.glTarget, GL_SPECULAR, self.luzspecular)
        glLightfv(self.glTarget, GL_POSITION, self.posicion)
        print(f"Se ha activado el foco {self.name}")
    
    def __desactivarFoco__(self):
        '''
        ## Método privado
        No deberías de usar este método.

        ### Funcionamiento
        Desactiva el foco utilizando la propiedad glTarget mediante el uso de la primitiva de OpenGL "glDisable".
        '''
        glDisable(self.glTarget)
        print(f"Se ha desactivado el foco {self.name}")
    
    def toggleFoco(self):
        '''
        Cambia el estado del foco activandolo o desactivandolo.
        
        ### Funcionamiento
        Utiliza la primitiva de OpenGL "glIsEnabled" para comprobar si el foco se encuentra activado o no, manejando el estado y haciéndolo cambiar de cierto a falso y viceversa. 
        '''
        if glIsEnabled(self.glTarget):
            self.__desactivarFoco__()
        else:
            self.__activarFoco__()
    
    @staticmethod
    def deserialize(data):
        '''
        ## Método estático
        Este método puede usarse sin instanciar un objeto de la clase Foco.

        ### Deserialize
        Obtiene una lista de objetos de tipo Foco a partir de los datos json decodificados que recibe por parámetro.

        ### Parámetros:
        - data: Datos recibidos después de cargar la información del .json.
        
        Usar json.load('file.json') antes de este método.
        '''
        focos = []
        index = 0
        for val in data['focos']:
            focos.append(
                Foco(index, val['luzdifusa'], val['luzambiente'], val['luzspecular'], val['posicion'])
            )
            index+=1
        return focos