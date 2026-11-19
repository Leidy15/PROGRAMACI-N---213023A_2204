"""Utilidades del sistema (registro de eventos y errores)."""

from .registro_eventos import registrar_evento, registrar_error, ejecutar_de_forma_segura

__all__ = ["registrar_evento", "registrar_error", "ejecutar_de_forma_segura"]
