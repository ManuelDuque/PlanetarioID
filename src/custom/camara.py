import math
from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Camara:

    def __init__(self, index, eyes, center, up):
        '''
        ## Camara
        Constructor de la clase Camara.

        ### Parámetros:
        - index: Número de la camara generada en orden de aparición dentro del archivo de configuración .json cargado.
        - eyes: Lista de 3 valores enteros que indican la posición de la camara en el espacio. 
        - center: Lista de 3 valores enteros que indican la posición del espacio hacia donde mira la camara.
        - up: Lista de 3 valores enteros para representar la orientacion de la camara frente a la línea de visión.
        '''
        self.eyes = eyes
        self.center = center
        self.up = up
        print(f"Se ha generado la cámara CAMARA_{index}")

    def display(self, omega=60, aspect_ratio=1, near=1, far=1000):
        '''
        Renderiza la cámara con cada tick.

        ### Parámetros (opcionales):
        - omega: Valor entero que representa el ángulo de apertura de la cámara.
        - aspect_ratio: Valor double que representa el aspecto de ratio entre el ancho y el alto del frustum.
        - near: Valor entero que representa la distancia desde la cámara hasta el principio del frustum.
        - far: Valor entero que representa la distancia desde la cámara hasta el final del frustum.

        ### Funcionamiento:
        Utiliza la primitiva de OpenGL "gluPerspective" para establecer la perspectiva, para usar posteriormente "glMatrixMode(GL_MODELVIEW)", "glLoadIdentity()" y, finalmente, "gluLookAt" para establecer los ajustes de la cámara.
        '''
        gluPerspective(omega, aspect_ratio, near, far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eyes[0], self.eyes[1], self.eyes[2], self.center[0], self.center[1], self.center[2], self.up[0], self.up[1], self.up[2])        

    @staticmethod
    def deserialize(data):
        '''
        Devuelve una lista de objetos de tipo Camara.
        Ejemplo de json correcto:
        {
            "camaras": [
                {
                    "posx": 3,
                    "posy": 0,
                    "posz": 0,
                    "povx": 0,
                    "povy": 0,
                    "povz": 0,
                    "orientacionx": 0,
                    "orientaciony": 1,
                    "orientacionz": 0
                },
                {...}
            ]
        }
        '''
        camaras = []
        index = 0
        for val in data['camaras']:
            camaras.append(
                Camara(index, [val['posx'], val['posy'], val['posz']], [val['povx'], val['povy'], val['povz']], [val['orientacionx'], val['orientaciony'], val['orientacionz']])
            )
            index+=1
        return camaras