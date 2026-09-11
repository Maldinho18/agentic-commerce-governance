# Arquitectura v0 — Semana 6

## Propósito

La arquitectura separa las responsabilidades del flujo de compra para poder comparar posteriormente un flujo base (V1) contra un flujo gobernado (V2) sin reescribir el sistema completo.

## Componentes

### AgentOrchestrator
Coordina el flujo de compra. Recibe una intención ya estructurada, descubre ofertas, filtra restricciones, selecciona una alternativa y coordina checkout, pago y orden.

### MerchantSimulator
Representa comercios simulados. Cada merchant conserva su catálogo, disponibilidad, precio, checkout y creación de orden. Esto refleja la idea de que el comercio mantiene el estado autoritativo de la compra.

### PaymentMock
Simula el procesamiento del pago sin usar dinero ni credenciales reales.

### GovernanceGateway
Punto explícito de extensión entre decisión y ejecución. En V1 funciona en modo `bypass`. En Sprint 2 se reemplazará por validación de mandato, políticas, revalidación, revocación y escalamiento humano.

### EvidenceLogger
Registra eventos del flujo para reconstruir qué ocurrió: descubrimiento, selección, evaluación de governance, checkout, pago y orden.

## Flujo

```text
PurchaseRequest
      |
      v
AgentOrchestrator
      |
      +--> Merchant A
      +--> Merchant B
      |
      v
Product offers
      |
      v
Filter + selection
      |
      v
GovernanceGateway (bypass V1)
      |
      v
Merchant checkout
      |
      v
PaymentMock
      |
      v
Merchant order
      |
      v
Evidence log
```

## Fronteras de confianza

- El agente puede proponer una acción, pero no debe ser la autoridad final sobre sus propios permisos.
- El comercio controla catálogo, precio, stock, checkout y orden.
- El procesador de pago controla la aprobación del pago.
- La futura capa de governance decidirá si una acción propuesta está dentro de la autoridad delegada.
- El evidence log conecta decisiones y resultados para trazabilidad y atribución técnica.

## Decisiones de diseño de semana 6

1. Entorno completamente simulado por ausencia de acceso a sistemas de Bancolombia.
2. Python estándar para tener un baseline mínimo y reproducible sin infraestructura innecesaria.
3. Dos comercios simulados para que exista una decisión entre alternativas.
4. Pago mock, porque el objetivo de Sprint 1 es el flujo base, no integrar pagos reales.
5. Governance desacoplada y en bypass para permitir comparación V1/V2.
6. Evidencia presente desde V1 para que la comparación futura use la misma instrumentación.
