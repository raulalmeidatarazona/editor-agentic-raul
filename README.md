# Raúl Almeida Agentic Video Studio

Sistema de producción audiovisual para la marca personal de Raúl Almeida:
idea → captura real → producción asistida → revisión humana → entrega aprobada.

El primer objetivo es un vídeo vertical basado en voz y footage reales, con
edición semántica, explicaciones visuales, captions y audio claro. La arquitectura
y los criterios de aceptación se desarrollan mediante Spec-Driven Development.

## Estado actual

- Fase 0: base documental y convenciones `OWNER_APPROVED`.
- F001: `DONE`; evidencia e5 aceptada expresamente por Raúl el 2026-10-03
  conforme al bundle r1. V-01–V-10 y AC-01–AC-10 PASS; identidad del RAW,
  recuperación, revisión humana y limitaciones retenidas.
- F002 r1 del commit `ae36327` y D001 aprobados expresamente; IMPLEMENT/VERIFY
  de ingestión e inspección local completados. `DONE`: evidencia e1 aceptada
  por Raúl el 2026-10-04, implementación `3e53205`; V-01–V-14 y AC-01–AC-10
  PASS. Estado, acta y hashes exactos en su plan/validación.
- F003: PLAN ONLY autorizado; bundle r1 en `PLAN_READY`, pendiente de aprobación.
  D002 propuesto; ninguna implementación, llamada STT ni upload autorizados.
  Ninguna aceptación declara un vídeo PRODUCTION_APPROVED.

El propietario autorizó publicar todo el trabajo actual en un repositorio público
y mantenerlo en `main`. Los documentos describen capacidades futuras; el estado
vigente y la evidencia de cada feature están en su plan y validación.

## Documentos de entrada

| Documento | Responsabilidad |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Instrucciones operativas para agentes. |
| [constitution.md](constitution.md) | Principios y restricciones de máxima autoridad. |
| [mission.md](mission.md) | Producto, audiencia y resultados. |
| [tech-stack.md](tech-stack.md) | Tecnologías, límites y gates de validación. |
| [roadmap.md](roadmap.md) | Dependencias y secuencia de desarrollo. |
| [specs/README.md](specs/README.md) | Protocolo PLAN → aprobación → IMPLEMENT → VERIFY → HUMAN REVIEW → DONE. |

## F003 — PLAN de transcripción alineada

- [Requisitos y contrato canónico v1](specs/features/F003-time-aligned-transcription/requirements.md)
- [Plan, investigación oficial y gate de aprobación](specs/features/F003-time-aligned-transcription/plan.md)
- [Validación predefinida de texto, tiempo, fallos y coste](specs/features/F003-time-aligned-transcription/validation.md)
- [D002 — proveedor inicial, propuesta pendiente](specs/decisions/D002-initial-f003-stt-provider.md)

Qwen Filetrans Singapore/International es candidato documentado; la precisión
en el fixture sigue sin validar. Respuesta saneada retenida, replay local, una
solicitud real propuesta y transporte privado gestionado por el propietario.
F001/F002 permanecen intactos; F004 no autorizado.

## F001 — Captura real y calibración STUDIO

- [Requisitos](specs/features/F001-real-capture-fixture/requirements.md)
- [Plan, instrucciones de grabación y aprobación de r1](specs/features/F001-real-capture-fixture/plan.md)
- [Contrato de validación](specs/features/F001-real-capture-fixture/validation.md)
- [Bundle r1 exacto y hashes aprobados](.local/spec-approvals/F001/r1/SHA256SUMS)
- [Notas de referencia y evidencia](.local/fixtures/F001-studio-001/reference-notes.md)

El original STUDIO `C0216.MP4` y su sidecar se conservan sin cambios en
`.local/fixtures/F001-studio-001/raw/`; metadata, hashes, logs y frames pequeños
están en `evidence/`, fuera de Git. La recuperación y referencias están verificadas; e5 aceptada y F001 DONE.
El RAW MOBILE permanece separado como candidato futuro, fuera de F001.

## F002 — Ingestión e inspección local

- [Requisitos y contrato v1](specs/features/F002-content-project-ingestion/requirements.md)
- [Plan, aprobación y estado](specs/features/F002-content-project-ingestion/plan.md)
- [Validación](specs/features/F002-content-project-ingestion/validation.md)
- [D001 aceptada](specs/decisions/D001-local-source-contract.md)
- [Comandos y recuperación](docs/F002-ingestion.md)

Python estándar y FFmpeg/ffprobe existentes. Copia íntegra, inventario audiovisual,
orientación de presentación y reloj basado en PTS. Proyectos y evidencia generada
en `.local/`, sin transcripción ni edición. READY del input no es aceptación de
feature ni aprobación de producción.

## Skills y archivos locales

Las 28 skills HyperFrames están instaladas dentro del proyecto en `.agents/skills/`;
`.hermes/skills/` contiene enlaces relativos a esas mismas copias.
[skills-lock.json](skills-lock.json) registra sus fuentes y fingerprints.
La auditoría y las reglas para usarlas están en el protocolo SDD.

Por decisión expresa del propietario se versionan los cinco documentos pequeños
actuales bajo `.local/`: el bundle r1, su manifest y las notas de
referencia. RAW, previews, outputs, caches y credenciales siguen excluidos por
[.gitignore](.gitignore). Los assets incluidos en las skills forman parte de su
snapshot de terceros y conservan los avisos/licencias suministrados.
