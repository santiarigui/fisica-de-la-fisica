import tkinter as tk
from tkinter import ttk, messagebox
from fisica import SistemaFisico
from simulacion import Simulacion


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

root = tk.Tk()
root.title("Simulador de Física Mecánica")
root.geometry("1200x720")
root.resizable(False, False)


# ============================================================
# VARIABLES
# ============================================================

m1_var = tk.DoubleVar(value=5.0)
m2_var = tk.DoubleVar(value=8.0)

theta1_var = tk.DoubleVar(value=30.0)
theta2_var = tk.DoubleVar(value=30.0)

g_var = tk.DoubleVar(value=9.81)


# ============================================================
# ESTILO
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "Titulo.TLabel",
    font=("Arial", 20, "bold")
)

style.configure(
    "Subtitulo.TLabel",
    font=("Arial", 11, "bold")
)

style.configure(
    "Resultado.TLabel",
    font=("Arial", 10)
)

style.configure(
    "Boton.TButton",
    font=("Arial", 10, "bold"),
    padding=8
)


# ============================================================
# ESTRUCTURA
# ============================================================

contenedor = ttk.Frame(root)
contenedor.pack(fill="both", expand=True)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    contenedor,
    width=850,
    height=680,
    bg="white",
    highlightthickness=0
)

canvas.pack(side="left", padx=10, pady=10)


# ============================================================
# PANEL DERECHO
# ============================================================

panel = ttk.Frame(
    contenedor,
    width=300,
    padding=15
)

panel.pack(
    side="right",
    fill="y",
    padx=(0, 10),
    pady=10
)

panel.pack_propagate(False)


ttk.Label(
    panel,
    text="SIMULADOR",
    style="Titulo.TLabel"
).pack(pady=(5, 0))

ttk.Label(
    panel,
    text="Dos masas + polea",
    style="Subtitulo.TLabel"
).pack(pady=(0, 20))


# ============================================================
# FUNCIÓN PARA CREAR SLIDERS
# ============================================================

def crear_slider(parent, nombre, variable, minimo, maximo, unidad):

    marco = ttk.Frame(parent)
    marco.pack(fill="x", pady=8)

    encabezado = ttk.Frame(marco)
    encabezado.pack(fill="x")

    etiqueta = ttk.Label(
        encabezado,
        text=nombre,
        font=("Arial", 10, "bold")
    )

    etiqueta.pack(side="left")

    valor_label = ttk.Label(
        encabezado,
        text=f"{variable.get():.1f} {unidad}",
        font=("Arial", 10)
    )

    valor_label.pack(side="right")

    def actualizar(valor):

        valor = float(valor)
        variable.set(valor)

        if unidad == "°":
            valor_label.config(text=f"{valor:.0f} {unidad}")
        else:
            valor_label.config(text=f"{valor:.1f} {unidad}")

    slider = tk.Scale(
        marco,
        from_=minimo,
        to=maximo,
        orient="horizontal",
        variable=variable,
        resolution=0.1 if unidad != "°" else 1,
        showvalue=False,
        command=actualizar,
        length=250
    )

    slider.pack(fill="x")

    return slider


# ============================================================
# DATOS
# ============================================================

ttk.Label(
    panel,
    text="VARIABLES DEL SISTEMA",
    style="Subtitulo.TLabel"
).pack(anchor="w", pady=(0, 5))


crear_slider(
    panel,
    "Masa m₁",
    m1_var,
    0.5,
    20,
    "kg"
)

crear_slider(
    panel,
    "Masa m₂",
    m2_var,
    0.5,
    20,
    "kg"
)

crear_slider(
    panel,
    "Ángulo θ₁",
    theta1_var,
    5,
    75,
    "°"
)

crear_slider(
    panel,
    "Ángulo θ₂",
    theta2_var,
    5,
    75,
    "°"
)


# ============================================================
# GRAVEDAD
# ============================================================

marco_g = ttk.Frame(panel)
marco_g.pack(fill="x", pady=(5, 10))

ttk.Label(
    marco_g,
    text="Gravedad g",
    font=("Arial", 10, "bold")
).pack(side="left")

ttk.Label(
    marco_g,
    text="9.81 m/s²"
).pack(side="right")


# ============================================================
# SISTEMA FÍSICO
# ============================================================

sistema_actual = None


def obtener_sistema():

    try:

        sistema = SistemaFisico(
            m1_var.get(),
            m2_var.get(),
            theta1_var.get(),
            theta2_var.get(),
            g_var.get()
        )

        return sistema

    except ValueError as error:

        messagebox.showerror(
            "Datos inválidos",
            str(error)
        )

        return None


# ============================================================
# SIMULACIÓN
# ============================================================

simulacion = Simulacion(canvas)


def calcular():

    global sistema_actual

    sistema = obtener_sistema()

    if sistema is None:
        return

    sistema_actual = sistema

    simulacion.establecer_sistema(sistema)

    resultados = sistema.resultados()

    resultado_a.config(
        text=f"Aceleración\n{resultados['aceleracion']:.2f} m/s²"
    )

    resultado_t.config(
        text=f"Tensión\n{resultados['tension']:.2f} N"
    )

    resultado_f1.config(
        text=f"m₁g sin(θ₁)\n{resultados['paralelo1']:.2f} N"
    )

    resultado_f2.config(
        text=f"m₂g sin(θ₂)\n{resultados['paralelo2']:.2f} N"
    )

    resultado_n1.config(
        text=f"N₁\n{resultados['normal1']:.2f} N"
    )

    resultado_n2.config(
        text=f"N₂\n{resultados['normal2']:.2f} N"
    )

    resultado_dir.config(
        text=resultados["direccion"]
    )


def iniciar():

    calcular()

    if sistema_actual is not None:
        simulacion.iniciar()


def detener():

    simulacion.detener()


def reiniciar():

    simulacion.reiniciar()


# ============================================================
# BOTONES
# ============================================================

ttk.Button(
    panel,
    text="CALCULAR",
    style="Boton.TButton",
    command=calcular
).pack(fill="x", pady=(5, 5))


ttk.Button(
    panel,
    text="▶  SIMULAR",
    style="Boton.TButton",
    command=iniciar
).pack(fill="x", pady=5)


ttk.Button(
    panel,
    text="■  DETENER",
    style="Boton.TButton",
    command=detener
).pack(fill="x", pady=5)


ttk.Button(
    panel,
    text="↻  REINICIAR",
    style="Boton.TButton",
    command=reiniciar
).pack(fill="x", pady=5)


# ============================================================
# RESULTADOS
# ============================================================

ttk.Separator(
    panel,
    orient="horizontal"
).pack(
    fill="x",
    pady=15
)


ttk.Label(
    panel,
    text="RESULTADOS",
    style="Subtitulo.TLabel"
).pack(anchor="w")


resultado_a = ttk.Label(
    panel,
    text="Aceleración\n--",
    style="Resultado.TLabel"
)

resultado_a.pack(anchor="w", pady=5)


resultado_t = ttk.Label(
    panel,
    text="Tensión\n--",
    style="Resultado.TLabel"
)

resultado_t.pack(anchor="w", pady=5)


resultado_f1 = ttk.Label(
    panel,
    text="m₁g sin(θ₁)\n--",
    style="Resultado.TLabel"
)

resultado_f1.pack(anchor="w", pady=3)


resultado_f2 = ttk.Label(
    panel,
    text="m₂g sin(θ₂)\n--",
    style="Resultado.TLabel"
)

resultado_f2.pack(anchor="w", pady=3)


resultado_n1 = ttk.Label(
    panel,
    text="N₁\n--",
    style="Resultado.TLabel"
)

resultado_n1.pack(anchor="w", pady=3)


resultado_n2 = ttk.Label(
    panel,
    text="N₂\n--",
    style="Resultado.TLabel"
)

resultado_n2.pack(anchor="w", pady=3)


resultado_dir = ttk.Label(
    panel,
    text="Dirección\n--",
    style="Resultado.TLabel",
    wraplength=250
)

resultado_dir.pack(anchor="w", pady=8)


# ============================================================
# INICIAR
# ============================================================

sistema_inicial = obtener_sistema()

if sistema_inicial:
    simulacion.establecer_sistema(sistema_inicial)

    resultado_a.config(
        text=f"Aceleración\n{sistema_inicial.resultados()['aceleracion']:.2f} m/s²"
    )

root.mainloop()