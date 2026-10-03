# F001-studio-001 — Notas de referencia

**Entrega de evidencia:** e1 (2026-10-03, Europe/Malta), abierta; revisión pendiente.  
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
- **USER-REPORTED:** Raúl declara una copia/original recuperable en su mensaje de continuación del 2026-10-03, pero el valor comunicado es el placeholder `<LOCATION>`.
- **UNKNOWN:** ubicación real, instrucciones de acceso y hash de recuperación. V-01/V-10 permanecen BLOCKED hasta leer una copia situada fuera del directorio de trabajo y comprobar coincidencia.
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
| Audio seleccionado para decodificar | stream 1, única pista audio integrada; origen físico UNKNOWN |
| Codec / frecuencia / canales | pcm_s16be, 16 bits, 48.000 Hz, 2 canales |
| Channel layout | UNKNOWN: no informado por ffprobe; no asignar etiquetas de canal |
| Idioma en tags | und; idioma hablado UNKNOWN hasta escucha humana |
| Metadata adicional | stream 2 rtmd, timecode declarado 03:22:25:23; no es tiempo de fuente mm:ss |
| Fecha del contenedor / streams | creation_time 2026-10-03T14:02:10.000000Z |
| Fecha/zona declarada por XML | 2026-10-03T15:02:10+01:00; exactitud del reloj y zona física UNKNOWN |
| Dispositivo declarado por XML | manufacturer Sony; modelName ZV-E10; uso físico pendiente de confirmación |
| Gamma/color declarados | XML rec709-xvycc / rec709; ffprobe bt709, transfer iec61966-2-4 |

No convertir creation_time en fecha real confirmada, ni metadatos de codificación en ajustes elegidos por Raúl. Focal, exposición, ISO, apertura, balance de blancos y lecturas de luces: **UNKNOWN** en las evidencias disponibles.

## Orientación y encuadre — OBSERVED

FFmpeg autorrota la imagen según su matriz al extraer estos tres pequeños frames. Las imágenes resultantes son 360 × 640, verticales 9:16 y con el sujeto erguido. Es vista de evidencia, no un nuevo RAW, crop, proxy de producción ni normalización F002. El comportamiento de un reproductor usado por Raúl y su confirmación de orientación siguen **UNKNOWN** (V-04).

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
| Fecha/hora real y zona física | UNKNOWN; valores de reloj arriba son MEASURED metadata, pendientes de confirmación. |
| Idea, idioma hablado e intención | UNKNOWN; no se presume que se recitó el guion Go. |
| Objetivo, trípode y montaje | UNKNOWN; metadata solo declara el cuerpo de cámara. |
| Micrófono / ruta y voz original | UNKNOWN; confirmar dispositivo/conexión y escuchar la pista 1 completa. |
| Teleprompter / habitualidad / motivo si no usado | UNKNOWN; no observable en estos frames. |
| Luces reales y ajustes elegidos | UNKNOWN; separar del color observado del fondo. |
| Limitaciones advertidas por Raúl | UNKNOWN; no confundir con límites del muestreo visual del agente. |
| Representatividad del STUDIO | UNKNOWN; juicio de Raúl requerido por V-08/V-09. |

## Contenido: referencias aproximadas, sin STT ni detector

| Archivo | Intervalo de fuente | Tipo requerido | Estado |
| --- | --- | --- | --- |
| C0216.MP4 | UNKNOWN | Idea / narración natural / pausa normal | UNKNOWN; V-06 requiere escucha/revisión humana. |
| C0216.MP4 | UNKNOWN | Error intencional | UNKNOWN; no importar palabras del guion opcional. |
| C0216.MP4 | UNKNOWN | Pausa → Again aislado → pausa | UNKNOWN; V-07 requiere identificar el hecho escuchado. |
| C0216.MP4 | UNKNOWN | Corrección | UNKNOWN; palabras reales pendientes de revisión humana. |
| C0216.MP4 | UNKNOWN | NARRACIÓN VÁLIDA — NO RETOMA con again | UNKNOWN; frase real e intervalo pendientes de revisión humana. |
| C0216.MP4 | 00:30, 02:30, 03:40 (instantes muestreados) | Manos / postura visible | OBSERVED en frames; no son límites de una acción ni prueba de izquierda/derecha/adelante/atrás. |
| C0216.MP4 | UNKNOWN | Izquierda / centro / derecha / centro / adelante / atrás / teleprompter | UNKNOWN; V-08 requiere reproducción y referencia humana. |

Términos técnicos realmente pronunciados: **UNKNOWN** hasta V-06. No hay transcript, etiquetado automático de retomas ni corte. El agente redactará las referencias a partir de las respuestas de Raúl; no se le pide rellenar propiedades, hashes ni documentos manualmente.

## Evidencia y revisión

Directorio recuperable de evidencia: `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence`. Probe y versiones: ffprobe.json, ffprobe.stderr.log, ffmpeg-version.txt, ffprobe-version.txt. Procedimientos: commands.json, decode-result.json, frame-observations-procedure.json. Integridad: source.sha256, sidecar.sha256 y comprobaciones posteriores; manifest de evidencia al cerrar esta revisión.

**Revisión completa de imagen/voz por Raúl:** UNKNOWN; no se ha registrado reproductor, fecha ni observaciones V-04–V-09.  
**Aceptación expresa e1 del fixture:** NOT GRANTED.  
**Funciones futuras:** NOT YET VALIDATED conforme al contrato r1.  
**MOBILE:** Raúl declara grabación caminando al aire libre en `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/mobile-candidate-001/raw/PXL_20261003_092220543.mp4`; candidato conservado separadamente, sin inspección de contenido y fuera de F001/V-01–V-10.
