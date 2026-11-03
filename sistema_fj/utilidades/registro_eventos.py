"""
Registro de eventos y errores en un archivo de log.

Todo el equipo debe usar las funciones de este modulo (registrar_evento y
registrar_error) para que los eventos y errores de todo el sistema queden
guardados en un unico archivo: logs/sistema_fj.log.
"""

import logging
import os

_RUTA_LOGS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
os.makedirs(_RUTA_LOGS, exist_ok=True)
_RUTA_ARCHIVO_LOG = os.path.join(_RUTA_LOGS, "sistema_fj.log")

_logger = logging.getLogger("sistema_fj")
_logger.setLevel(logging.INFO)

# Se evita agregar el mismo "handler" varias veces si el modulo se vuelve a importar.
if not _logger.handlers:
    _formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    _manejador_archivo = logging.FileHandler(_RUTA_ARCHIVO_LOG, encoding="utf-8")
    _manejador_archivo.setFormatter(_formato)
    _logger.addHandler(_manejador_archivo)


def registrar_evento(mensaje: str) -> None:
    """Registra un evento normal del sistema (por ejemplo, un registro exitoso)."""
    _logger.info(mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra un error o una excepcion controlada por el sistema."""
    _logger.error(mensaje)
