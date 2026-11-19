"""
Clase Cliente.

Representa a un cliente de Software FJ. Todos los datos personales
(nombres, apellidos, correo, telefono) se guardan en atributos "privados"
(con un guion bajo al inicio) y solo se pueden leer o modificar a traves
de las propiedades (@property), que validan cada dato antes de guardarlo.
Esto evita que en cualquier parte del programa se pueda poner un dato
invalido directamente en el objeto.
"""

import re

from ..excepciones.errores_cliente import ErrorValidacionCliente
from .entidad_base import EntidadBase

# Expresiones regulares usadas para validar cada dato del cliente.
_PATRON_SOLO_LETRAS = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$")
_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[A-Za-z]{2,}$")
_PATRON_TELEFONO = re.compile(r"^\d{7,10}$")
_PATRON_IDENTIFICACION = re.compile(r"^\d{6,10}$")


class Cliente(EntidadBase):
    """Cliente del sistema, con validaciones estrictas y datos encapsulados."""

    def __init__(self, identificacion, nombres, apellidos, correo, telefono):
        self._validar_identificacion(identificacion)
        super().__init__(str(identificacion).strip())

        # Los "setters" de abajo validan cada valor antes de asignarlo.
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.telefono = telefono
        self._activo = True

    # ------------------------------------------------------------------
    # Identificacion: no tiene setter porque un cliente no puede cambiar
    # su numero de identificacion despues de registrado.
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_identificacion(identificacion):
        if identificacion is None or not str(identificacion).strip():
            raise ErrorValidacionCliente("La identificacion del cliente es obligatoria.")
        if not _PATRON_IDENTIFICACION.match(str(identificacion).strip()):
            raise ErrorValidacionCliente(
                f"La identificacion '{identificacion}' no es valida: debe tener entre 6 y 10 digitos numericos."
            )

    # ------------------------------------------------------------------
    # Nombres
    # ------------------------------------------------------------------
    @property
    def nombres(self) -> str:
        return self._nombres

    @nombres.setter
    def nombres(self, valor: str):
        if valor is None or not valor.strip():
            raise ErrorValidacionCliente("Los nombres del cliente son obligatorios.")
        if not _PATRON_SOLO_LETRAS.match(valor.strip()):
            raise ErrorValidacionCliente(f"Los nombres '{valor}' solo pueden contener letras y espacios.")
        self._nombres = valor.strip().title()

    # ------------------------------------------------------------------
    # Apellidos
    # ------------------------------------------------------------------
    @property
    def apellidos(self) -> str:
        return self._apellidos

    @apellidos.setter
    def apellidos(self, valor: str):
        if valor is None or not valor.strip():
            raise ErrorValidacionCliente("Los apellidos del cliente son obligatorios.")
        if not _PATRON_SOLO_LETRAS.match(valor.strip()):
            raise ErrorValidacionCliente(f"Los apellidos '{valor}' solo pueden contener letras y espacios.")
        self._apellidos = valor.strip().title()

    # ------------------------------------------------------------------
    # Correo electronico
    # ------------------------------------------------------------------
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if valor is None or not valor.strip():
            raise ErrorValidacionCliente("El correo electronico del cliente es obligatorio.")
        if not _PATRON_CORREO.match(valor.strip()):
            raise ErrorValidacionCliente(f"El correo '{valor}' no tiene un formato valido.")
        self._correo = valor.strip().lower()

    # ------------------------------------------------------------------
    # Telefono
    # ------------------------------------------------------------------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor_texto = str(valor).strip() if valor is not None else ""
        if not valor_texto:
            raise ErrorValidacionCliente("El telefono del cliente es obligatorio.")
        if not _PATRON_TELEFONO.match(valor_texto):
            raise ErrorValidacionCliente(f"El telefono '{valor}' no es valido: debe tener entre 7 y 10 digitos.")
        self._telefono = valor_texto

    # ------------------------------------------------------------------
    # Estado del cliente (activo / inactivo)
    # ------------------------------------------------------------------
    @property
    def activo(self) -> bool:
        return self._activo

    def desactivar(self) -> None:
        """Marca al cliente como inactivo, sin borrarlo del sistema."""
        self._activo = False

    def activar(self) -> None:
        """Vuelve a marcar al cliente como activo."""
        self._activo = True

    # ------------------------------------------------------------------
    # Implementacion del metodo abstracto de EntidadBase
    # ------------------------------------------------------------------
    def describir(self) -> str:
        estado = "activo" if self._activo else "inactivo"
        return (
            f"Cliente [{self.identificador}] {self.nombres} {self.apellidos} "
            f"- Correo: {self.correo} - Telefono: {self.telefono} - Estado: {estado}"
        )

    def __str__(self) -> str:
        return self.describir()
