# Agentic Commerce Governance

Proyecto de grado — Universidad de los Andes · 2026-2

**Línea 02: Cuando una IA compra por ti**  
**Integrantes:** Sebastián Maldonado y Yair Andrade

## Objetivo

Construir y evaluar un flujo de compra agéntica end-to-end en un entorno simulado. La primera versión (V1) implementa el flujo base de descubrimiento, comparación/negociación, checkout, pago de prueba, orden y evidencia. Sobre la misma arquitectura se añadirá en el Sprint 2 una capa de governance para mandato, políticas, revalidación, revocación y escalamiento humano.

## Estado actual — Semana 6

Este repositorio contiene la base del **Sprint 1 (semanas 6–8)**:

- comercio simulado con dos merchants;
- descubrimiento y comparación de productos;
- orquestador de compra;
- checkout simulado;
- pago simulado sin dinero real;
- creación de orden;
- registro de evidencia auditable;
- escenarios iniciales y pruebas automáticas;
- punto explícito de extensión para governance.

## Arquitectura V1

```text
Usuario
  |
  v
PurchaseRequest
  |
  v
AgentOrchestrator
  |
  +--> Merchant A ----+
  |                   |
  +--> Merchant B ----+--> candidatos --> selección
                                      |
                                      v
                            GovernanceGateway
                               (BYPASS en V1)
                                      |
                                      v
                                  Checkout
                                      |
                                      v
                                PaymentMock
                                      |
                                      v
                                    Order
                                      |
                                      v
                                Evidence Log
```

En V2 el `GovernanceGateway` dejará de ser un bypass y evaluará mandato, límites de autoridad, revalidación y escalamiento.

## Ejecutar demo

Requiere Python 3.11+ y no necesita dependencias externas.

```bash
python -m src.main
```

La demo ejecuta una compra de audífonos con restricciones de precio y entrega, consulta dos comercios simulados, selecciona la mejor alternativa válida, procesa un pago mock, crea una orden y guarda evidencia en `artifacts/evidence.jsonl`.

## Ejecutar pruebas

```bash
python -m unittest discover -s tests -v
```

## Estructura

```text
.
├── docs/
│   ├── architecture.md
│   └── week-6-progress.md
├── scenarios/
│   └── scenarios.json
├── src/
│   ├── agent/
│   ├── evidence/
│   ├── governance/
│   ├── merchants/
│   ├── payments/
│   ├── models.py
│   └── main.py
├── tests/
│   └── test_end_to_end.py
└── README.md
```

## Alcance actual

La implementación es deliberadamente pequeña y reproducible. No usa credenciales reales, dinero real, sistemas de Bancolombia ni protocolos completos de producción. El entorno simulado permite aislar el problema de investigación y construir un baseline comparable antes de incorporar governance.

## Próximos pasos

1. estabilizar V1 durante semanas 6–8;
2. ampliar escenarios y fallos controlados;
3. incorporar mandato y motor de políticas en semanas 9–11;
4. ejecutar la misma matriz sobre V1 y V2;
5. medir utilidad end-to-end, control, consentimiento, trazabilidad, atribución y reproducibilidad.
