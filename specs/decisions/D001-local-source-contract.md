# D001 — Fuente local, contrato de ingestión y reloj de fuente

**Status:** Proposed — NOT ACCEPTED\
**Fecha:** 2026-10-03\
**Feature:** [F002 r1](../features/F002-content-project-ingestion/plan.md)\
**Autoridad:** [Constitución](../../constitution.md), [misión](../../mission.md),
[tech-stack §§6/11/13](../../tech-stack.md), [roadmap Fases 2–3](../../roadmap.md)

## Contexto

F001 está DONE, e5, cierre 7e0bc22. F002 debe convertir un archivo real en input
recuperable sin alterar su contenido ni implementar transcripción. Local files y
FFmpeg/ffprobe ya son dirección aprobada; lenguaje, contrato y tiempos no estaban
elegidos. Fuente/identidad/reloj afectan a F003 y posteriores, por lo que requieren
este ADR; los detalles internos de código permanecen en el PLAN F002.

## Decisión propuesta

1. Un Content Project F002 posee **una copia completa verificada** de una fuente
   principal, un manifest de procedencia y revisiones derivadas de inspección.
   No depende para operar de la ruta original. No hay link/hardlink como sustituto
   de la copia; no se transcodifica ni normaliza. Audio separado/múltiples captures
   requieren una feature posterior.
2. JSON UTF-8 versionado conserva el dominio independiente de ffprobe, Python,
   STT y renderer. Bytes/SHA-256 identifican la fuente; hashes de manifest y
   artefactos vinculan cada revisión. El probe original es evidencia de herramienta,
   no el contrato del consumidor. El esquema mínimo lo define requirements.md.
3. Reloj `source-presentation-v1`: cero en el primer PTS presentado del vídeo
   seleccionado; segundos racionales exactos, offsets de audio preservados,
   incluso negativos. No confundir PTS con DTS, timecode de cámara, fecha o tiempo
   editado. La identidad del reloj incluye hash de fuente, vídeo y origen PTS.
4. Para F002, **Python 3.14.7 ya disponible + biblioteca estándar**, con invocaciones
   locales de FFmpeg/ffprobe 9.0.1 ya disponibles. Se necesita código pequeño para
   copiar/hash, validar JSON, racionales, transacciones y pruebas de fallos; una
   colección de comandos manuales no entrega ese comportamiento repetible.
   Sin pip, framework, package manager, modelo, API ni nuevo servicio. La versión
   efectiva se registra y verifica antes de IMPLEMENT. Un runtime distinto exige
   revisar compatibilidad; no instalar/actualizar automáticamente.

Es una propuesta para aceptación conjunta con F002 r1, no arquitectura ya
adoptada. No elige lenguaje universal, provider, transcript, EDL, composición o
normalización futura. Ninguna aceptación de este documento modifica por sí sola
los cuatro specs raíz. Tras aceptación explícita, registrar allí solo la resolución
de lenguaje/contrato antes de implementar, según la superficie del PLAN.

## Alternativas

| Alternativa | Motivo de preferir la propuesta |
| --- | --- |
| Referencia absoluta al original | Ahorra disco, pero desconectar/mover el disco rompe el proyecto y exige otro modo de recuperación. |
| Hardlink/symlink | Comparte mutaciones o disponibilidad; no da propiedad independiente del contenido. |
| JSON ffprobe como dominio | Filtra convenciones y ausencias del vendor; no establece reloj, integridad ni readiness. |
| FPS × índice o timestamps flotantes | No conserva VFR, offsets ni precisión racional. |
| Cero de audio o de contenedor | Puede variar al elegir otra pista o ser desconocido; el vídeo presentado es referencia estable para F003 y edición audiovisual. |
| Shell/jq | Requeriría parsing, aritmética y validación/transacciones repartidos, y posiblemente jq adicional. |
| Node/TypeScript | Posible, pero TypeScript añade toolchain y racionales grandes requieren tratamiento propio; no necesitamos runtime del renderer en ingestión. |
| Go | Posible, pero compilación/distribución no resuelven una necesidad F002; stdlib de Python cubre JSON, SHA-256, filesystem, Fraction y unittest. |

## Consecuencias

Una copia de C0216.MP4 ocupa otros 2.873.163.442 bytes, más inspección/evidencia.
Se comprueba espacio antes de copiar; fuente y recovery F001 se conservan. No se
promete backup independiente del disco local: la copia de trabajo y la referencia
de recuperación son conceptos distintos. Futuros consumidores deberán verificar
hashes y usar el reloj publicado; deberán mapear su propio reloj de audio al reloj
de fuente, sin que F002 implemente extracción o STT.

Los artefactos F002 se pueden regenerar conservando fuente/manifest. La validación
real y negativa del bundle debe demostrar portabilidad, integridad, tiempos y
fallos; documentación del proveedor no constituye esa prueba. Cambios materiales
de este contrato requieren revisión de PLAN/ADR y evaluación de consumidores.

## Aceptación

**Owner acceptance:** NOT GRANTED. Approver, fecha y palabras reales: pendientes.
Aceptar F002 r1 debe mencionar explícitamente D001; no se infiere de silencio.
