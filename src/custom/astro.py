import math
from custom.material import Material
from modelo import Modelo

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

class Astro(Modelo):
    '''
    Cada Astro es único y está identificado por un id.
    '''

    ASTRO_ID = 0

    def __init__(self, id, radio=0, velRotacion=0.0, velProp=0.0, size=0.0, name="", satelites=[], material:dict=None, parent=None):
        '''
        ## Astro
        Constructor de la clase Astro.

        ### Parámetros:
        - id: Identificador del astro generado en orden de aparición dentro del archivo de configuración .json cargado.
        - radio: Distancia al centro del objecto sobre el que orbita el astro. 
        - velRotacio: Velocidad de movimiento del astro.
        - velProp: Velocidad con la que el astro rota sobre sí mismo.
        - size: Tamaño del astro.
        - name: Nombre del astro.
        - satelites: Lista de nuevos astros que giran sobre el astro. Deben de estar sin serializar.
        - material: Material del astro. Puede ser una referencia o la definición de un nuevo material.
        - parent: Referencia al astro sobre el que gira. Si es el centro del universo, entonces no tiene: None.
        '''
        self.id = id
        self.parent:Astro = parent
        self.radio = radio
        self.velRotacion = velRotacion
        self.velProp = velProp
        self.size = size
        self.name = name
        self.astros = []
        # Recursive deserialization and save a reference to parent in the childrens
        self.astros = Astro.deserialize( data={ "astros": satelites }, parent=self )
        self.__resolveMaterial__(material)
        print(f"Created the astro {self.id} with the material object {self.material}")

    def __resolveMaterial__(self, material:dict=None):
        '''
        ## Método privado
        No deberías de usar este método.

        ### Funcionamiento
        Guarda el material dado en forma de diccionario deserializandolo en un objeto de tipo Material u obteniendolo como referencia a las props del mundo.
        
        El diccionario dado debe de tener una clave "refPosition" o "definition" para resolver el material.
        * Si es refPosition, entonces buscará en las props del mundo y obtendrá el material de la posición indicada en la refPosition.
        * Si es definition, entonces deserializará el objeto Material invocando al método correspondiente.
        '''
        # Check if the material is a id or if it's a definition. If a definition is given, the id shouldn't work.
        raiseExceptionMessage = f"Astro {self.id} hasn't got any material"
        if material is None:
            raise Exception( raiseExceptionMessage )
        val = material.get('definition', None)
        if val is not None:
            # Deserialize the material
            self.material = Material.deserialize( {"materiales": [val]} )[0]
        else:
            # If the material doesn't have a definition, try to get the referenced name 
            refPosition = material.get('refPosition', None)
            if refPosition is None:
                # Raise a exception when a astro hasn't got any type of material
                raise Exception( raiseExceptionMessage )
            else:
                # Get from mundo props the material with the id given (get the material number id)
                from mundo import Mundo
                from custom.customType import CustomType
                self.material:Material = Mundo.obtenerProp(CustomType.MATERIALES)[ refPosition ]

    def loadModelsRecursive(self):
        '''
        Carga recursivamente el modelo para este astro y todos los astros que giran en torno a él.
        Permite la propagación de modelos de padre a hijos.
        '''
        from mundo import Mundo
        Mundo.loadModel(self)
        for astro in self.astros:
            astro.loadModelsRecursive()

    def display(self, time, speed, drawModelCallback, setColorsCallback, zoom=1, orbits=False, orbitColors=[1.0, 1.0, 1.0]):
        '''
        ## display

        Permite renderizar el astro, su orbita, y a todos los astros que giran en torno a él.

        ### Parámetros:
        - time: Tiempo que lleva ejecutándose el programa.
        - speed: Velocidad de la simulación.
        - drawModelCallback: Función que permite dibujar a un modelo escalandolo.
        - setColorsCallback: Función que permite cambiar el color.
        - zoom: Zoom del programa.
        - orbits: Valor booleano que indica si se quiere o no dibujar a las orbitas.
        - orbitColors: Lista de 3 valores doubles que permiten especificar un color para las orbitas.
        '''
        glPushMatrix()
        # Check if the parent is none. If it's none, then it's the center of the world.
        if self.parent is None:
            # Now the astro is the center of universe
            glRotatef(500 * self.velProp * speed * time * math.pi / 360, 0, 1, 0)
            time += 1
        else:
            setColorsCallback()
            glTranslatef(
                (self.radio * zoom / 100) * math.cos( ( self.velRotacion * speed ) * time * math.pi / 360 ),
                0,
                -(self.radio * zoom / 100) * math.sin( ( self.velRotacion * speed) * time * math.pi / 360)
            )
            glRotatef(500 * self.velProp * speed * time * math.pi / 360, 0, 1, 0)
        self.material.activarMaterial()
        drawModelCallback(self, self.size)
        # Recursive call to display each astro that orbits this one.
        for astro in self.astros:
            astro.display(time, speed, drawModelCallback, setColorsCallback, zoom=zoom, orbits=orbits, orbitColors=orbitColors)
        glPopMatrix()
        # Try to draw the orbits
        if orbits and self.parent is not None:
            self.__drawOrbit__(zoom)
        return time

    def __drawOrbit__(self, zoom, color=[1.0, 1.0, 1.0]):
        '''
        ## Método privado
        No deberías de usar este método.

        ### Parámetros
        - zoom: Nivel del zoom actual sobre el mundo.
        - color: Permite especificar los colores a usar a la hora de dibujar la orbita.

        ### Funcionamiento
        Utiliza las primitivas glDisable, glBegin, glColor3f, glVertex3d, glEnd y glEnable.
        
        1. Calcula la distancia máxima del astro al centro del universo para permitir pintar toda la orbita.
        2. Calcula la orbita en función de la velocidad y el zoom.
        3. Pinta a la orbita.
        '''
        glDisable(GL_LIGHTING)
        glBegin(GL_LINE_STRIP)
        glColor3f(color[0], color[1], color[2])
        # Obtenemos la distancia al centro del universo para renderizar hasta esa distancia y optimizar el bucle.
        distanceToCenter = self.getDistanceToCenterOfUniverse()
        # Renderizamos a la orbita de este astro.
        for i in range( 0 - distanceToCenter, distanceToCenter, 1):
            glVertex3d(
                (self.radio * zoom / 100) * math.cos(self.velRotacion * 2 * i * math.pi / 360),
                0,
                (self.radio * zoom / 100) * math.sin(self.velRotacion * 2 * i * math.pi / 360)
            )
        glEnd()
        glEnable(GL_LIGHTING)

    def getDistanceToCenterOfUniverse(self):
        '''
        Devuelve en forma de entero la distancia máxima a la que se encontrará el astro contada desde el centro del universo.
        '''
        if self.parent is None:
            return int(self.radio)
        else:
            return int(self.parent.getDistanceToCenterOfUniverse() + self.radio)

    @staticmethod
    def deserialize(data, parent=None):
        '''
        Devuelve una lista de objetos de tipo Astro.
        Ejemplo de json correcto:
        {
            "planetas": [
                {
                    "radio": 0.0,
                    "wRotAstro": 0.0,
                    "wRotProp": 0.2,
                    "tamanio": 0.7,
                    "nombre": "Sol",
                    "astros": [],
                    "material": {
                        "name": "sol",
                        "definition": {
                        "brillo": 100.0,
                        "luzdifusa": [0.75164, 0.60648, 0.22648, 1.0],
                        "luzambiente": [0.24725, 0.1995, 0.0745, 1.0],
                        "luzspecular": [0.628281, 0.555802, 0.366065, 1.0]
                        }
                    }
                },
                {...}
            ]
        }
        '''
        astros = []
        for val in data['astros']:
            astros.append(
                Astro(
                    Astro.ASTRO_ID,
                    radio=val['radio'], 
                    velRotacion=val['wRotAstro'], 
                    velProp=val['wRotProp'], 
                    size=val['tamanio'], 
                    name=val['nombre'], 
                    satelites=val['astros'],
                    material=val.get('material', None),
                    parent=parent
                )
            )
            Astro.ASTRO_ID+=1
        return astros