# F002 — Content Project Ingestion and Media Inspection

**Documento:** requirements — QUÉ debe existir\
**Bundle revision:** r1\
**Owner:** Raúl Almeida\
**Roadmap:** Fase 2 — Ingestion + Media Inspection\
**Predecesor:** [F001 DONE, e5](../F001-real-capture-fixture/validation.md), cierre 7e0bc22\
**Decisión relacionada:** [D001](../../decisions/D001-local-source-contract.md), Proposed, no aceptada\
**Estado y aprobación:** únicamente en [plan.md](plan.md)

## Objetivo y alcance

Introducir una grabación real como input local, inspeccionable y recuperable para
las siguientes features. Raúl debe poder localizar los bytes originales, saber
qué streams y reloj usar, distinguir mediciones de hechos declarados y entender
por qué un input todavía no está listo. Un MP4 o un comando exitoso no bastan.

F002 entrega una operación local repetible: copia verificada, manifest de fuente,
inspección determinista, clasificación técnica y reporte legible. Una fuente
principal por proyecto con vídeo y audio integrados; todos los streams se
inventarían y se seleccionan vídeo/audio sin adivinar el micrófono. Se admiten
otros nombres, rutas, contenedores/codecs soportados por herramientas existentes,
resoluciones, cadencias y perfiles, sin dependencia del montaje STUDIO.

Fuera: STT, extracción de audio para proveedores, detección de idioma/voz/retomas,
semántica, storyboard, edición, EDL, captions, mejora de audio, proxies de trabajo,
normalización de FPS/orientación, tracking, zonas de marca, assets, HyperFrames,
render, UI, DB, API, colas, CI/CD, LFS, nube y publicación. Tampoco validar el
MOBILE real candidato, cambiar F001 ni implementar F003. Muestras sintéticas
pequeñas para probar ingestión no son vídeos de producción.

## Términos y autoridad

| Término | Significado F002 |
| --- | --- |
| Source/original | Archivo externo introducido, sin cambios por F002. |
| Owned RAW | Copia de bytes idénticos dentro del proyecto; autoridad del contenido. |
| Content Project | ID explícito + una fuente poseída + manifest de identidad/procedencia + revisiones de inspección; no scaffold de pipeline. |
| Source ID | `sha256:<64 hex minúsculas>`; identidad de contenido, independiente de nombre/ruta. |
| Project ID | Identidad del trabajo, explícita por operador, `[a-z0-9][a-z0-9-]{0,63}`; no derivada del nombre del vídeo. |
| READY | Input técnicamente verificado según este contrato; no prueba voz inteligible, narrativa, posibilidad de crop ni producción aprobada. |
| UNKNOWN | Propiedad no establecida; `null` y motivo. Nunca cero, cadena vacía, falso o dato deseado. |

Constitución §§8–14/24/35–39: preservar RAW/voz, no asumir orientación física,
mostrar incertidumbre y evidencia; §§4–6: aprobación humana por revisión. Tech-stack
§§6/11/12: herramientas deterministas, archivos locales, límites de recursos y
separación de responsabilidades. Mission §§5–6 y roadmap Fases 2–3 limitan el
primer supply chain; un fixture Sony no se convierte en criterio universal.

Los specs raíz tienen referencias históricas «F002 no autorizado» anteriores a
este turno. El mensaje adjunto 09eb3b1a-f082-4d19-b2fb-5bdcac283c62 autoriza ahora
solo PLAN; no es contradicción material de producto ni permiso de implementar.

## Requisitos e invariantes

| ID | Comportamiento obligatorio |
| --- | --- |
| R-01 | Input: ruta local regular no vacía legible, ID, perfil declarado `STUDIO`, `MOBILE` o `UNKNOWN`; hash esperado opcional para uso general, obligatorio en prueba F001. No URL/carpeta/dispositivo ni dependencia de XML. |
| R-02 | Copia completa independiente; SHA-256 de origen antes/después y copia leída por separado coinciden, además de bytes. Nunca escribir en fuente, recovery, F001 o vendor. Hash esperado divergente impide READY. |
| R-03 | Procedencia: nombre/ruta original y resuelta, fecha UTC de ingestión, perfil/limitaciones declarados y referencia de fixture/recovery si se aportan. La ruta original es información, no dependencia operativa. No inventar equipo, idioma, captura o permiso de nube. |
| R-04 | Inspeccionar contenedor y todos los streams; preservar probe y normalizar solo campos necesarios. Selección inequívoca/expresa, codec/properties, raster/display y tiempos conforme a las secciones siguientes. |
| R-05 | Comprobar decodificación completa de streams seleccionados y recorrer sus timestamps presentados. No decidir CFR por `avg_frame_rate == r_frame_rate`; no determinar orientación física con dimensiones. |
| R-06 | READY requiere integridad vigente, revisión completa consistente, vídeo/audio seleccionados, dimensiones/codec/audio/time bases y duración útiles, reloj exacto y geometría vertical identificada. Desconocidos opcionales no fallan; ausencias necesarias sí. |
| R-07 | JSON versionado, serialización estable, offsets exactos y binding por hashes. El consumidor no parsea ffprobe ni depende de Python, nombre Sony o ruta de origen. |
| R-08 | Idempotencia, revisión/regeneración y fallos observables según el contrato; no sobrescribir otra fuente/proyecto ni conservar READY como fallback tras fallo de reinspección. |
| R-09 | Fuentes/proyectos/evidencia multimedia ignorados; solo código/especificaciones/pruebas y pequeños resúmenes saneados en Git. Nunca 2,8 GB RAW, credenciales o logs de auth. |
| R-10 | Evidencia independiente real/negativa y revisión humana del paquete exacto antes de DONE. F002 READY y feature DONE no son autorización F003 ni PRODUCTION_APPROVED. |

No umbral 4K/25 FPS/H.264/PCM/Sony/trípode/DJI/luces/teleprompter. Audio integrado
no demuestra su origen ni contenido. Información reportada de captura se mantiene
separada de propiedades medidas. La selección automática de una única pista no
se describe como identificación de la voz.

## Inputs, copia y artefactos

Propuesta [D001](../../decisions/D001-local-source-contract.md): copia en vez de
referencia externa. Ruta por defecto relativa al repositorio, configurable por
operador, siempre local e ignorada durante validación:

```text
.local/projects/<project-id>/
    raw/source                  # bytes exactos, sin depender de extensión/nombre
    project.json                # manifest autoritativo de fuente/contexto
    current.json                # resultado/puntero derivado; no autoridad de RAW
    inspections/<run-id>/
        inspection.json         # contrato normalizado, derivado
        ffprobe.json            # respuesta original de herramienta
        timing-summary.json     # recorrido completo, conteos/orígenes/extremos
        frames.tsv              # PTS/duración de streams elegidos, sin píxeles
        decode.log              # errores y exit code en execution.json
        execution.json          # versión, argv saneado, tiempos, resultado
        report.md               # resumen humano
```

No crear carpetas idea/transcript/storyboard/assets/composition/review/output.
`run-id` es UUID aleatorio de intento, no identidad del contenido normalizado.
Staging/locks/diagnósticos fallidos viven como hermanos ignorados bajo
`.local/projects/.staging/`, `.locks/`, `.failures/`. No constituir servicios.

Autoritativos: RAW copiado y `project.json` para identidad/procedencia original;
decisiones de selección/orientación declarada quedan retenidas en cada revisión,
no se presentan como metadata del archivo. Fuente externa/recovery son referencias
históricas. Derivados: inspección, probe, puntero, reportes/logs; se regeneran desde
RAW + manifest + opciones registradas + versión de inspector/herramientas.
No copiar sidecar ni notas F001 como fuente adicional: enlazar su identidad para
procedencia/evidencia; nunca requerir su disponibilidad para operar el proyecto.

## Contratos máquina mínimos — propuesta normativa v1

Las tablas definen keys/tipos y reglas obligatorias; se implementará un validador
pequeño con stdlib, sin dependencia de librería/schema externa. No se diseña
contrato de transcript ni de pipeline completo.

Reglas comunes:

- `schema_version: 1` entero y `kind` identifica cada documento. Keys v1 siempre
  presentes; valores opcionales `null` con `unknowns` por ruta de campo y motivo
  (`NOT_REPORTED`, `NOT_PROVIDED`, `INVALID_METADATA`, `AMBIGUOUS`, `UNSUPPORTED`).
  Lista vacía significa inventario conocido vacío. Campo necesario desconocido
  impide READY. `0/0`, N/A, NaN e Infinity nunca se convierten en cero.
- Tiempo/ratio `R` = string racional reducido `n/d`, denominador positivo, cero
  `0/1`; PTS/ticks enteros como strings decimales, sin flotantes. Rotación reportada
  como string decimal exacta. Bytes/índices/counts/dimensiones enteros JSON no
  negativos ≤ 2^53−1; exceso => limitación explícita, nunca pérdida silenciosa.
- UTF-8, keys ordenadas recursivamente, indentación 2, LF final, sin NaN/Infinity,
  arrays de streams por índice, motivos por código/ruta. Unicode se preserva.
  SHA-256 sobre esos bytes, sin campos de hash autorreferenciales. No redactar
  valores fuente en el contrato local; sanear copias/reportes públicos por separado.
- Core v1 cerrado; extensiones solo en `extensions` objeto con keys por namespace
  (`org.example.feature`), ignorables sin afectar readiness. Documentos futuros
  separados; no reescribir los artefactos F002 para añadir transcripts. Nueva
  semántica incompatible => nueva versión/decisión, conservar revisión anterior.
  Versión/kind desconocidos se rechazan; un consumidor no supone compatibilidad.

### project.json — `kind: content-project-source`

| Key | Tipo / contenido |
| --- | --- |
| `schema_version`, `kind`, `project_id` | Versión 1, kind anterior, ID validado. |
| `source` | `{id, path, bytes, sha256, original_name, original_path, resolved_original_path, ingested_at_utc}`; path exactamente `raw/source`; ID/hash/bytes obligatorios, fecha ISO 8601 UTC con `Z`. Paths originales absolutos locales solo procedencia. |
| `capture_context` | `{profile, limitations}`; profile enum declarado, limitations array de textos USER-REPORTED; vacío no prueba ausencia de problemas. No language/equipment defaults. |
| `references` | `{fixture_id, feature_revision, recovery_location, evidence_manifest_sha256}`: strings/null, declarados/referencia a evidencia previa; backup no verificado por F002 debe indicarse en reporte, no afirmar equivalencia actual. |
| `unknowns`, `extensions` | Mapa de motivos y extensiones; captura/contexto/referencias USER-REPORTED o REFERENCED, bytes/hashes MEASURED. |

Manifest creado una vez después de copia verificada. No alterar bytes/identidad
por reinspección; cambio de fuente/contexto inicial usa nuevo project ID en F002.

### inspection.json — `kind: media-inspection`

| Key | Tipo / contenido |
| --- | --- |
| `schema_version`, `kind`, `project_id`, `source_id`, `source_sha256`, `project_manifest_sha256` | Binding obligatorio a fuente y manifest existentes. |
| `inspector_version`, `tool_versions` | Versión del contrato/normalizador y strings de ffprobe/ffmpeg; afectan identidad derivada, sin IDs de provider. |
| `container` | `{format_names, reported_start_s, reported_duration_s}`; nombres array, tiempos `R`/null, duración positiva cuando informada. No duración ≡ narración válida. |
| `streams` | Array de `{index, type, codec, time_base_s, start_pts, reported_start_s, reported_duration_s, duration_ticks, video, audio}`. type video/audio/data/subtitle/attachment/unknown; optional no informados null. |
| `streams[].video` | Solo vídeo: `{width, height, pixel_format, sar, dar_reported, r_frame_rate, avg_frame_rate, attached_picture, rotation_reported_deg, rotation_tag_deg, display_matrix}`; ratios `R`/null, matriz string/null literal conservada. |
| `streams[].audio` | Solo audio: `{sample_rate_hz, channels, channel_layout, sample_format, bits_per_sample}`; enteros/string/null. No inferir layout estéreo por 2 canales. |
| `selection` | `{video_index, audio_index, basis}`; índices/null, basis `{video: UNIQUE_CANDIDATE/USER_SELECTED/UNRESOLVED, audio: ...}`. Se preservan streams no elegidos. |
| `display` | `{transform_basis, rotation_to_apply_deg, raster_axis_width, raster_axis_height, square_pixel_width, square_pixel_height, aspect, geometry}`; basis `MATRIX/TAG/NO_ROTATION_DECLARED/USER_OVERRIDE/UNRESOLVED`; ángulo entero/null (positivo antihorario), ejes ints/null, dimensiones de vista y aspecto `R`/null; geometry `PORTRAIT/LANDSCAPE/SQUARE/UNKNOWN`. No campo que pretenda medir orientación física de cámara. |
| `timing` | `{clock, origin_video_pts, origin_time_base_s, origin_media_s, clock_id, video_start_s, video_end_s, audio_start_s, audio_end_s, extent_basis, cadence, frame_count, audio_frame_count}`. clock `source-presentation-v1`, tiempos `R`/null, cadence `UNIFORM/VARYING/UNKNOWN`, extent_basis por stream `FRAME_EXTENTS/STREAM_DURATION/UNKNOWN`. Clock ID SHA-256 de JSON canónico `{source_id, video_index, origin_video_pts, origin_time_base_s, clock}`. |
| `options` | `{video_index, audio_index, display_rotation_override_deg, override_reason, override_reviewer}`; opciones originales nullable; override humano separado, no borra matriz/tags. Sin edición. |
| `readiness` | `{status, reasons}`; `READY/NEEDS_REVIEW/BLOCKED/INVALID`; reasons array de `{code, field, action}`; vacío solo READY. |
| `unknowns`, `extensions` | Ausencias explícitas y extensión; metadata MEASURED, cálculos de display/tiempo DERIVED, overrides USER-REPORTED. |

No fecha/run-id/path absoluto de staging en inspection.json: con el mismo input,
opciones y versiones produce los mismos bytes. No es necesario prometer que
ffprobe bruto sea byte-idéntico entre versiones/rutas. Fecha/run-id/argv/rendimiento
viven en execution.json, fuera de identidad normalizada.

### current.json — `kind: current-media-inspection`

`schema_version`, `kind`, `project_id`, `source_id`, `status`, `reasons`,
`inspection_path`, `inspection_sha256`, `execution_path`, `execution_sha256`,
`project_manifest_sha256`, `artifact_hashes`, `unknowns`, `extensions`.
Paths relativos, sin `..` ni symlinks escapando del proyecto. Hashes de artefactos
publicados, excepto current.json mismo. En intento incompleto pointers/hashes
pueden ser null, con motivo; estado BLOCKED. Nunca READY con una referencia
inexistente, un hash divergente o ejecución no completada.

### Evidencia auxiliar y origen de los datos

`execution.json` (`kind: media-inspection-execution`, schema_version 1) contiene
`project_id`, `run_id`, `source_id`, `project_manifest_sha256`, `started_at_utc`,
`finished_at_utc` (null mientras incomplete), `completed` boolean, `status`,
`reasons`, `options`, `versions`, `commands`, `integrity`, `artifact_hashes`.
Commands array: `{argv, exit_code, timed_out, output_truncated, stdout_path,
stderr_path}`; paths locales relativos/null, argv sin entorno/credenciales.
Versions registra Python/ffmpeg/ffprobe/inspector; options incluye selecciones y
límites efectivos. Integrity registra bytes/hashes/stats de owned source y origen
cuando utilizado, antes/después. Artefactos listados no incluyen execution.json
ni current.json para evitar ciclos. Un completed=false no permite READY.

`timing-summary.json` es evidencia auxiliar versionada de conteos, primer/último
PTS y durations por stream, time bases, delta(s) de vídeo, fuente del extent y
errores; reproduce los campos timing publicados. `frames.tsv` tiene encabezado
`stream_index`, `pts`, `duration_ticks`, `time_base_s`; valores desconocidos se
representan explícitos, no ceros. No publicar su contenido como transcript.
Probe original es JSON vendor, no versionarlo como contrato propio.

Clasificación de evidencia: source bytes/SHA/metadata y resultados de comandos
MEASURED; display/clock/extents/cadencia DERIVED con inputs retenidos; capture
context/selección humana/override USER-REPORTED; metadata no disponible UNKNOWN
con motivo. Referencias a F001 son REFERENCED y conservan su clasificación previa.
No promover tags de fecha/idioma/handler a hechos humanos de captura o de voz.

## Selección, propiedades y orientación

Un vídeo candidato no puede ser attached picture/thumbnail/cover art. Un candidato
único y un único audio se seleccionan automáticamente; múltiples candidatos
requieren índices explícitos del operador, no preferencia por primer índice,
`default`, nombre del handler o resolución. Selección inexistente/de tipo erróneo
=> INVALID. Streams auxiliares se inventarían; no decodificar rtmd como vídeo.
Si la evidencia disponible no permite establecer si un stream de vídeo es imagen
adjunta/thumbnail, su elegibilidad queda UNKNOWN y bloquea la selección automática;
no sustituir esa ausencia por `attached_picture=false`.

Rotación: conservar matriz y tags originales. Admitir matrices de rotación pura
ortogonal (0/±90/180, permitiendo traslación del origen), sin reflexión, escala,
shear/perspectiva; comparación de coeficientes en representación fija de matriz.
Tag sin matriz es fallback, convención convertida/documentada por adaptador.
Tag/matriz incompatibles, transformación no soportada o signo no resoluble
=> NEEDS_REVIEW; no elegir por conveniencia. No redondear rotación arbitraria.

`rotation_to_apply_deg` y override usan grados **antihorarios positivos** desde
raster sin rotación, normalizados a 0/90/−90/180. La metadata ffprobe se preserva
aparte. Para matriz válida, corresponde a la transformación de presentación, no
al parámetro inverso de una función que construye matrices. La documentación de
[matrices FFmpeg](https://ffmpeg.org/doxygen/trunk/group__lavu__video__display.html)
distingue extraer ángulo antihorario de construir giro horario; V-10 valida los
cuatro sentidos con patrón visual. Para F001, −90° equivale a 90° horario.

Con SAR conocido, dimensiones de vista en píxeles cuadrados antes de rotación
son `width × SAR` y `height` (racionales); a 90° se intercambian, aspecto se invierte.
DAR reportado se retiene, y si su ratio racional contradice el cálculo exacto
se marca conflicto. Los ejes raster después de
rotación siguen separados de dimensión física de visualización. No renderizar
resolución redondeada ni aplicar cambios al RAW. SAR/DAR ausentes => geometría
UNKNOWN; no inventar 1:1. Geometry describe el display calculado, no el montaje.

Sin metadata de rotación: `NO_ROTATION_DECLARED`, transformación del contenedor
identidad para cálculo si SAR conocido, rotation_reported_deg=null. No afirmar
«cámara horizontal» ni «0° medidos». Un vídeo de lado, contradicción de vista o
geometría no vertical requiere revisión. Override humano puede resolver solo
rotación de vista (0/±90/180) conservando metadata/conflictos; no reemplaza codec,
SAR, dimensiones o tiempos desconocidos ni certifica encuadre. Landscape/square
quedan NEEDS_REVIEW en este supply chain hasta resolver orientación; no se rechaza
el contenido universalmente ni se intenta crop. Portrait READY no exige 9:16
exacto ni 1080×1920: compatibilidad de entrega/layout se valida después.

Para F001: los datos aceptados son referencia externa de comparación, no lógica
de ingestión: raster 3840×2160, SAR 1:1, matriz −90°, display 2160×3840, aspecto
9/16; vista erguida ya confirmada por Raúl. XML no interviene en esa resolución.

## Reloj y duración

`source-presentation-v1`: `t_source = PTS × time_base − origin_media_s`.
Origen = menor PTS presentado del vídeo seleccionado en recorrido completo bajo
el demuxer/version registrado; no DTS ni primer paquete de codificación. `PTS`
y time_base se retienen, cálculo con racionales. Timecode/capture date quedan
fuera del reloj. Cambiar vídeo u origen cambia clock_id y obliga a invalidar
referencias dependientes; cambiar solo audio conserva ese reloj de vídeo.

Vídeo comienza en 0. Audio puede comenzar antes (offset negativo) o después; no
desplazar cada stream a cero ni reparar sincronía. Para un futuro audio extraído
sin cambio temporal, un consumidor mapearía `audio_t + audio_start_s` al reloj
de fuente; F003 deberá validar su extracción/mapping, sin asumir que su provider
usa este reloj. Intervalos fuente son `[inicio, fin)`, en segundos racionales;
no índices/FPS ni coordenadas de entrega.

Recorrer frames presentados de streams seleccionados, sus PTS reales/duraciones,
con conteo >0. PTS faltantes/duplicados/no monótonos o solo best-effort estimado
=> BLOCKED para el reloj exacto; conservar evidencia, no inventar tiempos. B-frames
con DTS distinto no son fallo si PTS presentados son válidos. Diferencias exactas
entre PTS consecutivos del vídeo: todas iguales => UNIFORM, diferentes => VARYING;
menos de dos frames => UNKNOWN. VARYING es input válido; no normalizar a CFR.

End de cada stream = máximo PTS+duración de frames cuando se conoce cada duración.
Fallback: `start_pts + duration_ticks`, en time_base del stream, solo si start
coincide con primer PTS y duración positiva; base STREAM_DURATION declarada, no
precisión de frame inventada. Si ninguna base sirve => end UNKNOWN/BLOCKED.
Duración efectiva de vídeo `video_end_s > 0` y audio `audio_end_s > audio_start_s`
son obligatorias; duration de contenedor/reportada se conserva separada. Duración
reportada discrepante > máximo de un frame observado y una muestra de audio
=> NEEDS_REVIEW, nunca sustituir a escondidas. No extrapolar último frame con
average FPS. Para F001 el origen es 0 y extremos de audio/vídeo 1164/5 s.

Comparar reported stream duration con end−start del stream correspondiente;
container duration con `max(video_end_s,audio_end_s) − min(0,audio_start_s)`.
El contenedor puede incluir streams no seleccionados: discrepancia se informa
como NEEDS_REVIEW, no corrupción inferida. La tolerancia temporal se deriva del
máximo delta/duración de vídeo observado y 1/sample_rate; si no se puede calcular
una base necesaria, no declarar comparación PASS.

## Idempotencia, regeneración y validez

- ID existente + mismos bytes/SHA + manifest/contexto inicial idénticos + mismas
  opciones/versiones + revisión completa válida => `NO_OP`, sin copia nueva,
  nuevo run, modificación de archivos ni timestamps de proyecto. Verificar hashes
  del owned RAW y artefactos cada vez; atime de lectura no forma parte de identidad.
  Alias/ruta nueva de la misma fuente no reescribe procedencia inicial.
- ID existente con fuente/hash/contexto distinto => `PROJECT_CONFLICT`; conservar
  proyecto, pedir otro ID. Proyectos con IDs distintos pueden usar mismos bytes;
  no catálogo global/deduplicación. Cambio de selección/override requiere operación
  explícita inspect, no una mutación disimulada de ingest idempotente.
- `inspect` usa owned RAW/manifest, aunque origen esté desconectado/movido. Nueva
  inspección explícita crea nueva revisión, conserva previas y solo cambia puntero
  tras commit completo. Con mismos input/opciones/versiones, normalized inspection
  byte-idéntica. El informe de ejecución puede diferir.
- Artefactos derivados ausentes/corruptos => guard no READY; inspect puede regenerar.
  RAW ausente/divergente => BLOCKED, nunca aceptar hash nuevo o sobrescribirlo.
  Recuperación desde copia externa requiere verificar identidad y acción explícita
  del operador; no reparaciones automáticas ni borrado de originales.
- `current.json` es snapshot, no garantía de que el filesystem no cambie después.
  Toda operación de lectura/consumo debe usar guard que revalide manifest, fuente,
  hashes/paths, versión y completitud de revisión **en ese momento**. Contrato para
  futuros consumidores: volver a verificar inmediatamente antes de procesamiento;
  no confiar solo en el string READY ni en una comprobación antigua. Se documenta
  la ventana de cambio externo posterior: el consumidor futuro deberá comprobar
  estabilidad durante su operación; no se promete inmutabilidad frente a terceros.

## Fallos y publicación local

Un solo writer por ID mediante lock exclusivo local; segundo writer devuelve
BUSY sin mutar. Lock abandonado tras interrupción requiere diagnóstico/recuperación
explícita, nunca borrar por antigüedad. No servicio/concurrencia distribuida.

Copia por chunks, stats y hash inicial/final para detectar cambios, lectura del
destino independiente. Staging en el mismo filesystem; publicar por rename/replace
atómico solo artefactos completos (flush/fsync antes), mantener revisions antiguas.
Antes de reinspección, puntero atómico BLOCKED/INSPECTION_IN_PROGRESS invalida READY
previo; interrupción no lo restaura. Publicación final liga hashes de manifest,
fuente e inspección/ejecución. En primer intento fallido no aparece un proyecto
READY; copia/evidencia de staging se conservan identificadas, nunca source recovery.
Puede publicarse proyecto con fuente verificada y resultado NEEDS_REVIEW/BLOCKED/
INVALID, claramente no apto; no reutilizar un directorio preexistente ajeno.

| Caso | Resultado de operación / clasificación, acción |
| --- | --- |
| Ausente/vacío/no regular/no legible | INVALID / INPUT_*; no copia/publicación READY. Diagnóstico indica ruta/problema sin secretos. |
| Tool ausente/falla, probe JSON inválido, timeout | BLOCKED / TOOL_* o PROBE_FAILED; conservar salidas, no instalar/reintentar automáticamente. |
| Sin vídeo no attached | INVALID / NO_VIDEO; preservar input, solicitar grabación apta. |
| Sin audio | INVALID / NO_AUDIO para este contrato AV; no fabricar voz ni READY para F003. |
| Múltiples vídeo/audio sin índices | NEEDS_REVIEW / SELECT_VIDEO o SELECT_AUDIO; inventario y comando de resolución, detener checks dependientes. |
| Decode falla o no produce frames seleccionados | INVALID / DECODE_FAILED o EMPTY_STREAM; metadata exit 0 no basta. |
| Codec/dimensiones/audio sample rate o canales no útiles | BLOCKED / REQUIRED_PROPERTY_UNKNOWN; no inferir por extensión. |
| Rotation/SAR/vista conflictiva o no vertical | NEEDS_REVIEW / DISPLAY_*; Raúl decide vista, sin crop/normalización. |
| Duración/reloj no establecibles | BLOCKED / TIMING_UNKNOWN; no valores FPS como fallback de precisión. |
| Metadata opcional ausente | `null` + motivo; READY posible solo si todas las condiciones necesarias conocidas. |
| Fuente cambia durante copia/inspección o owned RAW diverge | BLOCKED / SOURCE_CHANGED; invalidar estado, preservar versiones y pedir recuperación/verificación. |
| Sin espacio/fallo de escritura/rename/interrupción | BLOCKED / IO_*; staging o revisión fallida retenida; nunca copia parcial válida. |
| Conflicto de ID/path/version/manifest/hash de revisión | BLOCKED/INVALID con código específico; no sobrescribir ni fallback READY. |

Readiness precedence: INVALID > BLOCKED > NEEDS_REVIEW > READY; conservar todos los
motivos aunque uno domine. Esta clasificación de inputs es independiente de los
resultados SDD PASS/FAIL/BLOCKED/HUMAN_REVIEW_REQUIRED de validation.md. Un caso
negativo correctamente rechazado puede pasar su prueba de comportamiento.

## Frontera mínima hacia futura F003

Desde raíz de proyecto + current.json + project.json + inspection.json, un
consumidor sin FFmpeg parser ni conocimiento Sony puede obtener: fuente local
relativa, bytes/SHA, bindings/hash de revisión/versiones, audio/vídeo elegidos y
codecs/properties, time bases/PTS, reloj ID/origen, intervalos/offset de audio y
vídeo, raster/display, estado/motivos y contexto declarado separado. Debe validar
guard/readiness. No API/provider/config/upload, audio derivado, texto ni schema
transcript. F003 seleccionará formato de extracción y proveedor tras aprobación.

## Criterios de aceptación

| ID | Condición observable / evidencia requerida | Validación |
| --- | --- | --- |
| AC-01 | RAW F001 real introducido como proyecto local con estructura mínima, origen y owned copy localizables; source/context no codificados en lógica. | V-01, V-02, V-12 |
| AC-02 | Bytes y hash de origen/copia antes/después coinciden con identidad F001; RAW/recovery/F001 intactos, copia independiente. | V-01, V-02, V-07 |
| AC-03 | Propiedades e inventario correctos por probe independiente, audio/vídeo elegidos sin ignorar ambigüedad; unknowns honestos. | V-03, V-04, V-11 |
| AC-04 | Raster y display separados; F001 representa vista vertical a pesar de raster horizontal; casos sin metadata/conflicto/no vertical y SAR no cuadrado cumplen contrato. | V-04, V-10, V-14 |
| AC-05 | Reloj/PTS/time bases/duraciones/offsets correctos, VFR y timestamps no cero/negativos sin FPS supuesto; no confundir timecode. | V-05, V-10 |
| AC-06 | JSON v1 validable/serialización estable, bindings y guard bloquean versión/hash/paths inválidos; extensions inocuas. | V-06, V-12 |
| AC-07 | Reingest idéntico NO_OP sin cambios; distinto origen mismo ID rechaza sin sobrescribir; alias válido no cambia provenance. | V-07 |
| AC-08 | Regeneración independiente del origen y byte-idéntica del contrato con mismas opciones/versiones; conserva fuente/manifest/previas. | V-08 |
| AC-09 | Negativos, fallos parciales, interrupción, writer simultáneo y source mutation nunca falsamente READY ni destruyen originales. | V-09, V-11, V-13 |
| AC-10 | Prueba de consumidor mínimo encuentra inputs/reloj sin vendor ni F003; reporte evidencia y aprobación humana exacta, media ignorada y límites declarados. | V-12, V-14 |

## Preguntas, propuestas y decisiones diferidas

| Tipo | Decisión / gate |
| --- | --- |
| Blocking questions | Ninguna para presentar PLAN. Fuente, contexto, recuperación y convenciones están documentados; las decisiones nuevas están propuestas, no asumidas como aprobadas. |
| Propuesta a aprobar | D001, copy ownership, JSON v1/reloj de vídeo y runtime limitado Python; espacio extra/scan completo como coste local. |
| Supuesto reversible | Una fuente AV integrada por proyecto; F001 lo satisface. Otros captures/audio separado se diseñan después, sin schema especulativo ahora. |
| Verificar en IMPLEMENT | Runtime/tools exactos y espacio/acceso al RAW, hashes/manifests recuperables; no actualizaciones automáticas. |
| Deferred F003 | STT, extracción/resampling, idioma, términos, confianza, provider, gastos y precisión de palabras. |
| Deferred edición/render/audio/MOBILE | Normalización temporal/display, source-to-delivery, retomas, crop/safe zones, loudness, validación del candidato real MOBILE. |
| Deferred arquitectura | Fuentes múltiples/sesiones, migraciones v2, deduplicación, GUI, distribución/install, multiwriter/red, backup remoto y servicios. |

Aceptar este PLAN decide solo el contrato y alcance F002; no autoriza una feature
siguiente ni modifica aceptación de F001.
