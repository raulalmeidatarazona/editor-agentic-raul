# F003 — operación y revisión local

F003 r1 aprobado: `74aaa0b64254dfbf0c801e3e7a46a11fb402d357`. F001/F002 son
antecedentes inmutables. El estado real, aprobación y evidencia están en
[`plan.md`](../specs/features/F003-time-aligned-transcription/plan.md) y
[`validation.md`](../specs/features/F003-time-aligned-transcription/validation.md).
Esta entrega no autoriza F004 ni aprueba ningún vídeo para producción.

## Fronteras y configuración

`audio_preparation.py` recibe únicamente un Content Project READY y compara el
recorrido independiente de muestras con el scan F002. Prepara WAV PCM16 mono
nativo, sin mezcla, resampling, tratamiento, corte o padding. `transcript_contract.py`
define exclusivamente texto/intervalos/binding/UNKNOWN propios. Un consumidor
llama a `verify_transcript(project_root)` antes de usar el documento y obtiene
un contrato sin Alibaba, endpoints, claves, precio o decisiones editoriales.

`qwen_asr_adapter.py` encapsula el esquema vendor, endpoint, workspace, lectura
de key, HTTPS, mensajes de contexto, hotwords, respuesta y accounting. Resuelve
`F003_QWEN_WORKSPACE` cuando el campo local workspace está null. Lee
`DASHSCOPE_API_KEY` exclusivamente dentro de su cliente HTTP. La key nunca forma
parte de config/fingerprint/proyecto/argv/log; workspace sí queda como identidad
no secreta de ejecución para impedir reutilizar una respuesta de otra cuenta.
La URL firmada se lee de `F003_AUDIO_URL`, pasa al HTTP en memoria y se sustituye
por el SHA del audio en la solicitud retenida.

La orquestación usa la interfaz del módulo adaptador: configuración resuelta,
endpoint/body, HTTP, validación de job, payload genérico y coste. Una futura
implementación compatible sustituye ese módulo y su selección explícita;
no requiere cambiar `source-transcript v1` ni consumidores. Actualmente existe
una sola implementación de servicio. Otro proveedor requiere su PLAN/aprobación;
el doble de prueba no implementa ni llama a otro servicio.

Config F003 aparte de F002, versión1: provider/model/region/scope, workspace
(null permitido **solo para preparación offline**), language `{declared,requested}`,
channel_index, vocabulary, context y limits. Se rechazan opciones no soportadas.
Primera solicitud: `es/en`, cuatro términos técnicos peso1, context null,
diarización off y solo canal0 del WAV mono. El canal de cámara elegido es 1.
La referencia acústica no se inyecta como contexto/hotwords.

Los secretos se cargan mediante el almacén local/entorno del proceso; no se pegan
en chat ni se guardan con esta documentación. No se imprime el entorno, no se
copia ninguna key al código y no se instala SDK, modelo o dependencia.

## Comandos

Desde la raíz del repositorio, con config local fuera de Git:

```sh
python3 tools/transcribe.py prepare --project .local/projects/f002-studio-001 \
  --config .local/validation/F003/work-e1/config.json \
  --evidence .local/validation/F003/work-e1/listening
python3 tools/transcribe.py verify --project .local/projects/f002-studio-001
```

`prepare` es local y devuelve NEEDS_REVIEW/exit2 mientras pide escucha de canal;
eso no es un fallo de extracción. `verify` no crea una transcripción ni hace red;
sin transcript actual completo no devuelve READY. Solo después de todos los
gates reales y actas registradas se usa:

```sh
python3 tools/transcribe.py submit --project .local/projects/f002-studio-001 \
  --config .local/validation/F003/work-e1/config.json \
  --review .local/validation/F003/work-e1/review.json \
  --approval-reference 74aaa0b --allow-provider-call
python3 tools/transcribe.py resume --project .local/projects/f002-studio-001 \
  --execution-id <uuid-del-journal>
python3 tools/transcribe.py normalize --project .local/projects/f002-studio-001 \
  --execution-id <uuid-del-journal>
python3 tools/transcribe.py evaluate --project .local/projects/f002-studio-001 \
  --reference .local/validation/F003/work-e1/reference.json \
  --output .local/validation/F003/work-e1/quantitative-review.json
```

El output público es JSON pequeño sin URL/key/cuerpo de error. Exit0 solamente
READY o NO_OP verificado;2 NEEDS_REVIEW;3 BLOCKED;4 INVALID. La evaluación numérica
puede fallar o quedar HUMAN_REVIEW_REQUIRED; nunca firma aceptación humana.

## Escucha y referencia antes del STT

El paquete local contiene WAV completo por canal, las cinco ventanas fijas,
buffers de eventos y una pausa candidata, cada clip con sample offsets/SHA,
CSV de extremos PCM cada20ms y SVG medido. SVG/energía no identifica palabras.
La selección de canal y escucha completa1× deben provenir de Raúl. Las muestras
de audio/hashes/layout no identifican por sí solos el micrófono físico.

El archivo local `reference.json` empieza con **UNKNOWN**, no con una referencia
inventada. Antes de obtener el candidato, un observador competente en español
escucha y aporta texto literal para las ventanas fuente `[0,25)`, `[60,85)`,
`[90,115)`, `[130,155)`, `[195,228)`: al menos200 palabras. Si no se alcanza,
extender desde228s hacia atrás sin cambiar las ventanas originales. La plantilla
y los clips están preparados: solo se piden datos de escucha, no metadatos.

Controles: primeras10 palabras léxicas de apertura/corrección/cierre, cinco
palabras críticas (Again/try/again/try/again) y una ocurrencia de cada término.
Se deduplican por posición `(window_index,lexical_index)` y hay mínimo30.
Cada onset/offset requiere un intervalo de posible borde con incertidumbre≤50ms,
escucha repetible1× y waveform. Un tiempo aproximado del handoff no satisface esto.
Raúl confirma ambigüedades; el agente registra sus respuestas/índices y campos
medidos. No hace falta editar JSON ni volver a grabar. Si no se establecen bordes,
V-09/V-10 quedan BLOCKED, sin reducir tolerancias.

El evaluator solo compara: NFC/casefold/puntuación para WER S/D/I/N, alignment
determinista para ubicar controles, errores conservadores, p95 nearest-rank,
max/drift y núcleos de tres pausas. No reescribe transcript ni clasifica retomas.
La selección de palabras de ventana usa el punto medio del intervalo conocido;
la referencia conserva sus ventanas originales. Una palabra de borde ambigua
se explica en la revisión; no se elimina para mejorar WER.

## Transporte y cuenta antes del único POST

Raúl confirma workspace/key Singapore **API metered**, modelo habilitado y key
distinta de Coding Plan; poseer una key no prueba esa elegibilidad. Confirma el
objeto privado OSS Singapore existente y la gestión de upload/cleanup. El agente
registra el acta real en `review.json`, ligada a binding/preparación/referencia.
Sin esos facts, la llamada se detiene antes de consumir el intento.

Raúl sube **solo el WAV del canal seleccionado**, nunca RAW, clips, sidecar ni
evidencia, al objeto existente. Configura su URL GET firmada en el entorno local.
TTL solicitado2h; entre30min y2h restantes al enviar. El adapter admite únicamente
HTTPS de buckets `*.oss-ap-southeast-1.aliyuncs.com`, sin redirects ni Bearer en
OSS. Comprueba en streaming bytes/SHA exactos del WAV antes del POST. No crea
cuenta/bucket/uploader, ACL pública, CDN ni transporte Beijing.

Antes de enviar se revalida precio oficial vigente para modelo/región exactos,
no superior a USD0.15/1M input y0.47/1M output, y se registra fecha/URL. El coste
previo total no tiene techo USD garantizado. Scope International no garantiza
inferencia solo en Singapore; retención exacta del proveedor sigue UNKNOWN.
Tras recuperar el resultado Raúl borra el objeto, como máximo24h, y se conserva
su confirmación. TTL/cleanup OSS no demuestran borrado de copias Model Studio.

## Recuperación, inmutabilidad y coste

Lock exclusivo sin borrado automático por edad. Si `.lock` queda tras un crash,
el operador comprueba que no vive el proceso y registra resolución antes de
retirarlo; no hay comando `force`. RAW/preparaciones/respuestas/revisiones se
preservan. Solo journal y puntero F003 cambian administrativamente.

`SUBMIT_INTENT` se fsync antes del POST. El intento r1 se consume desde ese punto,
incluido crash/timeout/5xx/resultado desconocido. No retries POST. Un UUID con job
conocido se recupera mediante GET del mismo job; con envelope local completo,
se finaliza/replay local sin volver a descargar. Un intento sin job conocido
requiere conciliación por operador, nunca un reenvío automático. Un segundo
gasto o cambio de reconocimiento exige otra autorización puntual.

Preparación válida/repetida no toca archivos; submit READY con igual fingerprint
es NO_OP sin red. Normalize explícito conserva bytes para versión igual; versión
nueva crea otra revisión y no modifica las anteriores. Cambios de precio/key/URL
no alteran el fingerprint; los de reconocimiento/cuenta/binding sí.

Se conserva respuesta vendor **saneada** con recognition/timing/usage y campos
desconocidos, manifest de redacciones y SHA wire/retained. Texto de reconocimiento
que contenga secretos bloquea la respuesta: no se presenta texto alterado como
transcripción. Errores malformados no se guardan indiscriminadamente.

`cost.json` registra usage final, IDs y duración preparada. Tokens informados
permiten fórmula Decimal de lista; duration-only deja total/min/hora UNKNOWN,
sin convertir segundos a tokens. No sumar usage acumulativo de polling.
Facturación real/créditos/impuestos/storage/transferencia se concilian aparte:
una cuenta agregada no prueba coste exacto del job. El journal pendiente puede
actualizar cost al recuperar usage final; la respuesta y transcript no cambian.
La conciliación debe tener consulta/fuente/fecha y aceptación humana de límites;
una intención de consultar después no completa V-13.

## Validación y gate

`python3 -m unittest discover -s tests -v`: tests locales con HTTP inyectado y red
bloqueada; AV sintético de1–3s/≤2MiB, oracles Fraction/Decimal/JSON independientes,
consumer de wire, replay, fallos/locks/intent/caps/secret-canaries. Ningún test
es un resultado real de Alibaba ni una revisión acústica humana.

La suite y preparación son solo parte de V-01–V-15. El envío/resultado real,
≥200 palabras, timing real, terminología/negaciones, billing/cleanup y aceptación
exacta siguen obligatorios. No DONE por una suite verde ni por elegir el canal.
