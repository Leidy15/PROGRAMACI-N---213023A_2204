"""
Simulacion de reservas (Parte 3 del proyecto) usando los servicios reales
de la Parte 2 (ReservaSala, AlquilerEquipo, AsesoriaEspecializada).
"""

from ..excepciones.errores_cliente import ErrorValidacionCliente
from ..excepciones.errores_reserva import ErrorReserva
from ..modelos.cliente import Cliente
from ..modelos.reserva import Reserva
from ..modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from ..utilidades.registro_eventos import registrar_error, registrar_evento

# ----------------------------------------------------------------------
# Clientes y servicios reales usados en esta simulacion.
# ----------------------------------------------------------------------
cliente_activo = Cliente("1001234567", "Leidy Carolina", "Nino Rivera", "leidy.nr15@gmail.com", "3001234567")

cliente_inactivo = Cliente("1009998887", "Ricardo", "Lopez", "ricardo.lopez@correo.com", "3201112233")
cliente_inactivo.desactivar()

sala_reuniones = ReservaSala("SRV-SALA-01", "Sala de juntas principal", 50000, capacidad=12, es_premium=False)
equipo_video = AlquilerEquipo("SRV-EQUIPO-01", "Videobeam Full HD", 20000, requiere_deposito=True, valor_deposito=100000)
asesoria = AsesoriaEspecializada("SRV-ASESORIA-01", "Consultoria de software", 90000, nivel_asesor="senior", area="Desarrollo")
asesoria_fuera = AsesoriaEspecializada(
    "SRV-ASESORIA-02", "Asesoria de procesos", 60000, nivel_asesor="semi", area="Gestion", disponible=False
)

# Lista interna donde se guardan las reservas que si se pudieron crear.
reservas_registradas = []


def crear_reserva(identificador, cliente, servicio, duracion):
    """Intenta crear una Reserva y maneja cualquier error sin detener el programa."""
    try:
        nueva_reserva = Reserva(identificador, cliente, servicio, duracion)
    except (ErrorReserva, ErrorValidacionCliente) as error:
        registrar_error(f"No fue posible crear la reserva '{identificador}'. Causa: {error}")
        print(f"[RECHAZADA] Reserva '{identificador}': {error}")
        return None
    else:
        reservas_registradas.append(nueva_reserva)
        registrar_evento(f"Reserva creada: {nueva_reserva.describir()}")
        print(f"[CREADA] {nueva_reserva.describir()}")
        return nueva_reserva
    finally:
        print("-" * 70)


def ejecutar_operacion(descripcion, funcion, *args):
    """Ejecuta una operacion sobre una reserva de forma segura."""
    try:
        resultado = funcion(*args)
    except ErrorReserva as error:
        registrar_error(f"{descripcion}: {error}")
        print(f"[FALLO] {descripcion}: {error}")
    else:
        registrar_evento(f"{descripcion}: operacion exitosa.")
        print(f"[OK] {descripcion}" + (f" -> costo: ${resultado:,.2f}" if resultado is not None else ""))
    finally:
        print("-" * 70)


def ejecutar_simulacion():
    print("=== Simulacion de reservas - Software FJ ===\n")

    # 1. Reserva valida de principio a fin: crear, confirmar y procesar.
    reserva_1 = crear_reserva("RES-001", cliente_activo, sala_reuniones, 3)
    if reserva_1:
        ejecutar_operacion("Confirmar RES-001", reserva_1.confirmar)
        ejecutar_operacion("Procesar RES-001 (sin impuesto ni descuento)", reserva_1.procesar)

    # 2. Reserva valida, procesada con impuesto.
    reserva_2 = crear_reserva("RES-002", cliente_activo, equipo_video, 2)
    if reserva_2:
        ejecutar_operacion("Confirmar RES-002", reserva_2.confirmar)
        ejecutar_operacion("Procesar RES-002 (con impuesto del 19%)", reserva_2.procesar, 0.19)

    # 3. Reserva valida, procesada con impuesto y descuento.
    reserva_3 = crear_reserva("RES-003", cliente_activo, sala_reuniones, 5)
    if reserva_3:
        ejecutar_operacion("Confirmar RES-003", reserva_3.confirmar)
        ejecutar_operacion("Procesar RES-003 (impuesto 19%, descuento 10%)", reserva_3.procesar, 0.19, 0.10)

    # 4. Reserva valida que se cancela antes de confirmar.
    reserva_4 = crear_reserva("RES-004", cliente_activo, equipo_video, 1)
    if reserva_4:
        ejecutar_operacion("Cancelar RES-004", reserva_4.cancelar)

    # 5. Intento de confirmar una reserva que ya esta cancelada -> debe fallar.
    if reserva_4:
        ejecutar_operacion("Confirmar RES-004 (ya cancelada)", reserva_4.confirmar)

    # 6. Intento de procesar una reserva que todavia no ha sido confirmada -> debe fallar.
    reserva_5 = crear_reserva("RES-005", cliente_activo, sala_reuniones, 2)
    if reserva_5:
        ejecutar_operacion("Procesar RES-005 (sin confirmar)", reserva_5.procesar)

    # 7. Intento de cancelar una reserva que ya fue procesada -> debe fallar.
    if reserva_1:
        ejecutar_operacion("Cancelar RES-001 (ya procesada)", reserva_1.cancelar)

    # 8. Reserva con un cliente inactivo -> debe fallar al crearse.
    crear_reserva("RES-006", cliente_inactivo, sala_reuniones, 2)

    # 9. Reserva con un servicio no disponible -> debe fallar al crearse.
    crear_reserva("RES-007", cliente_activo, asesoria_fuera, 1)

    # 10. Reserva con una duracion invalida (negativa) -> debe fallar.
    crear_reserva("RES-008", cliente_activo, sala_reuniones, -3)

    # 11. Reserva con una duracion de tipo invalido -> debe fallar.
    crear_reserva("RES-009", cliente_activo, equipo_video, "dos horas")

    # 12. Doble confirmacion de la misma reserva -> la segunda debe fallar.
    reserva_6 = crear_reserva("RES-010", cliente_activo, asesoria, 4)
    if reserva_6:
        ejecutar_operacion("Confirmar RES-010 (primera vez)", reserva_6.confirmar)
        ejecutar_operacion("Confirmar RES-010 (segunda vez, debe fallar)", reserva_6.confirmar)
        ejecutar_operacion("Procesar RES-010 (impuesto 19%)", reserva_6.procesar, 0.19)

    print(f"\nTotal de reservas creadas con exito: {len(reservas_registradas)}")


if __name__ == "__main__":
    ejecutar_simulacion()
