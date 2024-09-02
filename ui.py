import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
try:
    from PIL import Image, ImageTk
except ImportError:
    print("PIL no está instalado. Por favor, instala Pillow con 'pip install Pillow'")
    exit(1)

class PantallaInicio:
    def __init__(self, master, iniciar_juego_callback):
        self.master = master
        self.master.title("¿Dónde está la bolita? - Inicio")
        self.master.geometry("400x300")
        self.master.configure(bg="red")  # Cambio del color de fondo a rojo

        self.iniciar_juego_callback = iniciar_juego_callback

        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.master, text="¿Dónde está la bolita?", font=("Arial", 20, "bold"), bg="red", fg="white").pack(pady=20)

        tk.Button(self.master, text="Jugar Solo", font=("Arial", 14), command=lambda: self.iniciar_juego_callback("solo"), bg="yellow").pack(pady=10)
        tk.Button(self.master, text="Multijugador Local", font=("Arial", 14), command=lambda: self.iniciar_juego_callback("multijugador"), bg="yellow").pack(pady=10)

class JuegoVasos:
    def __init__(self, master, modo_juego):
        self.master = master
        self.master.title("¿Dónde está la bolita?")
        self.master.geometry("800x600")
        self.master.configure(bg="red")  # Cambio del color de fondo a rojo

        self.modo_juego = modo_juego
        self.posicion_bolita = 1  # Siempre empieza en el medio
        self.puntuacion = 0
        self.nivel_dificultad = 1
        self.jugador_actual = 1
        self.puntuaciones = {1: 0, 2: 0}
        self.cargar_imagenes()
        self.crear_widgets()
        self.mostrar_instrucciones()
        self.mostrar_bolita_inicial()

    def cargar_imagenes(self):
        try:
            self.imagen_vaso = ImageTk.PhotoImage(Image.open("assets/VASO.png").resize((100, 150)))
            self.imagen_bolita = ImageTk.PhotoImage(Image.open("assets/bolita.jpeg").resize((50, 50)))
        except FileNotFoundError as e:
            print(f"No se encontró la imagen: {e.filename}")
            exit(1)

    def crear_widgets(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.master, bg="red")
        self.frame_principal.pack(expand=True, fill=tk.BOTH)

        # Frame para las instrucciones
        self.frame_instrucciones = tk.Frame(self.frame_principal, bg="red")
        self.frame_instrucciones.pack(pady=20)

        self.label_instrucciones = tk.Label(self.frame_instrucciones, text="¿Dónde está la bolita?", font=("Arial", 20, "bold"), bg="red", fg="white")
        self.label_instrucciones.pack()

        # Frame para los vasos
        self.frame_vasos = tk.Frame(self.frame_principal, bg="red")
        self.frame_vasos.pack(pady=20)

        # botones de vasos con imágenes usando `place`
        self.vasos = []
        self.posiciones_iniciales = [150, 350, 550]  # Posiciones X iniciales de los vasos
        for i in range(3):
            vaso = tk.Button(self.master, image=self.imagen_vaso, bd=0, command=lambda x=i: self.verificar_seleccion(x))
            vaso.place(x=self.posiciones_iniciales[i], y=200)
            self.vasos.append(vaso)

        # Frame para controles (debajo de los vasos)
        self.frame_controles = tk.Frame(self.master, bg="red")
        self.frame_controles.place(x=150, y=400)

        # Botón para revolver
        self.boton_revolver = tk.Button(self.frame_controles, text="Mezclar Vasos", font=("Arial", 14), command=self.revolver_vasos, bg="yellow")
        self.boton_revolver.grid(row=0, column=2, padx=20)

        # Label para la puntuación
        if self.modo_juego == "solo":
            self.label_puntuacion = tk.Label(self.frame_controles, text=f"Puntuación: {self.puntuacion}", font=("Arial", 14), bg="red", fg="white")
        else:
            self.label_puntuacion = tk.Label(self.frame_controles, text=f"Jugador 1: {self.puntuaciones[1]} | Jugador 2: {self.puntuaciones[2]}", font=("Arial", 14), bg="red", fg="white")
        self.label_puntuacion.grid(row=0, column=0, padx=20)

        # Label para el nivel de dificultad
        self.label_dificultad = tk.Label(self.frame_controles, text=f"Nivel de dificultad: {self.nivel_dificultad}", font=("Arial", 14), bg="yellow")
        self.label_dificultad.grid(row=0, column=1, padx=20)

        # Botón para cambiar la dificultad
        self.boton_dificultad = tk.Button(self.frame_controles, text="Cambiar Dificultad", font=("Arial", 14), command=self.cambiar_dificultad, bg="yellow")
        self.boton_dificultad.grid(row=1, column=1, pady=20)

        # Botón para volver al menú principal
        self.boton_volver = tk.Button(self.frame_controles, text="Volver al Menú", font=("Arial", 14), command=self.volver_al_menu, bg="yellow")
        self.boton_volver.grid(row=1, column=2, pady=20)

    def mostrar_instrucciones(self):
        instrucciones = "La bolita está escondida bajo el vaso del medio.\n Mezcla los vasos \n¡Adivina dónde está!"
        messagebox.showinfo("Instrucciones", instrucciones)

    def mostrar_bolita_inicial(self):
        self.mostrar_bolita(1)  # Muestra la bolita en el vaso del medio
        self.master.after(2000, self.restaurar_vasos)  # Restaura los vasos después de 2 segundos

    def revolver_vasos(self):
        self.posicion_bolita = random.randint(0, 2)
        self.animar_mezcla()

    def animar_mezcla(self):
        velocidad = 0.3 / self.nivel_dificultad
        secuencia = [(0, 1), (1, 2), (2, 0)] * self.nivel_dificultad

        for i, j in secuencia:
            self.mover_vasos(i, j, velocidad)

        self.master.after(int(velocidad * 1000), lambda: messagebox.showinfo("Mezcla completada", "¡Los vasos han sido mezclados!"))

    def mover_vasos(self, i, j, duracion):
        pasos = 30  # Más pasos para un movimiento más suave
        dx = (self.vasos[j].winfo_x() - self.vasos[i].winfo_x()) // pasos

        for paso in range(pasos + 1):
            self.vasos[i].place(x=self.vasos[i].winfo_x() + dx, y=self.vasos[i].winfo_y())
            self.vasos[j].place(x=self.vasos[j].winfo_x() - dx, y=self.vasos[j].winfo_y())

            self.master.update()
            time.sleep(duracion / pasos)

        # Intercambiar posiciones en la lista
        self.vasos[i], self.vasos[j] = self.vasos[j], self.vasos[i]

    def verificar_seleccion(self, seleccion):
        if seleccion == self.posicion_bolita:
            self.mostrar_bolita(seleccion)
            self.master.after(1000, self.celebrar_victoria)
        else:
            messagebox.showinfo("¡Fallaste!", "La bolita no está aquí. ¡Mezcle de nuevo y vuelve a intentarlo!")
            if self.modo_juego == "multijugador":
                self.cambiar_jugador()

        #las imágenes de los vasos
        self.master.after(1500, self.restaurar_vasos)

    def mostrar_bolita(self, seleccion):
        try:
            imagen_vaso = Image.open("assets/VASO.png").convert("RGBA")
            imagen_bolita = Image.open("assets/bolita.jpeg").convert("RGBA")

            imagen_vaso = imagen_vaso.resize((100, 150))
            imagen_bolita = imagen_bolita.resize((50, 50))

            imagen_combinada = Image.new('RGBA', (100, 150), (0, 0, 0, 0))
            imagen_combinada.paste(imagen_vaso, (0, 0))
            imagen_combinada.paste(imagen_bolita, (25, 100), imagen_bolita)

            imagen_tk = ImageTk.PhotoImage(imagen_combinada)
            self.vasos[seleccion].config(image=imagen_tk)
            self.vasos[seleccion].image = imagen_tk
        except Exception as e:
            print(f"Error al mostrar la bolita: {e}")

    def restaurar_vasos(self):
        for i, vaso in enumerate(self.vasos):
            vaso.config(image=self.imagen_vaso)
            vaso.place(x=self.posiciones_iniciales[i], y=200)

    def celebrar_victoria(self):
        # Cambia el fondo a un color festivo
        self.master.configure(bg="yellow")

        # Muestra un mensaje de felicitaciones
        if self.modo_juego == "solo":
            self.puntuacion += 1
            self.label_puntuacion.config(text=f"Puntuación: {self.puntuacion}")
        else:
            self.puntuaciones[self.jugador_actual] += 1
            self.label_puntuacion.config(text=f"Jugador 1: {self.puntuaciones[1]} | Jugador 2: {self.puntuaciones[2]}")

        messagebox.showinfo("¡Ganaste!", "¡Encontraste la bolita!")

        # fondo de nuevo al color 
        self.master.configure(bg="red")

        if self.modo_juego != "solo":
            self.cambiar_jugador()

    def cambiar_jugador(self):
        self.jugador_actual = 2 if self.jugador_actual == 1 else 1
        messagebox.showinfo("Cambio de Jugador", f"Es el turno del Jugador {self.jugador_actual}")

    def cambiar_dificultad(self):
        nueva_dificultad = simpledialog.askinteger("Cambiar Dificultad", "Selecciona la nueva dificultad (1-5):", minvalue=1, maxvalue=5)
        if nueva_dificultad:
            self.nivel_dificultad = nueva_dificultad
            self.label_dificultad.config(text=f"Nivel de dificultad: {self.nivel_dificultad}")

    def volver_al_menu(self):
        self.master.destroy()
        root = tk.Tk()
        PantallaInicio(root, iniciar_juego)
        root.mainloop()

def iniciar_juego(modo):
    root = tk.Tk()
    JuegoVasos(root, modo)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    pantalla_inicio = PantallaInicio(root, iniciar_juego)
    root.mainloop()