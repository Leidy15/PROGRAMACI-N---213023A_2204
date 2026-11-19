"""
Jerarquia de Servicios (Parte 2: Herencia y Polimorfismo).

Clase abstracta Servicio y tres servicios especializados:
  - ReservaSala
  - AlquilerEquipo
  - AsesoriaEspecializada

Cada subclase implementa de forma diferente los metodos abstractos
(calcular_costo, describir y validar_parametros), demostrando polimorfismo.
"""

from abc import abstractmethod

from ..excepciones.errores_servicio import ErrorValidacionServicio, ErrorServicioNoDisponible
from .entidad_base import EntidadBase


class Servicio(EntidadBase):
    """
    Clase abstracta que representa cualquier servicio ofrecido por Software FJ.

    Todos los servicios tienen un nombre, una tarifa base y un estado de
    disponibilidad. Las subclases deben implementar el calculo de costos
    y la validacion de parametros especificos de cada tipo de servicio.
    """

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(identificador)
        self._validar_nombre(nombre)
        self._validar_tarifa(tarifa_base)

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    # ------------------------------------------------------------------
    # Validaciones comunes
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_nombre(nombre):
        if nombre is None or not str(nombre).strip():
            raise ErrorValidacionServicio("El nombre del servicio es obligatorio.")

    @staticmethod
    def _validar_tarifa(tarifa):
        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)):
            raise ErrorValidacionServicio("La tarifa base debe ser un numero.")
        if tarifa < 0:
            raise ErrorValidacionServicio("La tarifa base no puede ser negativa.")

    # ------------------------------------------------------------------
    # Propiedades encapsuladas
    # ------------------------------------------------------------------
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    def marcar_disponible(self) -> None:
        """Marca el servicio como disponible."""
        self._disponible = True

    def marcar_no_disponible(self) -> None:
        """Marca el servicio como no disponible."""
        self._disponible = False

    # ------------------------------------------------------------------
    # Metodos abstractos (polimorfismo)
    # ------------------------------------------------------------------
    @abstractmethod
    def calcular_costo(self, duracion: float) -> float:
        """
        Calcula el costo del servicio segun la duracion.
        Cada subclase implementa su propia formula.
        """
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **kwargs) -> None:
        """
        Valida parametros especificos del tipo de servicio.
        Lanza ErrorValidacionServicio si algo no cumple las reglas.
        """
        raise NotImplementedError

    def describir(self) -> str:
        """Descripcion generica; las subclases pueden sobrescribirla."""
        estado = "disponible" if self._disponible else "no disponible"
        return f"Servicio [{self.identificador}] {self._nombre} - Tarifa base: ${self._tarifa_base:,.0f} - Estado: {estado}"

    def __str__(self) -> str:
        return self.describir()


# ======================================================================
# Subclase 1: Reserva de salas
# ======================================================================
class ReservaSala(Servicio):
    """
    Servicio de reserva de salas (juntas, conferencias, etc.).

    Costo = tarifa_base * duracion * factor_capacidad.
    Si la sala es premium se aplica un recargo adicional.
    """

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int = 10,
        es_premium: bool = False,
        disponible: bool = True,
    ):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self.validar_parametros(capacidad=capacidad, es_premium=es_premium)
        self._capacidad = int(capacidad)
        self._es_premium = bool(es_premium)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def es_premium(self) -> bool:
        return self._es_premium

    def validar_parametros(self, **kwargs) -> None:
        capacidad = kwargs.get("capacidad")
        if capacidad is not None:
            if isinstance(capacidad, bool) or not isinstance(capacidad, (int, float)):
                raise ErrorValidacionServicio("La capacidad de la sala debe ser un numero entero.")
            if capacidad <= 0:
                raise ErrorValidacionServicio("La capacidad de la sala debe ser mayor que cero.")

    def calcular_costo(self, duracion: float) -> float:
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"La sala '{self._nombre}' no esta disponible para reserva."
            )
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorValidacionServicio("La duracion debe ser un numero positivo.")

        # Factor por capacidad: salas mas grandes cuestan un poco mas
        factor_capacidad = 1.0 + (self._capacidad / 100.0)
        costo = self._tarifa_base * duracion * factor_capacidad

        if self._es_premium:
            costo *= 1.25  # 25% de recargo por sala premium

        return round(costo, 2)

    def describir(self) -> str:
        tipo = "premium" if self._es_premium else "estandar"
        estado = "disponible" if self._disponible else "no disponible"
        return (
            f"Reserva de sala [{self.identificador}] {self._nombre} "
            f"(capacidad: {self._capacidad} personas, {tipo}) "
            f"- Tarifa: ${self._tarifa_base:,.0f}/h - Estado: {estado}"
        )


# ======================================================================
# Subclase 2: Alquiler de equipos
# ======================================================================
class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos (videobeam, laptops, sonido, etc.).

    Costo = tarifa_base * duracion + deposito (si aplica).
    Algunos equipos requieren deposito reembolsable.
    """

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        requiere_deposito: bool = False,
        valor_deposito: float = 0.0,
        disponible: bool = True,
    ):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self.validar_parametros(requiere_deposito=requiere_deposito, valor_deposito=valor_deposito)
        self._requiere_deposito = bool(requiere_deposito)
        self._valor_deposito = float(valor_deposito) if requiere_deposito else 0.0

    @property
    def requiere_deposito(self) -> bool:
        return self._requiere_deposito

    @property
    def valor_deposito(self) -> float:
        return self._valor_deposito

    def validar_parametros(self, **kwargs) -> None:
        requiere = kwargs.get("requiere_deposito", False)
        valor = kwargs.get("valor_deposito", 0.0)
        if requiere:
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise ErrorValidacionServicio("El valor del deposito debe ser un numero.")
            if valor < 0:
                raise ErrorValidacionServicio("El valor del deposito no puede ser negativo.")

    def calcular_costo(self, duracion: float) -> float:
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"El equipo '{self._nombre}' no esta disponible para alquiler."
            )
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorValidacionServicio("La duracion debe ser un numero positivo.")

        costo = self._tarifa_base * duracion
        if self._requiere_deposito:
            costo += self._valor_deposito  # se suma el deposito (luego se puede devolver)

        return round(costo, 2)

    def describir(self) -> str:
        deposito_txt = (
            f" - Deposito: ${self._valor_deposito:,.0f}" if self._requiere_deposito else ""
        )
        estado = "disponible" if self._disponible else "no disponible"
        return (
            f"Alquiler de equipo [{self.identificador}] {self._nombre} "
            f"- Tarifa: ${self._tarifa_base:,.0f}/h{deposito_txt} - Estado: {estado}"
        )


# ======================================================================
# Subclase 3: Asesorias especializadas
# ======================================================================
class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesorias especializadas (software, procesos, consultoria).

    Costo = tarifa_base * duracion * multiplicador_nivel.
    El nivel del asesor (junior, semi, senior) cambia el precio.
    """

    NIVELES_VALIDOS = {"junior": 1.0, "semi": 1.4, "senior": 1.8}

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        nivel_asesor: str = "semi",
        area: str = "General",
        disponible: bool = True,
    ):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self.validar_parametros(nivel_asesor=nivel_asesor, area=area)
        self._nivel_asesor = nivel_asesor.strip().lower()
        self._area = area.strip()

    @property
    def nivel_asesor(self) -> str:
        return self._nivel_asesor

    @property
    def area(self) -> str:
        return self._area

    def validar_parametros(self, **kwargs) -> None:
        nivel = kwargs.get("nivel_asesor")
        if nivel is not None:
            nivel_norm = str(nivel).strip().lower()
            if nivel_norm not in self.NIVELES_VALIDOS:
                raise ErrorValidacionServicio(
                    f"Nivel de asesor invalido '{nivel}'. "
                    f"Valores permitidos: {', '.join(self.NIVELES_VALIDOS.keys())}."
                )
        area = kwargs.get("area")
        if area is not None and (not str(area).strip()):
            raise ErrorValidacionServicio("El area de la asesoria no puede estar vacia.")

    def calcular_costo(self, duracion: float) -> float:
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"La asesoria '{self._nombre}' no esta disponible."
            )
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorValidacionServicio("La duracion debe ser un numero positivo.")

        multiplicador = self.NIVELES_VALIDOS.get(self._nivel_asesor, 1.0)
        costo = self._tarifa_base * duracion * multiplicador
        return round(costo, 2)

    def describir(self) -> str:
        estado = "disponible" if self._disponible else "no disponible"
        return (
            f"Asesoria especializada [{self.identificador}] {self._nombre} "
            f"(area: {self._area}, nivel: {self._nivel_asesor}) "
            f"- Tarifa base: ${self._tarifa_base:,.0f}/h - Estado: {estado}"
        )
