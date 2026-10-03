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
- F002 no está autorizada; F001 no declara el vídeo PRODUCTION_APPROVED.

El propietario autorizó publicar todo el trabajo actual en un repositorio público
y mantenerlo en `main`. Los documentos describen capacidades futuras; el estado
vigente y la evidencia de F001 están en su plan y validación.

## Documentos de entrada

| Documento | Responsabilidad |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Instrucciones operativas para agentes. |
| [constitution.md](constitution.md) | Principios y restricciones de máxima autoridad. |
| [mission.md](mission.md) | Producto, audiencia y resultados. |
| [tech-stack.md](tech-stack.md) | Tecnologías, límites y gates de validación. |
| [roadmap.md](roadmap.md) | Dependencias y secuencia de desarrollo. |
| [specs/README.md](specs/README.md) | Protocolo PLAN → aprobación → IMPLEMENT → VERIFY → HUMAN REVIEW → DONE. |

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
