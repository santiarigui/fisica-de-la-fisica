import math


class Simulacion:
    """
    Se encarga de dibujar y animar el sistema físico.

    El cálculo de la física se realiza en fisica.py.
    Aquí solamente usamos esos resultados para representar
    visualmente el movimiento.
    """

    def __init__(self, canvas):

        self.canvas = canvas

        # Sistema físico recibido desde fisica.py
        self.sistema = None

        # Tiempo de simulación
        self.tiempo = 0.0

        # Estado de la animación
        self.animando = False

        # Escala visual:
        # cuántos píxeles representa 1 metro
        self.escala = 70

        # Tiempo entre cuadros
        self.dt = 0.03

    # =========================================================
    # RECIBIR EL SISTEMA FÍSICO
    # =========================================================

    def establecer_sistema(self, sistema):

        self.sistema = sistema
        self.tiempo = 0.0
        self.animando = False

        self.dibujar()

    # =========================================================
    # DIBUJAR TODO EL SISTEMA
    # =========================================================

    def dibujar(self):

        self.canvas.delete("all")

        if self.sistema is None:
            return

        # -----------------------------------------------------
        # POLEA
        # -----------------------------------------------------

        cx = 425
        cy = 110

        radio_polea = 30

        # -----------------------------------------------------
        # PLANOS
        # -----------------------------------------------------

        longitud = 380

        theta1 = math.radians(
            self.sistema.theta1
        )

        theta2 = math.radians(
            self.sistema.theta2
        )

        # Punto inferior del plano izquierdo
        izquierda_x = (
            cx
            - longitud * math.cos(theta1)
        )

        izquierda_y = (
            cy
            + longitud * math.sin(theta1)
        )

        # Punto inferior del plano derecho
        derecha_x = (
            cx
            + longitud * math.cos(theta2)
        )

        derecha_y = (
            cy
            + longitud * math.sin(theta2)
        )

        # -----------------------------------------------------
        # SUELO
        # -----------------------------------------------------

        self.canvas.create_line(
            40,
            470,
            810,
            470,
            width=4
        )

        # -----------------------------------------------------
        # PLANO IZQUIERDO
        # -----------------------------------------------------

        self.canvas.create_line(
            izquierda_x,
            izquierda_y,
            cx,
            cy,
            width=6
        )

        # -----------------------------------------------------
        # PLANO DERECHO
        # -----------------------------------------------------

        self.canvas.create_line(
            cx,
            cy,
            derecha_x,
            derecha_y,
            width=6
        )

        # -----------------------------------------------------
        # POLEA
        # -----------------------------------------------------

        self.canvas.create_oval(
            cx - radio_polea,
            cy - radio_polea,
            cx + radio_polea,
            cy + radio_polea,
            width=4
        )

        self.canvas.create_oval(
            cx - 6,
            cy - 6,
            cx + 6,
            cy + 6,
            fill="black"
        )

        # -----------------------------------------------------
        # MOVIMIENTO FÍSICO
        # -----------------------------------------------------

        desplazamiento = (
            self.sistema.posicion(self.tiempo)
        )

        # Convertimos metros → píxeles
        desplazamiento_px = (
            desplazamiento * self.escala
        )

        # -----------------------------------------------------
        # DIRECCIONES DE LOS PLANOS
        # -----------------------------------------------------

        u1x = math.cos(theta1)
        u1y = math.sin(theta1)

        u2x = math.cos(theta2)
        u2y = math.sin(theta2)

        # -----------------------------------------------------
        # POSICIÓN BASE DE LAS MASAS
        # -----------------------------------------------------

        distancia_bloque = longitud * 0.50

        # m1 inicialmente
        x1_base = (
            cx
            - distancia_bloque * u1x
        )

        y1_base = (
            cy
            + distancia_bloque * u1y
        )

        # m2 inicialmente
        x2_base = (
            cx
            + distancia_bloque * u2x
        )

        y2_base = (
            cy
            + distancia_bloque * u2y
        )

        # -----------------------------------------------------
        # MOVIMIENTO
        #
        # Si desplazamiento > 0:
        #
        # m2 baja
        # m1 sube
        # -----------------------------------------------------

        x1 = (
            x1_base
            + desplazamiento_px * u1x
        )

        y1 = (
            y1_base
            + desplazamiento_px * u1y
        )

        x2 = (
            x2_base
            - desplazamiento_px * u2x
        )

        y2 = (
            y2_base
            - desplazamiento_px * u2y
        )

        # -----------------------------------------------------
        # TAMAÑO DE LOS BLOQUES
        # -----------------------------------------------------

        tamaño = 50

        # -----------------------------------------------------
        # BLOQUE m1
        # -----------------------------------------------------

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
            font=("Arial", 16, "bold")
        )

        # -----------------------------------------------------
        # BLOQUE m2
        # -----------------------------------------------------

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
            font=("Arial", 16, "bold")
        )

        # -----------------------------------------------------
        # CUERDA
        # -----------------------------------------------------

        self.canvas.create_line(
            x1,
            y1,
            cx,
            cy,
            width=3
        )

        self.canvas.create_line(
            cx,
            cy,
            x2,
            y2,
            width=3
        )

        # -----------------------------------------------------
        # ÁNGULOS
        # -----------------------------------------------------

        self.canvas.create_text(
            izquierda_x + 50,
            izquierda_y - 25,
            text=f"θ₁ = {self.sistema.theta1}°",
            font=("Arial", 12, "bold")
        )

        self.canvas.create_text(
            derecha_x - 50,
            derecha_y - 25,
            text=f"θ₂ = {self.sistema.theta2}°",
            font=("Arial", 12, "bold")
        )

        # -----------------------------------------------------
        # FUERZAS
        # -----------------------------------------------------

        self.dibujar_fuerzas(
            x1,
            y1,
            theta1,
            self.sistema.m1,
            izquierda=True
        )

        self.dibujar_fuerzas(
            x2,
            y2,
            theta2,
            self.sistema.m2,
            izquierda=False
        )

        # -----------------------------------------------------
        # INFORMACIÓN DE LA SIMULACIÓN
        # -----------------------------------------------------

        self.canvas.create_text(
            425,
            30,
            text="SIMULADOR DE FÍSICA MECÁNICA",
            font=("Arial", 20, "bold")
        )

        self.canvas.create_text(
            425,
            525,
            text=f"Tiempo: {self.tiempo:.2f} s",
            font=("Arial", 13)
        )

        velocidad = self.sistema.velocidad(
            self.tiempo
        )

        self.canvas.create_text(
            425,
            550,
            text=f"Velocidad: {velocidad:.2f} m/s",
            font=("Arial", 13)
        )

        self.canvas.create_text(
            425,
            575,
            text=f"Aceleración: {self.sistema.aceleracion:.2f} m/s²",
            font=("Arial", 13)
        )

        self.canvas.create_text(
            425,
            605,
            text=self.sistema.direccion,
            font=("Arial", 13, "bold")
        )

    # =========================================================
    # DIBUJAR FUERZAS
    # =========================================================

    def dibujar_fuerzas(
        self,
        x,
        y,
        theta,
        masa,
        izquierda
    ):

        # -----------------------------------------------------
        # Componente del peso paralela al plano
        # -----------------------------------------------------

        longitud_flecha = 60

        dx = math.cos(theta)
        dy = math.sin(theta)

        # Para el bloque izquierdo la componente va
        # hacia abajo del plano.
        #
        # Para el derecho también usamos la dirección
        # hacia abajo del plano.

        x_final = x + dx * longitud_flecha
        y_final = y + dy * longitud_flecha

        self.canvas.create_line(
            x,
            y,
            x_final,
            y_final,
            width=2,
            arrow="last"
        )

        if izquierda:

            texto = "m₁g sin(θ₁)"

        else:

            texto = "m₂g sin(θ₂)"

        self.canvas.create_text(
            x_final,
            y_final + 15,
            text=texto,
            font=("Arial", 9)
        )

    # =========================================================
    # INICIAR
    # =========================================================

    def iniciar(self):

        if self.sistema is None:
            return

        if self.animando:
            return

        self.animando = True

        self.animar()

    # =========================================================
    # ANIMAR
    # =========================================================

    def animar(self):

        if not self.animando:
            return

        # Aumentar el tiempo
        self.tiempo += self.dt

        # -----------------------------------------------------
        # Límite de seguridad
        # -----------------------------------------------------

        desplazamiento = abs(
            self.sistema.posicion(
                self.tiempo
            )
        )

        if desplazamiento >= 1.8:

            self.animando = False

        # Redibujar
        self.dibujar()

        # Siguiente cuadro
        if self.animando:

            self.canvas.after(
                30,
                self.animar
            )

    # =========================================================
    # DETENER
    # =========================================================

    def detener(self):

        self.animando = False

    # =========================================================
    # REINICIAR
    # =========================================================

    def reiniciar(self):

        self.animando = False
        self.tiempo = 0.0

        self.dibujar()