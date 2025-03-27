# Máquina Tragaperritos VIP 🎰🐶

Este proyecto es una aplicación gráfica de una máquina tragaperras temática de perritos, desarrollada en Python utilizando las bibliotecas `customtkinter`, `pygame` y `Pillow`. La aplicación incluye efectos visuales, sonidos y animaciones para simular una experiencia de juego interactiva.

## Características

- **Interfaz gráfica**: Utiliza `customtkinter` para un diseño atractivo y personalizable.
- **Efectos visuales**: Animaciones y cambios de color durante el giro de los rodillos.
- **Sonidos**: Incluye efectos de sonido para tiradas, premios, errores y avances.
- **Modo de avance**: Gira un rodillo específico cuando se obtienen dos símbolos iguales.
- **Temática de perritos**: Los símbolos de los rodillos son emojis de perros.

## Requisitos del sistema

- Python 3.8 o superior.
- Las siguientes bibliotecas de Python:
  - `customtkinter==5.2.0`
  - `pygame==2.5.0`
  - `Pillow==10.0.0`
  - `tkinter` (incluido en la instalación estándar de Python).

## Instalación

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Asegúrate de tener Python instalado. Puedes verificarlo ejecutando:

   ```bash
   python --version

Recopilando información del área de trabajo```markdown
# Máquina Tragaperritos VIP 🎰🐶

Este proyecto es una aplicación gráfica de una máquina tragaperras temática de perritos, desarrollada en Python utilizando las bibliotecas `customtkinter`, `pygame` y `Pillow`. La aplicación incluye efectos visuales, sonidos y animaciones para simular una experiencia de juego interactiva.

## Características

- **Interfaz gráfica moderna**: Utiliza `customtkinter` para un diseño atractivo y personalizable.
- **Efectos visuales**: Animaciones y cambios de color durante el giro de los rodillos.
- **Sonidos**: Incluye efectos de sonido para tiradas, premios, errores y avances.
- **Modo de avance**: Gira un rodillo específico cuando se obtienen dos símbolos iguales.
- **Temática de perritos**: Los símbolos de los rodillos son emojis de perros.

## Requisitos del sistema

- Python 3.8 o superior.
- Las siguientes bibliotecas de Python:
  - `customtkinter==5.2.0`
  - `pygame==2.5.0`
  - `Pillow==10.0.0`
  - `tkinter` (incluido en la instalación estándar de Python).

## Instalación

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Asegúrate de tener Python instalado. Puedes verificarlo ejecutando:

   ```bash
   python --version
   ```

3. Instala las dependencias necesarias utilizando el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. Asegúrate de que los archivos de sonido (`tirada.mp3`, `ganar.mp3`, `error.mp3`, `avance.mp3`) estén en la carpeta `sonidos/` dentro del directorio del proyecto.

## Ejecución

1. Navega al directorio del proyecto desde la terminal:

   ```bash
   cd /ruta/a/Tragaperritos
   ```

2. Ejecuta el archivo principal `tragaperritos.py`:

   ```bash
   python tragaperritos.py
   ```

3. Se abrirá una ventana con la interfaz gráfica de la máquina tragaperritos. Sigue las instrucciones en pantalla para jugar.

## Cómo jugar

1. **Pantalla de inicio**:
   - Introduce tu nombre y la cantidad de monedas iniciales.
   - Haz clic en el botón "INICIAR JUEGO".

2. **Pantalla de juego**:
   - Haz clic en el botón "TIRAR" para girar los rodillos.
   - Si obtienes tres símbolos iguales, ganas el bote acumulado.
   - Si obtienes dos símbolos iguales, puedes girar el tercer rodillo gratis en modo de avance.
   - Si te quedas sin monedas, el juego termina.

## Estructura del proyecto

```
requirements.txt   # Archivo con las dependencias del proyecto.
tragaperritos.py     # Código principal de la aplicación.
sonidos/           # Carpeta que contiene los archivos de sonido.
    avance.mp3
    error.mp3
    ganar.mp3
    tirada.mp3
```

## Personalización

Puedes personalizar los colores, fuentes y sonidos modificando las constantes definidas en el archivo `tragaperras.py`. Por ejemplo:

- **Colores**: Cambia las constantes `COLOR_FONDO`, `COLOR_ACENTO`, etc.
- **Fuentes**: Modifica las constantes `FUENTE_TITULO`, `FUENTE_TEXTO`, etc.
- **Sonidos**: Sustituye los archivos de sonido en la carpeta `sonidos/`.

## Créditos

Este proyecto fue desarrollado como una demostración de una aplicación gráfica interactiva en Python. Utiliza las siguientes bibliotecas:

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [pygame](https://www.pygame.org/)
- [Pillow](https://python-pillow.org/)

¡Diviértete jugando con la Máquina Tragaperritos VIP! 🎰🐕
```