import re
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL import *
import math as m

from point_face import Point3D, Face

class Modelo:  
    alpha=None
    beta=None

    ListaPuntos3D=[]
    ListaCaras=[]

    numCaras=None
    NumVertices=None

    def __init__(self, ncaras=None, nvertices=None):
        self.NumCaras = ncaras
        self.NumVertices = nvertices
        self.inicializarParametros()

    def setVector4(self,v, v0, v1, v2, v3):
        v[0]=v0
        v[1]=v1
        v[2]=v2
        v[3]=v3

    def inicializarParametros(self):
        self.alpha=0
        self.beta=0

    def getNCaras(self):
        return self.numCaras

    def setNCaras(self, val):
        self.numCaras = val
    def getNVertices(self):
        return self.numVertices

    def setNVertices(self, val):
        self.numVertices = val

    def setVertices(self, val):
        self.ListaPuntos3D = val
    
    def setCaras(self, val):
        self.ListaCaras = val

    @staticmethod
    def load(path: str):
        """Loads a asc file as a 3D model

        Args:
            path (str): The path where the asc file can be found

        Returns:
            str: Name of the imported model
            list: List of vertices (Point3D)
            list: List of faces (Face)
        """

        num_vertices, num_faces = 0, 0
        vertices, faces = list(), list()
        name = ''

        def regex(types, regex, string):
            return [t(s) for t, s in zip(types, re.search(regex, string).groups())]

        with open(path) as file:
            for line in file:
                line = line.strip()
                if line[:5] == 'Named':
                    name = re.search('"(.*)"', line).groups()[0]
                    line = next(file)
                    _, num_vertices, _, _, num_faces = regex((str, int, str, str, int),
                                                             'Tri-mesh, Vertices:(\s+)(\d+)(\s+)Faces:(\s+)(\d+)', line)

                if line == 'Vertex list:':
                    for n in range(0, num_vertices):
                        line = next(file)

                        _, x = regex((str, float), 'X:(\s*)(-?\d*\.?\d*)', line)
                        _, y = regex((str, float), 'Y:(\s*)(-?\d*\.?\d*)', line)
                        _, z = regex((str, float), 'Z:(\s*)(-?\d*\.?\d*)', line)

                        vertices.append(Point3D(x, y, z))

                if line == 'Face list:':
                    for n in range(0, num_faces):
                        line = next(file)
                        if line.strip() == '' or 'Page' in line or 'Smoothing:' in line:
                            continue

                        _, a = regex((str, int), 'A:(\s*)(\d+)', line)
                        _, b = regex((str, int), 'B:(\s*)(\d+)', line)
                        _, c = regex((str, int), 'C:(\s*)(\d+)', line)

                        ax = vertices[a].x - vertices[b].x  # X[A] - X[B]
                        ay = vertices[a].y - vertices[b].y  # Y[A] - Y[B]
                        az = vertices[a].z - vertices[b].z  # Z[A] - Z[B]
                        bx = vertices[b].x - vertices[c].x  # X[B] - X[C]
                        by = vertices[b].y - vertices[c].y  # Y[B] - Y[C]
                        bz = vertices[b].z - vertices[c].z  # Z[B] - Z[C]

                        normal = Point3D(
                            (ay * bz) - (az * by),
                            (az * bx) - (ax * bz),
                            (ax * by) - (ay * bx))

                        l = ((normal.x ** 2) + (normal.y ** 2) + (normal.z ** 2)) ** (1 / 2)

                        normal.x /= l
                        normal.y /= l
                        normal.z /= l

                        faces.append(Face(a, b, c, normal))

        return name, vertices, faces

    def Draw_Model(self, iForma, scale_from_editor, zoom):
        for face in self.ListaCaras:
            if(iForma == 6):    #Wired
                glDisable(GL_LIGHTING)
                glBegin(GL_LINES)

                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)

            elif(iForma == 7):  #Solid
                glEnable(GL_LIGHTING)
                glBegin(GL_POLYGON)

                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)

            elif(iForma == 8):  #Flat
                glShadeModel(GL_FLAT)
                glEnable(GL_LIGHTING)
                glBegin(GL_POLYGON)

                glNormal3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)


                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)

            elif(iForma == 9):  #Smooth
                glShadeModel(GL_SMOOTH)
                glEnable(GL_LIGHTING)
                glBegin(GL_POLYGON)

                glNormal3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)
                
                glNormal3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.b].x * scale_from_editor * zoom, self.ListaPuntos3D[face.b].y * scale_from_editor * zoom, self.ListaPuntos3D[face.b].z * scale_from_editor * zoom)
                
                glNormal3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)
                glVertex3f(self.ListaPuntos3D[face.c].x * scale_from_editor * zoom, self.ListaPuntos3D[face.c].y * scale_from_editor * zoom, self.ListaPuntos3D[face.c].z * scale_from_editor * zoom)

            glVertex3f(self.ListaPuntos3D[face.a].x * scale_from_editor * zoom, self.ListaPuntos3D[face.a].y * scale_from_editor * zoom, self.ListaPuntos3D[face.a].z * scale_from_editor * zoom)

            glEnd()
