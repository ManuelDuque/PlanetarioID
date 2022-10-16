from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Material:
    '''
    Cada Material es único y es identificado por un índice.
    '''

    def __init__(self, index, brillo=0, luzdifusa=(0.0, 0.0, 0.0, 0.1), luzambiente=(0.0, 0.0, 0.0, 1.0), luzspecular=(0.0, 0.0, 0.0, 1.0)):
        '''
        ## Material
        Constructor de la clase Material.

        ### Parámetros:
        - index: Número del material generado en orden de aparición dentro del archivo de configuración .json cargado.
        - brillo: Valor entero que representa la intensidad de brillo del material. 
        - luzdifusa: Lista de 4 valores doubles para representar la luz difusa.
        - luzambiente: Lista de 4 valores doubles para representar la luz ambiente.
        - luzspecular: Lista de 4 valores doubles para representar la luz especular.
        '''
        self.index = index
        self.brillo = brillo
        self.luzdifusa = luzdifusa
        self.luzambiente = luzambiente
        self.luzspecular = luzspecular
        print("Material {} cargado".format(index))

    def activarMaterial(self):
        '''
        Cambia el estado del material activandolo.
        
        ### Funcionamiento
        Utiliza la primitiva de OpenGL "glMaterialfv" para manejar el estado y estableciendo las propiedades del material. 
        '''
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.luzdifusa)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.luzambiente)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.luzspecular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.brillo)
        print("Se ha activado el material {}".format(self.index))
    
    @staticmethod
    def deserialize(data):
        '''
        ## Método estático
        Este método puede usarse sin instanciar un objeto de la clase Foco.

        ### Deserialize
        Obtiene una lista de objetos de tipo Material a partir de los datos json decodificados que recibe por parámetro.

        ### Parámetros:
        - data: Datos recibidos después de cargar la información del .json.
        
        Usar json.load('file.json') antes de este método.
        '''
        materiales = []
        index = 0
        for val in data['materiales']:
            materiales.append(
                Material(index, val['brillo'], val['luzdifusa'], val['luzambiente'], val['luzspecular'])
            )
            index+=1
        return materiales