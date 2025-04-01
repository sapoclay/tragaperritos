import tkinter as tk
import customtkinter as ctk
import random
import time
import threading
from PIL import Image, ImageTk
import os
import pygame

# Cargar estilos desde estilos.css manualmente
def cargar_estilos(filepath):
    estilos = {}
    with open(filepath, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith("--"):
                propiedad, valor = linea.split(":")
                estilos[propiedad.strip()] = valor.strip().rstrip(";")
    return estilos

# Cargar estilos
estilos = cargar_estilos("estilos.css")

class MaquinaTragaperras:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina Tragaperritos VIP")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        
        # Aplicar estilos desde el archivo CSS
        self.aplicar_estilos()
        
        # Configurar el fondo después de cargar los estilos
        self.root.configure(bg=COLOR_FONDO)
        
        # Inicializar pygame para reproducir sonidos
        pygame.mixer.init()
        
        # Cargar sonidos
        self.sonido_tirada = pygame.mixer.Sound("sonidos/tirada.mp3")
        self.sonido_ganar = pygame.mixer.Sound("sonidos/ganar.mp3")
        self.sonido_error = pygame.mixer.Sound("sonidos/error.mp3")
        self.sonido_avance = pygame.mixer.Sound("sonidos/avance.mp3")
        
        # Variables del juego
        self.nombre_jugador = ""
        self.credito = 0
        self.bote = 10
        self.girando = False
        self.modo_avance = False
        self.posicion_avance = -1
        self.ultimo_fue_avance = False
        
        # Perretes disponibles
        self.perros = ["Guía", "Perrete", "Caniche"]
        self.emojis_perros = {
            "guia": "🦮",
            "perrete": "🐕",
            "caniche": "🐩"
        }
        
        # Resultados actuales
        self.resultados = ["", "", ""]
        
        # Iniciar el juego
        self.pantalla_inicio()
    
    def aplicar_estilos(self):
        """Aplica los estilos desde el archivo estilos.css"""
        global COLOR_FONDO, COLOR_ACENTO, COLOR_SECUNDARIO, COLOR_BOTON
        global FUENTE_TITULO, FUENTE_TEXTO, FUENTE_NUMEROS, FUENTE_SIMBOLOS
        
        COLOR_FONDO = estilos["--color-fondo"]
        COLOR_ACENTO = estilos["--color-acento"]
        COLOR_SECUNDARIO = estilos["--color-secundario"]
        COLOR_BOTON = estilos["--color-boton"]
        
        FUENTE_TITULO = (estilos["--fuente-titulo"], 26, "bold")
        FUENTE_TEXTO = (estilos["--fuente-texto"], 14)
        FUENTE_NUMEROS = (estilos["--fuente-numeros"], 20)
        FUENTE_SIMBOLOS = (estilos["--fuente-simbolos"], 72, "bold")

    def efecto_iluminacion(self):
        colors = [COLOR_ACENTO, "#FF0000", "#00FF00", "#0000FF"]
        current_color = 0
        for _ in range(8):
            for frame in self.frames_rodillos:
                frame.configure(border_color=colors[current_color])
            current_color = (current_color + 1) % len(colors)
            time.sleep(0.1)
            self.root.update()
        for frame in self.frames_rodillos:
            frame.configure(border_color=COLOR_ACENTO)
    
    def efectos_durante_giro(self):
        """Método para cambiar colores del borde y luces inferiores durante el giro"""
        colors = [COLOR_ACENTO, "#FF0000", "#00FF00", "#0000FF", "#FF00FF", "#00FFFF", "#FFFF00", "#FFA500", "#800080", "#008080"]
        simbolos = ["★", "✦", "✧", "❈", "✺", "✨", "⚡", "💫", "🌟"]
        
        # Obtener las etiquetas de luces inferiores
        luces_labels = []
        for widget in self.frame_principal.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget.winfo_height() == 20:
                for luz in widget.winfo_children():
                    if isinstance(luz, ctk.CTkLabel):
                        luces_labels.append(luz)
        
        # Guardar el color original del botón para restaurarlo después
        color_original_boton = COLOR_BOTON
        
        # Contador para cambiar símbolos más rápido que los colores
        contador = 0
        
        while not self.detener_efectos:
            contador += 1
            
            # Cambiar color del borde exterior del frame principal
            color_borde_exterior = random.choice(colors)
            self.root.after(0, lambda c=color_borde_exterior: self.frame_principal.configure(border_color=c))
            
            # Cambiar color de bordes de rodillos
            for frame in self.frames_rodillos:
                color = random.choice(colors)
                self.root.after(0, lambda f=frame, c=color: f.configure(border_color=c))
            
            # Cambiar color del botón Tirar
            color_boton = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.root.after(0, lambda c=color_boton: self.boton_tirar.configure(fg_color=c))
            
            # Cambiar color y símbolo de luces inferiores con más frecuencia
            for luz in luces_labels:
                color = random.choice(colors)
                simbolo = random.choice(simbolos)
                # Usar una función lambda para aplicar los cambios
                # Crear una copia local de las variables para cada iteración
                def actualizar_luz(luz_local=luz, color_local=color, simbolo_local=simbolo):
                    luz_local.configure(text_color=color_local)
                    luz_local.configure(text=simbolo_local)
                self.root.after(0, actualizar_luz)
            
            # Cambiar símbolos más rápido cada 2 iteraciones
            if contador % 2 == 0:
                for luz in luces_labels:
                    simbolo = random.choice(simbolos)
                    # Usar una función en lugar de lambda para evitar problemas de captura de variables
                    def actualizar_simbolo(luz_local=luz, simbolo_local=simbolo):
                        luz_local.configure(text=simbolo_local)
                    self.root.after(0, actualizar_simbolo)
            
            time.sleep(0.1)  # Reducir el tiempo para animación más fluida
        
        # Restaurar colores originales
        self.root.after(0, lambda: self.frame_principal.configure(border_color=COLOR_ACENTO))
        
        for frame in self.frames_rodillos:
            self.root.after(0, lambda f=frame: f.configure(border_color=COLOR_ACENTO))
        
        # Restaurar color original del botón
        self.root.after(0, lambda: self.boton_tirar.configure(fg_color=color_original_boton))
        
        # Restaurar luces inferiores con colores aleatorios pero fijos
        for luz in luces_labels:
            color = random.choice(["#FF0000", "#00FF00", "#0000FF"])
            simbolo = random.choice(simbolos)
            # Usar una función en lugar de lambda para evitar problemas de captura de variables
            def restaurar_luz(luz_local=luz, color_local=color, simbolo_local=simbolo):
                luz_local.configure(text_color=color_local)
                luz_local.configure(text=simbolo_local)
            self.root.after(0, restaurar_luz)
    
    def parpadear_bote(self):
        original_color = self.label_bote.cget("text_color")
        for _ in range(3):
            self.label_bote.configure(text_color="#FF0000")
            time.sleep(0.2)
            self.label_bote.configure(text_color=original_color)
            time.sleep(0.2)
    
    def pantalla_inicio(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame_principal = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_FONDO,
            border_width=4,
            border_color=COLOR_ACENTO,
            corner_radius=15
        )
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título con efecto neón
        ctk.CTkLabel(
            self.frame_principal, 
            text="🎰🐶 TRAGAPERRITOS VIP 🐕🎰",
            font=FUENTE_TITULO,
            text_color=COLOR_ACENTO,
            pady=30
        ).pack()
        
        # Marco decorativo
        decoracion_frame = ctk.CTkFrame(
            self.frame_principal,
            fg_color=COLOR_ACENTO,
            height=3
        )
        decoracion_frame.pack(fill=tk.X, pady=10, padx=50)
        
        # Contenido de inicio
        ctk.CTkLabel(
            self.frame_principal, 
            text="Introduce tus datos:",
            font=FUENTE_TEXTO,
            text_color=COLOR_SECUNDARIO,
            pady=20
        ).pack()
        
        # Entrada de nombre
        self.entry_nombre = ctk.CTkEntry(
            self.frame_principal,
            font=FUENTE_TEXTO,
            width=300,
            height=40,
            border_color=COLOR_ACENTO,
            placeholder_text="Nombre del jugador"
        )
        self.entry_nombre.pack(pady=10)
        
        # Entrada de monedas
        self.entry_monedas = ctk.CTkEntry(
            self.frame_principal,
            font=FUENTE_TEXTO,
            width=300,
            height=40,
            border_color=COLOR_ACENTO,
            placeholder_text="Monedas iniciales"
        )
        self.entry_monedas.pack(pady=10)
        
        # Botón de inicio
        ctk.CTkButton(
            self.frame_principal, 
            text="INICIAR JUEGO",
            font=("Arial Rounded MT Bold", 18),
            command=self.validar_datos,
            fg_color=COLOR_BOTON,
            hover_color="#B03A2E",
            border_color=COLOR_ACENTO,
            border_width=2,
            width=250,
            height=50,
            corner_radius=20
        ).pack(pady=30)
        
        # Efectos de luces inferiores
        luces_frame = ctk.CTkFrame(
            self.frame_principal,
            height=20,
            fg_color=COLOR_FONDO
        )
        luces_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        luces = ["★", "✦", "✧", "❈", "✺"]
        for _ in range(8):
            ctk.CTkLabel(
                luces_frame,
                text=random.choice(luces),
                text_color=random.choice(["#FF0000", "#00FF00", "#0000FF"]),
                font=("Symbola", 18)
            ).pack(side=tk.LEFT, expand=True)
    
    def pantalla_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame_principal = ctk.CTkFrame(
            self.root,
            fg_color=COLOR_FONDO,
            border_width=4,
            border_color=COLOR_ACENTO,
            corner_radius=15
        )
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabecera del juego
        cabecera_frame = ctk.CTkFrame(
            self.frame_principal,
            fg_color=COLOR_FONDO
        )
        cabecera_frame.pack(fill=tk.X, padx=30, pady=10)
        
        ctk.CTkLabel(
            cabecera_frame,
            text="🎰🐶 TRAGAPERRITOS VIP 🐕🎰",
            font=FUENTE_TITULO,
            text_color=COLOR_ACENTO
        ).pack(side=tk.TOP, pady=10)
        
        # Panel informativo
        info_frame = ctk.CTkFrame(
            self.frame_principal,
            fg_color="#2c3e50",
            border_width=2,
            border_color=COLOR_ACENTO,
            corner_radius=10
        )
        info_frame.pack(fill=tk.X, padx=30, pady=10)
        
        # Información del jugador
        jugador_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        jugador_frame.pack(side=tk.LEFT, padx=20, pady=5)
        
        ctk.CTkLabel(
            jugador_frame,
            text=f"JUGADOR: {self.nombre_jugador}",
            font=FUENTE_TEXTO,
            text_color=COLOR_SECUNDARIO
        ).pack(side=tk.LEFT)
        
        # Crédito
        self.label_credito = ctk.CTkLabel(
            jugador_frame,
            text=f"FICHAS: {self.credito}",
            font=FUENTE_NUMEROS,
            text_color="#00FF00",
            padx=20
        )
        self.label_credito.pack(side=tk.RIGHT)
        
        # Bote
        bote_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        bote_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        self.label_bote = ctk.CTkLabel(
            bote_frame,
            text=f"BOTE: {self.bote}",
            font=FUENTE_NUMEROS,
            text_color="#FF0000"
        )
        self.label_bote.pack(side=tk.RIGHT)
        
        # Rodillos
        self.rodillos_frame = ctk.CTkFrame(
            self.frame_principal,
            fg_color=COLOR_FONDO
        )
        self.rodillos_frame.pack(pady=30, fill=tk.BOTH, expand=True, padx=30)

        self.frames_rodillos = []
        self.labels_rodillos = []
        
        for i in range(3):
            frame_rodillo = ctk.CTkFrame(
                self.rodillos_frame,
                fg_color="#2c3e50",
                border_width=3,
                border_color=COLOR_ACENTO,
                corner_radius=10,
                width=150,  # Tamaño fijo
                height=150  # Tamaño fijo
            )
            frame_rodillo.pack_propagate(False)  # Evitar que los widgets internos cambien el tamaño del frame
            frame_rodillo.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
            self.frames_rodillos.append(frame_rodillo)
            
            label_rodillo = ctk.CTkLabel(
                frame_rodillo,
                text="?",
                font=FUENTE_SIMBOLOS,
                text_color=COLOR_ACENTO
            )
            label_rodillo.pack(expand=True)
            self.labels_rodillos.append(label_rodillo)
        
        # Panel de control
        control_frame = ctk.CTkFrame(
            self.frame_principal,
            fg_color=COLOR_FONDO
        )
        control_frame.pack(fill=tk.X, padx=30, pady=20)
        
        # Botón de tirar
        self.boton_tirar = ctk.CTkButton(
            control_frame,
            text="🎰🎲 TIRAR 🎲🎰",
            font=("Arial Rounded MT Bold", 24),
            command=self.tirar,
            fg_color=COLOR_BOTON,
            hover_color="#B03A2E",
            border_color=COLOR_ACENTO,
            border_width=2,
            width=250,
            height=70,
            corner_radius=25
        )
        self.boton_tirar.pack(pady=10)
        
        # Mensaje de resultado
        self.label_resultado = ctk.CTkLabel(
            control_frame,
            text="",
            font=("Impact", 18),
            text_color=COLOR_ACENTO,
            wraplength=400
        )
        self.label_resultado.pack(pady=10)
        
        # Efectos de luces inferiores
        luces_frame = ctk.CTkFrame(
            self.frame_principal,
            height=20,
            fg_color=COLOR_FONDO
        )
        luces_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        luces = ["★", "✦", "✧", "❈", "✺"]
        for _ in range(8):
            ctk.CTkLabel(
                luces_frame,
                text=random.choice(luces),
                text_color=random.choice(["#FF0000", "#00FF00", "#0000FF"]),
                font=("Symbola", 18)
            ).pack(side=tk.LEFT, expand=True)
        
        self.actualizar_rodillos(["?", "?", "?"])
       
    def actualizar_rodillos(self, simbolos):
        for i, simbolo in enumerate(simbolos):
            self.labels_rodillos[i].configure(text=simbolo)
            # Asegurar que el tamaño de la fuente sea siempre el mismo
            self.labels_rodillos[i].configure(font=FUENTE_SIMBOLOS)
        # Asegurar que los frames mantengan el tamaño fijo
        for frame in self.frames_rodillos:
            frame.configure(width=150, height=150)
    
    def tirar(self):
        if self.girando:
            return
        
        if not self.modo_avance and self.credito <= 0:
            self.mostrar_error("¡FICHAS INSUFICIENTES!\nJUEGO TERMINADO", es_fin_juego=True)
            return
        
        if not self.modo_avance:
            self.credito -= 1
            self.label_credito.configure(text=f"FICHAS: {self.credito}")
            self.bote += 1
            self.label_bote.configure(text=f"JACKPOT: {self.bote}")
            self.ultimo_fue_avance = False
        
        self.boton_tirar.configure(state="disabled")
        self.label_resultado.configure(text="¡GIRANDO... BUENA SUERTE!")
        
        self.girando = True
        threading.Thread(target=self.animar_giro).start()
    
    def animar_giro(self):
        if self.modo_avance:
            rodillos_a_girar = [self.posicion_avance]
            self.modo_avance = False
            self.posicion_avance = -1
        else:
            rodillos_a_girar = [0, 1, 2]
        
        # Efecto de arranque
        for _ in range(3):
            for rodillo in self.labels_rodillos:
                rodillo.configure(text_color="#FF0000")
            time.sleep(0.1)
            for rodillo in self.labels_rodillos:
                rodillo.configure(text_color=COLOR_ACENTO)
            time.sleep(0.1)
        
        # Iniciar efectos de luces mientras gira
        self.detener_efectos = False
        threading.Thread(target=self.efectos_durante_giro, daemon=True).start()
        
        self.sonido_tirada.play()
        duracion_sonido = self.sonido_tirada.get_length()
        iteraciones = int((duracion_sonido / 2) / 0.1)
        
        for _ in range(iteraciones):
            simbolos_animacion = self.resultados.copy()
            for pos in rodillos_a_girar:
                simbolos_animacion[pos] = random.choice(list(self.emojis_perros.values()))
                color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                self.root.after(0, lambda p=pos, c=color: self.frames_rodillos[p].configure(fg_color=c))
            
            self.root.after(0, lambda s=simbolos_animacion: self.actualizar_rodillos(s))
            time.sleep(0.1)
        
        # Detener los efectos de luces
        self.detener_efectos = True
        
        for pos in rodillos_a_girar:
            self.root.after(0, lambda p=pos: self.frames_rodillos[p].configure(fg_color="#2c3e50"))
        
        # Determinar resultados finales
        if len(rodillos_a_girar) == 3:
            # Asegurar que no siempre sean iguales
            if random.random() < 0.05:  # Baja probabilidad de que sean iguales
                perro_elegido = random.choice(self.perros)
                for pos in rodillos_a_girar:
                    self.resultados[pos] = perro_elegido
            else:
                # Generar resultados aleatorios con al menos un símbolo diferente
                self.resultados = random.sample(self.perros, 3)
        else:
            for pos in rodillos_a_girar:
                self.resultados[pos] = random.choice(self.perros)
        
        simbolos_finales = [self.emojis_perros[perro.lower().replace('í', 'i').replace('á', 'a').replace('é', 'e').replace('ó', 'o').replace('ú', 'u')] for perro in self.resultados]
        self.root.after(0, lambda s=simbolos_finales: self.actualizar_rodillos(s))
        self.root.after(100, self.verificar_resultado)
    
    def verificar_resultado(self):
        conteo = {}
        for perro in self.resultados:
            conteo[perro] = conteo.get(perro, 0) + 1
        
        for perro, cantidad in conteo.items():
            if cantidad == 3:
                self.sonido_ganar.play()
                self.label_resultado.configure(
                    text=f"¡PREMIO! ¡{self.bote} FICHAS!",
                    text_color="#FFD700"
                )
                self.credito += self.bote
                self.bote = 10
                self.label_credito.configure(text=f"FICHAS: {self.credito}")
                self.label_bote.configure(text=f"JACKPOT: {self.bote}")
                threading.Thread(target=self.efecto_iluminacion).start()
                self.girando = False
                self.boton_tirar.configure(state="normal")
                self.ultimo_fue_avance = False
                return
        
        for perro, cantidad in conteo.items():
            if cantidad == 2 and not self.ultimo_fue_avance:
                for i, p in enumerate(self.resultados):
                    if p != perro:
                        self.posicion_avance = i
                        break
                self.modo_avance = True
                self.ultimo_fue_avance = True
                self.sonido_avance.play()
                self.label_resultado.configure(
                    text=f"¡AVANCE!\nVa a girar el perro {['IZQUIERDO', 'CENTRAL', 'DERECHO'][self.posicion_avance]} GRATIS",
                    text_color="#4CAF50"
                )
                self.girando = False
                self.boton_tirar.configure(state="normal")
                return
        
        self.label_resultado.configure(
            text="¡PRUEBA OTRA VEZ!",
            text_color=COLOR_SECUNDARIO
        )
        self.girando = False
        self.boton_tirar.configure(state="normal")
        self.ultimo_fue_avance = False

    def validar_datos(self):
        nombre = self.entry_nombre.get().strip()
        monedas = self.entry_monedas.get().strip()
        
        # Validar que el nombre no esté vacío
        if not nombre:
            self.mostrar_error("¡ERROR!\nEl nombre no puede estar vacío.")
            return
        
        # Validar que las monedas sean un número entero positivo
        try:
            monedas = int(monedas)
            if monedas <= 0:
                self.mostrar_error("¡ERROR!\nEl número de monedas debe ser positivo.")
                return
        except ValueError:
            self.mostrar_error("¡ERROR!\nEl número de monedas debe ser un número entero.")
            return
        
        # Si todo es válido, guardar los datos y pasar a la pantalla de juego
        self.nombre_jugador = nombre
        self.credito = monedas
        self.pantalla_juego()
    
    def mostrar_error(self, mensaje, es_fin_juego=False):
        # Reproducir sonido de error
        self.sonido_error.play()
        
        # Crear ventana de error con tamaño fijo para que el borde se muestre completo
        error_frame = ctk.CTkFrame(
            self.root,
            fg_color="#2c3e50",
            border_width=3,
            border_color="#FF0000",
            corner_radius=15,
            width=400,
            height=250
        )
        error_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Importante: configurar el frame para que no se redimensione con los widgets internos
        error_frame.pack_propagate(False)
        
        # Mensaje de error
        ctk.CTkLabel(
            error_frame,
            text=mensaje,
            font=("Impact", 20),
            text_color="#FF0000",
            wraplength=350,
            pady=20
        ).pack(expand=True)
        
        # Botón para cerrar
        if es_fin_juego:
            ctk.CTkButton(
                error_frame,
                text="REINICIAR",
                font=("Arial Rounded MT Bold", 16),
                command=lambda: [error_frame.destroy(), self.pantalla_inicio()],
                fg_color=COLOR_BOTON,
                hover_color="#B03A2E",
                width=150,
                height=40,
                corner_radius=20
            ).pack(pady=20)
        else:
            ctk.CTkButton(
                error_frame,
                text="CERRAR",
                font=("Arial Rounded MT Bold", 16),
                command=error_frame.destroy,
                fg_color=COLOR_BOTON,
                hover_color="#B03A2E",
                width=150,
                height=40,
                corner_radius=20
            ).pack(pady=20)
    

def main():
    root = ctk.CTk()
    app = MaquinaTragaperras(root)
    root.mainloop()

if __name__ == "__main__":
    main()