"""
Clase Reserva.

Une a un Cliente con un Servicio durante una duracion determinada, y
controla el ciclo de vida de la reserva:

    pendiente -> confirmada -> procesada
    pendiente -> cancelada
    confirmada -> cancelada

Nota importante sobre el servicio:
Esta clase todavia no depende de una clase concreta de Servicio (esa es la
Parte 2 del proyecto, que construye otro integrante del equipo). Mientras
tanto, Reserva solo espera que el objeto que se le pase como "servicio"
tenga:

  - un metodo describir() -> str
  - un metodo calcular_costo(duracion) -> numero
  - un atributo o propiedad "disponible" -> bool

Gracias a esto se puede programar y probar la clase Reserva de forma
independiente, y conectarla con la clase Servicio real (o cualquiera de
sus subclases: salas, equipos, asesorias) sin tener que cambiar nada aqui,
siempre que esa clase cumpla con los tres puntos anteriores.
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
    # Propiedades de solo lectura (encapsulacion: no se pueden cambiar
    # desde afuera, solo a traves de los metodos de la clase).
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

        Admite los mismos parametros opcionales que calcular_costo_total
        (ver abajo): sin parametros, con impuesto, o con impuesto y
        descuento.
        """
        if self._estado != CONFIRMADA:
            raise ErrorEstadoReserva(
                f"Solo se puede procesar una reserva confirmada (estado actual: '{self._estado}')."
            )

        try:
            costo = self.calcular_costo_total(*args)
        except ErrorReserva:
            # Los errores de validacion de la propia reserva se dejan pasar tal cual.
            raise
        except Exception as error_calculo:
            # Si el error viene de otra parte (por ejemplo del servicio),
            # se encadena dentro de un ErrorReserva para no perder el detalle
            # de la causa, pero sin dejar caer el programa.
            raise ErrorReserva(
                f"No fue posible calcular el costo de la reserva '{self.identificador}'."
            ) from error_calculo
        else:
            self._costo_final = costo
            self._estado = PROCESADA
            return self._costo_final

    # ------------------------------------------------------------------
    # Metodos "sobrecargados" para calcular el costo.
    #
    # Python no tiene sobrecarga real de metodos (no se pueden tener dos
    # metodos con el mismo nombre pero distinta cantidad de parametros).
    # Para lograr un efecto parecido, se usa *args y se revisa cuantos
    # argumentos llegaron:
    #
    #   calcular_costo_total()                    -> costo base
    #   calcular_costo_total(impuesto)             -> costo + impuesto
    #   calcular_costo_total(impuesto, descuento)  -> costo + impuesto - descuento
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
            texto += f" - Costo final: {self._costo_final}"
        return texto

    def __str__(self):
        return self.describir()
