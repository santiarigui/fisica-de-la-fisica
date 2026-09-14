import tkinter as tk
from tkinter import ttk
import math


# ============================================================
# CONFIGURACIÓN DE LA VENTANA
# ============================================================

VENTANA_ANCHO = 1000
VENTANA_ALTO = 700

root = .Tk()
root.title("Simulador de Física Mecánica - Dos masas")
root.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}")
root.resizable(False, False)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    root,
    width=VENTANA_ANCHO,
    height=VENTANA_ALTO,
    bg="white"
)

canvas.pack(side="left", padx=10, pady=10)


# ============================================================
# PANEL DE DATOS
# ============================================================

panel = ttk.Frame(root, padding=15)
panel.pack(side="right", fill="y")


ttk.Label(
    panel,
    text="SIMULADOR\nDOS MASAS",
    font=("Arial", 16, "bold")
).pack(pady=10)


# -----------------------------
# Variables de entrada
# -----------------------------

m1_var = tk.StringVar(value="5")
m2_var = tk.StringVar(value="8")

theta1_var = tk.StringVar(value="30")
theta2_var = tk.StringVar(value="30")

g_var = tk.StringVar(value="9.81")


def crear_entrada(texto, variable):
    ttk.Label(
        panel,
        text=texto
    ).pack(anchor="w", pady=(10, 2))

    ttk.Entry(
        panel,
        textvariable=variable,
        width=15
    ).pack()


crear_entrada("Masa m₁ (kg)", m1_var)
crear_entrada("Masa m₂ (kg)", m2_var)

crear_entrada("Ángulo θ₁ (°)", theta1_var)
crear_entrada("Ángulo θ₂ (°)", theta2_var)

crear_entrada("Gravedad g (m/s²)", g_var)


# ============================================================
# VARIABLES DE LA SIMULACIÓN
# ============================================================

a = 0
t = 0

posicion = 0

movimiento = 0
animando = False


# ============================================================
# DIBUJAR EL SISTEMA
# ============================================================

def dibujar_sistema(pos=0):

    canvas.delete("all")

    # --------------------------------------------------------
    # Centro de la polea
    # --------------------------------------------------------

    cx = 500
    cy = 150

    radio_polea = 30

    # --------------------------------------------------------
    # Planos inclinados
    # --------------------------------------------------------

    izquierda_x = 180
    izquierda_y = 500

    derecha_x = 820
    derecha_y = 500

    # Plano izquierdo
    canvas.create_line(
        izquierda_x,
        izquierda_y,
        cx,
        cy,
        width=6
    )

    # Plano derecho
    canvas.create_line(
        cx,
        cy,
        derecha_x,
        derecha_y,
        width=6
    )

    # Suelo
    canvas.create_line(
        100,
        500,
        900,
        500,
        width=4
    )

    # --------------------------------------------------------
    # Polea
    # --------------------------------------------------------

    canvas.create_oval(
        cx - radio_polea,
        cy - radio_polea,
        cx + radio_polea,
        cy + radio_polea,
        width=4
    )

    canvas.create_oval(
        cx - 5,
        cy - 5,
        cx + 5,
        cy + 5,
        fill="black"
    )

    # --------------------------------------------------------
    # Posiciones de los bloques
    # --------------------------------------------------------

    # Movimiento máximo permitido
    max_pos = 120

    p = max(-max_pos, min(max_pos, pos))

    # Bloque izquierdo
    x1 = 320 + p
    y1 = 380 - p * 0.60

    # Bloque derecho
    x2 = 680 + p
    y2 = 380 + p * 0.60

    tamaño = 45

    # --------------------------------------------------------
    # Bloque m1
    # --------------------------------------------------------

    canvas.create_rectangle(
        x1 - tamaño / 2,
        y1 - tamaño / 2,
        x1 + tamaño / 2,
        y1 + tamaño / 2,
        fill="lightblue",
        outline="black",
        width=3
    )

    canvas.create_text(
        x1,
        y1,
        text="m₁",
        font=("Arial", 16, "bold")
    )

    # --------------------------------------------------------
    # Bloque m2
    # --------------------------------------------------------

    canvas.create_rectangle(
        x2 - tamaño / 2,
        y2 - tamaño / 2,
        x2 + tamaño / 2,
        y2 + tamaño / 2,
        fill="lightgreen",
        outline="black",
        width=3
    )

    canvas.create_text(
        x2,
        y2,
        text="m₂",
        font=("Arial", 16, "bold")
    )

    # --------------------------------------------------------
    # Cuerda
    # --------------------------------------------------------

    canvas.create_line(
        x1 + 20,
        y1 - 15,
        cx - 20,
        cy + 15,
        width=3
    )

    canvas.create_line(
        cx + 20,
        cy + 15,
        x2 - 20,
        y2 - 15,
        width=3
    )

    # --------------------------------------------------------
    # Ángulos
    # --------------------------------------------------------

    canvas.create_text(
        250,
        455,
        text="θ₁",
        font=("Arial", 15, "bold")
    )

    canvas.create_text(
        750,
        455,
        text="θ₂",
        font=("Arial", 15, "bold")
    )

    # --------------------------------------------------------
    # Título
    # --------------------------------------------------------

    canvas.create_text(
        500,
        50,
        text="Sistema de dos masas y polea",
        font=("Arial", 22, "bold")
    )


# ============================================================
# CÁLCULOS FÍSICOS
# ============================================================

def calcular():

    global a
    global movimiento

    try:

        m1 = float(m1_var.get())
        m2 = float(m2_var.get())

        theta1 = float(theta1_var.get())
        theta2 = float(theta2_var.get())

        g = float(g_var.get())

        # Convertir grados a radianes
        th1 = math.radians(theta1)
        th2 = math.radians(theta2)

        # ----------------------------------------------------
        # Componentes del peso paralelas al plano
        # ----------------------------------------------------

        f1 = m1 * g * math.sin(th1)
        f2 = m2 * g * math.sin(th2)

        # ----------------------------------------------------
        # Fuerza neta del sistema
        # ----------------------------------------------------

        fuerza_neta = f2 - f1

        # ----------------------------------------------------
        # Aceleración
        # ----------------------------------------------------

        a = fuerza_neta / (m1 + m2)

        # ----------------------------------------------------
        # Tensión
        # ----------------------------------------------------

        if a >= 0:

            # m2 baja y m1 sube
            tension = m1 * (g * math.sin(th1) + a)

            direccion = "m₂ baja → m₁ sube"

        else:

            # m1 baja y m2 sube
            tension = m2 * (g * math.sin(th2) - abs(a))

            direccion = "m₁ baja → m₂ sube"

        # ----------------------------------------------------
        # Mostrar resultados
        # ----------------------------------------------------

        resultado_a.config(
            text=f"Aceleración: {abs(a):.2f} m/s²"
        )

        resultado_t.config(
            text=f"Tensión: {tension:.2f} N"
        )

        resultado_f1.config(
            text=f"m₁g sin(θ₁): {f1:.2f} N"
        )

        resultado_f2.config(
            text=f"m₂g sin(θ₂): {f2:.2f} N"
        )

        resultado_dir.config(
            text=direccion
        )

        # Reiniciar posición
        movimiento = 0

        dibujar_sistema(movimiento)

    except ValueError:

        resultado_dir.config(
            text="Error: revisa los datos"
        )


# ============================================================
# ANIMACIÓN
# ============================================================

def animar():

    global movimiento
    global animando

    if not animando:
        return

    # Velocidad visual
    velocidad_visual = abs(a) * 2

    if a > 0:

        movimiento += velocidad_visual

    elif a < 0:

        movimiento -= velocidad_visual

    else:

        animando = False

    # Limitar movimiento
    if movimiento > 120:
        movimiento = 120
        animando = False

    if movimiento < -120:
        movimiento = -120
        animando = False

    dibujar_sistema(movimiento)

    if animando:
        root.after(30, animar)


def iniciar_simulacion():

    global animando

    calcular()

    animando = True

    animar()


def detener():

    global animando

    animando = False


# ============================================================
# BOTONES
# ============================================================

ttk.Button(
    panel,
    text="CALCULAR",
    command=calcular
).pack(fill="x", pady=(25, 5))


ttk.Button(
    panel,
    text="▶ SIMULAR",
    command=iniciar_simulacion
).pack(fill="x", pady=5)


ttk.Button(
    panel,
    text="■ DETENER",
    command=detener
).pack(fill="x", pady=5)


# ============================================================
# RESULTADOS
# ============================================================

ttk.Separator(
    panel,
    orient="horizontal"
).pack(fill="x", pady=20)


ttk.Label(
    panel,
    text="RESULTADOS",
    font=("Arial", 12, "bold")
).pack()


resultado_a = ttk.Label(
    panel,
    text="Aceleración: --"
)

resultado_a.pack(pady=5)


resultado_t = ttk.Label(
    panel,
    text="Tensión: --"
)

resultado_t.pack(pady=5)


resultado_f1 = ttk.Label(
    panel,
    text="m₁g sin(θ₁): --"
)

resultado_f1.pack(pady=5)


resultado_f2 = ttk.Label(
    panel,
    text="m₂g sin(θ₂): --"
)

resultado_f2.pack(pady=5)


resultado_dir = ttk.Label(
    panel,
    text="Dirección: --",
    wraplength=180
)

resultado_dir.pack(pady=10)


# ============================================================
# INICIAR
# ============================================================

dibujar_sistema()

root.mainloop()