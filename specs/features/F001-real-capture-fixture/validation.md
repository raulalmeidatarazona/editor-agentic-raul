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

## Evidencia de ejecución — entrega e1 abierta (2026-10-03)

**Verification result:** BLOCKED — ubicación/hash de recuperación pendientes (V-01/V-10).  
**Juicios humanos pendientes:** V-02 (voz/origen), V-04–V-09 y aceptación de V-10.  
**Owner acceptance of feature:** NOT GRANTED.  
**Operador:** Codex; inspección objetiva 2026-10-03 15:45–15:48 Europe/Malta (13:45–13:48 UTC).  
**Contrato:** bundle r1 archivado sin cambios; la sección normativa anterior conserva sus bytes. e1 identifica esta evidencia parcial, no una modificación del PLAN ni DONE.

Raúl informó que la captura física estaba completa, designó el STUDIO autoritativo
y autorizó continuar IMPLEMENT/VERIFY. Las rutas concretas se resolvieron por
inventario del directorio indicado: un MP4 Sony y su sidecar; no hay toma auxiliar.
El MOBILE fue excluido explícitamente por el propietario y no se usa en ningún check.
Su mensaje conserva `<LOCATION>` para recuperación; no es una ruta válida.

| Campo de identidad | Valor real / clasificación |
| --- | --- |
| Fixture / revisión / rol | F001-studio-001 / e1 abierta / principal; USER-REPORTED designación autoritativa de Raúl |
| Nombre original / RAW absoluto | C0216.MP4 / `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216.MP4` |
| Bytes | MEASURED: 2.873.163.442 |
| SHA-256 inicial y posterior | MEASURED, ambos `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`; bytes y mtime estables |
| Sidecar | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216M01.XML`; 1.933 bytes; SHA-256 155550ef95eaf6e885e6e5be67667c8089e4060c774023cbfa0f34ad14c1bde5, inicial/posterior coincidentes |
| Backup / hash / acceso | UNKNOWN; copia declarada USER-REPORTED pero sin ubicación concreta ni lectura; no se acepta por declaración sola |
| Duración / propiedades | MEASURED: 232,800 s; H.264 3840×2160, 25/1 reportados, SAR 1:1, DAR almacenado 16:9, rotation −90; audio stream 1 PCM 16-bit BE, 48 kHz, 2 canales |
| Orientación de evidencia | OBSERVED: autorrotación FFmpeg produce sujeto erguido en frame 360×640 9:16; confirmación/player de Raúl UNKNOWN |
| Notes / identidad | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/reference-notes.md`; SHA-256 `25d337319c2a0049bead43a4b311e1ffbb839e9f40c881b1feb31ff3aec71a38` |
| Evidencia / manifest | `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence` / `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/evidence/evidence.sha256`; SHA-256 del manifest `abf2c1b4404172b060082237f2238239d9f0ed6e51164b908a90b7718bd099f3`; 29 artefactos cubiertos, incluyendo notas |
| Herramientas | /opt/homebrew/bin/ffmpeg y ffprobe 9.0.1; /usr/bin/shasum -a 256; versiones completas y comandos/exit codes retenidos; sin instalación |

### Resultados por check

Todos los resultados se vinculan al SHA-256 principal arriba. Las rutas de
artefactos que siguen se resuelven dentro del directorio absoluto de evidencia.
El manifest permite verificar los hashes individuales. No se equipara decode
sin errores con una escucha humana ni se presume el origen DJI del stream 1.

| Check / AC | Procedimiento real / esperado vs observado | Evidencia | Resultado |
| --- | --- | --- | --- |
| V-01 / AC-01 | Fuente regular no vacía, bytes/hash inicial y posterior iguales; copia recuperable no localizable con el placeholder proporcionado. | initial-file-stat.json, source.sha256, source-after.sha256, integrity-result.json; backup pendiente | BLOCKED |
| V-02 / AC-02/03 | Probe salida 0, stderr vacío; vídeo real visible en frames, duración/dimensiones positivas, una pista audio integrada con propiedades conocidas. Identificarla como voz y verificar su procedencia requiere V-05. Metadata objetiva satisfecha; voz UNKNOWN. | ffprobe.json, ffprobe.stderr.log, commands.json; frames | HUMAN_REVIEW_REQUIRED |
| V-03 / AC-02 | Decodificación completa streams 0 y 1, -xerror -err_detect explode; salida 0, decode.log vacío (0 bytes). Stream 2 es metadata fuera de la selección audiovisual; origen de audio se mantiene pendiente. | decode-result.json, decode.log, decode.stdout.log, versiones; SHA estable | PASS — solo decodificación completa de vídeo/audio integrado |
| V-04 / AC-03 | Matriz −90 y píxeles 3840×2160; frames autorrotados verticales 9:16 erguido. Falta contraste con montaje y comportamiento del player de Raúl. | ffprobe.json, frame-030s.png, frame-150s.png, frame-220s.png, frame-observations-procedure.json; confirmación pendiente | HUMAN_REVIEW_REQUIRED |
| V-05 / AC-02/04 | No se ha registrado escucha completa normal con Raúl; inteligibilidad, palabras críticas, distorsión/dropouts y origen conocido de voz UNKNOWN. No hay umbral numérico inventado ni sustituto por metadata. | reference-notes.md; respuesta de revisión solicitada, pendiente | HUMAN_REVIEW_REQUIRED |
| V-06 / AC-05 | Idea/idioma, pausa normal, tres términos y palabras completas al inicio/final pendientes de escucha humana; no copiar el guion opcional. | reference-notes.md, referencias habladas UNKNOWN | HUMAN_REVIEW_REQUIRED |
| V-07 / AC-06 | Error, pausa, Again aislado, pausa, corrección y frase válida NO RETOMA: palabras/intervalos UNKNOWN; no STT ni detector. | reference-notes.md; revisión solicitada | HUMAN_REVIEW_REQUIRED |
| V-08 / AC-07/09 | Tres muestras muestran cabeza/hombros/torso/manos y postura aproximadamente centrada. No prueban todos los movimientos, continuidad, habitualidad de teleprompter ni representatividad. | Frames en 00:30, 02:30, 03:40; notes; revisión de Raúl pendiente | HUMAN_REVIEW_REQUIRED |
| V-09 / AC-08/09 | Notas objetivas completas y separadas MEASURED/OBSERVED/USER-REPORTED/UNKNOWN; fecha real/zona, montaje, mic/ruta, teleprompter, ajustes/luces, intención, limitaciones y juicio pendientes. XML declara reloj/modelo, no confirma hecho físico. | reference-notes.md, sidecar.sha256; preguntas al propietario pendientes | HUMAN_REVIEW_REQUIRED |
| V-10 / AC-01/10 | Paquete identificado, manifest y exclusión RAW/evidencia de Git comprobados. Falta hash/lectura de recuperación y aceptación expresa de e1; futuras funciones NOT YET VALIDATED. | evidence.sha256, git-exclusion.log, RAW/notas/tabla; backup y aceptación pendientes | BLOCKED; además requiere revisión/aceptación humana |

### Cobertura por aceptación

| AC | Resultado actual / evidencia que falta |
| --- | --- |
| AC-01 | BLOCKED: recuperación verificable con SHA coincidente; integridad local satisfecha. |
| AC-02 | HUMAN_REVIEW_REQUIRED: V-03 pasa; reproducibilidad/voz/escucha completa aún sin evidencia humana. |
| AC-03 | HUMAN_REVIEW_REQUIRED: metadata y vista FFmpeg disponibles; confirmación de orientación/player pendiente. |
| AC-04 | HUMAN_REVIEW_REQUIRED: escucha completa. |
| AC-05 | HUMAN_REVIEW_REQUIRED: idea, términos, pausas y bordes de palabras. |
| AC-06 | HUMAN_REVIEW_REQUIRED: contraste retoma/NO RETOMA con referencias reales. |
| AC-07 | HUMAN_REVIEW_REQUIRED: movimientos, continuidad y teleprompter habitual. |
| AC-08 | HUMAN_REVIEW_REQUIRED: contexto humano no observable, separado de mediciones. |
| AC-09 | HUMAN_REVIEW_REQUIRED: representatividad y limitaciones juzgadas por Raúl. |
| AC-10 | BLOCKED: recuperación; revisión exacta/aceptación aún no otorgada. |

No se han observado errores de decodificación ni cambios de integridad. Esto no
demuestra que no existan fallos de voz/contenido/movimientos. UNKNOWN no es PASS.
No hay indicio que obligue hoy a cambiar r1: se esperan sus evidencias faltantes.

## Revisión humana y aceptación final

**Paquete mínimo:** `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216.MP4` + `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/reference-notes.md` + esta tabla.  
**Revisor requerido:** Raúl; reproductor, escucha completa, fecha y observaciones pendientes.  
**Revisor adicional:** no designado; opcional, sin sustituir juicio de Raúl.  
**Owner acceptance of feature:** NOT GRANTED.  
**Frase de aceptación / fixture ID / SHA / revisión:** pendiente después de completar evidencia.

Preguntas enviadas en este chat el 2026-10-03: ruta/acceso del backup; contexto físico
no observable y exactitud del reloj Sony; revisión completa V-04–V-08 con referencias
habladas/movimientos y juicio representativo. El agente escribirá las respuestas en
las notas; Raúl no debe medir propiedades ni editar Markdown manualmente.

Al recibir la ruta recuperable, leer/hash y comparar contra la identidad indicada.
Al recibir juicios, registrarlos como USER-REPORTED/HUMAN EVIDENCE con fecha y
revisor, actualizar resultados sin relajar AC y regenerar manifest/revisión de
evidencia afectada. Luego presentar el paquete exacto para aceptación de F001.
Si hay ausencia de contenido requerido, señalarla y seguir la recuperación r1;
no corregir mediante edición ni inventar observaciones.

El MOBILE se conserva separado en
`/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/mobile-candidate-001/raw/PXL_20261003_092220543.mp4`:
candidato futuro de Mobile Capture Validation, sin probe/decode/hash/contenido
revisados aquí y sin inclusión en AC/V de F001. No se autoriza F002 ni pipeline.
