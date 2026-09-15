import math


class SistemaFisico:
    """
    Modelo físico de dos masas sobre planos inclinados
    conectadas mediante una cuerda y una polea ideal.

    Convención:
        Dirección positiva:
        m2 baja por su plano y m1 sube por su plano.

    Suposiciones:
        - Cuerda inextensible
        - Cuerda sin masa
        - Polea ideal
        - No hay fricción
    """

    def __init__(self, m1, m2, theta1, theta2, g=9.81):

        self.m1 = float(m1)
        self.m2 = float(m2)

        self.theta1 = float(theta1)
        self.theta2 = float(theta2)

        self.g = float(g)

        self.validar_datos()

        self.calcular()

    # ---------------------------------------------------------
    # VALIDACIÓN
    # ---------------------------------------------------------

    def validar_datos(self):

        if self.m1 <= 0:
            raise ValueError("m1 debe ser mayor que 0.")

        if self.m2 <= 0:
            raise ValueError("m2 debe ser mayor que 0.")

        if self.g <= 0:
            raise ValueError("La gravedad debe ser mayor que 0.")

        if not 0 < self.theta1 < 90:
            raise ValueError("θ1 debe estar entre 0° y 90°.")

        if not 0 < self.theta2 < 90:
            raise ValueError("θ2 debe estar entre 0° y 90°.")

    # ---------------------------------------------------------
    # CÁLCULOS
    # ---------------------------------------------------------

    def calcular(self):

        # Convertimos grados → radianes
        theta1 = math.radians(self.theta1)
        theta2 = math.radians(self.theta2)

        # -----------------------------------------------------
        # Peso
        # -----------------------------------------------------

        self.peso1 = self.m1 * self.g
        self.peso2 = self.m2 * self.g

        # -----------------------------------------------------
        # Componentes del peso
        # -----------------------------------------------------

        # Paralelas al plano
        self.peso_paralelo1 = (
            self.m1 * self.g * math.sin(theta1)
        )

        self.peso_paralelo2 = (
            self.m2 * self.g * math.sin(theta2)
        )

        # Perpendiculares al plano
        self.peso_perpendicular1 = (
            self.m1 * self.g * math.cos(theta1)
        )

        self.peso_perpendicular2 = (
            self.m2 * self.g * math.cos(theta2)
        )

        # -----------------------------------------------------
        # Fuerza neta del sistema
        # -----------------------------------------------------

        self.fuerza_neta = (
            self.peso_paralelo2
            - self.peso_paralelo1
        )

        # -----------------------------------------------------
        # Aceleración
        # -----------------------------------------------------

        self.aceleracion = (
            self.fuerza_neta
            / (self.m1 + self.m2)
        )

        # -----------------------------------------------------
        # Tensión
        #
        # T - m1*g*sin(theta1) = m1*a
        #
        # T = m1*a + m1*g*sin(theta1)
        # -----------------------------------------------------

        self.tension = (
            self.m1 * self.aceleracion
            + self.peso_paralelo1
        )

        # -----------------------------------------------------
        # Normales
        # -----------------------------------------------------

        self.normal1 = self.peso_perpendicular1
        self.normal2 = self.peso_perpendicular2

        # -----------------------------------------------------
        # Dirección del movimiento
        # -----------------------------------------------------

        if self.aceleracion > 0:

            self.direccion = "m₂ baja / m₁ sube"

        elif self.aceleracion < 0:

            self.direccion = "m₁ baja / m₂ sube"

        else:

            self.direccion = "El sistema está en equilibrio"

    # ---------------------------------------------------------
    # MOVIMIENTO
    # ---------------------------------------------------------

    def posicion(self, tiempo):

        """
        Desplazamiento desde el reposo:

            x = 1/2 a t²
        """

        return 0.5 * self.aceleracion * tiempo ** 2

    def velocidad(self, tiempo):

        """
        Velocidad desde el reposo:

            v = a t
        """

        return self.aceleracion * tiempo

    # ---------------------------------------------------------
    # INFORMACIÓN
    # ---------------------------------------------------------

    def resultados(self):

        return {
            "aceleracion": abs(self.aceleracion),
            "tension": self.tension,
            "direccion": self.direccion,
            "peso1": self.peso1,
            "peso2": self.peso2,
            "paralelo1": self.peso_paralelo1,
            "paralelo2": self.peso_paralelo2,
            "normal1": self.normal1,
            "normal2": self.normal2,
        }