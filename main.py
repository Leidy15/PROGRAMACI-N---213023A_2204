"""
Punto de entrada principal del Sistema Integral de Gestion de Clientes,
Servicios y Reservas - Software FJ.

Ejecuta en orden todas las simulaciones del proyecto:
  1. Registro de clientes (Parte 1)
  2. Jerarquia de servicios (Parte 2)
  3. Gestion de reservas (Parte 3)
  4. Manejo avanzado de excepciones (Parte 4)
  5. Simulacion integrada completa con listas internas (Parte 5)
"""

from sistema_fj.pruebas.prueba_cliente import ejecutar_simulacion as simular_clientes
from sistema_fj.pruebas.prueba_servicios import ejecutar_simulacion as simular_servicios
from sistema_fj.pruebas.prueba_reserva import ejecutar_simulacion as simular_reservas
from sistema_fj.pruebas.prueba_excepciones import ejecutar_simulacion as simular_excepciones
from sistema_fj.pruebas.prueba_integracion import ejecutar_simulacion as simular_integracion


if __name__ == "__main__":
    print("\n" + "#" * 70)
    print("#  SOFTWARE FJ - Sistema Integral de Gestion")
    print("#  Clientes | Servicios | Reservas")
    print("#" * 70 + "\n")

    simular_clientes()
    print("\n")
    simular_servicios()
    print("\n")
    simular_reservas()
    print("\n")
    simular_excepciones()
    print("\n")
    simular_integracion()

    print("\n" + "#" * 70)
    print("#  Todas las simulaciones finalizaron correctamente.")
    print("#  Revise el archivo logs/sistema_fj.log para el historial completo.")
    print("#" * 70 + "\n")
