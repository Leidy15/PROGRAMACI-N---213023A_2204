# PROGRAMACI-N---213023A_2204

**Fase 4 - Componente práctico - Prácticas simuladas**  
**Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas**  
**Empresa: Software FJ**

---

## Descripción del proyecto

Sistema orientado a objetos (sin bases de datos) que gestiona clientes, servicios y reservas. Implementa de forma rigurosa:

- Abstracción (clases abstractas)
- Encapsulación
- Herencia
- Polimorfismo (métodos sobrescritos)
- Métodos sobrecargados (simulados con `*args`)
- Manejo avanzado de excepciones (personalizadas, try/except/else/finally, encadenamiento)
- Registro de eventos y errores en archivo de logs
- Listas internas en memoria

El sistema continúa funcionando ante errores y registra todo en `logs/sistema_fj.log`.

---

## Estructura del proyecto

```
PROGRAMACI-N---213023A_2204/
├── main.py                          # Punto de entrada
├── README.md
├── logs/
│   └── sistema_fj.log               # Se genera al ejecutar
└── sistema_fj/
    ├── __init__.py
    ├── modelos/
    │   ├── entidad_base.py          # Clase abstracta base
    │   ├── cliente.py               # Clase Cliente
    │   ├── servicio.py              # Clase abstracta Servicio + 3 especializaciones
    │   └── reserva.py               # Clase Reserva
    ├── excepciones/
    │   ├── errores_generales.py
    │   ├── errores_cliente.py
    │   ├── errores_servicio.py
    │   └── errores_reserva.py
    ├── utilidades/
    │   └── registro_eventos.py      # Logs con rotación
    └── pruebas/
        ├── prueba_cliente.py        # Simulación Parte 1
        ├── prueba_servicios.py      # Simulación Parte 2
        ├── prueba_reserva.py        # Simulación Parte 3
        ├── prueba_excepciones.py    # Simulación Parte 4
        └── prueba_integracion.py    # Simulación Parte 5 (listas + 10+ operaciones)
```

---

## Partes del trabajo

### Parte 1: Gestión de Clientes y Abstracción Base
- `EntidadBase` (clase abstracta)
- `Cliente` con encapsulación y validaciones estrictas
- Excepción `ErrorValidacionCliente`
- Simulación de registros válidos e inválidos

### Parte 2: Jerarquía de Servicios (Herencia y Polimorfismo)
- Clase abstracta `Servicio`
- `ReservaSala` (capacidad, premium)
- `AlquilerEquipo` (depósito opcional)
- `AsesoriaEspecializada` (nivel del asesor: junior/semi/senior)
- Métodos sobrescritos: `calcular_costo`, `describir`, `validar_parametros`

### Parte 3: Gestión de Reservas y Métodos Sobrecargados
- Clase `Reserva` (ciclo de vida: pendiente → confirmada → procesada / cancelada)
- Métodos `confirmar()`, `cancelar()`, `procesar()`
- `calcular_costo_total()` con 0, 1 o 2 parámetros (impuesto / descuento)

### Parte 4: Sistema de Excepciones Avanzadas y Logs
- Jerarquía de excepciones personalizadas
- `try/except`, `try/except/else`, `try/except/finally`
- Encadenamiento de excepciones (`raise ... from`)
- Archivo de logs con rotación automática
- Función `ejecutar_de_forma_segura` como último respaldo

### Parte 5: Integración, Listas Internas y Simulación
- Listas en memoria: `lista_clientes`, `lista_servicios`, `lista_reservas`
- Simulación integrada de más de 10 operaciones completas (válidas e inválidas)
- El programa nunca se detiene ante errores

---

## Cómo ejecutar

```bash
python main.py
```

Esto ejecuta todas las simulaciones en orden y genera el archivo de log en `logs/sistema_fj.log`.

También se puede ejecutar cada simulación por separado:

```bash
python -m sistema_fj.pruebas.prueba_cliente
python -m sistema_fj.pruebas.prueba_servicios
python -m sistema_fj.pruebas.prueba_reserva
python -m sistema_fj.pruebas.prueba_excepciones
python -m sistema_fj.pruebas.prueba_integracion
```

---

## Requisitos cumplidos

| Requisito | Estado |
|-----------|--------|
| Clase abstracta general | ✅ `EntidadBase` |
| Clase Cliente con encapsulación y validaciones | ✅ |
| Clase abstracta Servicio + 3 especializaciones | ✅ |
| Polimorfismo (métodos sobrescritos) | ✅ |
| Clase Reserva (confirmación, cancelación, procesamiento) | ✅ |
| Métodos sobrecargados (costo con impuesto/descuento) | ✅ |
| Excepciones personalizadas | ✅ |
| try/except, try/except/else, try/except/finally | ✅ |
| Encadenamiento de excepciones | ✅ |
| Archivo de logs | ✅ |
| Listas internas (sin base de datos) | ✅ |
| ≥ 10 operaciones completas (válidas e inválidas) | ✅ |
| El sistema no se detiene ante errores | ✅ |
