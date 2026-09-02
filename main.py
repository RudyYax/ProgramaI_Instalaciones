import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

AREA_CONDUCTOR_MM2 = {
    14: 9.24,
    12: 12.0,
    10: 16.1,
    8: 29.2,
    6: 48.0,
    4: 64.2,
    2: 87.8,
}

TUBERIA_CONDUIT = [
    ("1/2", 260),
    ("3/4", 438),
    ("1", 723),
    ("1 1/4", 1170),
    ("1 1/2", 1534),
    ("2", 2397),
    ("3", 5350),
]
CALIBRE_AWG_AREA_MM2 = [
    ("14", 2.082),
    ("12", 3.307),
    ("10", 5.260),
    ("8", 8.367),
    ("6", 13.300),
    ("4", 21.150),
    ("2", 33.620),
    ("1/0", 53.480),
    ("2/0", 67.430),
    ("3/0", 85.010),
    ("4/0", 107.200),

]
RESISTIVIDAD_MATERIAL = [
    ("Cobre", 0.0175),
    ("Aluminio", 0.0282),
]

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
        ancho // 2, 420,
        text=f"Bienvenido, {nombre}",
        font=("Arial", 24, "bold"),
        fill="white"
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
    lienzo.create_window(ancho // 2, 460, window=boton_calculadora)

    def mostrar_bienvenida():
        messagebox.showinfo("Bienvenid@", f"¡Hola, {nombre}! Bienvenido al sistema.")

    boton_prueba = tk.Button(
        ventana,
        text="Caida de tensión",
        command=lambda :ventana_caida_tension(ventana),
        bg="#2196F3",
        fg="white",
        font=("Arial", 14),
        width=25
    )
    lienzo.create_window(ancho // 2, 500, window=boton_prueba)


    boton_factor_relleno = tk.Button(
        ventana,
        text="Factor de Relleno (Tubería)",
        command=lambda: preguntar_cantidad_relleno(ventana),
        bg="#2196F3",
        fg="white",
        font=("Arial", 14),
        width=25
    )
    boton_salir = tk.Button(
        ventana,
        text="Cerrar Sesión",
        command=ventana.destroy,
        bg="red",
        fg="white",
        font=("Arial", 12),
        width=25
    )

    lienzo.create_window(ancho // 2, 540, window=boton_factor_relleno)
    lienzo.create_window(ancho // 2, 580, window=boton_salir)

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

def ventana_caida_tension(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Caída de Tensión")
    ventana.geometry("450x550")
    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    tk.Label(
        ventana,
        text="Calcular Caída de Tensión",
        font=("Arial", 16, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=15)

    tk.Label(ventana, text="ΔV = (p * L * I) / A", font=("Arial", 10), fg="gray").grid(row=1, column=0, columnspan=2)


    campos = {

        "longitud": "Longitud (m):",
        "corriente": "Corriente I (A):",
        "seccion": "Sección S (mm²):",
        "resistividad": "Resistividad ρ (Ω·mm²/m):",

    }
    tipo_circuito = tk.StringVar(value="derivado")

    tk.Label(
        ventana,
        text="Tipo de circuito:",
        font=("Arial", 11, "bold")
    ).grid(row=2, column=0, columnspan=2, pady=(0, 5))

    marco_tipo = tk.Frame(ventana)
    marco_tipo.grid(row=3, column=0, columnspan=2, pady=(0, 15))

    tk.Radiobutton(
        marco_tipo, text="Circuito derivado (3%)",
        variable=tipo_circuito, value="derivado",
        font=("Arial", 10)
    ).grid(row=0, column=0, padx=8)

    tk.Radiobutton(
        marco_tipo, text="Tablero principal a carga (5%)",
        variable=tipo_circuito, value="principal",
        font=("Arial", 10)
    ).grid(row=0, column=1, padx=8)

    opciones_seccion = [f"{area} mm² ({awg} AWG)" for awg, area in CALIBRE_AWG_AREA_MM2]
    variable_seccion = tk.StringVar(value=opciones_seccion[0])

    opciones_resistividad = [f"{valor} Ω·mm²/m ({material})" for material, valor in RESISTIVIDAD_MATERIAL]
    variable_resistividad = tk.StringVar(value=opciones_resistividad[0])

    entradas = {}
    for i, (clave, etiqueta) in enumerate(campos.items()):
        tk.Label(ventana, text=etiqueta, font=("Arial", 12)).grid(
            row=i + 4, column=0, padx=10, pady=8, sticky="e"
        )

        if clave == "seccion":
            entrada = ttk.Combobox(
                ventana,
                textvariable=variable_seccion,
                values=opciones_seccion,
                font=("Arial", 12),
                width=18,
                state="readonly"
            )
        elif clave == "resistividad":
            entrada = ttk.Combobox(
                ventana,
                textvariable=variable_resistividad,
                values=opciones_resistividad,
                font=("Arial", 12),
                width=18,
                state="readonly"
            )
        else:
            entrada = tk.Entry(ventana, font=("Arial", 12), width=18)

        entrada.grid(row=i + 4, column=1, padx=10, pady=8, sticky="w")
        entradas[clave] = entrada
    etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 13, "bold"), fg="#2E7D32")
    etiqueta_resultado.grid(row=8, column=0, columnspan=2, pady=10)
    resultado_valores = {}
    etiqueta_pregunta = tk.Label(
        ventana,
        text="¿Deseas calcular el porcentaje?",
        font=("Arial", 11, "bold")
    )

    marco_si_no = tk.Frame(ventana)

    boton_si = tk.Button(
        marco_si_no, text="Sí", command=lambda: abrir_ventana_porcentaje(ventana, resultado_valores, tipo_circuito.get()),
        bg="#4CAF50", fg="white", font=("Arial", 11), width=10
    )
    boton_si.grid(row=0, column=0, padx=6)

    boton_no = tk.Button(
        marco_si_no, text="No", command=lambda: (etiqueta_pregunta.grid_remove(), marco_si_no.grid_remove()),
        bg="#F44336", fg="white", font=("Arial", 11), width=10
    )
    boton_no.grid(row=0, column=1, padx=6)



    def calcular():
        valores = {}
        for clave in campos:
            texto = entradas[clave].get().strip()
            if texto == "":
                messagebox.showwarning("Validación", "Debes llenar todos los campos")
                return

            if clave == "seccion":
                valores[clave] = float(texto.split(" mm²")[0])
                continue

            if clave == "resistividad":
                valores[clave] = float(texto.split(" Ω")[0])
                continue

            try:
                valores[clave] = float(texto)
            except ValueError:
                messagebox.showwarning("Validación", f"El valor de {campos[clave]} no es válido")
                return
            try:
                valores[clave] = float(texto)
            except ValueError:
                messagebox.showwarning("Validación", f"El valor de {campos[clave]} no es válido")
                return

        if valores["seccion"] == 0:
            messagebox.showerror("Error", "La sección no puede ser cero")
            return
        caida = ((2*valores["longitud"])*valores["corriente"] * valores["resistividad"])/ valores["seccion"]


        resultado_valores["caida"] = caida

        etiqueta_resultado.config(
            text=f"Caída de tensión ≈ {caida:.4f} V"
        )

        etiqueta_pregunta.grid(row=9, column=0, columnspan=2, pady=(5, 0))
        marco_si_no.grid(row =10, column=0, columnspan=2, pady=(5, 10))


    def limpiar():
        for clave, entrada in entradas.items():
            if clave == "seccion":
                variable_seccion.set(opciones_seccion[0])
            elif clave == "resistividad":
                variable_resistividad.set(opciones_resistividad[0])
            else:
                entrada.delete(0, tk.END)
        etiqueta_resultado.config(text="")
        etiqueta_pregunta.grid_remove()
        marco_si_no.grid_remove()
        entradas["longitud"].focus()

    marco_botones = tk.Frame(ventana)
    marco_botones.grid(row=11, column=0, columnspan=2, pady=15)

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

    boton_cerrar = tk.Button(
        marco_botones, text="Cerrar", command=ventana.destroy,
        bg="#F44336", fg="white", font=("Arial", 12), width=12
    )
    boton_cerrar.grid(row=0, column=2, padx=6)

    entradas["longitud"].focus()

def abrir_ventana_porcentaje(padre, resultado_valores, tipo_circuito):
    if "caida" not in resultado_valores:
        messagebox.showwarning("Validación", "Primero calcula la caída de tensión")
        return

    limites = {"derivado": 3, "principal": 5}
    limite = limites[tipo_circuito]
    etiqueta_tipo = "Circuito derivado" if tipo_circuito == "derivado" else "Tablero principal a carga"

    ventana = tk.Toplevel(padre)
    ventana.title("Calcular Porcentaje")
    ventana.geometry("350x260")
    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    tk.Label(
        ventana, text=f"{etiqueta_tipo} (límite: {limite}%)",
        font=("Arial", 10), fg="gray"
    ).pack(pady=(15, 5))

    tk.Label(
        ventana, text="Tensión Nominal (V):", font=("Arial", 12)
    ).pack(pady=(10, 5))

    entrada_tension = tk.Entry(ventana, font=("Arial", 12), width=18)
    entrada_tension.pack()
    entrada_tension.focus()

    etiqueta_resultado_porcentaje = tk.Label(ventana, text="", font=("Arial", 13, "bold"), fg="#2E7D32")
    etiqueta_resultado_porcentaje.pack(pady=15)

    def calcular():
        texto_tension = entrada_tension.get().strip()
        if texto_tension == "":
            messagebox.showwarning("Validación", "Ingresa la tensión nominal")
            return
        try:
            tension_nominal = float(texto_tension)
            if tension_nominal == 0:
                raise ZeroDivisionError
        except ValueError:
            messagebox.showwarning("Validación", "El valor de tensión nominal no es válido")
            return
        except ZeroDivisionError:
            messagebox.showerror("Error", "La tensión nominal no puede ser cero")
            return

        porcentaje = (resultado_valores["caida"] / tension_nominal) * 100
        cumple = " Cumple con el porcentaje permitido :)" if porcentaje <= limite else "No cumple con el porcentaje permitido :("

        etiqueta_resultado_porcentaje.config(
            text=f"Porcentaje de caída ≈ {porcentaje:.2f} %\n{cumple}"
        )

    boton_calcular = tk.Button(
        ventana, text="Calcular", command=calcular,
        bg="#4CAF50", fg="white", font=("Arial", 12), width=14
    )
    boton_calcular.pack(pady=5)
    configurar_teclado_rapido(entrada_tension, funcion_enter=calcular)
    boton_cerrar = tk.Button(
        ventana, text="Cerrar", command=ventana.destroy,
        bg="#F44336", fg="white", font=("Arial", 12), width=14
    )
    boton_cerrar.pack(pady=5)
def preguntar_cantidad_relleno(padre):
    ventana = tk.Toplevel(padre)
    ventana.title("Factor de Relleno")
    ventana.geometry("350x200")
    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    tk.Label(
        ventana, text="¿Cuántos calibres distintos vas a utilizar?",
        font=("Arial", 12, "bold"), wraplength=300, justify="center"
    ).pack(pady=20)

    entrada_cantidad = tk.Entry(ventana, font=("Arial", 12), width=10, justify="center")
    entrada_cantidad.pack(pady=10)
    entrada_cantidad.focus()

    def continuar():
        texto = entrada_cantidad.get().strip()
        if texto == "":
            messagebox.showwarning("Validación", "Ingresa un número")
            return
        try:
            cantidad = int(texto)
        except ValueError:
            messagebox.showwarning("Validación", "Debe ser un número entero")
            return
        if cantidad <= 0:
            messagebox.showwarning("Validación", "La cantidad debe ser mayor a cero")
            return
        if cantidad > 12:
            messagebox.showwarning("Validación", "Máximo 12 calibres distintos")
            return
        ventana.destroy()
        ventana_factor_relleno(padre, cantidad)

    boton_continuar = tk.Button(
        ventana, text="Continuar", command=continuar,
        bg="#4CAF50", fg="white", font=("Arial", 12), width=14
    )
    boton_continuar.pack(pady=10)
    configurar_teclado_rapido(entrada_cantidad, funcion_enter=continuar)

def ventana_factor_relleno(padre, cantidad_calibres):
    ventana = tk.Toplevel(padre)
    ventana.title("Factor de Relleno - Tubería Conduit")

    alto = min(360 + cantidad_calibres * 35, 750)
    ventana.geometry(f"480x{alto}")
    configurar_teclado_rapido(ventana, funcion_escape=ventana.destroy)

    tk.Label(
        ventana,
        text="Factor de Relleno de Tubería Conduit",
        font=("Arial", 16, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=15)

    tk.Label(
        ventana,
        text="Fr = (Área conductores / Área tubo) x 100",
        font=("Arial", 10),
        fg="gray"
    ).grid(row=1, column=0, columnspan=2, pady=(0, 10))

    calibres_validos = sorted(AREA_CONDUCTOR_MM2.keys(), reverse=True)
    tk.Label(
        ventana,
        text=f"Calibres disponibles (AWG): {', '.join(str(c) for c in calibres_validos)}",
        font=("Arial", 9),
        fg="gray"
    ).grid(row=2, column=0, columnspan=2, pady=(0, 15))

    tk.Label(ventana, text="Calibre AWG", font=("Arial", 11, "bold")).grid(row=3, column=0, padx=10)
    tk.Label(ventana, text="Cantidad", font=("Arial", 11, "bold")).grid(row=3, column=1, padx=10)

    fila_inicio = 4
    filas = []
    for i in range(cantidad_calibres):
        entrada_calibre = tk.Entry(ventana, font=("Arial", 12), width=12)
        entrada_calibre.grid(row=fila_inicio + i, column=0, padx=10, pady=5)
        entrada_cantidad = tk.Entry(ventana, font=("Arial", 12), width=12)
        entrada_cantidad.grid(row=fila_inicio + i, column=1, padx=10, pady=5)
        filas.append((entrada_calibre, entrada_cantidad))

    fila_resultado = fila_inicio + cantidad_calibres
    etiqueta_resultado = tk.Label(
        ventana, text="", font=("Arial", 11), fg="#2E7D32", justify="left"
    )
    etiqueta_resultado.grid(row=fila_resultado, column=0, columnspan=2, pady=15)

    def calcular():
        area_total = 0.0
        num_total = 0

        for entrada_calibre, entrada_cantidad in filas:
            texto_cal = entrada_calibre.get().strip()
            texto_cant = entrada_cantidad.get().strip()

            if texto_cal == "" and texto_cant == "":
                continue
            if texto_cal == "" or texto_cant == "":
                messagebox.showwarning("Validación", "Completa calibre y cantidad en cada fila que uses")
                return
            try:
                calibre = int(texto_cal)
                cantidad = int(texto_cant)
            except ValueError:
                messagebox.showwarning("Validación", "Calibre y cantidad deben ser números enteros")
                return

            if calibre not in AREA_CONDUCTOR_MM2:
                messagebox.showwarning(
                    "Validación",
                    f"El calibre {calibre} no está en la tabla.\nUsa uno de: {calibres_validos}"
                )
                return
            if cantidad <= 0:
                messagebox.showwarning("Validación", "La cantidad debe ser mayor a cero")
                return

            area_total += AREA_CONDUCTOR_MM2[calibre] * cantidad
            num_total += cantidad

        if num_total == 0:
            messagebox.showwarning("Validación", "Ingresa al menos un conductor")
            return

        if num_total == 1:
            fr_limite = 0.55
        elif num_total == 2:
            fr_limite = 0.30
        else:
            fr_limite = 0.40

        area_minima_tubo = area_total / fr_limite

        diametro_elegido = None
        for diametro, area_interna in TUBERIA_CONDUIT:
            if area_interna >= area_minima_tubo:
                diametro_elegido = (diametro, area_interna)
                break

        texto = (
            f"Número total de conductores: {num_total}\n"
            f"Área total de conductores (Ac): {area_total:.2f} mm²\n"
            f"Factor de relleno permitido: {fr_limite * 100:.0f} %\n"
            f"Área mínima requerida del tubo: {area_minima_tubo:.2f} mm²\n"
        )

        if diametro_elegido:
            texto += (
                f" Diámetro de tubería recomendado: {diametro_elegido[0]}\" "
                f"(área interna {diametro_elegido[1]} mm²)"
            )
        else:
            texto += "⚠ Ningún diámetro de la tabla alcanza; se necesita tubería mayor a 3\""

        etiqueta_resultado.config(text=texto)

    def limpiar():
        for entrada_calibre, entrada_cantidad in filas:
            entrada_calibre.delete(0, tk.END)
            entrada_cantidad.delete(0, tk.END)
        etiqueta_resultado.config(text="")
        filas[0][0].focus()

    fila_botones = fila_resultado + 1
    marco_botones = tk.Frame(ventana)
    marco_botones.grid(row=fila_botones, column=0, columnspan=2, pady=10)

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

    boton_cerrar = tk.Button(
        marco_botones, text="Cerrar", command=ventana.destroy,
        bg="#F44336", fg="white", font=("Arial", 12), width=12
    )
    boton_cerrar.grid(row=0, column=2, padx=6)

    filas[0][0].focus()


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