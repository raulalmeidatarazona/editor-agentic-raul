# F003 — Provider-Independent Time-Aligned Transcription

**Documento:** requirements — QUÉ debe existir\
**Bundle revision:** r1\
**Owner:** Raúl Almeida\
**Roadmap:** Fase 3 — Transcription\
**Predecesores:** F001 DONE/e5 y F002 DONE/r1/e1\
**Decisión propuesta:** [D002 — initial F003 STT provider](../../decisions/D002-initial-f003-stt-provider.md)\
**Estado y aprobación:** únicamente en [plan.md](plan.md)

## Objetivo, autoridad y alcance

Transformar el audio de un Content Project READY en texto y referencias temporales
auditables para futuros consumidores. El consumidor recibe nuestro contrato, no
JSON Alibaba, URLs, precios ni instrucciones editoriales. La transcripción es
probabilística; la normalización de una respuesta conservada es determinista.
No se promete reproducir la misma respuesta volviendo a llamar al modelo.

Constitución §§4–6/8–14/20/22/24/35–39: aprobación por revisión, voz/RAW preservados,
significado sin correcciones inventadas, QA y coste visibles. Mission y roadmap
Fase 3 exigen texto/tiempo útil antes de semántica; tech-stack §7 exige cloud STT
replaceable, confianza honesta y resultado original recuperable. [D001 aceptada](../../decisions/D001-local-source-contract.md)
define identidad, guard y reloj F002; F003 los consume sin modificarlos.

Alcance: guard F002, preparación técnica de audio, adaptador cloud inicial,
respuesta retenida, normalizador/validador v1, identidad/revisiones, ejecución,
coste, CLI local y evidencia real/negativa/humana. Un proyecto, una fuente AV,
una pista F002 y un canal explícito de voz por solicitud. Sin pipeline scaffold.

Fuera: F004, detección/clasificación de Again/try again/error/retoma, semántica,
hooks/conceptos/secciones, storyboard, cortes/EDL, captions o styling/render,
HyperFrames, assets, tracking, mejora/denoise/EQ/loudness de audio, síntesis de
voz, publicación, analytics de producto, GUI, DB/API/colas/CI/CD, proveedores
alternativos implementados, alineador adicional, chunking y nuevas dependencias.
Los eventos F001 solo son referencias del evaluador en validation.md.

## Entrada obligatoria y conservación

Entrada operativa: raíz del Content Project F002 + configuración F003 explícita.
No aceptar una ruta arbitraria de MP4/WAV como entrada alternativa al proyecto.
Usar `tools/content_contract.py:verify_project` inmediatamente antes de preparar,
enviar y consumir; comprobar estabilidad/hash al terminar. Leer el contrato
normalizado, no reinterpretar ffprobe para sustituir selección/origen de F002.

El fixture primario es `.local/projects/f002-studio-001/`, source ID
`sha256:68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`,
2.873.163.442 bytes. Manifest SHA
`7350428f4c3b7f5ffbf685c4d39a7fad52aae527a4ae08070189442c6aefa3ce`;
inspección `inspections/d48b0e46-af7e-405e-a5ee-0d703d53bcb0/inspection.json`, SHA
`d08658c3542e2a7d10b1093a0de5e464752fd6cbca14588cc816b323478b428f`.
Audio elegido: stream 1, PCM s16be, 48 kHz, 16 bits, 2 canales, layout UNKNOWN.
No identificar DJI ni canal de micrófono a partir de esos datos.

F001 original, recovery, notas y bundles/evidencia F001/F002, `raw/source`,
`project.json`, `current.json` e `inspections/` permanecen intactos. F003 agrega
solo `transcription/` al proyecto y evidencia ignorada. No ejecutar `ingest inspect`
para resolver un fallo F003. Fuente/revisión F002 no válida => detener dependientes.

## Audio preparado y frontera de transporte

Elegir explícitamente canal 0 o 1 tras escucha local de ambos y comprobación de
voz completa; registrar razón/revisor. No usar ambos (doble facturación), downmix
automático ni elegir el canal con mayor volumen como prueba de micrófono. Si no
hay un canal completo/inteligible, NEEDS_REVIEW; otra política requiere PLAN.

Derivado: WAV mono PCM s16le al sample rate nativo, sin resampling, ganancia,
silence removal, padding, corte ni cambio de velocidad. Para F001 son 11.174.400
muestras a 48 kHz, payload 22.348.800 bytes más cabecera, duración 1164/5 s.
Estos son cálculos de planificación, no una extracción ya medida. Conservar
hash/bytes/frame count/comando/versiones/canal y primer PTS de muestra. Verificar
continuidad de frames contra el scan F002 y recorrido de audio propio; gap,
overlap, priming no resuelto o discrepancia de muestra => BLOCKED. No colapsar gaps
para obtener un archivo aparentemente apto. Decodificación/conversión endian y
selección de canal son preparación de transporte, no tratamiento de la voz.

El candidato requiere una URL accesible por el servicio; un path local no basta.
La propuesta r1 usa un objeto privado en OSS Singapore **preexistente y autorizado
por Raúl**, subido manualmente por él desde el WAV preparado. F003 no provisiona
bucket/cuenta ni implementa un uploader. Recibe una URL GET HTTPS firmada por
entorno, comprueba descargando en streaming bytes/SHA iguales al derivado y
envía esa URL en memoria. Sin ACL pública, CDN, vídeo RAW, sidecar ni datos F001.
TTL propuesto 2 horas (mínimo 30 minutos restantes al enviar); borrar el objeto
concreto tras recuperar resultado, como máximo a las 24 horas, por el propietario.
URL expirada puede renovarse para consulta/descarga; nunca implica nueva STT.
Si no existe ese almacenamiento, queda BLOCKED/TRANSPORT_UNAVAILABLE en ejecución;
volver a PLAN para otro transporte/servicio, sin recurrir a Beijing.

## Contrato canónico mínimo v1

JSON UTF-8: keys ordenadas, indentación 2, LF final, Unicode preservado,
sin NaN/Infinity ni floats para tiempo. Core cerrado; versión/kind desconocidos
rechazados. Extensiones solo objeto namespaced inerte. IDs locales de segmentos
y palabras son ordinales estables dentro de una revisión (`s000001`, `w000001`),
no identidades semánticas entre modelos. Todo campo de la tabla está presente.
`null` requiere motivo por JSON Pointer en `unknowns`: `NOT_REPORTED`,
`NOT_REQUESTED`, `UNSUPPORTED`, `UNRESOLVED`; nunca 0/false/string vacío como UNKNOWN.
Lista vacía es un inventario conocido vacío; `words: null` es capacidad ausente.

`transcript.json`, `kind: source-transcript`, `schema_version: 1`:

| Key | Tipo / significado |
| --- | --- |
| `transcript_id` | `sha256:<digest>` de todos los demás campos canónicos, excluyendo solo esta key. Identifica bytes/contenido de revisión, no archivo de cámara. |
| `binding` | `{project_id, source_id, source_sha256, project_manifest_sha256, inspection_sha256, clock_id, audio_stream_index}`; valores del guard F002 y revisión concreta, no defaults Sony. |
| `provenance` | `{execution_id, response_sha256, request_fingerprint, audio_sha256, preparation_sha256, normalization_version}`; referencias opacas independientes del proveedor. |
| `clock` | `{name: source-presentation-v1, unit: seconds, representation: rational, interval: half-open, provider_resolution_s, audio_zero_source_s, audio_end_source_s}`; tiempos racionales reducidos `n/d`, quantum informado/null sin inventarlo. |
| `language` | `{declared, requested, detected}`; declared string/null USER-REPORTED, requested array de códigos, detected string/null solo si provider lo informa. No convertir un hint `es` en detección. |
| `text` | String completo del único transcript/canal. Se conserva exactamente el valor textual del provider; normalización es de estructura/unidades, no reescritura de prosa. |
| `segments` | Array ordenado de `{id, text, start_s, end_s, confidence}`. Segmento = agrupación de frase del provider, sin significado editorial ni nombre vendor. |
| `words` | Array global ordenado de `{id, segment_id, text, punctuation, start_s, end_s, confidence}` o null. Text conserva espacios/texto entregados; punctuation string (incluido `""` conocido) o null. No fabricar palabras dividiendo texto cuando faltan timings. |
| `readiness` | `{status: READY/NEEDS_REVIEW/BLOCKED/INVALID, reasons: [{code, field, action}]}`; READY solo con contrato/integridad/completitud y timing por palabra verificados. No certifica contenido ni producción. |
| `unknowns`, `extensions` | Motivos de ausencias y extensiones sin afectar semántica/readiness. |

Confianza: número decimal finito 0..1 únicamente si su escala está documentada
y mapeada por el adaptador; si no, null. El candidato no documenta confianza:
null/NOT_REPORTED. No añadir probabilidad inventada ni threshold de confianza.
No campo speaker: diarización desactivada y no requerida para una sola voz;
si llega speaker_id se preserva en respuesta, no se nombra Raúl por inferencia.

`text`/segmentos/palabras pueden diferir por puntuación o normalización interna
del proveedor. Comparar concatenación de palabras+punctuation y segmentos con
whitespace colapsado únicamente para diagnosticar consistencia; no modificar
sus strings. Divergencia léxica => NEEDS_REVIEW/TEXT_ALIGNMENT_MISMATCH. No
expandir números, corregir términos mediante LLM ni añadir palabras de referencia.
Cambios de terminología traceables pertenecen a otra revisión aprobada, no a r1.

Timestamps obligatorios para READY: todos los segmentos y todas las palabras
conocidos, fin > inicio, al menos un segmento/una palabra con texto no vacío.
Si un provider futuro solo ofrece segmentos, puede representarse con words=null
y motivo, pero **no satisface F003 READY** ni esta aceptación. No fallback oculto.

## Tiempo: provider → audio preparado → fuente

`t_source = audio_zero_source_s + t_provider`.
Para este adaptador, `t_provider = begin_time/1000` o `end_time/1000` exacto.
`audio_zero_source_s = first_decoded_sample_pts × audio_time_base − origin_media_s`
con inputs del contrato F002 y preparación validada. No usar fecha de job,
content_duration, timecode, FPS ni comenzar cada stream de cámara en cero.
F001 permite `audio_zero_source_s = 0/1`; el código no contiene ese supuesto.

Resolución documentada 1 ms es granularidad, **no precisión acústica**. Ningún
redondeo en el núcleo: Fraction, enteros vendor conservados en respuesta.
Solo reportes a 3 decimales, half-even, etiquetados como aproximados; nunca usar
los decimales de UI para hacer el mapping. Intervalos `[start_s,end_s)`.

Inicio y fin de segmentos y palabras deben ser no decrecientes en orden entregado;
no ordenar una respuesta inválida para hacerla pasar. Palabras pueden tocarse o
solaparse si ambos extremos son monótonos; conservar y reportar solapamientos.
Agrupación `segment_id` no exige contención: una palabra que cruza el borde de
su frase conserva el intervalo global y vínculo, sin duplicación/corte/clamp.
El consumidor no usa el segmento como límite de esa palabra. Timing no monótono,
duración cero/negativa o timestamps faltantes impiden READY.

Cada intervalo debe estar dentro del audio preparado y del extent fuente audio
F002; sin tolerancia para ocultar intervalos fuera de rango. Si una palabra de
audio adelantado/retrasado queda fuera de vídeo `[0,video_end_s)`, conservar el
mapping exacto pero NEEDS_REVIEW/OUTSIDE_VIDEO; no recortar ni desplazar el audio.
Duración reportada del archivo vendor puede redondearse: comparar con duración
por muestras con tolerancia **1 ms + 1 muestra**, solo para ese campo, no timings.
Silencio final es válido; último word_end no tiene que igualar duración del archivo.

No corregir drift por fitting, time stretch ni un offset aprendido desde la
transcripción. La prueba humana fija tolerancias en validation.md. Si no las
cumple, proveedor no demostrado: FAIL/PLAN_REVISION_REQUIRED para cualquier
alineador o cambio de proveedor, sin rebajar el criterio ni declarar aptitud F004.

## Respuesta retenida, ejecución y revisiones

```text
transcription/
    preparations/<preparation-id>/audio.wav, preparation.json
    requests/<request-fingerprint>/attempts/<execution-id>/
        request.json, execution.json, provider-response.json, redaction.json
        cost.json, report.md
        revisions/<normalization-version-id>/transcript.json
    current.json
```

Todos locales/ignorados. Paths relativos sin traversal/symlink escape. Preparación
y respuesta completadas son inmutables; revisión nueva no sobrescribe una previa.
Puntero F003 propio, no `current.json` F002. Hashes sin ciclos/self-hash. Locks
exclusivos F003 por project ID, staging mismo filesystem, publicación atómica,
interrupciones conservadas; no auto-borrado por edad ni restauración de READY stale.

`provider-response.json`: envelope propio versionado `kind: retained-stt-response`,
binding/request/execution ID + payloads submit, terminal y result del vendor.
Conservar todos los datos de reconocimiento, tiempos, usage y campos vendor
desconocidos; no adaptar su semántica aquí. Secretos/URLs firmadas no pueden
persistirse. Antes de escribir, redactar únicamente datos de transporte/auth y
ecos de URLs/secretos en mensajes. `redaction.json` conserva paths y razones,
SHA-256 del cuerpo recibido calculado en memoria y SHA del cuerpo retenido;
sin valores retirados. Bytes sin secretos pueden retenerse sin modificación;
payload con redacciones es **RAW vendor saneado**, no respuesta wire byte-exacta.
Esta excepción explícita cumple seguridad; transcript/timings/usage no se redactan.
Si no se puede preservar contenido útil sin secretos, BLOCKED/UNSAFE_RESPONSE.
No registrar headers completos ni cuerpos malformados potencialmente secretos.

`request.json` guarda binding, fingerprint, opciones efectivas, vocab/contexto,
audio hash/preparation hash y versión de adaptador; URL se sustituye por audio ID.
Fingerprint = SHA de JSON canónico de esos inputs + provider/model/region/scope/
workspace identity/endpoint y configuración de reconocimiento, **sin secretos,
URLs, precios, timestamps de ejecución ni versión del normalizador**.
Cada intento usa UUID `execution_id`; la respuesta se liga a él, task_id y request_id.

`execution.json` v1 `kind: stt-execution`: binding, execution_id/fingerprint,
provider/model/requested model/reported model nullable, region/scope/workspace,
adapter version, request/preparation hashes, started/finished UTC, completed,
phase/status/reasons, job/request IDs, audio duration, result/response hashes,
límites efectivos y pruebas de estabilidad antes/después. Model revision/backend
no informado = UNKNOWN; no afirmar snapshot de pesos por el nombre del modelo.
Journal fsync registra SUBMIT_INTENT **antes** de POST; el registro de evolución
de intento es administrativo, y el envelope final/evidencia se congela al completar.

Puntero `transcription/current.json` v1 `kind: current-source-transcript`: binding,
request fingerprint, execution/preparation/response/transcript paths+hashes,
normalization_version, status/reasons, unknowns/extensions. Guard F003 revalida
guard F002 vigente, bindings y todos los hashes/completitud antes de cada consumo;
revisión inspección/canal/reloj divergente invalida el resultado aunque RAW no cambie.
El coste es observabilidad externa, no pricing en el transcript ni semántica de READY.

## Idempotencia y coste de repetir

| Caso | Comportamiento obligatorio |
| --- | --- |
| Misma fuente/revisión/preparación/provider/model/config y respuesta válida | NO_OP: guard fresco y mismos hashes/mtime; cero upload/POST/polling innecesario. |
| Respuesta válida, transcript ausente o nueva versión del normalizador | Regeneración local explícita, sin red ni coste STT; versión igual da bytes idénticos. Nueva versión crea revisión distinta, preserva anterior. |
| Task conocido PENDING/RUNNING, timeout al consultar/descargar | Resume solo GET del mismo task; plazo limitado, no nueva solicitud. |
| POST con conexión rota/timeout/5xx o crash tras SUBMIT_INTENT sin task ID | SUBMISSION_UNKNOWN, no READY/no resubmit automático. Reconciliar operador con provider; no prometer exactly-once remoto sin idempotency key documentada. |
| FAILED/CANCELED/UNKNOWN o subtask fallido/parcial | No READY, conservar códigos/uso disponible. Otro POST requiere nueva autorización puntual de intento/coste. |
| Malformed/truncated/incompatible response, resultados/canales inesperados | BLOCKED/INVALID, sin fallback a transcript previo, sin retranscripción automática; replay local si la respuesta saneada completa existe. |
| Cambia fuente/inspección/canal/preparación/config/hotwords/context/provider/model | Fingerprint nuevo, invalidar current para ese input; nuevo gasto requiere autorización específica, no reusar otro resultado como si fuera equivalente. |
| Cambian solo precio, credencial o URL renovada del mismo audio/workspace | No cambia reconocimiento/fingerprint; no autoriza ni causa otro POST. Nuevo precio fuera del aprobado detiene envío. |

F003 r1 propone autorizar **una sola solicitud STT**, un archivo/canal, fixture
de 232,8 s. Intento consumido desde SUBMIT_INTENT, incluso si resultado económico
es incierto. No suite con red, optimización A/B, batch ni retry automático POST.
Cada llamada exige operación `submit` y flag explícito; prepare/verify/normalize
son locales; resume consulta únicamente el task existente. No copiar flag a tests.

## Vocabulario/configuración y confianza

Input F003 aparte de manifest F002: `config.json` local versionado con provider,
model, region, scope, workspace, language declarado/hints, canal, vocabulary,
context y límites. No secretos ni URL. Campos genéricos → mapping del adaptador
documentado, reject de opción no soportada, no ignorarla silenciosamente.

Propuesta inicial: declared es USER-REPORTED; hints `[es,en]` para el español y
las frases inglesas. Vocabulario opcional genérico de proyecto, traducido por
adaptador a `parameters.vocabulary`. Primera solicitud: monolito, microservicios,
eventos, idempotencia, peso 1; máximo propio 32 entradas/64 caracteres por término,
pesos 1..5, sin superhotwords. No vocabulario Again/try again, frases de error/
corrección ni referencia exacta para inducir el resultado esperado.

Contexto opcional genérico `{text}`: máximo 400 caracteres, una descripción de
dominio no editorial; adapter → un `input.context` user/input_text. Default
null/NOT_REQUESTED en fixture. Nada de historia LLM, prompts de corrección o
hotword service/precompiled lists. Cambio de hints altera fingerprint/gasto.
No añadir enable_words, enable_itn ni parámetros de otro modelo por similitud.

## Coste, credenciales y clasificación de evidencia

Provider execution cost en `cost.json` v1 `kind: stt-execution-cost`: execution_id,
provider/model/region/job/request IDs, original/prepared duration_s, vendor
usage literal saneado, input/output tokens null si no informados, metered speech
duration separada, pricing snapshot (URL/fecha/moneda/rates), calculated list
cost USD, effective USD/min y USD/hour extrapolation, billing amount/currency,
reconciliation status/reference, storage/transfer cost aparte, unknowns.

Tarifas verificadas en PLAN 2026-10-04: 0.15 USD/1M input, 0.47 USD/1M output.
Para tokens realmente informados: `C=(Tin*0.15+Tout*0.47)/1000000`, Decimal exacto;
`USD/min=C/(prepared_duration_s/60)`; extrapolación hora = USD/min*60. Esta última
es proyección del fixture, no tarifa garantizada de una hora futura. No sumar
usage acumulativo de cada poll; identificar unidades/finalidad sin inferirlas.
Si solo hay duration, **los tres costes son UNKNOWN**, no estimación por segundos
de Qwen 3.0 ni tokenización local. Reconciliar con facturación Alibaba identificada;
si solo agregado disponible, no adjudicarlo exactamente al job. Precio de lista
calculado no es débito real después de créditos/free quota/descuentos/impuestos.

Secretos solo entorno/local secret store externo al proyecto: `DASHSCOPE_API_KEY`
y `F003_AUDIO_URL`. No flags argv con credenciales, archivos .env en proyecto,
env dump, URLs en stdout, logs curl, auth en fallos ni Git. Workspace ID es
configuración, no API key. Key de Model Studio Singapore apta para API metered;
**no asumir elegibilidad Alibaba Coding Plan**, ni usar GITHUB_TOKEN_ALL.

Evidencia: hashes/muestras/tool results MEASURED; mapping/coste de lista DERIVED;
voz/limites por escucha OBSERVED; idioma/contexto aportado USER-REPORTED;
propiedad no informada UNKNOWN. Provider text/timestamps son PROVIDER-REPORTED,
no ground truth; observación humana posterior se registra por separado.

## Criterios de aceptación

| ID | Condición observable | Validación |
| --- | --- | --- |
| AC-01 | Proyecto real READY consumido por guard F002, audio/canal/preparación validada; originales/predecesores intactos, sin bypass de path. | V-01/02/03/15 |
| AC-02 | Respuesta completa útil saneada/inmutable y provenance recuperable; replay local mismo normalizador byte-idéntico y nueva revisión sin STT. | V-04/05/12 |
| AC-03 | Contrato independiente v1, binding exacto, UNKNOWN honesto y consumer independiente sin vendor/parser/STT/semántica. | V-05/06/14/15 |
| AC-04 | Mapping racional exacto source-presentation-v1, precisión/unidades honestas, monotonicidad/extents y offsets/crossing/drift según contrato. | V-02/06/07/09/10 |
| AC-05 | Español suficientemente fiel, cuatro términos F001 evaluados y referencias críticas correctas sin corrección de lo dicho. | V-08/09/10/16 |
| AC-06 | Again aislado y ambos try again válidos con palabras y timing usable; ninguna clasificación de contenido en F003. | V-09/10/14/16 |
| AC-07 | Fallos/parciales/timeout/malformed/crash/tamper nunca falso READY; identidad/idempotencia y pago limitado demostrados. | V-06/11/12 |
| AC-08 | Secrets ausentes en persistencia/Git/salidas; transporte firmado autorizado, región/retención/límites y elegibilidad documentados. | V-03/11/13 |
| AC-09 | Uso real y precios/identificadores retenidos; total/min/hora calculados solo con datos suficientes, UNKNOWN y conciliación explícitos si faltan. | V-13/16 |
| AC-10 | Todas las pruebas requeridas y revisión/aceptación humana de evidencia exacta, limitaciones y costes antes de DONE; sin F004/PRODUCTION_APPROVED. | V-14/15/16 |

## Preguntas, decisiones propuestas y diferidas

Preguntas bloqueantes del **PLAN**: ninguna. D002, transporte manual privado,
una llamada limitada y tolerancias son propuestas concretas incluidas en r1,
no aprobaciones ya recibidas. Disponibilidad de cuenta/bucket/key, canal y precios
vigentes se comprueban en IMPLEMENT antes del envío; falta => BLOCKED, sin gastar.
No afirmar que existen hoy. Un transporte diferente requiere revisión del PLAN.

Selección inicial Qwen condicionada a prueba real: capacidades documentadas no
equivalen a precisión demostrada. Token accounting y límites de contexto frente
a la API larga son ambiguos (plan.md); se registran, se detecta incompletitud y
se aplica conciliación, nunca se ocultan. Sin valor numérico garantizado de coste
previo; se limita número/duración/canal/tarifa de solicitudes, no se inventa cap USD.
Speaker, correcciones de términos, otras voces/formatos/pistas, chunking,
forced alignment, provider fallback, transporte automático y políticas de corte/
caption son decisiones posteriores. F001/F002 y D001 no se reabren.
