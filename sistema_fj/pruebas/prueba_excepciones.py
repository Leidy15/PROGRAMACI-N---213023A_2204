"""
Simulacion del manejo de excepciones (Parte 4 del proyecto).

Este script no agrega funcionalidad nueva: reutiliza las clases Cliente y
Reserva ya construidas, pero se enfoca en demostrar, de forma explicita,
cada tipo de error que pide la actividad:

  1. Datos invalidos.
  2. Parametros faltantes.
  3. Operaciones no permitidas.
  4. Servicios no disponibles.
  5. Calculos inconsistentes.
  6. Un error totalmente inesperado, que ni siquiera es una de las
     excepciones propias del sistema (para probar que igual queda
     registrado y el programa no se detiene).

Tambien muestra los distintos bloques de manejo de excepciones pedidos:
try/except, try/except/else, try/except/finally, y encadenamiento de
excepciones (raise ... from).
"""

from ..excepciones.errores_generales import (
    ErrorCalculoInconsistente,
    ErrorDatosInvalidos,
    ErrorOperacionNoPermitida,
    ErrorParametroFaltante,
    ErrorServicioNoDisponible,
    ErrorSistemaFJ,
)
from ..excepciones.errores_reserva import ErrorReserva
from ..modelos.cliente import Cliente
from ..modelos.reserva import Reserva
from ..utilidades.registro_eventos import ejecutar_de_forma_segura, registrar_error, registrar_evento
from .servicio_de_prueba import ServicioDePrueba


class ServicioConCalculoDefectuoso(ServicioDePrueba):
    """
    Servicio de prueba que simula un calculo inconsistente (division por
    cero), para demostrar que un error inesperado dentro de un calculo no
    hace caer el sistema, sino que queda controlado y registrado.
    """

    def calcular_costo(self, duracion):
        return self.tarifa_por_hora / 0  # provoca un ZeroDivisionError a proposito


def caso_1_datos_invalidos():
    """try/except simple: se atrapa un dato invalido al crear un cliente."""
    print("1) Datos invalidos al registrar un cliente")
    try:
        Cliente("1010101010", "Ana", "Perez123", "ana.perez@correo.com", "3001112233")
    except ErrorDatosInvalidos as error:
        registrar_error(f"[Datos invalidos] {error}")
        print(f"   [RECHAZADO] {error}")
    print("-" * 70)


def caso_2_parametro_faltante():
    """Encadenamiento de excepciones: falta un parametro obligatorio (el servicio) al crear una reserva."""
    print("2) Parametro faltante al crear una reserva")
    cliente = Cliente("1020202020", "Mario", "Cruz", "mario.cruz@correo.com", "3002223344")
    try:
        Reserva("RES-PARAM-01", cliente, None, 2)  # no se indico ningun servicio
    except ErrorReserva as error_original:
        try:
            raise ErrorParametroFaltante("Falta indicar el servicio que se desea reservar.") from error_original
        except ErrorParametroFaltante as error_encadenado:
            registrar_error(f"[Parametro faltante] {error_encadenado} Causa: {error_original}")
            print(f"   [RECHAZADO] {error_encadenado} (causa: {error_original})")
    print("-" * 70)


def caso_3_operacion_no_permitida():
    """try/except/finally: cancelar una reserva que ya fue procesada."""
    print("3) Operacion no permitida: cancelar una reserva ya procesada")
    cliente = Cliente("1030303030", "Paula", "Rios", "paula.rios@correo.com", "3003334455")
    servicio = ServicioDePrueba("SRV-SALA-X", "Sala de prueba", tarifa_por_hora=30000)
    reserva = Reserva("RES-OP-01", cliente, servicio, 2)
    reserva.confirmar()
    reserva.procesar()
    try:
        reserva.cancelar()
    except ErrorOperacionNoPermitida as error:
        registrar_error(f"[Operacion no permitida] {error}")
        print(f"   [RECHAZADO] {error}")
    finally:
        print(f"   Estado final de la reserva: {reserva.estado}")
    print("-" * 70)


def caso_4_servicio_no_disponible():
    """Encadenamiento de excepciones: un servicio no disponible impide crear la reserva."""
    print("4) Servicio no disponible, con encadenamiento de excepciones")
    cliente = Cliente("1040404040", "Diego", "Mora", "diego.mora@correo.com", "3004445566")
    servicio_agotado = ServicioDePrueba("SRV-AGOTADO", "Asesoria agotada", tarifa_por_hora=50000, disponible=False)
    try:
        Reserva("RES-SERV-01", cliente, servicio_agotado, 1)
    except ErrorServicioNoDisponible as error_original:
        try:
            raise ErrorSistemaFJ("La reserva no se pudo completar por falta de disponibilidad.") from error_original
        except ErrorSistemaFJ as error_encadenado:
            registrar_error(f"[Servicio no disponible] {error_encadenado} Causa: {error_original}")
            print(f"   [RECHAZADO] {error_encadenado} (causa: {error_original})")
    print("-" * 70)


def caso_5_calculo_inconsistente():
    """Se atrapa un error inesperado (ZeroDivisionError) y se convierte en un error propio del sistema."""
    print("5) Calculo inconsistente dentro de un servicio")
    cliente = Cliente("1050505050", "Sara", "Vega", "sara.vega@correo.com", "3005556677")
    servicio_defectuoso = ServicioConCalculoDefectuoso("SRV-DEF", "Servicio con error de calculo", tarifa_por_hora=1000)
    reserva = Reserva("RES-CALC-01", cliente, servicio_defectuoso, 2)
    reserva.confirmar()
    try:
        reserva.procesar()
    except ErrorReserva as error:
        # Reserva.procesar() ya encadena el ZeroDivisionError original dentro
        # de un ErrorReserva, asi que aqui se puede mostrar la causa real.
        registrar_error(f"[Calculo inconsistente] {error} Causa: {error.__cause__}")
        print(f"   [RECHAZADO] {error} (causa: {error.__cause__})")
    print("-" * 70)


def operacion_con_error_de_programacion():
    """Funcion que falla con un error que no tiene nada que ver con las reglas del negocio."""
    lista_vacia = []
    return lista_vacia[0]  # IndexError: esto no es un ErrorSistemaFJ


def caso_6_error_totalmente_inesperado():
    """Se usa ejecutar_de_forma_segura para que un error no previsto no detenga el programa."""
    print("6) Error totalmente inesperado (no es una excepcion propia del sistema)")
    resultado = ejecutar_de_forma_segura(
        operacion_con_error_de_programacion,
        descripcion="caso_6_error_totalmente_inesperado",
        valor_si_falla="valor por defecto",
    )
    print(f"   El sistema siguio funcionando. Resultado de respaldo: '{resultado}'")
    print("-" * 70)


def ejecutar_simulacion():
    print("=== Simulacion del manejo de excepciones - Software FJ ===\n")
    registrar_evento("Inicio de la simulacion de excepciones (Parte 4).")

    caso_1_datos_invalidos()
    caso_2_parametro_faltante()
    caso_3_operacion_no_permitida()
    caso_4_servicio_no_disponible()
    caso_5_calculo_inconsistente()
    caso_6_error_totalmente_inesperado()

    registrar_evento("Fin de la simulacion de excepciones (Parte 4). El programa no se detuvo en ningun momento.")
    print("\nTodos los casos se probaron sin que el programa se detuviera.")


if __name__ == "__main__":
    ejecutar_simulacion()
