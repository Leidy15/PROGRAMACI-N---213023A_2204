"""
Registro de eventos y errores (Parte 4: Sistema de Excepciones Avanzadas y Logs).

Todo el equipo debe usar las funciones de este modulo (registrar_evento y
registrar_error) para que los eventos y errores de todo el sistema queden
guardados en un unico archivo: logs/sistema_fj.log.

El archivo de log usa rotacion automatica (RotatingFileHandler): cuando
llega a 1 MB se renombra y se empieza uno nuevo, para que nunca crezca sin
control. Ademas, los errores tambien se muestran por consola, para que un
fallo grave no pase desapercibido aunque nadie revise el archivo de log.
"""

import logging
from logging.handlers import RotatingFileHandler
import os

_RUTA_LOGS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
os.makedirs(_RUTA_LOGS, exist_ok=True)
_RUTA_ARCHIVO_LOG = os.path.join(_RUTA_LOGS, "sistema_fj.log")

_logger = logging.getLogger("sistema_fj")
_logger.setLevel(logging.INFO)

# Se evita agregar los mismos "handlers" varias veces si el modulo se vuelve a importar.
if not _logger.handlers:
    _formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    _manejador_archivo = RotatingFileHandler(
        _RUTA_ARCHIVO_LOG, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    _manejador_archivo.setFormatter(_formato)
    _logger.addHandler(_manejador_archivo)

    _manejador_consola = logging.StreamHandler()
    _manejador_consola.setLevel(logging.ERROR)
    _manejador_consola.setFormatter(_formato)
    _logger.addHandler(_manejador_consola)


def registrar_evento(mensaje: str) -> None:
    """Registra un evento normal del sistema (por ejemplo, un registro exitoso)."""
    _logger.info(mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra un error o una excepcion controlada por el sistema."""
    _logger.error(mensaje)


def ejecutar_de_forma_segura(operacion, *args, descripcion=None, valor_si_falla=None, **kwargs):
    """
    Ejecuta cualquier operacion (una funcion o un metodo) sin dejar que un
    error inesperado detenga el programa.

    Si la operacion termina bien, se devuelve su resultado. Si lanza
    cualquier excepcion, esta se registra en el log (con registrar_error)
    y la funcion devuelve 'valor_si_falla' en su lugar, para que el resto
    del programa pueda seguir ejecutandose con normalidad.

    Esta funcion es el "ultimo respaldo" del sistema: aunque a una parte
    especifica (clientes, servicios, reservas) se le escape un error que no
    previo, aqui queda atrapado y registrado igual.
    """
    etiqueta = descripcion or getattr(operacion, "__name__", "operacion")
    try:
        resultado = operacion(*args, **kwargs)
    except Exception as error:
        registrar_error(f"Error inesperado en '{etiqueta}': {error}")
        return valor_si_falla
    else:
        return resultado
