import math


class Simulacion:

    def __init__(self, canvas):

        self.canvas = canvas
        self.sistema = None

        self.tiempo = 0.0
        self.animando = False

        self.dt = 0.03

        # Escala física → píxeles
        self.escala = 65

    # ==========================================================
    # ESTABLECER SISTEMA
    # ==========================================================

    def establecer_sistema(self, sistema):

        self.sistema = sistema
        self.tiempo = 0.0
        self.animando = False

        self.dibujar()

    # ==========================================================
    # DIBUJAR SISTEMA COMPLETO
    # ==========================================================

    def dibujar(self):

        self.canvas.delete("all")

        if self.sistema is None:
            return

        # ------------------------------------------------------
        # CENTRO DE LA POLEA
        # ------------------------------------------------------

        cx = 425
        cy = 145

        radio = 32

        # ------------------------------------------------------
        # ÁNGULOS
        # ------------------------------------------------------

        theta1 = math.radians(self.sistema.theta1)
        theta2 = math.radians(self.sistema.theta2)

        # ------------------------------------------------------
        # LONGITUD DE LOS PLANOS
        # ------------------------------------------------------

        L1 = 390
        L2 = 390

        # ------------------------------------------------------
        # EXTREMOS DE LOS PLANOS
        # ------------------------------------------------------

        izquierda_x = cx - L1 * math.cos(theta1)
        izquierda_y = cy + L1 * math.sin(theta1)

        derecha_x = cx + L2 * math.cos(theta2)
        derecha_y = cy + L2 * math.sin(theta2)

        # ------------------------------------------------------
        # SUELO
        # ------------------------------------------------------

        suelo_y = 560

        self.canvas.create_line(
            45,
            suelo_y,
            805,
            suelo_y,
            width=4
        )

        # ------------------------------------------------------
        # PLANOS INCLINADOS
        # ------------------------------------------------------

        self.canvas.create_line(
            izquierda_x,
            izquierda_y,
            cx,
            cy,
            width=7
        )

        self.canvas.create_line(
            cx,
            cy,
            derecha_x,
            derecha_y,
            width=7
        )

        # ------------------------------------------------------
        # POLEA
        # ------------------------------------------------------

        self.canvas.create_oval(
            cx - radio,
            cy - radio,
            cx + radio,
            cy + radio,
            width=4
        )

        self.canvas.create_oval(
            cx - 6,
            cy - 6,
            cx + 6,
            cy + 6,
            fill="black"
        )

        # ------------------------------------------------------
        # TRIÁNGULOS / REFERENCIA DE LOS ÁNGULOS
        # ------------------------------------------------------

        self.dibujar_angulo(
            izquierda_x,
            suelo_y,
            theta1,
            izquierda=True
        )

        self.dibujar_angulo(
            derecha_x,
            suelo_y,
            theta2,
            izquierda=False
        )

        # ------------------------------------------------------
        # VECTORES UNITARIOS
        # ------------------------------------------------------

        # m1: dirección desde la masa hacia abajo-izquierda
        u1x = -math.cos(theta1)
        u1y = math.sin(theta1)

        # m2: dirección desde la masa hacia abajo-derecha
        u2x = math.cos(theta2)
        u2y = math.sin(theta2)

        # ------------------------------------------------------
        # POSICIÓN INICIAL
        # ------------------------------------------------------

        distancia = 230

        x1_base = cx + u1x * distancia
        y1_base = cy + u1y * distancia

        x2_base = cx + u2x * distancia
        y2_base = cy + u2y * distancia

        # ------------------------------------------------------
        # DESPLAZAMIENTO
        # ------------------------------------------------------

        desplazamiento = self.sistema.posicion(
            self.tiempo
        )

        desplazamiento_px = (
            desplazamiento * self.escala
        )

        # ------------------------------------------------------
        # POSICIÓN m1
        # ------------------------------------------------------

        x1 = (
            x1_base
            - desplazamiento_px * u1x
        )

        y1 = (
            y1_base
            - desplazamiento_px * u1y
        )

        # ------------------------------------------------------
        # POSICIÓN m2
        # ------------------------------------------------------

        x2 = (
            x2_base
            + desplazamiento_px * u2x
        )

        y2 = (
            y2_base
            + desplazamiento_px * u2y
        )

        # ------------------------------------------------------
        # CUERDA
        # ------------------------------------------------------

        self.canvas.create_line(
            x1,
            y1,
            cx,
            cy,
            width=4
        )

        self.canvas.create_line(
            cx,
            cy,
            x2,
            y2,
            width=4
        )

        # ------------------------------------------------------
        # MASAS
        # ------------------------------------------------------

        tamaño = 52

        # m1

        self.canvas.create_rectangle(
            x1 - tamaño / 2,
            y1 - tamaño / 2,
            x1 + tamaño / 2,
            y1 + tamaño / 2,
            fill="lightblue",
            outline="black",
            width=3
        )

        self.canvas.create_text(
            x1,
            y1,
            text="m₁",
            font=("Arial", 17, "bold")
        )

        # m2

        self.canvas.create_rectangle(
            x2 - tamaño / 2,
            y2 - tamaño / 2,
            x2 + tamaño / 2,
            y2 + tamaño / 2,
            fill="lightgreen",
            outline="black",
            width=3
        )

        self.canvas.create_text(
            x2,
            y2,
            text="m₂",
            font=("Arial", 17, "bold")
        )

        # ------------------------------------------------------
        # FUERZAS m1
        # ------------------------------------------------------

        self.dibujar_fuerzas(
            x1,
            y1,
            theta1,
            self.sistema.m1,
            True
        )

        # ------------------------------------------------------
        # FUERZAS m2
        # ------------------------------------------------------

        self.dibujar_fuerzas(
            x2,
            y2,
            theta2,
            self.sistema.m2,
            False
        )

        # ------------------------------------------------------
        # TÍTULO
        # ------------------------------------------------------

        self.canvas.create_text(
            425,
            35,
            text="SISTEMA DE DOS MASAS Y POLEA",
            font=("Arial", 21, "bold")
        )

        self.canvas.create_text(
            425,
            67,
            text="Planos inclinados • cuerda tensa • polea ideal",
            font=("Arial", 11)
        )

        # ------------------------------------------------------
        # INFORMACIÓN INFERIOR
        # ------------------------------------------------------

        velocidad = self.sistema.velocidad(
            self.tiempo
        )

        self.canvas.create_text(
            425,
            590,
            text=f"Tiempo: {self.tiempo:.2f} s",
            font=("Arial", 11)
        )

        self.canvas.create_text(
            425,
            612,
            text=f"Velocidad: {velocidad:.2f} m/s",
            font=("Arial", 11)
        )

        self.canvas.create_text(
            425,
            634,
            text=f"Aceleración: {self.sistema.aceleracion:.2f} m/s²",
            font=("Arial", 11, "bold")
        )

        self.canvas.create_text(
            425,
            658,
            text=self.sistema.direccion,
            font=("Arial", 11, "bold")
        )

        # ------------------------------------------------------
        # LEYENDA
        # ------------------------------------------------------

        self.dibujar_leyenda()

    # ==========================================================
    # ÁNGULOS Y TRIÁNGULOS
    # ==========================================================

    def dibujar_angulo(
        self,
        x,
        y,
        theta,
        izquierda
    ):

        radio = 55

        if izquierda:

            # Línea horizontal
            self.canvas.create_line(
                x,
                y,
                x + 65,
                y,
                width=2
            )

            # Arco
            self.canvas.create_arc(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                start=0,
                extent=-math.degrees(theta),
                style="arc",
                width=2
            )

            texto_x = x + 70

        else:

            self.canvas.create_line(
                x,
                y,
                x - 65,
                y,
                width=2
            )

            self.canvas.create_arc(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                start=180,
                extent=math.degrees(theta),
                style="arc",
                width=2
            )

            texto_x = x - 70

        nombre = (
            f"θ₁ = {self.sistema.theta1:.0f}°"
            if izquierda
            else
            f"θ₂ = {self.sistema.theta2:.0f}°"
        )

        self.canvas.create_text(
            texto_x,
            y - 20,
            text=nombre,
            font=("Arial", 11, "bold")
        )

    # ==========================================================
    # FUERZAS
    # ==========================================================

    def dibujar_fuerzas(
        self,
        x,
        y,
        theta,
        masa,
        izquierda
    ):

        # ------------------------------------------------------
        # ESCALA VISUAL
        # ------------------------------------------------------

        L = 70

        # ------------------------------------------------------
        # PESO
        # ------------------------------------------------------

        self.flecha(
            x,
            y,
            x,
            y + L,
            "mg",
            "blue"
        )

        # ------------------------------------------------------
        # NORMAL
        # ------------------------------------------------------

        if izquierda:

            nx = math.sin(theta)
            ny = -math.cos(theta)

        else:

            nx = -math.sin(theta)
            ny = -math.cos(theta)

        self.flecha(
            x,
            y,
            x + nx * L,
            y + ny * L,
            "N",
            "green"
        )

        # ------------------------------------------------------
        # TENSIÓN
        # ------------------------------------------------------

        if izquierda:

            tx = math.cos(theta)
            ty = -math.sin(theta)

        else:

            tx = -math.cos(theta)
            ty = -math.sin(theta)

        self.flecha(
            x,
            y,
            x + tx * L,
            y + ty * L,
            "T",
            "red"
        )

        # ------------------------------------------------------
        # COMPONENTE PARALELA
        # ------------------------------------------------------

        if izquierda:

            px = math.cos(theta)
            py = -math.sin(theta)

        else:

            px = math.cos(theta)
            py = math.sin(theta)

        nombre = (
            "m₁g sin θ₁"
            if izquierda
            else
            "m₂g sin θ₂"
        )

        self.flecha(
            x,
            y,
            x + px * 55,
            y + py * 55,
            nombre,
            "orange"
        )

        # ------------------------------------------------------
        # COMPONENTE PERPENDICULAR
        # ------------------------------------------------------

        if izquierda:

            qx = math.sin(theta)
            qy = math.cos(theta)

        else:

            qx = -math.sin(theta)
            qy = math.cos(theta)

        nombre2 = (
            "m₁g cos θ₁"
            if izquierda
            else
            "m₂g cos θ₂"
        )

        self.flecha(
            x,
            y,
            x + qx * 50,
            y + qy * 50,
            nombre2,
            "purple"
        )

    # ==========================================================
    # DIBUJAR FLECHA
    # ==========================================================

    def flecha(
        self,
        x1,
        y1,
        x2,
        y2,
        texto,
        color
    ):

        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            width=3,
            arrow="last"
        )

        self.canvas.create_text(
            x2,
            y2 - 10,
            text=texto,
            fill=color,
            font=("Arial", 9, "bold")
        )

    # ==========================================================
    # LEYENDA
    # ==========================================================

    def dibujar_leyenda(self):

        x = 690
        y = 105

        self.canvas.create_text(
            x,
            y,
            text="FUERZAS",
            font=("Arial", 11, "bold")
        )

        elementos = [
            ("T", "Tensión"),
            ("mg", "Peso"),
            ("N", "Normal"),
            ("mg sin θ", "Componente paralela"),
            ("mg cos θ", "Componente perpendicular")
        ]

        colores = [
            "red",
            "blue",
            "green",
            "orange",
            "purple"
        ]

        for i, ((simbolo, nombre), color) in enumerate(
            zip(elementos, colores)
        ):

            yy = y + 25 + i * 22

            self.canvas.create_line(
                x - 65,
                yy,
                x - 30,
                yy,
                fill=color,
                width=3,
                arrow="last"
            )

            self.canvas.create_text(
                x - 20,
                yy,
                text=f"{simbolo} = {nombre}",
                anchor="w",
                font=("Arial", 8)
            )

    # ==========================================================
    # INICIAR
    # ==========================================================

    def iniciar(self):

        if self.sistema is None:
            return

        if self.animando:
            return

        self.animando = True

        self.animar()

    # ==========================================================
    # ANIMACIÓN
    # ==========================================================

    def animar(self):

        if not self.animando:
            return

        self.tiempo += self.dt

        desplazamiento = abs(
            self.sistema.posicion(
                self.tiempo
            )
        )

        if desplazamiento >= 2.5:

            self.animando = False

        self.dibujar()

        if self.animando:

            self.canvas.after(
                30,
                self.animar
            )

    # ==========================================================
    # DETENER
    # ==========================================================

    def detener(self):

        self.animando = False

    # ==========================================================
    # REINICIAR
    # ==========================================================

    def reiniciar(self):

        self.animando = False

        self.tiempo = 0.0

        self.dibujar()