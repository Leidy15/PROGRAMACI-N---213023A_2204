"""
Excepciones personalizadas relacionadas con reservas.

Todas heredan de ErrorSistemaFJ (definida en errores_cliente.py) para que
todo el sistema pueda manejar sus errores de forma unificada.
"""

from .errores_cliente import ErrorSistemaFJ


class ErrorReserva(ErrorSistemaFJ):
    """Error general relacionado con una reserva (datos invalidos, calculo fallido, etc.)."""


class ErrorEstadoReserva(ErrorReserva):
    """Se lanza cuando se intenta una operacion que no es valida para el estado actual de la reserva."""


class ErrorServicioNoDisponible(ErrorReserva):
    """Se lanza cuando el servicio solicitado no esta disponible para reservar."""
