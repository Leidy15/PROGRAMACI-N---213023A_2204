"""Excepciones personalizadas del sistema Software FJ."""

from .errores_generales import (
    ErrorSistemaFJ,
    ErrorDatosInvalidos,
    ErrorParametroFaltante,
    ErrorOperacionNoPermitida,
    ErrorServicioNoDisponible,
    ErrorCalculoInconsistente,
)
from .errores_cliente import ErrorValidacionCliente
from .errores_reserva import ErrorReserva, ErrorEstadoReserva
from .errores_servicio import ErrorValidacionServicio

__all__ = [
    "ErrorSistemaFJ",
    "ErrorDatosInvalidos",
    "ErrorParametroFaltante",
    "ErrorOperacionNoPermitida",
    "ErrorServicioNoDisponible",
    "ErrorCalculoInconsistente",
    "ErrorValidacionCliente",
    "ErrorReserva",
    "ErrorEstadoReserva",
    "ErrorValidacionServicio",
]
