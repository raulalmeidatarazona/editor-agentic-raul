# F001 — Contrato de validación y evidencia

**Bundle revision:** r1  
**Requirements:** [requirements.md](requirements.md)  
**Estado y aprobación:** [plan.md](plan.md)  
**Definido antes de grabar:** 2026-10-03

## Fixture y entorno

Fuente futura: toma principal STUDIO y, solo si se necesita, una auxiliar de
calibración. Ubicación canónica `.local/fixtures/F001-studio-001/`, relativa a
este repositorio; registrar rutas absolutas, nombres originales, bytes y hashes
reales al entregar. Si una toma se sustituye, usar un nuevo ID y conservar la
relación/historial. Todas las tomas incluidas deben satisfacer los checks que
les corresponden, no solo la principal.

Se encontraron ffprobe/FFmpeg 9.0.1 y shasum durante PLAN; no se instaló nada.
Ninguna inspección de media se ha ejecutado: no existe el fixture. Captura,
ubicación del backup, hashes, tiempos de contenido y revisión humana están
pendientes de ejecución. Comprobar disponibilidad/versiones de nuevo al validar.

## Checks predefinidos y correspondencia con aceptación

| Check | AC | Categoría | Procedimiento / expectativa | Evidencia a conservar |
| --- | --- | --- | --- | --- |
| V-01 | AC-01 | AUTOMATED / DETERMINISTIC EVIDENCE | Cada RAW es archivo regular no vacío; medir bytes y SHA-256 tras copiar; comparar con fuente/copia de recuperación y repetir hash al terminar checks. Todos coinciden. | Nombres/rutas/bytes, source.sha256 inicial/final y hash/ubicación de recuperación. |
| V-02 | AC-02/03 | AUTOMATED / DETERMINISTIC EVIDENCE | Probe exitoso; identificar vídeo real y pista de voz, duración positiva, dimensiones y datos FPS/audio. Registrar ausencias/campos no informados; no inventar valores. | ffprobe.json, streams seleccionados y resumen de propiedades. |
| V-03 | AC-02 | AUTOMATED / DETERMINISTIC EVIDENCE | Decodificar completos los streams seleccionados de cada toma con herramientas existentes; salida 0 y ningún error de decodificación. Probe/primer frame no bastan. | Comando, versión, exit code y decode.log. |
| V-04 | AC-03 | DETERMINISTIC + HUMAN EVIDENCE | Contrastar dimensiones/SAR/DAR/rotación disponible con montaje y vista humana. Identificar de forma inequívoca la vista vertical 9:16 y registrar comportamiento real del player. Puede requerir orientación de referencia externa al RAW; no exigir tag de rotación. | Campos medidos, descripción de vista/corrección necesaria, observación y confirmación de Raúl. |
| V-05 | AC-02/04 | HUMAN EVIDENCE | Reproducir y escuchar la explicación completa a velocidad normal con Raúl: voz original comprensible, sin distorsión/dropouts impeditivos; verificar origen conocido de la pista. | Player/archivo/pista revisados, fecha/revisor y observaciones de audio con momentos problemáticos si existen. |
| V-06 | AC-05 | HUMAN EVIDENCE | Verificar idea, entrega natural, pausa normal, tres términos técnicos realmente pronunciados y palabras completas al inicio/final. | Notas con términos, resumen e intervalos aproximados de fuente. |
| V-07 | AC-06 | HUMAN EVIDENCE | Escuchar error → pausa → Again aislado → pausa → corrección; contrastar con frase válida que contiene again. Notas identifican ambos usos sin ambigüedad. | Archivo/intervalos/palabras de error, marcador, corrección y NO RETOMA. |
| V-08 | AC-07/09 | HUMAN EVIDENCE | Ver postura normal, manos, izquierda/derecha y adelante/atrás y retorno al centro; evaluar encuadre útil y representatividad. Teleprompter usado si habitual; si no, registrar motivo real. | Intervalos por movimiento, partes visibles/limitaciones, uso/no-aplicabilidad y juicio de Raúl. |
| V-09 | AC-08/09 | HUMAN EVIDENCE | Revisar notas/contexto: equipo real, mic/ruta, fecha/zona, idioma, luces/ajustes conocidos o desconocidos, procedencia/permiso y limitaciones; Raúl confirma STUDIO representativo. | reference-notes.md y confirmación humana vinculada a hashes. |
| V-10 | AC-01/10 | DETERMINISTIC + HUMAN EVIDENCE | Revisar paquete local y resumen por AC, lectura/hash de copia recuperable, rutas de recuperación y exclusión de RAW de Git. Raúl acepta expresamente el fixture exacto; futuras funciones siguen NOT YET VALIDATED. | Tabla de identidad/resultados, recuperación verificada, alcance/fecha/frase de aceptación. |

No hay criterio de duración fija, 4K obligatorio, loudness numérico, tolerancia de
STT, crop digital o render. La ausencia de una propiedad opcional como bitrate
no es un fallo por sí sola: registrarla. No disponer de dimensiones, duración,
pistas o referencia de orientación suficiente sí bloquea su check obligatorio.

## Procedimientos deterministas — ejecutar solo después de aprobación

El agente operador sustituirá los valores por datos reales. Estos ejemplos son
comandos manuales, no software F002 ni scripts creados en F001. Guardar comando,
versión, stdout/stderr y código de salida en evidence/ sin secretos. Ninguno
escribe media de salida ni modifica el archivo fuente.

```sh
CAPTURE_RAW='/ruta/absoluta/.local/fixtures/F001-studio-001/raw/nombre-original.MP4'
test -f "$CAPTURE_RAW" && test -s "$CAPTURE_RAW"
wc -c < "$CAPTURE_RAW"
shasum -a 256 "$CAPTURE_RAW"
ffprobe -v error -show_format -show_streams -of json "$CAPTURE_RAW"
```

En la salida de probe registrar format/stream duration cuando estén disponibles,
width/height, sample_aspect_ratio/display_aspect_ratio, avg_frame_rate/r_frame_rate,
codec y tags/side_data de rotación/matriz si hay; para audio, codec, sample_rate,
channels/channel_layout cuando estén informados. La duración seleccionada debe
ser positiva y coherente con reproducción. FPS reportado no demuestra CFR; la
normalización temporal queda para F002. No convertir ausencia de rotation en
«0 grados confirmado» sin contrastar la imagen/contexto.

Decodificación completa, después de identificar los índices de vídeo real y voz
en probe; no asumir que el primer stream de audio es el micrófono deseado:

```sh
CAPTURE_VIDEO_INDEX='indice_real_del_stream_de_video'
CAPTURE_AUDIO_INDEX='indice_real_del_stream_de_voz'
ffmpeg -nostdin -hide_banner -v error -xerror -err_detect explode \
  -i "$CAPTURE_RAW" -map "0:${CAPTURE_VIDEO_INDEX}" \
  -map "0:${CAPTURE_AUDIO_INDEX}" -f null -
CAPTURE_DECODE_STATUS=$?
shasum -a 256 "$CAPTURE_RAW"
```

Conservar el exit code inmediatamente tras la decodificación, antes del comando
siguiente, además del log. Repetir para cada toma. Comparar hashes de cada fuente
y de su backup sin cambiar nombres/bytes para forzar una coincidencia. No basta
decir «hay una copia»: debe ser localizable y leíble, con hash coincidente. Una
herramienta no disponible o fallo de codec se informa con su salida; no instalar,
reconvertir ni rebajar aceptación automáticamente.

No se requieren capturas de pantalla, audio extraído ni proxy para pasar F001:
el RAW reproducible y las notas/checks son el paquete humano mínimo. Un pequeño
frame de evidencia, si resulta útil dentro de la ejecución aprobada, puede formar
parte de esos checks; no convertirlo en una composición o prueba de reframing.

## Cobertura negativa, límites y fallos

| Tipo | Cobertura acordada para F001 |
| --- | --- |
| Negativo semántico | La frase válida con again y una pausa normal contrastan con la retoma en V-06/07. Se valida la referencia humana, no un detector inexistente. |
| Archivo inválido / voz ausente | V-01–03/05 detectan archivo vacío, error de lectura/decodificación, ausencia de streams o voz ininteligible; bloquear aceptación, preservar originales. |
| Límites de orientación | V-04 contempla píxeles horizontales, autorrotación o metadata ausente; contexto+observación pueden resolver la vista. Conflicto no resoluble queda BLOCKED. |
| Límites de captura | V-06/08 revisan inicio/final de palabras, alcance natural de manos/movimientos y detalle visible. Sin probar zoom/crop finales. |
| Recuperación | V-01/10 comprueban lectura/hash de la copia existente. Diferencia o ausencia impide aceptar. No destruir ni interrumpir una copia para provocar fallos. |
| Tests de aplicación / failure injection destructiva | No aplican: no hay software/pipeline en F001. No fabricar corrupción, cortes o audio eliminado para probar funciones futuras. Los comportamientos ante fallos están predefinidos. |

## NOT YET VALIDATED — fuera de aceptación F001

STT y términos reconocidos automáticamente; detección de retomas/ambigüedad y
límites de corte; sincronía tras edición; captions; composición/render HyperFrames;
tracking o reframing digital; detección de safe zones y layouts finales; mezcla,
normalización/loudness de entrega; performance de render y calidad publicable.
No son «checks F001 pendientes» ni N/A añadidos para ocultar fallos: están fuera
de alcance desde PLAN. El fixture aporta casos para evaluarlos después.

## Reglas de decisión

Cada AC requiere sus evidencias. Criterio ejecutado que falla → FAIL. Inspección
requerida no ejecutable/identidad no resoluble → BLOCKED. Técnica disponible pero
juicios humanos pendientes → HUMAN_REVIEW_REQUIRED. PASS global solo con todos
los checks aplicables y humanos aprobados; conservar cada fallo/bloqueo individual.
Unknown/skipped nunca significa PASS. No aceptar por tener MP4 o probe exitoso.

DONE requiere aprobación previa del PLAN, entrega correspondiente a r1, evidencia
recuperable y aceptación expresa de Raúl vinculada a archivo/s y SHA-256. Es
aceptación de un fixture de desarrollo, no PRODUCTION_APPROVED de un vídeo.

## Evidencia de ejecución — entrega e2 abierta (2026-10-03)

**Verification result:** HUMAN_REVIEW_REQUIRED — recuperación/inspección completas; referencias humanas de V-06–V-08 y cierre de V-10 pendientes.  
**Lifecycle:** HUMAN_REVIEW, según plan.md.  
**Decisión humana recibida:** Raúl confirma C0216.MP4 representativo y adecuado como fixture STUDIO para F001. Esta confirmación se registra y satisface el juicio de adecuación; no convierte checks UNKNOWN en PASS ni completa la feature.  
**Verificación/aceptación final de la entrega completa:** pendiente; no DONE.  
**Operador objetivo:** Codex. **Revisor humano:** Raúl Almeida, mensajes directos del 2026-10-03; VLC a velocidad normal 1× confirmado. Hora exacta de revisión UNKNOWN.

e1 conserva la inspección objetiva de 2026-10-03 15:45–15:48 Europe/Malta y su commit
`a50c702`. e2 añade la respuesta humana y la búsqueda acotada de la recuperación.
No cambian RAW, selección de streams, requisitos ni contrato r1. No se repiten
probe/decode sin un cambio del material. La copia de notas e1 se conserva en
`/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/reference-notes-e1.md` y en Git; el manifest original evidence.sha256
se conserva. Su entrada para notas corresponde a esa copia e1, no a las notas e2.

| Identidad / evidencia | Valor real |
| --- | --- |
| Fixture / rol / original | F001-studio-001 / principal / C0216.MP4, designado por Raúl |
| RAW absoluto | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216.MP4` |
| Bytes / SHA-256 antes y después | MEASURED: 2.873.163.442 / `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`, estable; bytes y mtime iguales |
| Sidecar original | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216M01.XML` / 1.933 bytes / `155550ef95eaf6e885e6e5be67667c8089e4060c774023cbfa0f34ad14c1bde5`, estable |
| Recuperación | MEASURED: `/Volumes/PortableSSD/videos/raw/C0216.MP4`, 2.873.163.442 bytes, SHA-256 `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`, coincide. Lectura completada 2026-10-03 16:05:28 Europe/Malta (14:05:28 UTC), salida 0; original externo estable. Acceso: conectar/montar PortableSSD y leer esa ruta. |
| Duración / vídeo | MEASURED: 232,800 s; stream 0 H.264 3840×2160, 25/1 reportados, SAR 1:1, DAR almacenado 16:9, matriz rotation −90 |
| Audio | MEASURED: stream 1 PCM 16-bit BE, 48 kHz, 2 canales; USER-REPORTED: DJI Mic Mini conectado a cámara y voz comprensible de principio a fin |
| Vista | OBSERVED: FFmpeg muestra vertical 9:16 erguido; USER-REPORTED: Raúl confirma visualización vertical correcta |
| Notes e2 | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/reference-notes.md`; SHA-256 `2a165d193115050f013afa0c54df7f098cf6fc83046484dfeed0f1d6b9ba6492` |
| Acta literal humana e2 | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/human-review-e2.md`; SHA-256 `b70bec10cf37467f53efdd90821e3755243a99deb4b2f42f2559b38ae235b91c` |
| Manifest e2 | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/evidence-e2.sha256`; SHA-256 `a0caa60d63ebf48e0f6fb7ca514bf6d6566badd3eaa5c52ab6f2501a790acc6d`; 37 artefactos cubiertos incluyendo notas, acta, evidencia objetiva y copia e1 |
| Herramientas | FFmpeg/ffprobe 9.0.1 y shasum -a 256; versiones/comandos/exit codes en evidence/; sin instalaciones |

### Resultados por check

Las evidencias relativas siguientes se resuelven en `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence` y se vinculan al
SHA-256 del RAW indicado. Las respuestas humanas se clasifican USER-REPORTED /
HUMAN EVIDENCE; solo la metadata y resultados de herramientas son MEASURED.

| Check / AC | Resultado y cobertura real | Evidencia | Estado |
| --- | --- | --- | --- |
| V-01 / AC-01 | Fuente regular no vacía, bytes/hash locales estables; original externo localizado y leído, bytes/hash iguales y original externo estable tras lectura. Intento inicial sin disco conservado como historial, bloqueo resuelto. | source.sha256, source-after.sha256, integrity-result.json, recovery.sha256, recovery-result-e2.json, recovery-location-check-mounted-e2.json | PASS |
| V-02 / AC-02/03 | Probe salida 0, stderr vacío, vídeo real, duración/dimensiones positivas y una pista audio; Raúl confirma voz y DJI conectado a cámara. Stream seleccionado de voz: 1, único audio integrado. | ffprobe.json, commands.json, frames, human-review-e2.md | PASS |
| V-03 / AC-02 | Decodificación completa streams 0/1 salida 0, decode.log vacío; identidad local estable. No se exige decodificar el stream 2 de metadata como audiovisual. | decode-result.json, decode.log, decode.stdout.log, integrity-result.json | PASS |
| V-04 / AC-03 | Matriz −90 y píxeles almacenados horizontales; frames autorrotados 9:16 y Raúl confirma visualización vertical correcta. Nombre de player UNKNOWN, no inventado. Vista vertical inequívoca establecida por evidencia + confirmación. | ffprobe.json, frame-030s.png, frame-150s.png, frame-220s.png, human-review-e2.md | PASS |
| V-05 / AC-02/04 | Raúl confirma escucha completa con VLC a 1×, voz comprensible de principio a fin, DJI a cámara; ruido ambiente/posible eco no impeditivos. Limitación anotada; no se procesa audio ni se añade umbral no aprobado. | human-review-e2.md, reference-notes.md, ffprobe.json stream 1 | PASS |
| V-06 / AC-05 | Español, arquitectura/modernización; cuatro términos USER-REPORTED: monolito, microservicios, eventos, idempotencia. Pausa normal NO RETOMA y palabras completas/margen al inicio/final confirmados. Resumen específico de una idea e intervalos aproximados de referencia pendientes; no se inventan. | human-review-e2.md, reference-notes.md | HUMAN_REVIEW_REQUIRED |
| V-07 / AC-06 | Raúl confirma Again de retoma y varias apariciones normales. Palabras del error/corrección, secuencia de pausas/aislamiento, frases válidas completas e intervalos aproximados UNKNOWN. Su autorización para registrarlos UNKNOWN se respeta sin cambiar AC-06 ni declarar PASS. | human-review-e2.md, reference-notes.md | HUMAN_REVIEW_REQUIRED |
| V-08 / AC-07/09 | Frames muestran cabeza/hombros/torso/manos y postura centrada. Raúl confirma movimientos izquierda/derecha/adelante/atrás con retorno al centro, Elgato habitual y representatividad. Intervalos por movimiento/lectura UNKNOWN; referencias pendientes. | frames, human-review-e2.md, reference-notes.md | HUMAN_REVIEW_REQUIRED |
| V-09 / AC-08/09 | Raúl confirma fecha 03/10/2026 Europe/Malta, STUDIO, Sony ZV-E10/kit lens/trípode/Elgato habitual/DJI a cámara, key/rim/2 RGB, representatividad y limitación audio. Hora exacta, focal/exposición y lecturas reales no recordadas quedan UNKNOWN, permitidas/documentadas; metadata del reloj separada de hechos. Procedencia/permiso local F001 registrados. | human-review-e2.md, reference-notes.md, sidecar.sha256 | PASS |
| V-10 / AC-01/10 | Paquete, manifest, exclusión de media y recuperación verificada disponibles. Adecuación/representatividad confirmadas; V-06–V-08 y aceptación final de verificación completa pendientes. | evidence-e2.sha256, git-exclusion.log, recovery-result-e2.json, human-review-e2.md | HUMAN_REVIEW_REQUIRED |

### Cobertura por aceptación

| AC | Estado actual |
| --- | --- |
| AC-01 | PASS: integridad local estable y original externo leído con bytes/hash coincidentes y ruta/acceso registrados. |
| AC-02 | PASS: V-02/V-03/V-05 pasan; vídeo/audio decodifican completos y revisión normal VLC confirmada. |
| AC-03 | PASS: propiedades conocidas, duración positiva y vista vertical identificada/confirmada (V-02/V-04). |
| AC-04 | PASS: voz inteligible completa a 1× con Raúl; ruido/posible eco no impeditivos documentados. |
| AC-05 | HUMAN_REVIEW_REQUIRED: idioma/términos/pausa/bordes completos confirmados; resumen específico y referencias pendientes. |
| AC-06 | HUMAN_REVIEW_REQUIRED: usos de Again confirmados, contraste concreto/error/corrección e intervalos UNKNOWN. |
| AC-07 | HUMAN_REVIEW_REQUIRED: postura/movimientos/retornos/teleprompter habitual confirmados; referencias por movimiento pendientes. |
| AC-08 | PASS: fecha/zona/equipo/ruta/idioma/luces/teleprompter/procedencia/limitaciones registrados; ajustes desconocidos explícitos. |
| AC-09 | PASS: Raúl confirma expresamente representatividad/adecuación de imagen, voz, encuadre, iluminación, gestos y movimientos para F001; limitación de audio visible en notas. No promete crops futuros. |
| AC-10 | HUMAN_REVIEW_REQUIRED: recuperación y paquete identificados; faltan referencias V-06–V-08 y cierre humano de la verificación completa. |

No hay FAIL demostrado de integridad/decodificación. Ruido/posible eco no impiden
la comprensión según Raúl: limitación, no fallo impeditivo inventado. UNKNOWN
sigue sin ser PASS. No se implementa mezcla/audio correctivo ni ninguna función
futura. No hay revisión material de r1: sus pendientes quedan explícitos.

## Revisión humana y aceptación final

**Confirmación literal recibida de Raúl:**

> Confirmo que C0216.MP4 es representativo y adecuado como fixture STUDIO para F001.

Se registra su juicio sin pedir de nuevo confirmación de representatividad. No
es una renuncia a AC-01/05/06/07/08/10. Los intervalos pueden permanecer UNKNOWN
en las notas actuales, como pidió; r1 no permite cerrar los checks que los exigen
hasta que exista su referencia. No se fabrican intervalos ni frases a partir de
metadatos, silencio, guion opcional o usos normales de again. No STT/detector.

**Paquete:** RAW canónico + reference-notes.md e2 + esta tabla + manifest e2.  
**Revisor:** Raúl, mensajes del 2026-10-03; VLC a velocidad normal 1× confirmado.  
**Adecuación/representatividad:** CONFIRMED, vinculada al nombre autoritativo y SHA-256 medido arriba.  
**Feature DONE / aceptación final de verificación completa:** pendiente; estado HUMAN_REVIEW.

Recuperación y contexto/reproducción ya comprobados. Próximo paso autorizado:
registrar las referencias humanas de contenido/movimientos cuando estén disponibles
y cerrar revisión del paquete completo, sin modificar r1. No se necesitan tiempos
exactos de corte: r1 exige referencias aproximadas, aún UNKNOWN. F002 y tratamiento
futuro de audio permanecen fuera. MOBILE sigue preservado separadamente y no entra
en ninguno de estos resultados.
