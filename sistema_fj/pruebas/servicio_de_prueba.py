"""
Servicio de prueba (temporal).

La clase real "Servicio" y sus subclases (reserva de salas, alquiler de
equipos, asesorias) las construye el compañero encargado de la Parte 2.
Mientras esa parte no este lista, se usa esta clase minima solo para poder
programar y probar la clase Reserva (Parte 3) de forma independiente.

Cuando la Parte 2 este lista, esta clase se deja de usar y las reservas se
crean directamente con los servicios reales, sin cambiar nada en Reserva,
porque ambas cumplen la misma "interfaz" basica: describir(), disponible y
calcular_costo(duracion).
"""


class ServicioDePrueba:
    def __init__(self, identificador, nombre, tarifa_por_hora, disponible=True):
        self.identificador = identificador
        self.nombre = nombre
        self.tarifa_por_hora = tarifa_por_hora
        self.disponible = disponible

    def calcular_costo(self, duracion):
        return self.tarifa_por_hora * duracion

    def describir(self):
        return f"{self.nombre} (tarifa: {self.tarifa_por_hora}/hora)"
