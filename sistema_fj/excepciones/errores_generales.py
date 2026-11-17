"""
Excepciones generales del sistema (Parte 4: Sistema de Excepciones Avanzadas).

ErrorSistemaFJ es la excepcion "padre" de todo el proyecto. Las demas
excepciones de aqui representan los tipos de error mas comunes que puede
sufrir el sistema, segun lo pedido en la actividad:

  - ErrorDatosInvalidos        -> un dato no cumple el formato esperado.
  - ErrorParametroFaltante     -> falta un dato obligatorio para la operacion.
  - ErrorOperacionNoPermitida  -> se intento algo que no es valido en el
                                   momento (por ejemplo, confirmar una
                                   reserva que ya fue cancelada).
  - ErrorServicioNoDisponible  -> el servicio solicitado no esta disponible.
  - ErrorCalculoInconsistente  -> el resultado de un calculo no tiene sentido
                                   (por ejemplo, un costo negativo).

Las excepciones mas especificas de cada parte del proyecto (por ejemplo
ErrorValidacionCliente o ErrorEstadoReserva) heredan de estas categorias
generales, para que en cualquier punto del sistema se puedan atrapar por
su tipo especifico o por su categoria general, segun lo que convenga.
"""


class ErrorSistemaFJ(Exception):
    """Excepcion base de todo el sistema Software FJ."""


class ErrorDatosInvalidos(ErrorSistemaFJ):
    """Un dato recibido no cumple el formato o las reglas esperadas."""


class ErrorParametroFaltante(ErrorSistemaFJ):
    """Falta un parametro obligatorio para completar la operacion."""


class ErrorOperacionNoPermitida(ErrorSistemaFJ):
    """Se intento una operacion que no es valida en el estado o el momento actual."""


class ErrorServicioNoDisponible(ErrorSistemaFJ):
    """El servicio solicitado no esta disponible para ser usado."""


class ErrorCalculoInconsistente(ErrorSistemaFJ):
    """El resultado de un calculo (costo, impuesto, descuento) no es valido."""
