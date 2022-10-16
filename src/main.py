import os, sys
import mundo as m
import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

class Main:

    mundo = m.Mundo()

    def display(self):
        self.mundo.display()

    #Funcion que crea las distintas opciones que se pueden activar en los menus.
    def creacionMenu(self):
        menuFondo = glutCreateMenu(self.mundo.onMenu)
        glutAddMenuEntry("Negro", self.mundo.opcionesMenu["FONDO_1"])
        glutAddMenuEntry("Verde oscuro", self.mundo.opcionesMenu["FONDO_2"])
        glutAddMenuEntry("Azul oscuro", self.mundo.opcionesMenu["FONDO_3"])

        menuDibujo = glutCreateMenu(self.mundo.onMenu)
        glutAddMenuEntry("Blanco", self.mundo.opcionesMenu["DIBUJO_1"])
        glutAddMenuEntry("Verde claro", self.mundo.opcionesMenu["DIBUJO_2"])
        glutAddMenuEntry("Azul claro", self.mundo.opcionesMenu["DIBUJO_3"])

        menuForma = glutCreateMenu(self.mundo.onMenu)
        glutAddMenuEntry("Wired", self.mundo.opcionesMenu["FORMA_1"])
        glutAddMenuEntry("Solid", self.mundo.opcionesMenu["FORMA_2"])
        glutAddMenuEntry("Flat", self.mundo.opcionesMenu["FORMA_3"])
        glutAddMenuEntry("Smooth", self.mundo.opcionesMenu["FORMA_4"])

        # Iniciamos los submenús custom
        menuCamara = glutCreateMenu(self.mundo.onMenu)
        index = 1
        for index in range(1, 5):
            glutAddMenuEntry("Camera{}".format(index), self.mundo.opcionesMenu["CAMARA_{}".format(index)])

        menuMaterial = glutCreateMenu(self.mundo.onMenu)
        index = 1
        for index in range(1, 10):
            glutAddMenuEntry("Material{}".format(index), self.mundo.opcionesMenu["MATERIAL_{}".format(index)])

        menuPrincipal = glutCreateMenu(self.mundo.onMenu)
        glutAddSubMenu("Color de fondo", menuFondo)
        glutAddSubMenu("Color del dibujo", menuDibujo)
        glutAddSubMenu("Forma", menuForma)
        glutAddSubMenu("Camaras", menuCamara)
        glutAddSubMenu("Materiales", menuMaterial)
        
        #Carga el menú con el boton derecho.
        glutAttachMenu(GLUT_RIGHT_BUTTON)

    def onMotion(self, x, y):
        self.mundo.onMotion(x, y)

    def onMouse(self, button, state, x, y):
        self.mundo.onMouse(button, state, x, y)

    def keyPressed(self, key, x, y):
        self.mundo.keyPressed(key, x, y)

    def InitGL(self):
        #Activamos los buffers
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)	
        #Eestablece el tamaño de la ventana.
        glutInitWindowSize(self.mundo.getWidth(), self.mundo.getHeight())	
        #Establece la posicion inicial (esquina superior izquierda de la ventana).
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Mundo")
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)

    def main(self, argv):

        
        argc=1
        glutInit(argv)

        #Declaraciones Globales
        self.InitGL()
        
        self.mundo.cargarModelo(argv)

        #Gestion de los botones del raton
        glutMouseFunc(self.onMouse)
        
        #Gestion de los movimientos del raton	
        glutMotionFunc(self.onMotion)	
        
        #Dibujo e Idle
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        
        #Menús
        self.creacionMenu()
        #Pulsaciones del teclado
        glutKeyboardFunc(self.keyPressed)
            
        #Repeat.
        glutMainLoop()

if __name__ == '__main__':
    ma = Main()
    ma.main(sys.argv[1])
