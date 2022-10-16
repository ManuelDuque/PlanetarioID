import enum
from custom.foco import Foco
from custom.camara import Camara
from custom.material import Material

class CustomTypeProp(enum.Enum):
    '''
    Propiedades que pueden tomar los objetos custom.

    ### Obligatorios:
    - FILENAME: Nombre del fichero que contiene la información.
    - CLASS: Clase asociada al objeto custom. Se utilizará para instanciar la información a dicha clase.

    ### Opcionales:
    - PROPNAME: Nombre de la variable donde se guardará el resultado obtenido tras la deserialización del objeto.
    - RELATIVE_PATH: Ruta relativa al fichero que se tendrá que utilizar para la carga de la información de dicho objeto. Por ejemplo: './custom/focos/'
    '''
    FILENAME = "filename"
    CLASS = "class"
    PROPNAME = "propname"
    RELATIVE_PATH = "relativePath"

class CustomType(enum.Enum):
    '''
    Ofrece un nivel de abstracción mayor para la carga de objetos custom.
    Un objeto custom puede ser un Foco, una Camara, un Material, etc.
    '''
    FOCOS = {
        CustomTypeProp.FILENAME: 'focos',
        CustomTypeProp.CLASS: Foco,
        CustomTypeProp.PROPNAME: 'focos',
        CustomTypeProp.RELATIVE_PATH: './custom/focos/'
    }
    CAMARAS = {
        CustomTypeProp.FILENAME: 'config',
        CustomTypeProp.CLASS: Camara,
        CustomTypeProp.RELATIVE_PATH: './custom/',
        CustomTypeProp.PROPNAME: 'camaras'
    }
    MATERIALES = {
        CustomTypeProp.FILENAME: 'config',
        CustomTypeProp.CLASS: Material,
        CustomTypeProp.RELATIVE_PATH: './custom/',
        CustomTypeProp.PROPNAME: 'materiales'
    }

    def __init__(self, value:dict):
        obligatoryProps = [CustomTypeProp.FILENAME, CustomTypeProp.CLASS]
        for prop in obligatoryProps:
            if value.get(prop, None) is None:
                raise Exception(f"The {prop} property in CustomType {self.name} dict is obligatory!")

    def getPath(self):
        '''
        Obtiene la ruta relativa al archivo custom.
        '''
        relativePath = self.value.get(CustomTypeProp.RELATIVE_PATH, None)
        relativePath = relativePath if relativePath is not None else "./"
        return relativePath + self.value[ CustomTypeProp.FILENAME ] + ".json"

    def getPropName(self):
        '''
        Obtiene el nombre con el que se guardará en las props. Por defecto coincide con el nombre del fichero.
        '''
        return self.value.get(CustomTypeProp.PROPNAME, self.value.get(CustomTypeProp.FILENAME, None))

    def getClass(self):
        '''
        Obtiene la clase asociada al objeto CustomType.
        '''
        return self.value[CustomTypeProp.CLASS]