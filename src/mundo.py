import modelo as model

from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

from custom.customType import CustomType
from custom.foco import Foco
from custom.camara import Camara
from custom.material import Material

class Mundo:

    '''
    Custom Properties: List of CustomType props
    Example:
    {
        'focos': [
            <foco.Foco object at 0x000001DC31679EA0>,
            <foco.Foco object at 0x000001DC3167A410>
        ],
        "materiales": [
            <...>,
            <...>
        ],
        ...
    }
    '''
    props = {'activeCamera': None, 'activeMaterial': None}
    
    # Distintas opciones del menu.
    opcionesMenu = {
      "FONDO_1": 0,
      "FONDO_2": 1,
      "FONDO_3": 2,
      "DIBUJO_1": 3,
      "DIBUJO_2": 4,
      "DIBUJO_3": 5,
      "FORMA_1": 6,
      "FORMA_2": 7,
      "FORMA_3": 8,
      "FORMA_4": 9,
      "CAMARA_1": 10,
      "CAMARA_2": 11,
      "CAMARA_3": 12,
      "CAMARA_4": 13,
      "MATERIAL_1": 14,
      "MATERIAL_2": 15,
      "MATERIAL_3": 16,
      "MATERIAL_4": 17,
      "MATERIAL_5": 18,
      "MATERIAL_6": 19,
      "MATERIAL_7": 20,
      "MATERIAL_8": 21,
      "MATERIAL_9": 22,
    }

    #Número de vistas diferentes.
    numCamaras=3

    #Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    #Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores=[(0.00, 0.00, 0.00), (0.06, 0.25, 0.13), (0.10, 0.07, 0.33), (1.00, 1.00, 1.00), (0.12, 0.50, 0.26), (0.20, 0.14, 0.66)]

    def __init__(self):
        #Inicializamos todo:

        #Variables de la clase
        self.width=800
        self.height=800
        self.aspect = self.width/self.height
        self.angulo = 0
        self.window=0
        self.Sol=model.Modelo()

        #Tamaño de los ejes y del alejamiento de Z.
        self.tamanio=0
        self.z0=0

        #Factor para el tamaño del modelo.
        self.escalaGeneral = 0.005

        #Rotacion de los modelos.
        self.alpha=0
        self.beta=0

        #Variables para la gestion del ratón.
        self.xold=0
        self.yold=0
        self.zoom=1.0

        #Vistas del Sistema Planetario.
        #modelo.tipoVista iForma
        self.iDibujo=3
        self.iFondo=0
        self.iForma=6

        # Cargamos todos los componentes custom
        for customType in CustomType:
            self.cargarComponente(customType)

    def drawAxis(self):
        #Inicializamos
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glClearColor(0.0, 0.0, 0.0, 0.0)
	
        #Eje X Rojo
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.tamanio, 0.0, 0.0)

        #Eje Y Verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, self.tamanio, 0.0)

        #Eje Z Azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, self.tamanio)

        glClearColor(0.0, 0.0, 0.0, 0.0)

        glEnd()
        glEnable(GL_LIGHTING)

    def drawModel(self,forma, escala):
        forma.Draw_Model(self.iForma, escala, self.zoom)

    def display(self):
        glClearDepth(1.0)
        glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Seleccionamos la cámara que está activa y la mostramos.
        activeCamera: Camara = self.obtenerProp(name="activeCamera")
        if activeCamera is not None:
            activeCamera.display()

        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)

        #Establecemos el color del Modelo.
        glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])
            
        #Pintamos el modelo.
        self.drawModel(self.Sol,self.escalaGeneral)

        glFlush()
        glutSwapBuffers()

    #Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if (state == GLUT_UP):
                pass
            if(button==3):
                self.zoom=self.zoom+0.1
                print("Zoom positivo...." + str(self.zoom))
            else:
                self.zoom=self.zoom-0.1
                print("Zoom negativo...." + str(self.zoom))
        else:
            #Actualizamos los valores de x, y.
            self.xold = x
            self.yold = y 

    #Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
    def onMotion(self, x, y):
        self.alpha = (self.alpha + (y - self.yold))
        self.beta = (self.beta + (x - self.xold))
        self.xold = x
        self.yold = y
        glutPostRedisplay()

    # Funcion que gestiona las pulsaciones en el teclado.
    def keyPressed(self, key, x, y):
        key = ord(key)
        if(key == 27):  # Tecla Esc
            # Cerramos la ventana y salimos
            glutDestroyWindow(self.window)
            try:
                exit(self, 0)
            except:
                pass
        elif( key in range(48, 56) ):
            key = key - 48
            focos = self.obtenerProp(CustomType.FOCOS)
            if ( key in range(0, len(focos)) ):
                foco: Foco = focos[key]
                foco.toggleFoco()
        else:
            print('NO')
    
    def setVector4(self, v, v0, v1, v2, v3):
        v[0] = v0
        v[1] = v1
        v[2] = v2
        v[3] = v3
    
    # Funcion para activar las distintas opciones que permite el menu.
    def onMenu(self, opcion):
        if ( opcion in range( self.opcionesMenu["FONDO_1"] , self.opcionesMenu["FONDO_3"] + 1 ) ):
            self.setIFondo( opcion )
        elif ( opcion in range( self.opcionesMenu["DIBUJO_1"], self.opcionesMenu["DIBUJO_3"] + 1 ) ):
            self.setIDibujo( opcion )
        elif ( opcion in range( self.opcionesMenu["FORMA_1"], self.opcionesMenu["FORMA_4"] + 1 ) ):
            self.setIForma( opcion )
        elif ( opcion in range( self.opcionesMenu["CAMARA_1"], self.opcionesMenu["CAMARA_4"] + 1 ) ):
            self.setICamera( opcion )
        elif ( opcion in range( self.opcionesMenu["MATERIAL_1"], self.opcionesMenu["MATERIAL_9"] + 1 ) ):
            self.setIMaterial( opcion )
        glutPostRedisplay()
        return opcion
    
    def setIMaterial(self, opcion):
        '''
        Establece el material seleccionado.
        '''
        materialTarget = opcion - self.opcionesMenu["MATERIAL_1"]
        materiales = self.obtenerProp(CustomType.MATERIALES)
        if materialTarget in range(0, len(materiales)):
            print(f"Material {materialTarget} ha cambiado desde el menú...")
            material: Material = materiales[materialTarget]
            self.props['activeMaterial'] = material
            material.activarMaterial()
    
    def setICamera(self, opcion):
        '''
        Establece la cámara seleccionada.
        '''
        cameraTarget = opcion - self.opcionesMenu["CAMARA_1"]
        # Select from custom props the list of registered cameras
        cameras = self.obtenerProp(CustomType.CAMARAS)
        if cameraTarget in range(0, len(cameras)):
            print(f"Cámara {cameraTarget} ha cambiado desde el menú...")
            # Change the active camera custom prop to the selected camera
            self.props['activeCamera'] = cameras[cameraTarget]

    def cargarModelo(self, nombre):
        _, vertices, caras = self.Sol.load(nombre)
        self.Sol.setNVertices(len(vertices))
        self.Sol.setNCaras(len(caras))
        self.Sol.setCaras(caras)
        self.Sol.setVertices(vertices)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setIFondo(self, iFondo):
        self.iFondo = iFondo

    def getIFondo(self):
        return self.iFondo

    def setIDibujo(self, iDibujo):
        self.iDibujo = iDibujo

    def getIDibujo(self):
        return self.iDibujo
    
    def setIForma(self, iForma):
        self.iForma = iForma

    def getIForma(self):
        return self.iForma

    def obtenerProp(self, type: CustomType=None, name: str=None):
        '''
        Obtiene la respuesta deserializada almacenada en las props.

        ### Parámetros:
        - type: Valor enumerado de la clase CustomType que representa la propiedad que se quiere obtener. 
        '''
        if type is None and name is None:
            raise Exception(f"Call to obtenerProp method has failed. Remember give a type or a prop name to get the prop!")
        typeText = type.getPropName() if type is not None else None
        toSearch = typeText if type is not None else name
        return self.props.get(toSearch, None)

    def cargarComponente(self, type: CustomType):
        '''
        Carga el componente custom deserealizandolo en una lista de objetos.
        type: Valor CustomType que indica el nombre del componente a cargar. Debe coincidir con el nombre del fichero .json.
        '''
        import json
        with open( type.getPath() ) as file:
            data = json.load(file)
            typeClass = type.getClass()
            # Check if the custom type class has the method deserialize like attribute
            customTypeHasMethod = hasattr(typeClass, "deserialize")
            if customTypeHasMethod and callable(typeClass.deserialize):
                # If the custom type has the attribute and it is callable (it is a function)
                response = typeClass.deserialize(data)
                self.props.update({type.getPropName(): response})
            else:
                print(f"Error, custom type {typeClass} does not have method deserialize")
