import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def configurar_teclado_rapido(widget, funcion_enter=None, funcion_escape=None):
    if funcion_enter:
        widget.bind("<Return>", lambda e: funcion_enter())
    if funcion_escape:
        widget.bind("<Escape>", lambda e: funcion_escape())

def crear_fondo(ventana, ancho, alto):
    ruta_base = os.path.dirname(__file__)
    ruta_fondo = os.path.join(ruta_base, "imagenPrueba.png")

    if not os.path.exists(ruta_fondo):
        messagebox.showerror("Error", "No se encontró la imagen: " + ruta_fondo)
        ventana.destroy()
        return None
    fondo = Image.open(ruta_fondo)
    fondo = fondo.resize((ancho, alto), Image.Resampling.LANCZOS)
    fondo_tk = ImageTk.PhotoImage(fondo)

    lienzo = tk.Canvas(ventana, width=ancho, height=alto, highlightthickness=0)
    lienzo.pack(fill="both", expand=True)
    lienzo.create_image(0, 0, image=fondo_tk, anchor="nw")
    lienzo.imagen_fondo = fondo_tk
    return lienzo

def abrir_panel_principal(nombre):
    ventana = tk.Tk()
    ventana.title("Panel Principal")
    ventana.attributes('-fullscreen', True)

    ancho = ventana.winfo_screenwidth()
    alto = ventana.winfo_screenheight()

    lienzo = crear_fondo(ventana, ancho, alto)
    if lienzo is None:
        return

    lienzo.create_text(
        ancho // 2, 120,
        text=f"Bienvenido, {nombre}",
        font=("Arial", 24, "bold"),
        fill="black"
    )
    boton_calculadora = tk.Button(
        ventana,
        text="Calculadora Eléctrica",
        command=lambda: ventana_menu_calculadora(ventana),
        bg="#2196F3",
        fg="white",
        font=("Arial", 14),
        width=25
    )
    lienzo.create_window(ancho // 2, 160, window=boton_calculadora)

    def mostrar_bienvenida():
        messagebox.showinfo("Bienvenid@", f"¡Hola, {nombre}! Bienvenido al sistema.")

    boton_prueba = tk.Button(
        ventana,
        text="Boton 2",
        command=mostrar_bienvenida,
        bg="#2196F3",
        fg="white",
        font=("Arial", 14),
        width=25
    )
    lienzo.create_window(ancho // 2, 200, window=boton_prueba)

    boton_salir = tk.Button(
        ventana,
        text="Cerrar Sesión",
        command=ventana.destroy,
        bg="red",
        fg="white",
        font=("Arial", 12),
        width=25
    )
    lienzo.create_window(ancho // 2, 240, window=boton_salir)

    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    ventana.mainloop()


def ventana_ingreso_nombre():
    global ventana_inicio, entrada_nombre

    ventana_inicio = tk.Tk()
    ventana_inicio.title("Bienvenid@")
    ventana_inicio.attributes('-fullscreen', True)

    ancho = ventana_inicio.winfo_screenwidth()
    alto = ventana_inicio.winfo_screenheight()

    lienzo = crear_fondo(ventana_inicio, ancho, alto)
    if lienzo is None:
        return

    lienzo.create_text(
        ancho // 2, alto // 2 - 100,
        text="Ingresa tu nombre",
        font=("Arial", 20, "bold"),
        fill="white"
             ""
    )

    lienzo.create_text(
        ancho // 2 - 150, alto // 2 - 40,
        text="Nombre:",
        font=("Arial", 14),
        fill="black"
    )

    entrada_nombre = tk.Entry(ventana_inicio, font=("Arial", 14), width=20)
    lienzo.create_window(ancho // 2 + 20, alto // 2 - 40, window=entrada_nombre)

    def continuar():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "Por favor ingresa tu nombre")
            entrada_nombre.focus()
            return
        ventana_inicio.destroy()
        abrir_panel_principal(nombre)

    boton_continuar = tk.Button(
        ventana_inicio,
        text="Continuar",
        command=continuar,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 14),
        width=20
    )

    lienzo.create_window(ancho // 2, alto // 2 + 20, window=boton_continuar)

    boton_salir = tk.Button(
        ventana_inicio,
        text="Salir",
        command=ventana_inicio.destroy,
        bg="red",
        fg="white",
        font=("Arial", 14),
        width=20
    )
    lienzo.create_window(ancho // 2, alto // 2 + 70, window=boton_salir)

    lienzo.create_text(
        ancho // 2, alto // 2 + 120,
        text="Usa ENTER para continuar, ESC para salir...",
        font=("Arial", 10),
        fill="white"
    )

    configurar_teclado_rapido(entrada_nombre, funcion_enter=continuar)
    configurar_teclado_rapido(ventana_inicio, funcion_escape=ventana_inicio.destroy)
    entrada_nombre.focus()

    ventana_inicio.mainloop()

def ventana_menu_calculadora(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Calculadora Eléctrica - Ley de Ohm")
    ventana.geometry("350x350")

    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    tk.Label(
        ventana,
        text="¿Qué deseas calcular?",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        ventana, text="Voltios (V)", font=("Arial", 12), width=22,
        command=lambda: ventana_calcular_valor(ventana, "V")
    ).pack(pady=8)

    tk.Button(
        ventana, text="Amperios (I)", font=("Arial", 12), width=22,
        command=lambda: ventana_calcular_valor(ventana, "I")
    ).pack(pady=8)

    tk.Button(
        ventana, text="Ohmios (R)", font=("Arial", 12), width=22,
        command=lambda: ventana_calcular_valor(ventana, "R")
    ).pack(pady=8)

    tk.Button(
        ventana, text="Watios (P)", font=("Arial", 12), width=22,
        command=lambda: ventana_calcular_valor(ventana, "P")
    ).pack(pady=8)

    tk.Button(
        ventana, text="Cerrar", font=("Arial", 12), width=22,
        command=ventana.destroy
    ).pack(pady=20)


def ventana_calcular_valor(padre, objetivo):

    formulas = {
        "V": {
            frozenset({"I", "R"}): ("V = I x R", lambda v: v["I"] * v["R"]),
            frozenset({"I", "P"}): ("V = P / I", lambda v: v["P"] / v["I"]),
            frozenset({"R", "P"}):   ("V = √(P x R)", lambda v: (v["P"] * v["R"]) ** 0.5),
        },
        "I": {
            frozenset({"V", "R"}): ("I = V / R", lambda v: v["V"] / v["R"]),
            frozenset({"V", "P"}): ("I = P / V", lambda v: v["P"] / v["V"]),
            frozenset({"R", "P"}): ("I = √(P / R)", lambda v: (v["P"] / v["R"]) ** 0.5),
        },
        "R": {
            frozenset({"V", "I"}): ("R = V / I", lambda v: v["V"] / v["I"]),
            frozenset({"V", "P"}): ("R = V² / P", lambda v: (v["V"] ** 2) / v["P"]),
            frozenset({"I", "P"}): ("R = P / I²", lambda v: v["P"] / (v["I"] ** 2)),
        },
        "P": {
            frozenset({"V", "I"}): ("P = V x I", lambda v: v["V"] * v["I"]),
            frozenset({"V", "R"}): ("P = V² / R", lambda v: (v["V"] ** 2) / v["R"]),
            frozenset({"I", "R"}): ("P = I² x R", lambda v: (v["I"] ** 2) * v["R"]),
        },
    }

    nombres = {"V": "Voltios (V)", "I": "Amperios (I)", "R": "Ohmios (R)", "P": "Watios (P)"}
    otras = [c for c in ("V", "I", "R", "P") if c != objetivo]

    ventana = tk.Toplevel(padre)
    ventana.title(f"Calcular {nombres[objetivo]}")
    ventana.geometry("500x400")
    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    tk.Label(
        ventana,
        text=f"Calcular {nombres[objetivo]}",
        font=("Arial", 16, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=15)

    tk.Label(
        ventana,
        text="Llena exactamente 2 de estos valores",
        font=("Arial", 9),
        fg="gray"
    ).grid(row=1, column=0, columnspan=2, pady=(0, 15))

    entradas = {}
    for i, clave in enumerate(otras):
        tk.Label(ventana, text=nombres[clave] + ":", font=("Arial", 12)).grid(
            row=i + 2, column=0, padx=10, pady=8, sticky="e"
        )
        entrada = tk.Entry(ventana, font=("Arial", 12), width=18)
        entrada.grid(row=i + 2, column=1, padx=10, pady=8, sticky="w")
        entradas[clave] = entrada

    etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 13, "bold"), fg="#2E7D32")
    etiqueta_resultado.grid(row=5, column=0, columnspan=2, pady=10)

    def calcular():
        valores = {}
        for clave in otras:
            texto = entradas[clave].get().strip()
            if texto == "":
                continue
            try:
                valores[clave] = float(texto)
            except ValueError:
                messagebox.showwarning("Validación", f"El valor de {nombres[clave]} no es válido")
                return

        if len(valores) != 2:
            messagebox.showwarning(
                "Validación",
                "Debes llenar exactamente 2 valores"
            )
            return

        par = frozenset(valores.keys())
        if par not in formulas[objetivo]:
            messagebox.showwarning("Validación", "Combinación de valores no válida")
            return

        texto_formula, funcion = formulas[objetivo][par]
        try:
            resultado = funcion(valores)
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir entre cero")
            return

        etiqueta_resultado.config(
            text=f"{texto_formula}\n{nombres[objetivo]} = {resultado:.4f}"
        )

    def limpiar():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
        etiqueta_resultado.config(text="")
        entradas[otras[0]].focus()

    marco_botones = tk.Frame(ventana)
    marco_botones.grid(row=7, column=0, columnspan=2, pady=15)

    boton_calcular = tk.Button(
        marco_botones, text="Calcular", command=calcular,
        bg="#4CAF50", fg="white", font=("Arial", 12), width=12
    )
    boton_calcular.grid(row=0, column=0, padx=6)
    configurar_teclado_rapido(boton_calcular, funcion_enter=calcular)

    boton_limpiar = tk.Button(
        marco_botones, text="Limpiar", command=limpiar,
        bg="#FF9800", fg="white", font=("Arial", 12), width=12
    )
    boton_limpiar.grid(row=0, column=1, padx=6)

    entradas[otras[0]].focus()



if __name__ == "__main__":
    ventana_ingreso_nombre()