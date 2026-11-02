"""
Excepciones personalizadas relacionadas con clientes.

ErrorSistemaFJ es la excepcion "padre" de todo el proyecto: la idea es que
los otros integrantes del equipo tambien hereden de ella para sus propios
errores (por ejemplo ErrorServicio o ErrorReserva), de modo que todo el
sistema pueda manejar sus errores de forma unificada.
"""


class ErrorSistemaFJ(Exception):
    """Excepcion base de todo el sistema Software FJ."""


class ErrorValidacionCliente(ErrorSistemaFJ):
    """Se lanza cuando los datos de un cliente no cumplen las reglas de validacion."""
