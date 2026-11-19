"""
Excepciones personalizadas relacionadas con clientes.

ErrorValidacionCliente hereda de ErrorDatosInvalidos porque, en el fondo,
un cliente mal registrado siempre es un caso de "datos invalidos".
"""

from .errores_generales import ErrorDatosInvalidos


class ErrorValidacionCliente(ErrorDatosInvalidos):
    """Se lanza cuando los datos de un cliente no cumplen las reglas de validacion."""
