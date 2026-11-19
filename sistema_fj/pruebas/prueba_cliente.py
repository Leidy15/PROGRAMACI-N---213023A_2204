"""
Simulacion de registro de clientes (Parte 1 del proyecto).

Este script crea varios clientes, algunos con datos correctos y otros con
datos incorrectos a proposito. La idea es demostrar que el sistema:

  1. Valida correctamente los datos de un cliente.
  2. No se detiene ni se cae cuando encuentra un dato invalido.
  3. Deja un registro de cada evento y de cada error en el archivo de log.
"""

from ..excepciones.errores_cliente import ErrorValidacionCliente
from ..excepciones.errores_generales import ErrorSistemaFJ
from ..modelos.cliente import Cliente
from ..utilidades.registro_eventos import registrar_error, registrar_evento

# Lista interna donde se guardan los clientes que si se pudieron registrar.
clientes_registrados = []

# Cada tupla es un intento de registro. Hay intentos validos e invalidos.
datos_de_prueba = [
    ("1001234567", "Leidy Carolina", "Nino Rivera", "leidy.nr15@gmail.com", "3001234567"),
    ("1002345678", "Juan David", "Perez Gomez", "juan.perez@correo.com", "3109876543"),
    ("", "Maria", "Lopez", "maria.lopez@correo.com", "3201112233"),  # identificacion vacia
    ("1003456789", "", "Ramirez", "andres@correo.com", "3112223344"),  # nombre vacio
    ("1004567890", "Camila", "Torres99", "camila.torres@correo.com", "3113334455"),  # apellido con numeros
    ("1005678901", "Pedro", "Martinez", "pedro_sin_arroba.com", "3114445566"),  # correo invalido
    ("1006789012", "Laura", "Gomez", "laura.gomez@correo.com", "123"),  # telefono muy corto
    ("abc123", "Sofia", "Castro", "sofia.castro@correo.com", "3115556677"),  # identificacion invalida
    ("1007890123", "Carlos", "Diaz", "carlos.diaz@correo.com", "3005554433"),
    ("1008901234", "Valentina", "Suarez", "valentina.suarez@correo.com", "3167778899"),
]


def registrar_cliente(identificacion, nombres, apellidos, correo, telefono):
    """Intenta crear un Cliente y maneja cualquier error de validacion sin detener el programa."""
    try:
        nuevo_cliente = Cliente(identificacion, nombres, apellidos, correo, telefono)
    except ErrorValidacionCliente as error:
        error_sistema = ErrorSistemaFJ(f"No fue posible registrar al cliente '{identificacion}'.")
        try:
            raise error_sistema from error
        except ErrorSistemaFJ as error_encadenado:
            registrar_error(f"{error_encadenado} Causa: {error}")
            print(f"[RECHAZADO] {error}")
    except Exception as error_inesperado:
        registrar_error(f"Error inesperado registrando al cliente '{identificacion}': {error_inesperado}")
        print(f"[ERROR INESPERADO] {error_inesperado}")
    else:
        clientes_registrados.append(nuevo_cliente)
        registrar_evento(f"Cliente registrado con exito: {nuevo_cliente.describir()}")
        print(f"[OK] {nuevo_cliente.describir()}")
    finally:
        print("-" * 70)


def ejecutar_simulacion():
    print("=== Simulacion de registro de clientes - Software FJ ===\n")
    for identificacion, nombres, apellidos, correo, telefono in datos_de_prueba:
        registrar_cliente(identificacion, nombres, apellidos, correo, telefono)

    print(f"Total de intentos de registro: {len(datos_de_prueba)}")
    print(f"Clientes registrados con exito: {len(clientes_registrados)}")
    print(f"Registros rechazados: {len(datos_de_prueba) - len(clientes_registrados)}")


if __name__ == "__main__":
    ejecutar_simulacion()
