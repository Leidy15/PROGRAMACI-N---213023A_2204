"""
Simulacion de la jerarquia de servicios (Parte 2: Herencia y Polimorfismo).

Se crean instancias de los tres tipos de servicio (ReservaSala, AlquilerEquipo
y AsesoriaEspecializada), se prueban casos validos e invalidos, y se demuestra
el polimorfismo al llamar calcular_costo y describir sobre objetos de distinto
tipo a traves de la misma interfaz.
"""

from ..excepciones.errores_servicio import ErrorValidacionServicio, ErrorServicioNoDisponible
from ..modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from ..utilidades.registro_eventos import registrar_error, registrar_evento

servicios_registrados = []


def crear_servicio(factory, *args, **kwargs):
    """Intenta crear un servicio y maneja errores sin detener el programa."""
    nombre_intento = kwargs.get("nombre", args[1] if len(args) > 1 else "desconocido")
    try:
        servicio = factory(*args, **kwargs)
    except (ErrorValidacionServicio, ErrorServicioNoDisponible) as error:
        registrar_error(f"No fue posible crear el servicio '{nombre_intento}'. Causa: {error}")
        print(f"[RECHAZADO] {error}")
        return None
    except Exception as error_inesperado:
        registrar_error(f"Error inesperado creando servicio: {error_inesperado}")
        print(f"[ERROR INESPERADO] {error_inesperado}")
        return None
    else:
        servicios_registrados.append(servicio)
        registrar_evento(f"Servicio creado: {servicio.describir()}")
        print(f"[OK] {servicio.describir()}")
        return servicio
    finally:
        print("-" * 70)


def ejecutar_simulacion():
    print("=== Simulacion de servicios (Parte 2) - Software FJ ===\n")

    # --- Casos validos ---
    sala1 = crear_servicio(
        ReservaSala,
        "SRV-SALA-01",
        "Sala de juntas principal",
        50000,
        capacidad=12,
        es_premium=False,
    )

    sala2 = crear_servicio(
        ReservaSala,
        "SRV-SALA-02",
        "Sala premium de conferencias",
        80000,
        capacidad=30,
        es_premium=True,
    )

    equipo1 = crear_servicio(
        AlquilerEquipo,
        "SRV-EQUIPO-01",
        "Videobeam Full HD",
        20000,
        requiere_deposito=True,
        valor_deposito=150000,
    )

    equipo2 = crear_servicio(
        AlquilerEquipo,
        "SRV-EQUIPO-02",
        "Laptop corporativa",
        35000,
        requiere_deposito=False,
    )

    asesoria1 = crear_servicio(
        AsesoriaEspecializada,
        "SRV-ASESORIA-01",
        "Consultoria de arquitectura de software",
        90000,
        nivel_asesor="senior",
        area="Desarrollo",
    )

    asesoria2 = crear_servicio(
        AsesoriaEspecializada,
        "SRV-ASESORIA-02",
        "Asesoria de procesos",
        60000,
        nivel_asesor="semi",
        area="Gestion",
    )

    # --- Casos invalidos ---
    crear_servicio(ReservaSala, "SRV-SALA-X", "", 40000)  # nombre vacio
    crear_servicio(ReservaSala, "SRV-SALA-Y", "Sala pequeña", -10000)  # tarifa negativa
    crear_servicio(
        AsesoriaEspecializada,
        "SRV-ASESORIA-X",
        "Asesoria mala",
        50000,
        nivel_asesor="experto",  # nivel invalido
    )
    crear_servicio(
        AlquilerEquipo,
        "SRV-EQUIPO-X",
        "Equipo con deposito invalido",
        25000,
        requiere_deposito=True,
        valor_deposito=-50,
    )

    # --- Demostracion de polimorfismo ---
    print("\n=== Demostracion de polimorfismo (calcular_costo / describir) ===\n")
    servicios_validos = [s for s in servicios_registrados if s is not None]
    for servicio in servicios_validos:
        try:
            costo = servicio.calcular_costo(2)
            print(f"  {servicio.describir()}")
            print(f"  -> Costo por 2 horas: ${costo:,.2f}\n")
            registrar_evento(f"Polimorfismo OK - {servicio.identificador}: costo 2h = {costo}")
        except Exception as e:
            print(f"  [FALLO] {servicio.identificador}: {e}\n")
            registrar_error(f"Error en calculo polimorfico de {servicio.identificador}: {e}")

    # Servicio no disponible
    if sala1:
        sala1.marcar_no_disponible()
        try:
            sala1.calcular_costo(1)
        except ErrorServicioNoDisponible as e:
            print(f"[ESPERADO] Servicio no disponible: {e}")
            registrar_error(str(e))
        finally:
            print("-" * 70)

    print(f"\nTotal de servicios creados con exito: {len(servicios_registrados)}")


if __name__ == "__main__":
    ejecutar_simulacion()
