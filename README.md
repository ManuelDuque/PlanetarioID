# PlanetarioID

Simulador 3D del Sistema Solar construido con **Python** y **OpenGL**. Renderiza un modelo animado con el Sol, los ocho planetas principales y sus lunas, utilizando OpenGL primitives, iluminación configurable e interacción en tiempo real mediante ratón, teclado y menús contextuales.

## Características principales

- Renderizado 3D del Sistema Solar con jerarquía orbital (Sol → Planetas → Lunas)
- Múltiples modos de visualización: alambre (wired), sólido, sombreado plano (flat) y suave (smooth)
- Sistema de iluminación con hasta 8 fuentes de luz configurables (GL_LIGHT0–GL_LIGHT7)
- Materiales personalizados con propiedades de difuso, ambiente, especular y brillo
- 4 presets de cámara con diferentes puntos de vista
- Campo estelar generado proceduralmente
- Visualización de las órbitas de cada cuerpo celeste
- Arquitectura basada en configuración JSON para fácil extensión

## Prerrequisitos

- **Python 3.10** (compatible con `cp310-cp310-win_amd64`)
- **Sistema operativo:** Windows (las dependencias `.whl` están compiladas para `win_amd64`)
- Controladores de gráficos con soporte OpenGL

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/ManuelDuque/publicar.git
cd publicar/PlanetarioID
```

2. Instala las dependencias desde los archivos `.whl` incluidos en `lib/`:

```bash
pip install -r requirements.txt
```

Las dependencias se cargan localmente desde los siguientes paquetes:

| Paquete | Versión |
|---------|---------|
| PyOpenGL | 3.1.6 |
| PyOpenGL-accelerate | 3.1.6 |

## Ejecución

Ejecuta el siguiente comando desde el directorio `src/`:

```bash
cd src
python main.py Esfera.asc
```

Se abrirá una ventana de 800×800 píxeles titulada "Mundo" con el sistema solar en ejecución.

## Controles

### Ratón

| Acción | Comportamiento |
|--------|----------------|
| Clic izquierdo + arrastrar | Rotar la escena |
| Rueda del ratón | Acercar / alejar (zoom) |
| Clic derecho | Abrir menú contextual |

### Teclado

| Tecla | Comportamiento |
|-------|----------------|
| `0` – `7` | Activar / desactivar fuentes de luz (GL_LIGHT0–GL_LIGHT7) |
| `Escape` | Salir de la aplicación |

### Menú contextual (clic derecho)

| Submenú | Opciones disponibles |
|---------|----------------------|
| Color de fondo | Negro, Verde oscuro, Azul oscuro |
| Color del dibujo | Blanco, Verde claro, Azul claro |
| Forma | Wired, Solid, Flat, Smooth |
| Cámaras | Camera1, Camera2, Camera3, Camera4 |

## Estructura del proyecto

```
PlanetarioID/
├── .github/
│   └── workflows/
│       └── autoreleases.yml    # GitHub Actions: auto-release al etiquetar v*
├── lib/
│   ├── PyOpenGL-3.1.6-cp310-cp310-win_amd64.whl
│   └── PyOpenGL_accelerate-3.1.6-cp310-cp310-win_amd64.whl
├── src/
│   ├── main.py                 # Punto de entrada, inicialización de GLUT
│   ├── mundo.py                # Clase Mundo: gestión de escena y bucle de renderizado
│   ├── modelo.py               # Clase Modelo: carga y dibujado de mallas 3D
│   ├── point_face.py           # Estructuras de datos: Point2D, Point3D, Face, Rotation
│   ├── Esfera.asc              # Modelo 3D de una esfera (182 vértices, 360 caras)
│   └── custom/
│       ├── customType.py       # Registro de tipos personalizados (enum extensible)
│       ├── astro.py            # Clase Astro: cuerpo celeste con mecánica orbital
│       ├── camara.py           # Clase Cámara: configuración de vista con gluPerspective
│       ├── foco.py             # Clase Foco: fuentes de luz OpenGL
│       ├── material.py         # Clase Material: propiedades superficiales
│       └── json/
│           ├── planetas.json   # Definición del sistema solar jerárquico
│           ├── camaras.json    # 4 presets de posición/orientación de cámara
│           ├── focos.json      # 8 definiciones de fuentes de luz
│           └── materiales.json # 12 materiales para cuerpos celestes
├── requirements.txt
└── README.md
```

### Archivos principales

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Punto de entrada. Inicializa GLUT, configura la ventana de 800×800, registra callbacks y entra al bucle principal. |
| `mundo.py` | Clase `Mundo`: coordina la carga de modelos, renderiza la escena, gestiona la iluminación y procesa eventos de entrada. |
| `modelo.py` | Clase `Modelo`: carga archivos `.asc` y renderiza mallas 3D con soporte para diferentes modos de dibujado. |
| `astro.py` | Clase `Astro`: representa un cuerpo celeste con radio orbital, velocidad de rotación, tamaño y material propio. Soporta jerarquía (lunas orbitando planetas). |
| `camara.py` | Clase `Cámara`: configura la vista 3D utilizando `gluPerspective` y `gluLookAt`. |
| `foco.py` | Clase `Foco`: administra fuentes de luz OpenGL (difusa, ambiente, especular, posición, brillo). |
| `material.py` | Clase `Material`: define propiedades de superficie para rendering con iluminación. |
| `customType.py` | Enum `CustomType`: sistema de registro para tipos personalizables. Permite extender la arquitectura agregando nuevos tipos con su correspondiente JSON. |

## Configuración

El proyecto es **data-driven**: toda la configuración del sistema solar, cámaras, luces y materiales se define en archivos JSON dentro de `src/custom/json/`.

### planetas.json

Define la jerarquía orbital del sistema solar de forma recursiva:

```json
{
  "astros": [
    {
      "nombre": "Sol",
      "radio": 0.0,
      "wRotAstro": 0.0,
      "wRotProp": 0.2,
      "tamanio": 0.7,
      "material": { "refPosition": 0 },
      "astros": [
        {
          "nombre": "Mercurio",
          "radio": 110.0,
          "wRotAstro": -4.5,
          "wRotProp": 0.15,
          "tamanio": 0.1,
          "material": { "refPosition": 1 },
          "astros": []
        }
      ]
    }
  ]
}
```

| Campo | Descripción |
|-------|-------------|
| `radio` | Distancia orbital al cuerpo padre |
| `wRotAstro` | Velocidad de rotación orbital |
| `wRotProp` | Velocidad de rotación sobre el eje propio |
| `tamanio` | Escala del cuerpo celeste |
| `material.refPosition` | Índice del material en `materiales.json` |
| `astros` | Array de lunas / sub-cuerpos que orbitan este astro |

**Cuerpos celestes incluidos:** Sol, Mercurio, Venus, Tierra (con Luna), Marte, Júpiter (con Ío y Europa), Saturno, Urano, Neptuno.

### camaras.json

Configura 4 presets de cámara con posición, punto de vista y orientación:

```json
{
  "posx": 5, "posy": 5, "posz": 5,
  "povx": 0, "povy": 0, "povz": 0,
  "orientacionx": 0, "orientaciony": 1, "orientacionz": 0
}
```

### focos.json

Define hasta 8 fuentes de luz con color difuso, ambiente, especular, posición y brillo:

```json
{
  "brillo": 10,
  "luzdifusa": [1.0, 1.0, 0.0, 1.0],
  "luzambiente": [1.0, 1.0, 1.0, 1.0],
  "luzspecular": [1.0, 1.0, 1.0, 1.0],
  "posicion": [0.0, 100.0, 0.0, 0.0]
}
```

### materiales.json

Define las propiedades de material para renderizar los cuerpos celestes:

```json
{
  "brillo": 100.0,
  "luzdifusa": [0.75164, 0.60648, 0.22648, 1.0],
  "luzambiente": [0.24725, 0.1995, 0.0745, 1.0],
  "luzspecular": [0.928281, 0.855802, 0.366065, 1.0]
}
```

## Arquitectura

```
                    ┌──────────┐
                    │  main.py │  (Punto de entrada)
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  Mundo   │  (Gestión de escena, renderizado, eventos)
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
         ┌────▼───┐ ┌────▼───┐ ┌───▼────┐
         │ Modelo │ │  Foco  │ │ Cámara │
         └────┬───┘ └────────┘ └────────┘
              │
         ┌────▼───┐
         │  Astro │  (Hereda de Modelo)
         └────┬───┘
              │
        ┌─────▼─────┐
        │  Materiales│
        └───────────┘

Configuración: JSON ──► CustomType (enum) ──► Clases con deserialize()
```

La arquitectura utiliza un **sistema de tipos personalizables** (`CustomType` enum) que permite registrar nuevos tipos de entidades simplemente:
1. Creando un archivo JSON de configuración
2. Agregando una entrada al enum `CustomType` con su clase correspondiente
3. Implementando un método `deserialize()` estático en la clase

## CI/CD

El proyecto incluye un workflow de GitHub Actions (`.github/workflows/autoreleases.yml`) que crea automáticamente un release cuando se push una etiqueta con formato `v*`:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python 3.10 | Lenguaje de programación |
| PyOpenGL 3.1.6 | Bindings de Python para OpenGL |
| GLUT | Toolkit de ventanas y manejo de eventos |
| OpenGL | Renderizado 3D, iluminación, sombreado |

## Autor

[ManuelDuque](https://github.com/ManuelDuque)
