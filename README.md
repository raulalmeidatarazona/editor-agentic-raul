# Raúl Almeida Agentic Video Studio

Sistema de producción audiovisual para la marca personal de Raúl Almeida:
idea → captura real → producción asistida → revisión humana → entrega aprobada.

El primer objetivo es un vídeo vertical basado en voz y footage reales, con
edición semántica, explicaciones visuales, captions y audio claro. La arquitectura
y los criterios de aceptación se desarrollan mediante Spec-Driven Development.

## Estado actual

- Fase 0: base documental y convenciones `OWNER_APPROVED`.
- F001: bundle r1 aprobado; `IMPLEMENTING`, preparación local completada y
  pendiente de la grabación física de Raúl.
- La aceptación de F001 depende de su contrato de validación y revisión humana.

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
- [Notas de referencia preparadas](.local/fixtures/F001-studio-001/reference-notes.md)

Los originales de cámara vivirán en
`.local/fixtures/F001-studio-001/raw/`. Las carpetas vacías RAW/evidence no se
representan en Git; se preparan localmente según el plan. Conservar originales,
hashes y una copia recuperable antes de validar.

## Skills y archivos locales

Las 28 skills HyperFrames están instaladas dentro del proyecto en `.agents/skills/`;
`.hermes/skills/` contiene enlaces relativos a esas mismas copias.
[skills-lock.json](skills-lock.json) registra sus fuentes y fingerprints.
La auditoría y las reglas para usarlas están en el protocolo SDD.

Por decisión expresa del propietario se versionan los cinco documentos pequeños
actuales bajo `.local/`: el bundle r1, su manifest y las notas pendientes de
grabación. RAW, previews, outputs, caches y credenciales siguen excluidos por
[.gitignore](.gitignore). Los assets incluidos en las skills forman parte de su
snapshot de terceros y conservan los avisos/licencias suministrados.
