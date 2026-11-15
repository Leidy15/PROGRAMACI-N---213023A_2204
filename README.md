# PROGRAMACI-N---213023A_2204
Fase 4 - Componente práctico - Prácticas simuladas, Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Parte 1: Gestión de Clientes y Abstracción Base

**Responsable:** Leidy Carolina Niño Rivera (rama `leidy-nino`)

Esta parte del proyecto define la base del sistema y la gestión de clientes:

- `sistema_fj/modelos/entidad_base.py`: clase abstracta `EntidadBase`, de la
  que heredan todas las entidades del sistema (Cliente, y más adelante
  Servicio y Reserva).
- `sistema_fj/modelos/cliente.py`: clase `Cliente`, con los datos personales
  encapsulados (atributos privados + `@property`) y validaciones estrictas
  para identificación, nombres, apellidos, correo y teléfono.
- `sistema_fj/excepciones/errores_cliente.py`: excepciones personalizadas
  (`ErrorSistemaFJ` como base de todo el proyecto y `ErrorValidacionCliente`
  para errores de validación de clientes).
- `sistema_fj/utilidades/registro_eventos.py`: funciones para registrar
  eventos y errores en `logs/sistema_fj.log`.
- `sistema_fj/pruebas/prueba_cliente.py`: simulación con 10 intentos de
  registro de clientes (válidos e inválidos) que muestra que el sistema
  sigue funcionando aunque ocurran errores de validación.

## Parte 3: Gestión de Reservas y Métodos Sobrecargados

**Responsable:** Leidy Carolina Niño Rivera (rama `leidy-nino`)

- `sistema_fj/modelos/reserva.py`: clase `Reserva`, con ciclo de vida
  `pendiente → confirmada → procesada` (o `cancelada` en cualquier punto
  antes de procesarse), métodos `confirmar()`, `cancelar()` y `procesar()`
  con manejo de excepciones, y el método "sobrecargado"
  `calcular_costo_total()` (simulado con `*args`, ya que Python no tiene
  sobrecarga real de métodos): admite 0, 1 o 2 parámetros (impuesto,
  descuento).
- `sistema_fj/excepciones/errores_reserva.py`: `ErrorReserva`,
  `ErrorEstadoReserva` y `ErrorServicioNoDisponible`.
- `sistema_fj/pruebas/servicio_de_prueba.py`: **clase temporal**
  `ServicioDePrueba`, usada solo para poder probar `Reserva` mientras la
  Parte 2 (clase `Servicio` y sus especializaciones) no esté lista.
  `Reserva` no depende de ninguna clase concreta: solo espera que el
  servicio tenga `describir()`, `calcular_costo(duracion)` y el atributo
  `disponible`. Cuando la Parte 2 esté lista, basta con reemplazar
  `ServicioDePrueba` por los servicios reales.
- `sistema_fj/pruebas/prueba_reserva.py`: simulación con 12 operaciones de
  reserva (creación, confirmación, cancelación, procesamiento), mezclando
  casos exitosos y fallidos.

### Cómo ejecutar el proyecto

```bash
python main.py
```

Esto corre la simulación de clientes (Parte 1) y la simulación de reservas
(Parte 3), mostrando en consola cada operación y dejando un historial
completo de eventos y errores en `logs/sistema_fj.log`.
