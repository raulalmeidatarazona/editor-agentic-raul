# F003 — referencia humana reutilizable

Este documento conserva el método, la localización de los materiales y los
pendientes de la referencia F003. No es una nueva transcripción ni un resultado
STT. R1 aprobado: `74aaa0b`; estado y aceptación en
[plan.md](../specs/features/F003-time-aligned-transcription/plan.md).

## Fuente y procedimiento

C0216.MP4, proyecto F002 `f002-studio-001`, SHA-256
`68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`.
Canal 1; reloj `source-presentation-v1`, origen audio `0/1`, duración `1164/5` s.
WAV SHA-256 `4c71d1689fdec2fb419ec6b91cb6ca0317a0b172b594e3b6ab7532cbe00645f3`.
Estos datos son MEASURED; no identifican un micrófono por inferencia.

Raúl confirmó la comparación de ambos canales y la escucha completa del canal 1
a 1×. En su mensaje de continuación confirmó escucha y comparación con el texto
presentado, fidelidad del español/términos, presencia y orden de Again/try again,
correspondencia con la fuente autoritativa y concordancia acústica a precisión
humana normal. Método **listen-and-compare**, revisor **Raúl Almeida**,
evidencia **USER_VERIFIED / HUMAN_VERIFIED**. No se atribuye a Raúl la autoría de
una transcripción independiente nueva; tampoco se transforma ese juicio en
precisión de milisegundos.

Acta literal y evaluación: `.local/validation/F003/preflight-p3/owner-message.txt`
y `human-verification.json`. Raúl explicó posteriormente que había ejecutado un
script Python que devolvió el material, pero no tiene los artefactos disponibles ahora.
Nombre/ruta del script, salida exacta y producción original del texto: UNKNOWN.

## Material local conservado

| Ventana fuente | Audio canal 1 | Texto literal retenido en reference.json |
| --- | --- | --- |
| [0,25) s | [Apertura](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/validation/F003/work-e1/listening/channel-1/opening.wav) | UNKNOWN |
| [60,85) s | [Técnica](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/validation/F003/work-e1/listening/channel-1/technical.wav) | UNKNOWN |
| [90,115) s | [Corrección](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/validation/F003/work-e1/listening/channel-1/correction.wav) | UNKNOWN |
| [130,155) s | [try again](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/validation/F003/work-e1/listening/channel-1/ordinary-again.wav) | UNKNOWN |
| [195,228) s | [Cierre](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/validation/F003/work-e1/listening/channel-1/ending.wav) | UNKNOWN |

CSV/SVG por ventana en esos mismos directorios: medición PCM cada 20 ms,
sin identificación automática de palabras o bordes acústicos.

[Referencia estructurada local](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/validation/F003/work-e1/reference.json).
Las cinco ventanas siguen sin texto; recuento de palabras recuperables en ellas:
**0**. El número de palabras del material exacto que Raúl revisó es **UNKNOWN**,
porque su identidad no está recuperada. No se confunden ambos recuentos.

Existe una tabla antigua de citas reconocidas por máquina en
[handoff F001](/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/handoff-e3.txt:77).
Su procedencia sigue siendo reconocimiento automático sobre una copia comprimida,
con tiempos aproximados y alternativas UNCERTAIN. La nueva confirmación no
identifica esa tabla como el texto exacto revisado para F003; no se adopta
automáticamente ni se eliminan sus alternativas para simular una referencia.
La aceptación F001 tampoco proporciona bordes acústicos precisos F003.

## Requisitos pendientes de r1

V-08 exige el texto exacto de las cinco ventanas, referencia anterior al candidato,
con ≥200 palabras. Faltan 200 palabras **retenidas en las ventanas** para alcanzar
el umbral; el déficit del material realmente revisado no puede calcularse sin
recuperarlo. El agente calculará los recuentos, hashes e índices automáticamente.
No se pide a Raúl volver a escribir un texto ya revisado.

V-09/V-10 exigen al menos 30 controles, los grupos/ocurrencias predefinidos,
intervalos de onset/offset con incertidumbre ≤50 ms y tres núcleos de pausa.
Los 39 controles preparados conservan bordes UNKNOWN; ninguno tiene intervalos
numéricos recuperados. La conformidad humana general se registra, sin convertir
tiempos aproximados en límites exactos.

Para recuperar la referencia basta localizar el script/salida/documento exacto
revisado y su tabla de intervalos. Se preservará cómo se produjo el texto y se
comprobará su selección/procedencia. Si falta evidencia necesaria, el gate sigue
BLOCKED: no se inventan palabras, bordes ni una firma de aprobación.

Retomas/semántica permanecen fuera de F003. Ningún juicio aquí autoriza F004,
DONE o PRODUCTION_APPROVED. P1/P2 permanecen congelados y se conservan aparte.
