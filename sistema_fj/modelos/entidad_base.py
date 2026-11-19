"""
Clase abstracta base del sistema.

Todas las entidades principales de Software FJ (Cliente, Servicio, Reserva)
comparten algunas caracteristicas basicas: un identificador y una fecha de
creacion. Por eso esas caracteristicas comunes se definen una sola vez aqui,
y cada entidad especifica hereda de esta clase.

Al ser una clase abstracta, EntidadBase no se puede instanciar directamente;
solo sirve como "molde" para las clases que heredan de ella.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """Representa cualquier entidad general del sistema."""

    def __init__(self, identificador: str):
        self._identificador = identificador
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe poder devolver una descripcion legible de si misma."""
        raise NotImplementedError
