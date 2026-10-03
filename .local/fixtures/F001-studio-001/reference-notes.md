# F001-studio-001 — Notas de referencia

**Entrega de evidencia:** e2 (2026-10-03, Europe/Malta), abierta; revisión humana parcial registrada.  
**Aprobación aplicable:** bundle r1 archivado; no implica aceptación del fixture.  
**Fuente autoritativa designada por Raúl:** `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216.MP4`. No se selecciona por antigüedad del archivo.

## Clasificación de evidencia

- **MEASURED:** bytes, hashes y propiedades registradas por herramientas; una fecha o modelo declarado por metadata no prueba por sí solo el hecho físico.
- **OBSERVED:** inspección visual de los frames indicados; cobertura limitada a esas muestras.
- **USER-REPORTED:** afirmación explícita de Raúl, con mensaje y fecha; no se convierte en medición.
- **UNKNOWN:** no se ha establecido; no se infiere ni se sustituye por el guion opcional.

## Identidad y recuperación

| Rol / clasificación | Nombre original / ruta absoluta | Bytes | SHA-256 |
| --- | --- | --- | --- |
| Principal — MEASURED | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216.MP4` | 2.873.163.442 | `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc` |
| Sidecar Sony asociado por nombre — MEASURED; no es toma auxiliar | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216M01.XML` | 1.933 | `155550ef95eaf6e885e6e5be67667c8089e4060c774023cbfa0f34ad14c1bde5` |

- **MEASURED:** fuente regular no vacía; hash inicial en `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/source.sha256`. Hash posterior en source-after.sha256: coincide con el inicial; bytes y mtime permanecen idénticos. Sidecar igualmente estable. Decodificación completa de streams 0/1: salida 0, decode.log vacío (0 bytes). Véanse decode-result.json e integrity-result.json.
- **USER-REPORTED:** Raúl declara el original recuperable en `videos/raw/C0216.MP4` de su disco duro externo y acceso disponible; mensaje de revisión humana del 2026-10-03.
- **MEASURED:** tras el montaje se localizó y leyó `/Volumes/PortableSSD/videos/raw/C0216.MP4`, 2.873.163.442 bytes; SHA-256 `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`, idéntico al RAW local. Lectura/hash finalizó 2026-10-03 16:05:28 Europe/Malta (14:05:28 UTC); resultado PASS, bytes/mtime del original externo estables. Acceso: conectar/montar PortableSSD y abrir esa ruta, sin sobrescribir/borrar originales. Evidencia: recovery.sha256 y recovery-result-e2.json. El intento inicial sin disco se conserva en recovery-location-check-e2.json; la localización posterior en recovery-location-check-mounted-e2.json.
- **MEASURED:** espacio disponible antes de crear evidencia: 113,259,212,800 bytes, según statvfs. No se ha vuelto a copiar ni recomprimido el RAW.
- **MEASURED:** RAW, sidecar, evidencia y MOBILE están excluidos por `/.local/`; solo las notas ya seleccionadas están versionadas. Media permanece local.

## Propiedades del RAW — MEASURED

| Campo | Valor informado |
| --- | --- |
| Contenedor / marca | QuickTime/MOV-MP4; XAVC |
| Duración contenedor, vídeo y audio | 232,800 s = 03:52,800; inicio 0,000 s |
| Vídeo seleccionado | stream 0; H.264/AVC High, avc1, yuv420p, 8 bits, progressive |
| Píxeles almacenados | 3840 × 2160 |
| SAR / DAR | 1:1 / 16:9 |
| FPS reportados | r_frame_rate 25/1; avg_frame_rate 25/1; no se declara CFR probado |
| Frames reportados / base temporal | 5.820; 1/25.000 |
| Display Matrix | rotation −90; matriz íntegra en ffprobe.json |
| Audio seleccionado para decodificar | stream 1, única pista audio integrada; USER-REPORTED: voz comprensible y DJI Mic Mini conectado a cámara; detalle físico de conexión UNKNOWN |
| Codec / frecuencia / canales | pcm_s16be, 16 bits, 48.000 Hz, 2 canales |
| Channel layout | UNKNOWN: no informado por ffprobe; no asignar etiquetas de canal |
| Idioma en tags | und (MEASURED tag); español hablado USER-REPORTED por Raúl |
| Metadata adicional | stream 2 rtmd, timecode declarado 03:22:25:23; no es tiempo de fuente mm:ss |
| Fecha del contenedor / streams | creation_time 2026-10-03T14:02:10.000000Z |
| Fecha/zona declarada por XML | 2026-10-03T15:02:10+01:00; exactitud del reloj y hora física UNKNOWN; zona Europe/Malta USER-REPORTED |
| Dispositivo declarado por XML | manufacturer Sony; modelName ZV-E10 (MEASURED metadata); cuerpo Sony ZV-E10 confirmado USER-REPORTED |
| Gamma/color declarados | XML rec709-xvycc / rec709; ffprobe bt709, transfer iec61966-2-4 |

No convertir creation_time en fecha real confirmada, ni metadatos de codificación en ajustes elegidos por Raúl. Focal, exposición, ISO, apertura, balance de blancos y lecturas de luces: **UNKNOWN** en las evidencias disponibles.

## Orientación y encuadre — OBSERVED

FFmpeg autorrota la imagen según su matriz al extraer estos tres pequeños frames. Las imágenes resultantes son 360 × 640, verticales 9:16 y con el sujeto erguido. Es vista de evidencia, no un nuevo RAW, crop, proxy de producción ni normalización F002. **USER-REPORTED:** Raúl confirma que se visualiza correctamente como vídeo vertical; concuerda con la vista de evidencia 9:16. **USER-REPORTED:** revisión con VLC a velocidad normal 1×.

| Archivo / tiempo de fuente conocido | Evidencia visual | Observación limitada |
| --- | --- | --- |
| C0216.MP4, 00:30 | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/frame-030s.png` | Cabeza completa con margen superior, hombros, torso y ambas manos visibles; sujeto aproximadamente centrado. Manos gesticulando; brazos llegan a bordes del frame. |
| C0216.MP4, 02:30 | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/frame-150s.png` | Cabeza, hombros y torso visibles; gesto con una mano levantada; parte de la otra mano alcanza el borde inferior. |
| C0216.MP4, 03:40 | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/frame-220s.png` | Cabeza, hombros, torso y manos visibles; sujeto aproximadamente centrado. |

**OBSERVED:** fondo liso iluminado con zonas azul/cian a la izquierda de la imagen y rosa/violeta a la derecha; dispositivo pequeño sujeto al pecho. Esto no prueba número/modelo/ajustes de luces, modelo de micrófono, su conexión ni teleprompter. No se estima safe zone, focal, distancia, zoom/crop ni calidad futura a partir de muestras reducidas. Los tres instantes no prueban los desplazamientos requeridos ni la continuidad del encuadre.

## Contexto de captura y hechos humanos pendientes

| Campo | Clasificación / hecho disponible |
| --- | --- |
| Perfil / captura física / designación | USER-REPORTED: Raúl declara STUDIO físico completo y designa este fixture autoritativo en el mensaje del 2026-10-03. |
| Procedencia y uso | USER-REPORTED: Raúl aporta su grabación y autoriza inspección/validación local F001. No es permiso para publicar media ni subirla a un servicio. |
| Fecha/hora real y zona física | USER-REPORTED: 03/10/2026, Europe/Malta. Hora exacta y exactitud del reloj Sony UNKNOWN; conservar metadata separada. |
| Idea, idioma hablado e intención | USER-REPORTED: conversación en español sobre arquitectura/modernización de sistemas, fixture STUDIO F001. Formulación de una única idea central e intervalos específicos UNKNOWN; no es el guion Go. |
| Objetivo, trípode y montaje | USER-REPORTED: Sony ZV-E10 + Sony kit lens + trípode + Elgato Teleprompter. Focal exacta/modelo de trípode y orientación física exacta UNKNOWN. |
| Micrófono / ruta y voz original | USER-REPORTED: DJI Mic Mini conectado a cámara; voz comprensible de principio a fin. Cable/receptor/ajustes de ganancia UNKNOWN; no deducidos de PCM ni del dispositivo visible. |
| Teleprompter / habitualidad / motivo si no usado | USER-REPORTED: Elgato Teleprompter usado y parte habitual de su STUDIO. Intervalo concreto de lectura UNKNOWN; no inferido de la mirada. |
| Luces reales y ajustes elegidos | USER-REPORTED: key light + rim light + 2 RGB al fondo. Modelos y ajustes reales UNKNOWN; no sustituirlos por targets iniciales del tech stack. |
| Limitaciones advertidas por Raúl | USER-REPORTED: ruido ambiente y posible ligero eco, sin impedir comprender la voz; tratamiento futuro conveniente. No se aplica procesamiento en F001. |
| Representatividad del STUDIO | USER-REPORTED: imagen, voz, encuadre, iluminación, gestos y movimientos representan razonablemente su STUDIO; confirma C0216.MP4 representativo y adecuado para F001. |

## Contenido: referencias aproximadas, sin STT ni detector

| Archivo | Intervalo de fuente | Tipo requerido | Estado |
| --- | --- | --- | --- |
| C0216.MP4 | UNKNOWN | Idea / narración natural / pausa normal | USER-REPORTED: arquitectura/modernización; al menos una pausa natural NO RETOMA, inicio/final con palabras completas y buffers de grabación. Referencias temporales y resumen concreto de una idea central UNKNOWN. |
| C0216.MP4 | UNKNOWN | Error intencional | UNKNOWN; no importar palabras del guion opcional. |
| C0216.MP4 | UNKNOWN | Pausa → Again aislado → pausa | USER-REPORTED: utilizó Again como marcador de retoma; aislamiento/secuencia de pausas y palabras del error/corrección UNKNOWN. |
| C0216.MP4 | UNKNOWN | Corrección | UNKNOWN; palabras reales pendientes de revisión humana. |
| C0216.MP4 | UNKNOWN | NARRACIÓN VÁLIDA — NO RETOMA con again | USER-REPORTED: again más de una vez en narración normal. Frases completas/intervalos UNKNOWN; no identificar automáticamente como retoma. |
| C0216.MP4 | 00:30, 02:30, 03:40 (instantes muestreados) | Manos / postura visible | OBSERVED en frames; no son límites de una acción ni prueba de izquierda/derecha/adelante/atrás. |
| C0216.MP4 | UNKNOWN | Izquierda / centro / derecha / centro / adelante / atrás / teleprompter | USER-REPORTED: movimientos naturales izquierda/derecha y adelante/atrás con retorno al centro, teleprompter habitual y representatividad confirmados. Intervalos/segmento de lectura UNKNOWN. |

Términos técnicos realmente pronunciados: **USER-REPORTED:** monolito, microservicios, eventos, idempotencia. Grafía de referencia aportada por Raúl, sin STT ni atribución de timestamps. No hay transcript, etiquetado automático de retomas ni corte. El agente redactará las referencias a partir de las respuestas de Raúl; no se le pide rellenar propiedades, hashes ni documentos manualmente.

## Evidencia y revisión

Directorio recuperable de evidencia: `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence`. Probe y versiones: ffprobe.json, ffprobe.stderr.log, ffmpeg-version.txt, ffprobe-version.txt. Procedimientos: commands.json, decode-result.json, frame-observations-procedure.json. Integridad: source.sha256, sidecar.sha256 y comprobaciones posteriores; manifest e2: evidence/evidence-e2.sha256, que incluye el acta humana y prueba de recuperación.

**Revisión de imagen/voz por Raúl:** USER-REPORTED, respuesta en este chat del 2026-10-03. Orientación vertical y voz comprensible de principio a fin, ruido/posible eco y representatividad registrados en human-review-e2.md. USER-REPORTED: VLC, velocidad normal 1×. Hora exacta de revisión UNKNOWN.  
**Confirmación humana:** «Confirmo que C0216.MP4 es representativo y adecuado como fixture STUDIO para F001». Adecuación/representatividad confirmadas; aceptación final de toda la evidencia/verificación de F001 aún pendiente. La fuente/hash no cambian. Se conserva e1 en Git (commit a50c702); e2 incorpora esta respuesta sin modificar r1.  
**Funciones futuras:** NOT YET VALIDATED conforme al contrato r1.  
**MOBILE:** Raúl declara grabación caminando al aire libre en `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/mobile-candidate-001/raw/PXL_20261003_092220543.mp4`; candidato conservado separadamente, sin inspección de contenido y fuera de F001/V-01–V-10.
