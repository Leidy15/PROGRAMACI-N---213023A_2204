"""
Simulacion del manejo avanzado de excepciones (Parte 4).

Cubre:
  - try / except
  - try / except / else
  - try / except / finally
  - Encadenamiento de excepciones (raise ... from)
  - Excepciones personalizadas de distintas categorias
"""

from ..excepciones.errores_generales import (
    ErrorCalculoInconsistente,
    ErrorDatosInvalidos,
    ErrorOperacionNoPermitida,
    ErrorParametroFaltante,
    ErrorServicioNoDisponible,
    ErrorSistemaFJ,
)
from ..utilidades.registro_eventos import registrar_error, registrar_evento, ejecutar_de_forma_segura


def caso_datos_invalidos():
    print("--- Caso 1: Datos invalidos ---")
    try:
        valor = "abc"
        if not str(valor).isdigit():
            raise ErrorDatosInvalidos(f"Se esperaba un numero, se recibio '{valor}'.")
    except ErrorDatosInvalidos as e:
        registrar_error(f"Datos invalidos detectados: {e}")
        print(f"[CAPTURADO] {e}")
    finally:
        print("-" * 50)


def caso_parametro_faltante():
    print("--- Caso 2: Parametro faltante ---")
    try:
        datos = {"nombre": "Prueba"}
        if "identificacion" not in datos:
            raise ErrorParametroFaltante("Falta el parametro obligatorio 'identificacion'.")
    except ErrorParametroFaltante as e:
        registrar_error(str(e))
        print(f"[CAPTURADO] {e}")
    else:
        print("[OK] Todos los parametros presentes")
    finally:
        print("-" * 50)


def caso_operacion_no_permitida():
    print("--- Caso 3: Operacion no permitida ---")
    estado = "cancelada"
    try:
        if estado == "cancelada":
            raise ErrorOperacionNoPermitida("No se puede confirmar una reserva ya cancelada.")
    except ErrorOperacionNoPermitida as e:
        registrar_error(str(e))
        print(f"[CAPTURADO] {e}")
    finally:
        print("-" * 50)


def caso_servicio_no_disponible():
    print("--- Caso 4: Servicio no disponible ---")
    try:
        disponible = False
        if not disponible:
            raise ErrorServicioNoDisponible("El servicio solicitado no esta disponible en este momento.")
    except ErrorServicioNoDisponible as e:
        registrar_error(str(e))
        print(f"[CAPTURADO] {e}")
    finally:
        print("-" * 50)


def caso_calculo_inconsistente():
    print("--- Caso 5: Calculo inconsistente ---")
    try:
        costo = -15000
        if costo < 0:
            raise ErrorCalculoInconsistente(f"El costo calculado ({costo}) no puede ser negativo.")
    except ErrorCalculoInconsistente as e:
        registrar_error(str(e))
        print(f"[CAPTURADO] {e}")
    else:
        print("[OK] Calculo valido")
    finally:
        print("-" * 50)


def caso_error_inesperado_y_encadenamiento():
    print("--- Caso 6: Error inesperado + encadenamiento ---")
    try:
        try:
            # Simulamos un error interno (division por cero)
            resultado = 100 / 0
        except ZeroDivisionError as causa:
            # Encadenamos el error original dentro de una excepcion del sistema
            raise ErrorSistemaFJ("Fallo interno al calcular un valor.") from causa
    except ErrorSistemaFJ as e:
        registrar_error(f"{e} | Causa original: {e.__cause__}")
        print(f"[CAPTURADO] {e}")
        print(f"  Causa: {e.__cause__}")
    finally:
        print("-" * 50)


def caso_ejecutar_seguro():
    print("--- Caso 7: ejecutar_de_forma_segura (ultimo respaldo) ---")

    def operacion_que_falla():
        raise RuntimeError("Algo inesperado ocurrio")

    resultado = ejecutar_de_forma_segura(
        operacion_que_falla,
        descripcion="operacion_de_prueba",
        valor_si_falla="VALOR_POR_DEFECTO",
    )
    print(f"[RESULTADO] La operacion fallo de forma controlada. Valor devuelto: {resultado}")
    registrar_evento("ejecutar_de_forma_segura funciono correctamente")
    print("-" * 50)


def ejecutar_simulacion():
    print("=== Simulacion de manejo avanzado de excepciones - Software FJ ===\n")
    caso_datos_invalidos()
    caso_parametro_faltante()
    caso_operacion_no_permitida()
    caso_servicio_no_disponible()
    caso_calculo_inconsistente()
    caso_error_inesperado_y_encadenamiento()
    caso_ejecutar_seguro()
    print("Simulacion de excepciones finalizada. El programa continúo sin detenerse.")


if __name__ == "__main__":
    ejecutar_simulacion()
