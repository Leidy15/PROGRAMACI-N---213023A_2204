"""
Clase Reserva.

Une a un Cliente con un Servicio durante una duracion determinada, y
controla el ciclo de vida de la reserva:

    pendiente -> confirmada -> procesada
    pendiente -> cancelada
    confirmada -> cancelada

La clase espera que el objeto "servicio" tenga:
  - un metodo describir() -> str
  - un metodo calcular_costo(duracion) -> numero
  - un atributo o propiedad "disponible" -> bool
"""

from ..excepciones.errores_reserva import ErrorEstadoReserva, ErrorReserva, ErrorServicioNoDisponible
from .entidad_base import EntidadBase

# Posibles estados de una reserva.
PENDIENTE = "pendiente"
CONFIRMADA = "confirmada"
CANCELADA = "cancelada"
PROCESADA = "procesada"


class Reserva(EntidadBase):
    """Representa la reserva de un servicio por parte de un cliente."""

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        self._validar_cliente(cliente)
        self._validar_servicio(servicio)
        self._validar_duracion(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = PENDIENTE
        self._costo_final = None

    # ------------------------------------------------------------------
    # Validaciones de los datos de entrada
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_cliente(cliente):
        if cliente is None:
            raise ErrorReserva("La reserva necesita un cliente valido.")
        if not getattr(cliente, "activo", True):
            identificador_cliente = getattr(cliente, "identificador", "desconocido")
            raise ErrorReserva(f"El cliente '{identificador_cliente}' esta inactivo y no puede reservar.")

    @staticmethod
    def _validar_servicio(servicio):
        if servicio is None:
            raise ErrorReserva("La reserva necesita un servicio valido.")
        if not hasattr(servicio, "calcular_costo"):
            raise ErrorReserva("El servicio indicado no sabe calcular su propio costo.")
        if not getattr(servicio, "disponible", True):
            identificador_servicio = getattr(servicio, "identificador", "desconocido")
            raise ErrorServicioNoDisponible(f"El servicio '{identificador_servicio}' no esta disponible.")

    @staticmethod
    def _validar_duracion(duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ErrorReserva("La duracion de la reserva debe ser un numero.")
        if duracion <= 0:
            raise ErrorReserva("La duracion de la reserva debe ser mayor que cero.")

    # ------------------------------------------------------------------
    # Propiedades de solo lectura
    # ------------------------------------------------------------------
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_final(self):
        return self._costo_final

    # ------------------------------------------------------------------
    # Ciclo de vida de la reserva
    # ------------------------------------------------------------------
    def confirmar(self):
        """Pasa la reserva de 'pendiente' a 'confirmada'."""
        if self._estado != PENDIENTE:
            raise ErrorEstadoReserva(
                f"Solo se puede confirmar una reserva pendiente (estado actual: '{self._estado}')."
            )
        self._estado = CONFIRMADA

    def cancelar(self):
        """Cancela la reserva, siempre que todavia no haya sido procesada."""
        if self._estado == PROCESADA:
            raise ErrorEstadoReserva("No se puede cancelar una reserva que ya fue procesada.")
        if self._estado == CANCELADA:
            raise ErrorEstadoReserva("La reserva ya estaba cancelada.")
        self._estado = CANCELADA

    def procesar(self, *args):
        """
        Calcula el costo final de una reserva confirmada y la marca como
        'procesada'. Solo se puede procesar una reserva que ya este
        confirmada.

        Admite los mismos parametros opcionales que calcular_costo_total:
        sin parametros, con impuesto, o con impuesto y descuento.
        """
        if self._estado != CONFIRMADA:
            raise ErrorEstadoReserva(
                f"Solo se puede procesar una reserva confirmada (estado actual: '{self._estado}')."
            )

        try:
            costo = self.calcular_costo_total(*args)
        except ErrorReserva:
            raise
        except Exception as error_calculo:
            raise ErrorReserva(
                f"No fue posible calcular el costo de la reserva '{self.identificador}'."
            ) from error_calculo
        else:
            self._costo_final = costo
            self._estado = PROCESADA
            return self._costo_final

    # ------------------------------------------------------------------
    # Metodos "sobrecargados" para calcular el costo (simulados con *args)
    # ------------------------------------------------------------------
    def calcular_costo_total(self, *args):
        if len(args) == 0:
            impuesto, descuento = 0.0, 0.0
        elif len(args) == 1:
            impuesto, descuento = args[0], 0.0
        elif len(args) == 2:
            impuesto, descuento = args
        else:
            raise ErrorReserva("calcular_costo_total recibe como maximo dos parametros: impuesto y descuento.")

        if impuesto < 0 or descuento < 0:
            raise ErrorReserva("El impuesto y el descuento no pueden ser negativos.")
        if descuento > 1:
            raise ErrorReserva("El descuento debe expresarse como una fraccion entre 0 y 1 (ej. 0.1 equivale a 10%).")

        costo_base = self._servicio.calcular_costo(self._duracion)
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return round(costo_final, 2)

    # ------------------------------------------------------------------
    # Implementacion del metodo abstracto de EntidadBase
    # ------------------------------------------------------------------
    def describir(self):
        identificador_cliente = getattr(self._cliente, "identificador", "desconocido")
        texto = (
            f"Reserva [{self.identificador}] - Cliente: {identificador_cliente} "
            f"- Servicio: {self._servicio.describir()} - Duracion: {self._duracion}h "
            f"- Estado: {self._estado}"
        )
        if self._costo_final is not None:
            texto += f" - Costo final: ${self._costo_final:,.2f}"
        return texto

    def __str__(self):
        return self.describir()
