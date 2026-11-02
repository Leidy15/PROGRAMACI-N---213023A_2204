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

### Cómo ejecutar esta parte

```bash
python main.py
```

Esto registra varios clientes de prueba en consola y deja un historial de
eventos y errores en `logs/sistema_fj.log`.
