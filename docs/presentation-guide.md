# Guía de presentación — Semana 6

## Mensaje central

La semana 6 marca el paso de exploración a implementación. El objetivo no es demostrar que el proyecto está terminado, sino que ya existe una arquitectura base y un primer flujo ejecutable sobre el cual se construirán y evaluarán los controles de governance.

## Guion de 2–3 minutos

### 1. Contexto

> Bancolombia nos dio el problema y los lineamientos, pero por privacidad no tendremos acceso a sus sistemas internos. El profesor confirmó que tenemos libertad para proponer el stack, la arquitectura y el entorno simulado. Por eso decidimos construir un laboratorio controlado y reproducible.

### 2. Qué corresponde a semana 6

> Según nuestro plan, en semana 6 están activos cuatro frentes: flujo y fronteras de confianza, mandatos y políticas, evidencia y atribución, y el inicio del Sprint 1.

### 3. Flujo y fronteras de confianza

> Separamos responsabilidades. El agente descubre y propone una decisión; el comercio conserva catálogo, precio, inventario, checkout y orden; el procesador de pago aprueba o rechaza; governance está entre la decisión y la ejecución; y evidence conserva el rastro técnico. Así evitamos que el agente sea la autoridad final sobre sus propios permisos.

### 4. Sprint 1

> Ya construimos un baseline end-to-end. Una solicitud estructurada consulta dos comercios simulados, obtiene ofertas, filtra las que cumplen las restricciones, selecciona una alternativa, genera checkout, procesa un pago mock, crea una orden y registra evidencia.

### 5. Mandatos y políticas

> Aunque el enforcement corresponde al flujo gobernado, en semana 6 ya formalizamos el contrato. Tenemos un mandato con monto máximo, comercios permitidos, marcas, vigencia y umbral de intervención humana. También definimos políticas como MAX_AMOUNT, ALLOWED_MERCHANT, ALLOWED_BRAND, VALIDITY y DELIVERY_DEADLINE. En V1 se inspeccionan, pero no bloquean; eso es deliberado para mantener un baseline limpio.

### 6. Evidencia y atribución

> No guardamos únicamente logs genéricos. Cada evento puede registrar transaction_id, actor, componente, acción, decision_id, mandate_id, policy_id y resultado. Eso nos permitirá reconstruir qué componente hizo qué y conectar la decisión con la evidencia transaccional.

### 7. Qué sigue

> En semanas 7 y 8 vamos a estabilizar V1 y ampliar escenarios. En Sprint 2 activaremos el enforcement de governance, revalidación, revocación y escalamiento humano sobre la misma arquitectura. Así podremos comparar V1 y V2 con la misma matriz experimental.

## Qué mostrar en pantalla

1. `README.md`: arquitectura general y comandos de ejecución.
2. `docs/architecture.md`: fronteras de confianza.
3. `src/governance/mandate.py`: representación de autoridad delegada.
4. `src/governance/policies.py`: reglas formalizadas.
5. ejecutar `python -m src.main`.
6. abrir `artifacts/evidence.jsonl` y mostrar eventos `policy_inspected`, `governance_evaluated` y `order_created`.
7. opcional: ejecutar `python -m unittest discover -s tests -v`.

## Si preguntan por qué governance está en bypass

> Porque queremos un baseline experimental. Si activáramos los controles desde el primer prototipo no tendríamos una V1 comparable. El gateway ya existe y las políticas ya se pueden inspeccionar, pero el bloqueo se activa en Sprint 2 para medir de forma controlada el aporte de governance.

## Si preguntan por qué simulamos los comercios

> El profesor confirmó que no tendremos acceso a sistemas internos de Bancolombia y que debemos proponer el ambiente. El entorno simulado nos permite controlar inventario, precios, excepciones y condiciones de prueba, además de hacer los experimentos reproducibles.

## Si preguntan por los protocolos

> ACP, UCP, AP2 y TAP son referentes para separar responsabilidades del ecosistema. En este Sprint no buscamos implementar todos los protocolos de producción; estamos construyendo una arquitectura de referencia sobre la cual luego podemos emular o integrar las capacidades que sean relevantes para responder la pregunta de investigación.

## Si preguntan cuál es el aporte de la tesis

> El aporte no es solamente que un agente logre comprar. Queremos estudiar cómo gobernar esa autonomía de extremo a extremo: autoridad delegada, políticas, excepciones, trazabilidad y atribución, y medir qué cambia frente a un flujo base sin esos controles.
