"""
Excepciones personalizadas relacionadas con clientes.

ErrorValidacionCliente hereda de ErrorDatosInvalidos (ver errores_generales.py)
porque, en el fondo, un cliente mal registrado siempre es un caso de "datos
invalidos". Asi, el error se puede atrapar como algo especifico de clientes
o, en un nivel mas general, como cualquier otro error de datos del sistema.
"""

from .errores_generales import ErrorDatosInvalidos


class ErrorValidacionCliente(ErrorDatosInvalidos):
    """Se lanza cuando los datos de un cliente no cumplen las reglas de validacion."""
