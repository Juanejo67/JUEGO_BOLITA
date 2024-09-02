import tkinter as tk
from ui import PantallaInicio, JuegoVasos

def iniciar_juego(modo):
    root.destroy()
    nueva_ventana = tk.Tk()
    JuegoVasos(nueva_ventana, modo)
    nueva_ventana.mainloop()

def main():
    global root
    root = tk.Tk()
    PantallaInicio(root, iniciar_juego)
    root.mainloop()

if __name__ == "__main__":
    main()