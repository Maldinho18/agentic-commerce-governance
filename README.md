# Agentic Commerce Governance

Proyecto de grado — Universidad de los Andes · 2026-2

**Línea 02: Cuando una IA compra por ti**  
**Integrantes:** Sebastián Maldonado y Yair Andrade

## Objetivo

Construir y evaluar un flujo de compra agéntica end-to-end en un entorno simulado. La primera versión (V1) implementa el flujo base de descubrimiento, comparación/negociación, checkout, pago de prueba, orden y evidencia. Sobre la misma arquitectura se añadirá en el Sprint 2 una capa de governance con enforcement de mandato, políticas, revalidación, revocación y escalamiento humano.

## Estado actual — Semana 6

Este repositorio materializa los cuatro frentes activos de semana 6:

- **Flujo y fronteras de confianza:** responsabilidades separadas entre agente, comercio, pago, governance y evidencia.
- **Mandatos y políticas:** modelo inicial de autoridad delegada y reglas formales, todavía sin enforcement.
- **Evidencia y atribución:** registro de transacción, actor, componente, acción, decisión, mandato, política y resultado.
- **Sprint 1 — flujo base:** descubrimiento, selección, checkout, pago mock, orden y evidencia.

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
                         (inspección + BYPASS V1)
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

En V1 el `GovernanceGateway` inspecciona el mandato y las políticas, pero no bloquea. En V2 pasará a enforcement para permitir una comparación controlada entre flujo base y flujo gobernado.

## Mandato y políticas modeladas

El demo incluye un mandato de prueba con:

- monto máximo;
- comercios permitidos;
- marcas permitidas;
- vigencia;
- umbral de intervención humana.

Las políticas iniciales son:

```text
MAX_AMOUNT
ALLOWED_MERCHANT
ALLOWED_BRAND
VALIDITY
DELIVERY_DEADLINE
```

## Ejecutar demo

Requiere Python 3.11+ y no necesita dependencias externas.

```bash
git clone https://github.com/Maldinho18/agentic-commerce-governance.git
cd agentic-commerce-governance
git checkout week6-base
python -m src.main
```

Salida esperada aproximada:

```text
Compra simulada completada
order_id=ord_...
merchant=...
sku=...
total=...
governance=bypass_v1 (mandato y políticas inspeccionados, no aplicados)
evidence=artifacts/evidence.jsonl
```

La demo ejecuta una compra de audífonos con restricciones de precio y entrega, consulta dos comercios simulados, selecciona la mejor alternativa válida, inspecciona mandato/políticas, procesa un pago mock, crea una orden y guarda evidencia en `artifacts/evidence.jsonl`.

### Ver la evidencia

macOS/Linux:

```bash
cat artifacts/evidence.jsonl
```

PowerShell:

```powershell
Get-Content artifacts/evidence.jsonl
```

Windows CMD:

```cmd
type artifacts\evidence.jsonl
```

Busca eventos como `offer_selected`, `policy_inspected`, `governance_evaluated`, `payment_processed` y `order_created`. Cada línea incluye campos de atribución técnica.

## Ejecutar pruebas

```bash
python -m unittest discover -s tests -v
```

## Estructura

```text
.
├── docs/
│   ├── architecture.md
│   ├── presentation-guide.md
│   └── week-6-progress.md
├── scenarios/
│   └── scenarios.json
├── src/
│   ├── agent/
│   ├── evidence/
│   ├── governance/
│   │   ├── gateway.py
│   │   ├── mandate.py
│   │   └── policies.py
│   ├── merchants/
│   ├── payments/
│   ├── models.py
│   └── main.py
├── tests/
│   └── test_end_to_end.py
└── README.md
```

## Alcance actual

La implementación es deliberadamente pequeña y reproducible. No usa credenciales reales, dinero real, sistemas de Bancolombia ni protocolos completos de producción. El entorno simulado permite aislar el problema de investigación y construir un baseline comparable antes de incorporar enforcement de governance.

## Próximos pasos

1. estabilizar V1 durante semanas 6–8;
2. ampliar escenarios y fallos controlados;
3. transformar inspección de políticas en enforcement durante Sprint 2;
4. incorporar revalidación, revocación y escalamiento humano;
5. ejecutar la misma matriz sobre V1 y V2;
6. medir utilidad end-to-end, control, consentimiento, trazabilidad, atribución y reproducibilidad.
