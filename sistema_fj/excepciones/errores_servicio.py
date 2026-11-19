"""
Excepciones personalizadas relacionadas con servicios (Parte 2).

ErrorValidacionServicio se usa cuando los datos de un servicio no cumplen
las reglas (nombre vacio, tarifa negativa, nivel de asesor invalido, etc.).

Para "servicio no disponible" se reutiliza directamente la excepcion
general ErrorServicioNoDisponible definida en errores_generales.py.
"""

from .errores_generales import ErrorDatosInvalidos, ErrorServicioNoDisponible

__all__ = ["ErrorValidacionServicio", "ErrorServicioNoDisponible"]


class ErrorValidacionServicio(ErrorDatosInvalidos):
    """Se lanza cuando los datos de un servicio no cumplen las reglas de validacion."""
