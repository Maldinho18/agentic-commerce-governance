# Avance — Semana 6

## Objetivo de la semana

Iniciar el Sprint 1 del plan de trabajo: construir e instrumentar el flujo base end-to-end de descubrimiento, comparación/negociación, checkout, orden y pago en un entorno controlado.

## Contexto confirmado con el profesor

- Bancolombia aporta el contexto del problema y los lineamientos de la línea.
- No se espera acceso a sistemas internos por razones de privacidad.
- El equipo tiene libertad para elegir el stack tecnológico.
- El entorno donde opera el agente será simulado por el equipo.
- La arquitectura y el nivel de autonomía son decisiones de diseño del proyecto.

## Qué se construyó

- estructura inicial del repositorio;
- modelos de dominio para solicitud, oferta, checkout, pago y orden;
- dos comercios simulados con catálogo, stock, precio y tiempos de entrega;
- descubrimiento de ofertas entre varios comercios;
- selección automática usando restricciones de precio, entrega y marca;
- checkout simulado;
- pago mock sin dinero real;
- creación de orden;
- registro estructurado de evidencia;
- punto de extensión `GovernanceGateway` para el Sprint 2;
- pruebas automatizadas para compra válida y ausencia de oferta válida.

## Qué demuestra este avance

La semana 6 deja de ser únicamente exploratoria y materializa el inicio de V1. Ya existe una arquitectura ejecutable en la que una intención estructurada puede recorrer el flujo comercial hasta producir una orden y evidencia de lo ocurrido.

El diseño mantiene separadas dos preguntas distintas:

1. **¿Qué quiere hacer el agente?** — decisión/orquestación.
2. **¿Está autorizado a hacerlo?** — governance, que se incorporará en V2.

Esta separación permitirá comparar el mismo flujo con y sin controles de autoridad.

## Qué NO se pretende resolver todavía

- implementación completa de ACP, UCP, AP2 o TAP;
- pagos reales;
- credenciales personales;
- integración con sistemas de Bancolombia;
- motor completo de políticas;
- revocación, revalidación y human-in-the-loop.

Estos elementos se incorporarán o emularán únicamente cuando aporten a la pregunta de investigación.

## Próximos pasos — semanas 7 y 8

1. incorporar más escenarios y excepciones controladas;
2. mejorar la representación de intención;
3. definir estrategia de comparación entre alternativas;
4. instrumentar métricas básicas de éxito/fallo;
5. estabilizar el prototipo V1 end-to-end;
6. cerrar el contrato del `GovernanceGateway` para iniciar Sprint 2.

## Mensaje breve para sustentación

> En semana 6 comenzamos formalmente el Sprint 1. Como no tendremos acceso a sistemas reales de Bancolombia, diseñamos un entorno comercial simulado y una arquitectura modular. Ya tenemos un baseline donde el agente consulta varios comercios, filtra restricciones, selecciona una oferta, ejecuta checkout, procesa un pago simulado, crea una orden y deja evidencia. La capa de governance está desacoplada y en bypass en V1, de modo que en Sprint 2 podamos activarla con mandatos y políticas y comparar ambos flujos sobre la misma arquitectura.
