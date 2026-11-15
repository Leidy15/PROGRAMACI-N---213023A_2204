"""Punto de entrada para ejecutar las simulaciones ya desarrolladas del proyecto."""

from sistema_fj.pruebas.prueba_cliente import ejecutar_simulacion as simular_clientes
from sistema_fj.pruebas.prueba_reserva import ejecutar_simulacion as simular_reservas

if __name__ == "__main__":
    simular_clientes()
    print("\n")
    simular_reservas()
