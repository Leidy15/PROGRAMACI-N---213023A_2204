"""
Excepciones personalizadas relacionadas con reservas.

ErrorReserva es el error general de esta parte. Las otras excepciones
heredan tanto de ErrorReserva como de su categoria general equivalente.
"""

from .errores_generales import (
    ErrorOperacionNoPermitida,
    ErrorServicioNoDisponible as _ErrorServicioNoDisponibleGeneral,
    ErrorSistemaFJ,
)


class ErrorReserva(ErrorSistemaFJ):
    """Error general relacionado con una reserva (datos invalidos, calculo fallido, etc.)."""


class ErrorEstadoReserva(ErrorReserva, ErrorOperacionNoPermitida):
    """Se lanza cuando se intenta una operacion que no es valida para el estado actual de la reserva."""


class ErrorServicioNoDisponible(ErrorReserva, _ErrorServicioNoDisponibleGeneral):
    """Se lanza cuando el servicio solicitado no esta disponible para reservar."""
