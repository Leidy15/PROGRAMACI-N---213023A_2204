"""
Simulacion integrada completa (Parte 5).

Gestiona listas internas en memoria (clientes, servicios y reservas)
sin usar bases de datos, y ejecuta al menos 10 operaciones completas
mezclando casos exitosos y fallidos para demostrar la estabilidad del sistema.
"""

from ..excepciones.errores_cliente import ErrorValidacionCliente
from ..excepciones.errores_reserva import ErrorReserva, ErrorEstadoReserva
from ..excepciones.errores_servicio import ErrorValidacionServicio
from ..modelos.cliente import Cliente
from ..modelos.reserva import Reserva
from ..modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from ..utilidades.registro_eventos import registrar_error, registrar_evento

# ----------------------------------------------------------------------
# Listas internas en memoria (Parte 5)
# ----------------------------------------------------------------------
lista_clientes = []
lista_servicios = []
lista_reservas = []


def registrar_cliente_seguro(identificacion, nombres, apellidos, correo, telefono):
    try:
        c = Cliente(identificacion, nombres, apellidos, correo, telefono)
        lista_clientes.append(c)
        registrar_evento(f"[INTEGRACION] Cliente OK: {c.describir()}")
        print(f"[CLIENTE OK] {c.describir()}")
        return c
    except (ErrorValidacionCliente, Exception) as e:
        registrar_error(f"[INTEGRACION] Cliente rechazado ({identificacion}): {e}")
        print(f"[CLIENTE RECHAZADO] {e}")
        return None
    finally:
        print("-" * 60)


def registrar_servicio_seguro(factory, *args, **kwargs):
    try:
        s = factory(*args, **kwargs)
        lista_servicios.append(s)
        registrar_evento(f"[INTEGRACION] Servicio OK: {s.describir()}")
        print(f"[SERVICIO OK] {s.describir()}")
        return s
    except (ErrorValidacionServicio, Exception) as e:
        registrar_error(f"[INTEGRACION] Servicio rechazado: {e}")
        print(f"[SERVICIO RECHAZADO] {e}")
        return None
    finally:
        print("-" * 60)


def crear_reserva_segura(identificador, cliente, servicio, duracion):
    try:
        r = Reserva(identificador, cliente, servicio, duracion)
        lista_reservas.append(r)
        registrar_evento(f"[INTEGRACION] Reserva creada: {r.describir()}")
        print(f"[RESERVA CREADA] {r.describir()}")
        return r
    except (ErrorReserva, Exception) as e:
        registrar_error(f"[INTEGRACION] Reserva '{identificador}' fallida: {e}")
        print(f"[RESERVA RECHAZADA] {identificador}: {e}")
        return None
    finally:
        print("-" * 60)


def operar_reserva(descripcion, reserva, metodo, *args):
    if reserva is None:
        print(f"[OMITIDO] {descripcion} (reserva no existe)")
        print("-" * 60)
        return
    try:
        resultado = metodo(*args)
        registrar_evento(f"[INTEGRACION] {descripcion}: OK")
        extra = f" -> ${resultado:,.2f}" if resultado is not None else ""
        print(f"[OK] {descripcion}{extra}")
    except (ErrorReserva, ErrorEstadoReserva, Exception) as e:
        registrar_error(f"[INTEGRACION] {descripcion}: {e}")
        print(f"[FALLO] {descripcion}: {e}")
    finally:
        print("-" * 60)


def ejecutar_simulacion():
    print("=" * 70)
    print("  SIMULACION INTEGRADA COMPLETA - Software FJ (Parte 5)")
    print("  Listas internas + minimo 10 operaciones mixtas")
    print("=" * 70)
    print()

    # --- 1 a 4: Registro de clientes (validos e invalidos) ---
    print(">>> REGISTRO DE CLIENTES\n")
    c1 = registrar_cliente_seguro("1001111111", "Ana Maria", "Garcia Lopez", "ana.garcia@correo.com", "3001112233")
    c2 = registrar_cliente_seguro("1002222222", "Carlos", "Ramirez", "carlos.ramirez@correo.com", "3102223344")
    registrar_cliente_seguro("", "Nombre", "Apellido", "mal@correo.com", "3000000000")  # invalido
    registrar_cliente_seguro("1003333333", "Pedro", "Suarez", "correo-sin-arroba", "3113334455")  # invalido

    # --- 5 a 8: Registro de servicios (los 3 tipos + uno invalido) ---
    print("\n>>> REGISTRO DE SERVICIOS\n")
    s_sala = registrar_servicio_seguro(
        ReservaSala, "SRV-SALA-10", "Sala ejecutiva", 55000, capacidad=15, es_premium=True
    )
    s_equipo = registrar_servicio_seguro(
        AlquilerEquipo, "SRV-EQUIPO-10", "Kit de sonido profesional", 45000, requiere_deposito=True, valor_deposito=200000
    )
    s_asesoria = registrar_servicio_seguro(
        AsesoriaEspecializada, "SRV-ASESORIA-10", "Asesoria en ciberseguridad", 120000, nivel_asesor="senior", area="Seguridad"
    )
    registrar_servicio_seguro(ReservaSala, "SRV-SALA-XX", "Sala mala", -5000)  # tarifa negativa

    # --- 9 a 16: Operaciones de reserva (exitosas y fallidas) ---
    print("\n>>> OPERACIONES DE RESERVA\n")

    # Operacion exitosa completa
    r1 = crear_reserva_segura("RES-INT-01", c1, s_sala, 4)
    operar_reserva("Confirmar RES-INT-01", r1, r1.confirmar if r1 else None)
    operar_reserva("Procesar RES-INT-01 (impuesto 19%)", r1, r1.procesar if r1 else None, 0.19)

    # Otra exitosa con descuento
    r2 = crear_reserva_segura("RES-INT-02", c2, s_equipo, 3)
    operar_reserva("Confirmar RES-INT-02", r2, r2.confirmar if r2 else None)
    operar_reserva("Procesar RES-INT-02 (impuesto 19% + descuento 15%)", r2, r2.procesar if r2 else None, 0.19, 0.15)

    # Asesoria exitosa
    r3 = crear_reserva_segura("RES-INT-03", c1, s_asesoria, 2)
    operar_reserva("Confirmar RES-INT-03", r3, r3.confirmar if r3 else None)
    operar_reserva("Procesar RES-INT-03 (sin extras)", r3, r3.procesar if r3 else None)

    # Fallos controlados
    crear_reserva_segura("RES-INT-04", c1, s_sala, -2)  # duracion invalida
    crear_reserva_segura("RES-INT-05", None, s_equipo, 1)  # cliente nulo

    # Cancelacion
    r6 = crear_reserva_segura("RES-INT-06", c2, s_sala, 1)
    operar_reserva("Cancelar RES-INT-06", r6, r6.cancelar if r6 else None)
    operar_reserva("Intentar confirmar RES-INT-06 (ya cancelada)", r6, r6.confirmar if r6 else None)

    # --- Resumen final ---
    print("\n" + "=" * 70)
    print("  RESUMEN DE LA SIMULACION INTEGRADA")
    print("=" * 70)
    print(f"  Clientes en lista interna : {len(lista_clientes)}")
    print(f"  Servicios en lista interna: {len(lista_servicios)}")
    print(f"  Reservas en lista interna : {len(lista_reservas)}")
    print()
    print("  Detalle de clientes registrados:")
    for c in lista_clientes:
        print(f"    - {c.describir()}")
    print()
    print("  Detalle de servicios registrados:")
    for s in lista_servicios:
        print(f"    - {s.describir()}")
    print()
    print("  Detalle de reservas registradas:")
    for r in lista_reservas:
        print(f"    - {r.describir()}")
    print()
    print("  El sistema completo las operaciones sin interrumpirse.")
    print("  Todos los eventos y errores quedaron registrados en logs/sistema_fj.log")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_simulacion()
