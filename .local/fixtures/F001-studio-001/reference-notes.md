# F001-studio-001 — Notas de referencia

**Entrega de evidencia:** e5 (2026-10-03, Europe/Malta), lista para aceptación final; V-01–V-09 PASS, V-10 HUMAN_REVIEW_REQUIRED.  
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

## Contenido anterior al handoff — histórico e2, sin STT ni detector

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

## Evidencia y revisión recibidas hasta e2

Directorio recuperable de evidencia: `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence`. Probe y versiones: ffprobe.json, ffprobe.stderr.log, ffmpeg-version.txt, ffprobe-version.txt. Procedimientos: commands.json, decode-result.json, frame-observations-procedure.json. Integridad: source.sha256, sidecar.sha256 y comprobaciones posteriores; manifest e2: evidence/evidence-e2.sha256, que incluye el acta humana y prueba de recuperación.

**Revisión de imagen/voz por Raúl:** USER-REPORTED, respuesta en este chat del 2026-10-03. Orientación vertical y voz comprensible de principio a fin, ruido/posible eco y representatividad registrados en human-review-e2.md. USER-REPORTED: VLC, velocidad normal 1×. Hora exacta de revisión UNKNOWN.  
**Confirmación humana:** «Confirmo que C0216.MP4 es representativo y adecuado como fixture STUDIO para F001». Adecuación/representatividad confirmadas; aceptación final de toda la evidencia/verificación de F001 aún pendiente. La fuente/hash no cambian. Se conserva e1 en Git (commit a50c702); e2 incorpora esta respuesta sin modificar r1.  
**Funciones futuras:** NOT YET VALIDATED conforme al contrato r1.  
**MOBILE:** Raúl declara grabación caminando al aire libre en `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/mobile-candidate-001/raw/PXL_20261003_092220543.mp4`; candidato conservado separadamente, sin inspección de contenido y fuera de F001/V-01–V-10.

## Handoff de revisión — referencias candidatas e3

**Procedencia:** archivo adjunto del propietario `8663a4f6-52c8-4779-87f1-14c2679614b5/Pasted text.txt`, conservado exactamente como evidence/handoff-e3.txt. Raúl autoriza usarlo para continuar HUMAN_REVIEW. **USER-REPORTED (documento de tercero suministrado por Raúl):** declara inspección visual completa y reconocimiento de voz externo, pero ninguna escucha directa. No es una confirmación humana de todas las palabras ni evidencia HEARD. El agente no ha ejecutado STT ni detector.

**MEASURED — archivo revisado por el handoff:** `/Users/raulalmeida/Downloads/WhatsApp Video 2026-10-03 at 16.14.01.mp4`, 37.288.406 bytes, SHA-256 `e72d69b6adf74a156b17ebad9b88a4f3b72ba539711727977208ba7d2033d604`; duración 232,800 s, vídeo H.264 almacenado 848×480, rotation −90, audio AAC 44.100 Hz. Es diferente en bytes/propiedades al RAW. No se promueve a fuente ni toma auxiliar; no se copia a raw/.

**OBSERVED — comparación visual del agente:** frames de revisión a 00:30, 02:30 y 03:40 corresponden a escena, postura y gestos de los frames RAW retenidos; notas en handoff-sampled-comparison-e3.json. Esto apoya que sea la misma grabación, sin probar continuidad/alineación de toda la secuencia. **UNKNOWN:** procedencia de la copia, ausencia de cortes/cambio de velocidad/desplazamiento temporal; se pidió confirmación a Raúl. Hasta entonces, los tiempos siguientes corresponden al archivo WhatsApp revisado y son solo referencias candidatas para contrastar en C0216.MP4.

### V-06 — idea y pausa candidatas

**USER-REPORTED / INFERRED / UNCERTAIN (handoff):** idea central candidata: modernizar la parte del sistema que elimina una restricción identificable del negocio y justifica la inversión, en vez de reemplazar todo por antigüedad. Conclusión candidata 03:26–03:36 y pregunta final 03:37–03:47.4. Raúl ya confirmó conversación en español sobre arquitectura/modernización y cuatro términos, pausa normal y palabras completas; esa evidencia humana e2 sigue válida. Falta confirmar que este resumen y referencias describen la fuente.

Pausas normales candidatas: 00:09.7–00:10.4, transición de «el sistema no escala/rehacerlo» a cuestionar si el problema es todo el sistema; y 00:37.2–00:40.9 tras la lista de fuentes de fricción. El handoff observa actividad baja y clasifica NO RETOMA por inferencia. No se convierte nivel bajo en silencio oído ni en pausa normal confirmada.

Términos candidatos temporizados en el handoff: monolito 01:08–01:12, microservicios 01:12–01:16, eventos 01:19–01:24 y 01:31–01:38. «Idempotencia» cerca de 01:52 es UNCERTAIN en reconocimiento. Raúl ya confirmó la palabra como realmente utilizada: conservar USER-REPORTED, sin certificar su pronunciación en ese instante ni corregir un transcript inexistente. ERP/RP/RPD alrededor de 00:18 y la cola posterior a la pregunta final permanecen UNCERTAIN.

### V-07 — contraste candidato; todas las palabras son UNCERTAIN

| Archivo revisado / intervalo aproximado | Evento candidato | Estado y contenido provisional |
| --- | --- | --- |
| WhatsApp, 01:31.5–01:38.7 | Error identificable candidato | USER-REPORTED / UNCERTAIN: «De hecho, cuando desacoplamos dos sistemas mediante eventos, garantizamos automáticamente que nunca procesaremos el mismo evento dos veces». Intención deliberada UNKNOWN. |
| WhatsApp, 01:38.7–01:40.3 | Pausa previa candidata | Actividad baja informada en handoff; pausa como juicio audible pendiente. |
| WhatsApp, 01:40.3–01:40.8 | Again aislado candidato | UNCERTAIN: reconocimiento contextual devuelve Again; una comprobación corta devolvió Thank you. No HEARD. |
| WhatsApp, 01:40.8–01:42.7 (alineación también 01:43.2) | Pausa posterior candidata | UNCERTAIN referencia aproximada; no límite de corte ni medición original. |
| WhatsApp, 01:42.7–01:53.8 | Corrección candidata | UNCERTAIN: «Utilizar eventos no garantiza automáticamente que un mensaje vaya a procesarse una única vez. Tenemos que diseñar qué ocurre con duplicados, reintentos, [término incierto] y fallos parciales». |
| WhatsApp, 02:14–02:26 | NARRACIÓN VÁLIDA — NO RETOMA candidata | INFERRED / UNCERTAIN: «Si [fallo/falla] una operación, quizás podamos try again, try again, pero antes de reintentar, tengo que saber algo mucho más importante. ¿Es seguro ejecutar esa operación otra vez?». |
| WhatsApp, 02:17.3–02:18.0 y 02:18.4–02:19.1 | Dos try again en frase válida candidatos | INFERRED / UNCERTAIN, sin restarts reconocidos de la toma; no etiquetar como retoma automáticamente. |

No se trasladan todavía estos tiempos como hechos confirmados del RAW ni se declara PASS. Se solicitó escucha dirigida en C0216.MP4: 01:31–01:54 y 02:14–02:26, confirmación/corrección de frases, pausas/aislamiento y error intencional. La escucha general previa de Raúl no confirma por sí sola cada cita de máquina.

El handoff enumera siete candidatos a again, no siete eventos verificados ni un conteo exhaustivo obligatorio F001: 00:54.2–00:54.7, 01:40.3–01:40.8, 02:01.4–02:01.9, dos try again anteriores, 03:11.3–03:11.8 y 03:16.0–03:16.5. Ambigüedades en eventos 3/6 y cadena de frases abandonadas 03:07–03:23; sonido 03:14–03:15.4 UNKNOWN. No implementar detector, EDL ni ampliar r1 para exigir todas las retomas verificadas. El fixture puede conservar varias retomas naturales; se necesita el caso requerido por AC-06.

### V-08 — movimientos reportados en el handoff

| Archivo revisado / intervalo | Observación reportada | Clasificación de proyecto / límite |
| --- | --- | --- |
| WhatsApp, 01:22.6–01:24.3 | Pequeña inclinación cabeza/torso a la izquierda de pantalla y retorno | USER-REPORTED (handoff la etiqueta OBSERVED), confianza media; no observación directa del agente sobre ese tramo RAW ni traslación de cuerpo entero demostrada. |
| WhatsApp, 02:28.5–02:31.0 | Pequeña inclinación a la derecha de pantalla y retorno | USER-REPORTED / OBSERVED en el handoff, confianza media; referencia candidata. |
| WhatsApp, 02:47.1–02:49.3 | Cabeza/torso se bajan e inclinan, con retorno | USER-REPORTED / OBSERVED: inclinación; interpretación de profundidad/adelante UNCERTAIN. No inferir distancia de un movimiento de cabeza. |
| WhatsApp, UNKNOWN | Movimiento leve hacia atrás independiente | UNKNOWN / no confirmado por el handoff. Raúl ya declaró que lo hizo y volvió al centro, pero su referencia sigue pendiente; no negar ese hecho ni dar un intervalo inventado. |
| WhatsApp, 00:52.2–00:54.8 | Giro y alcance de brazo a la derecha, mano sale del plano, retorno | USER-REPORTED / OBSERVED en el handoff; alcance no demuestra desplazamiento corporal. |
| WhatsApp, 03:50.8–03:52.8 | Giro y alcance de brazo a la derecha al final, sin retorno mostrado | USER-REPORTED / OBSERVED en el handoff; no confundir con retorno de calibración ni asignar propósito no observado. |

Raúl ya confirmó movimientos naturales en cuatro direcciones y retorno, teleprompter habitual y representatividad. r1 exige movimientos leves identificados; **no exige pasos, pies visibles, traslación de todo el cuerpo ni una rutina extrema**. La ausencia de confirmación de traslación de cuerpo entero en el handoff no crea un nuevo criterio ni un FAIL. Sí sigue pendiente la referencia hacia atrás y la confirmación de los candidatos, sin usar retorno de una inclinación hacia adelante como un nuevo movimiento hacia atrás.

Limitaciones visuales reportadas: piernas fuera del plano; algunas manos/brazos pueden salir por laterales o borde inferior; detalle/framing útiles no prueban crops/zooms futuros. Lo muestreado directamente por el agente en e1/e2 se conserva con su etiqueta OBSERVED; el resto queda USER-REPORTED por documento, con incertidumbres.

**Resultado histórico de e3 al recibir el handoff:** V-06/V-07/V-08 HUMAN_REVIEW_REQUIRED; V-10 espera cierre de esos checks y aceptación final. V-01–V-05 y V-09 permanecen PASS por evidencia previa, no por el handoff. Evidencia en evidence/handoff-e3.txt, handoff-provenance-e3.json, handoff-media-probe-e3.json, handoff-frames-procedure-e3.json, handoff-sampled-comparison-e3.json ; los artefactos e3 quedan cubiertos por el manifest de la entrega e4, sin cerrar un manifest e3 independiente. No se declara DONE ni se empieza F002.

## Confirmación del propietario — evidencia e4 previa al cierre de V-08

Acta literal: evidence/owner-confirmation-e4.md. **USER-REPORTED / HUMAN EVIDENCE:** Raúl confirma que el archivo WhatsApp es una copia comprimida completa de C0216.MP4, sin cortes, cambios de velocidad ni desplazamiento del inicio. Las identidades de bytes siguen diferentes; la confirmación permite usar sus referencias aproximadas como tiempos de fuente RAW. No se cambió el RAW ni se validó el proxy como entrega F001.

### V-06 — PASS

**USER-REPORTED:** idea central confirmada: modernizar la parte que elimina una restricción de negocio, en vez de sustituir todo por antigüedad. Idioma español; conversación natural de arquitectura/modernización. Términos realmente dichos confirmados previamente: monolito, microservicios, eventos, idempotencia. Pausa natural NO RETOMA y palabras completas con margen al inicio/final confirmadas en revisión VLC a 1×.

Referencias aproximadas del material revisado, alineadas por confirmación de procedencia: desarrollo 00:01–03:23; regla/resumen 03:26–03:36; cierre/pregunta 03:37–03:47.4; monolito 01:08–01:12, microservicios 01:12–01:16 y eventos 01:19–01:24/01:31–01:38. Son referencias derivadas del handoff, no límites exactos ni citas HEARD. La idea/los términos/pausa/bordes están confirmados por Raúl; la grafía y posición puntual de la palabra reconocida cerca de 01:52 y ERP/RP/RPD permanecen UNCERTAIN sin afectar la cobertura humana de al menos tres términos. Pausas localizadas 00:09.7–00:10.4 y 00:37.2–00:40.9 siguen referencias candidatas del handoff, no una escucha directa nueva; la existencia de pausa natural ya fue confirmada por Raúl.

### V-07 — PASS para el contraste requerido por r1

Raúl responde a la escucha dirigida de 01:31–01:54 y 02:14–02:26: confirma error intencional «los eventos garantizan no procesar dos veces», pausa → Again aislado → pausa → corrección «los eventos no garantizan procesar una única vez» y «try again, try again» como narración válida. Estas formulaciones breves son las confirmadas en la pregunta/respuesta; no se convierten todas las citas extensas ni el conteo de siete candidatos del handoff en palabras o eventos humanos verificados.

| RAW / referencia aproximada | Hecho confirmado / procedencia del intervalo |
| --- | --- |
| C0216.MP4, 01:31.5–01:38.7 | USER-REPORTED: afirmación equivocada intencional sobre garantía automática de no procesar un evento dos veces. Tiempo aproximado suministrado en handoff, usado dentro del tramo escuchado consultado. |
| C0216.MP4, 01:38.7–01:40.3 | Pausa previa confirmada como parte de la secuencia; intervalo aproximado del handoff, no duración medida por el agente. |
| C0216.MP4, 01:40.3–01:40.8 | USER-REPORTED: Again aislado confirmado. Discrepancia de reconocimiento automático «Thank you» queda en el handoff, no sustituye el juicio de Raúl. |
| C0216.MP4, 01:40.8–01:42.7 (alineación aproximada hasta 01:43.2) | Pausa posterior confirmada; no fijar límite de corte. |
| C0216.MP4, 01:42.7–01:53.8 | USER-REPORTED: toma corregida niega la garantía de procesar una única vez. Las palabras extensas/posible término cerca de 01:52 no certificadas literalmente permanecen UNCERTAIN. |
| C0216.MP4, 02:14–02:26 | USER-REPORTED: contexto de reintentar y decidir si es seguro repetir la operación; «try again, try again» confirmado NARRACIÓN VÁLIDA — NO RETOMA. |
| C0216.MP4, 02:17.3–02:18.0 y 02:18.4–02:19.1 | Dos referencias aproximadas del handoff al try again válido confirmado. No son comandos ni instrucciones de corte. |

V-07 no afirma detección automática, eliminación de retomas, totalidad del conteo ni ausencia de ambigüedad en otras apariciones. F001 conserva el error intencional y marcador en el original; el contraste mínimo requerido ya tiene confirmación humana y referencias recuperables.

### V-08 — HUMAN_REVIEW_REQUIRED

Raúl reitera que inclinaciones derecha/izquierda/adelante/atrás son muy sutiles y permanece bien centrado en el entorno controlado. Esto es compatible con el encuadre observado y su representatividad ya aprobada. No es una renuncia a identificar movimientos ni un permiso para calibrar seguimiento de edición.

Referencias candidatas conocidas de cabeza/torso: izquierda de pantalla 01:22.6–01:24.3; derecha 02:28.5–02:31.0; posible inclinación adelante 02:47.1–02:49.3. Mantener sus límites/interpretación según el handoff; no inventar pasos de cuerpo entero. Raúl confirma los hechos de movimientos leves y retornos globalmente, pero **la referencia hacia atrás independiente sigue UNKNOWN**. Se solicitó solo una localización aproximada (principio/mitad/final también útil), sin regrabar ni exagerar gestos. No se transforma el retorno desde delante en movimiento atrás nuevo.

**Estado global e4:** HUMAN_REVIEW_REQUIRED; V-01–V-07 y V-09 PASS; V-08/V-10 pendientes. AC-01–AC-06 y AC-08/09 satisfechos; AC-07/10 pendientes. No se solicita aceptación final antes de resolver el check obligatorio. Source SHA y contrato r1 preservados. Archivo de recuperación ya comprobado; no se repiten V-01–V-05/V-09. Manifest de esta evidencia: evidence/evidence-e4.sha256.

## Revisión final preparada — estado vigente e5

**USER-REPORTED / HUMAN EVIDENCE:** Raúl responde «mitad» a la pregunta explícita de localizar la inclinación leve hacia atrás, independiente del retorno desde delante. Referencia: **zona media de C0216.MP4**. No es un punto/timestamp calculado ni una dirección inferida a partir de frames. Acta literal: evidence/movement-confirmation-e5.md. Se conserva su revisión e2 de movimiento atrás con regreso al centro.

### Referencias de V-08 concluidas

| Fuente / referencia aproximada | Evidencia del movimiento y límites |
| --- | --- |
| C0216.MP4, 01:22.6–01:24.3 (referencia de handoff, copiado sin desplazamiento confirmado) | Inclinación leve cabeza/torso a izquierda de pantalla y retorno, reportados por inspección del handoff; movimientos sutiles en ambas direcciones/retornos confirmados por Raúl. No se exige paso corporal. |
| C0216.MP4, 02:28.5–02:31.0 (handoff) | Inclinación a derecha de pantalla con retorno, evidencia reportada + confirmación humana de movimientos sutiles. |
| C0216.MP4, 02:47.1–02:49.3 (handoff, interpretación de profundidad incierta) | Inclinación candidata adelante; Raúl confirma movimiento adelante con retorno. No se infiere cambio medido de distancia ni pasos. |
| C0216.MP4, zona media / «mitad» (referencia aproximada cualitativa aportada por Raúl) | Inclinación leve hacia atrás independiente del retorno desde delante; retorno al centro confirmado previamente. Límites y punto exacto UNKNOWN, sin inventarlos. |
| C0216.MP4, durante la explicación (tiempo puntual UNKNOWN) | Elgato Teleprompter usado y habitual, confirmado por Raúl. No se atribuye la mirada a lectura mediante un detector ni se exige un segmento de duración fijada. |

El contrato r1 exige movimientos leves identificados y referencias aproximadas, sin precisión/duración numérica ni prueba de traslación corporal. La referencia de zona media del propietario ubica el movimiento atrás sin fabricar un intervalo medido. Se aceptan límites exactos desconocidos; no queda desconocida la existencia/dirección/retorno ni la región de la fuente. Postura centrada y cabeza/hombros/torso/manos: evidencia visual e1/e2 + juicio humano. Fuera de frame ocasional de brazos/manos y ruido/posible eco quedan como limitaciones, sin prometer tracking/crop/audio futuros.

**V-08: PASS.** La incertidumbre del revisor externo sobre desplazamiento de cuerpo entero no es criterio r1 y no se convierte en fallo. No se elimina ningún check ni se agrega requisito de seguimiento de edición.

### Identidad y gate final

Fixture F001-studio-001, principal C0216.MP4, 2.873.163.442 bytes. SHA-256 autoritativo `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`, idéntico antes/después y en /Volumes/PortableSSD/videos/raw/C0216.MP4. RAW y sidecar intactos según evidencia previa; no se repiten esos checks sin motivo.

**V-01–V-09 PASS; V-10 HUMAN_REVIEW_REQUIRED únicamente por aceptación final.** AC-01–AC-09 PASS; AC-10 HUMAN_REVIEW_REQUIRED por aceptación expresa de e5. Estado HUMAN_REVIEW; no DONE ni PRODUCTION_APPROVED. Manifest: evidence/evidence-e5.sha256.

UNKNOWNs permitidos: hora exacta de captura/revisión, focal/exposición/ISO/apertura/balance de blancos y lecturas físicas de luces, channel_layout no informado, límites frame-exactos y punto exacto de movimiento atrás. Otras citas o candidatos del reconocimiento suministrado permanecen UNCERTAIN; no se declara que todos los marcadores hayan sido contados/identificados ni que exista STT válido. Voz inteligible y términos/casos requeridos están confirmados por Raúl.

Solo resta la aceptación final de la revisión e5 y su identidad. No se inicia F002 ni se valida la pipeline futura.
