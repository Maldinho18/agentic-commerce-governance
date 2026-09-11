# Avance — Semana 6

## Objetivo de la semana

Iniciar el Sprint 1 del plan de trabajo y materializar los cuatro frentes activos de semana 6:

1. flujo y fronteras de confianza;
2. mandatos y políticas;
3. evidencia y atribución;
4. Sprint 1 — flujo base end-to-end.

## Contexto confirmado con el profesor

- Bancolombia aporta el contexto del problema y los lineamientos de la línea.
- No se espera acceso a sistemas internos por razones de privacidad.
- El equipo tiene libertad para elegir el stack tecnológico.
- El entorno donde opera el agente será simulado por el equipo.
- La arquitectura y el nivel de autonomía son decisiones de diseño del proyecto.

## Qué se construyó

### 1. Flujo y fronteras de confianza

Se definió una arquitectura modular donde las responsabilidades están separadas:

- `AgentOrchestrator`: descubre, compara y propone una acción;
- `MerchantSimulator`: conserva catálogo, precio, stock, checkout y orden;
- `PaymentMock`: representa al procesador de pago;
- `GovernanceGateway`: separa la decisión del agente de la autorización;
- `EvidenceLogger`: conserva evidencia de decisiones y resultados.

Esto evita que el agente sea juez de sus propios permisos y prepara el sistema para V2.

### 2. Mandatos y políticas

Se añadió un modelo explícito de `Mandate` con:

- monto máximo;
- comercios permitidos;
- marcas permitidas;
- vigencia;
- umbral de intervención humana.

También se formalizaron políticas iniciales:

- `MAX_AMOUNT`;
- `ALLOWED_MERCHANT`;
- `ALLOWED_BRAND`;
- `VALIDITY`;
- `DELIVERY_DEADLINE`.

En V1 estas políticas se inspeccionan y registran, pero deliberadamente **no bloquean** la compra. Esto mantiene limpio el baseline de Sprint 1 y deja preparado el enforcement de Sprint 2.

### 3. Evidencia y atribución

Cada evento importante registra:

- `transaction_id`;
- `actor`;
- `component`;
- `action`;
- `decision_id`;
- `mandate_id` cuando aplica;
- `policy_id` cuando aplica;
- `result`;
- payload del evento.

Esto permite reconstruir quién hizo qué, en qué componente, bajo qué decisión y con qué resultado.

### 4. Sprint 1 — flujo base

Ya existe un baseline donde una solicitud estructurada recorre:

```text
intención estructurada
→ descubrimiento multi-merchant
→ filtrado y selección
→ inspección de governance en bypass
→ checkout
→ pago mock
→ orden
→ evidencia
```

## Qué demuestra este avance

La semana 6 deja de ser únicamente exploratoria. Ya existe una arquitectura ejecutable que materializa el inicio de V1 y, al mismo tiempo, deja definidos los contratos de mandato, políticas, atribución y fronteras de confianza que serán usados en V2.

El diseño mantiene separadas dos preguntas distintas:

1. **¿Qué quiere hacer el agente?** — decisión/orquestación.
2. **¿Está autorizado a hacerlo?** — governance.

Esta separación permitirá comparar el mismo flujo con y sin controles de autoridad.

## Qué NO se pretende resolver todavía

- implementación completa de ACP, UCP, AP2 o TAP;
- pagos reales;
- credenciales personales;
- integración con sistemas de Bancolombia;
- enforcement completo de políticas;
- revocación, revalidación y human-in-the-loop.

Esos elementos corresponden a etapas posteriores o se emularán solo cuando aporten a la pregunta de investigación.

## Próximos pasos — semanas 7 y 8

1. ampliar escenarios y excepciones controladas;
2. mejorar la representación de intención;
3. instrumentar métricas básicas de éxito/fallo;
4. estabilizar el prototipo V1 end-to-end;
5. cerrar el contrato de entrada/salida del `GovernanceGateway`;
6. preparar el paso de inspección a enforcement para Sprint 2.

## Mensaje breve para sustentación

> En semana 6 comenzamos formalmente el Sprint 1 y aterrizamos los cuatro frentes que aparecen activos en el cronograma. Definimos las fronteras de confianza, construimos un baseline end-to-end con dos comercios simulados, formalizamos un modelo inicial de mandato y políticas, y enriquecimos la evidencia con atribución técnica. La gobernanza todavía está en bypass porque queremos que V1 sea nuestro baseline; en Sprint 2 activaremos esos controles sobre la misma arquitectura para poder comparar ambos flujos.
