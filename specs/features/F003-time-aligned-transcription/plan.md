# F003 — Provider-Independent Time-Aligned Transcription

**Documento:** plan — CÓMO entregar texto y tiempo de fuente\
**Bundle revision:** r1\
**Lifecycle state:** VERIFYING\
**Owner:** Raúl Almeida\
**Scope:** [requirements.md](requirements.md)\
**Proof contract:** [validation.md](validation.md)\
**Propuesta arquitectónica:** [D002](../../decisions/D002-initial-f003-stt-provider.md)

## Autorización real y antecedentes

Mensaje humano adjunto `45cab433-bc96-45c7-a63b-d033726c64fa/Pasted text.txt`:
F002 formalmente DONE; autoriza **PLAN ONLY F003**, prohíbe implementar, STT,
instalar, modificar F001/F002 o iniciar F004. Fecha de registro 2026-10-04.
Esta fue la autorización de PLAN; las exclusiones históricas de F003 en raíces
siguen válidas para IMPLEMENT, superadas solo para PLAN por ese mensaje.

Se leyeron los cuatro specs raíz completos, AGENTS/protocolo, templates/decisiones,
F001 requisitos/notas/aceptación relevantes y F002 r1 archivado/D001/contrato
implementado/validación y cierre. F001 DONE/e5/cierre 7e0bc22; F002 DONE,
r1 ae36327768a4186009a92619ef8e4b1bf379d8a8, implementación
3e53205bcfd55570968f891a5bd972d5fe6bc621, cierre 557afcf. No skill de vídeo
aplicable: esta feature no crea/edita/renderiza vídeo ni composición.

## Investigación oficial del candidato — snapshot documental 2026-10-04

Consulta de documentación pública, sin login/API/probe/extracción nuevos ni upload.
Referencias precisas (todas Alibaba oficial):

- **S1** [HTTP API del modelo Filetrans](https://www.alibabacloud.com/help/en/model-studio/fun-asr-recorded-speech-recognition-http-api), actualización 2026-09-28.
- **S2** [Guía offline, timestamps y regiones](https://www.alibabacloud.com/help/en/model-studio/non-realtime-speech-recognition-user-guide).
- **S3** [Formatos/inputs STT](https://www.alibabacloud.com/help/en/model-studio/asr-model/).
- **S4** [Model card exacta 3.1 Filetrans](https://www.alibabacloud.com/help/en/model-studio/qwen-audio-3-1-asr-flash-filetrans), actualización 2026-09-22.
- **S5** [Pricing — sección Qwen-Audio-3.x-ASR-Flash-Filetrans](https://www.alibabacloud.com/help/en/model-studio/model-pricing).
- **S6** [Regiones/endpoints/alcance de inferencia](https://www.alibabacloud.com/help/en/model-studio/regions).
- **S7** [Upload temporal](https://www.alibabacloud.com/help/en/model-studio/get-temporary-file-url), actualización 2026-09-28.
- **S8** [Privacidad Model Studio](https://www.alibabacloud.com/help/en/model-studio/privacy-notice).
- **S9** [Estados/consulta/cancelación async](https://www.alibabacloud.com/help/en/model-studio/manage-asynchronous-tasks).
- **S10** [Errores HTTP](https://www.alibabacloud.com/help/en/model-studio/error-code).
- **S11** [URLs privadas OSS firmadas](https://www.alibabacloud.com/help/en/oss/user-guide/how-to-obtain-the-url-of-a-single-object-or-the-urls-of-multiple-objects).

| Aspecto exigido | Hallazgo documentado y disposición r1 | Fuente |
| --- | --- | --- |
| Modelo/región | ID exacto `qwen-audio-3.1-asr-flash-filetrans`, Singapore/International disponible. No confundir con `qwen3-asr-flash-filetrans` o el modelo sin `-filetrans`. | S2/S4 |
| Español | `es` admitido; language_hints hasta 4 códigos; omitido = detección automática. Respuesta no promete campo detected language. | S1 |
| Formatos | aac/amr/avi/flac/flv/m4a/mkv/mov/mp3/mp4/mpeg/ogg/opus/wav/webm/wma/wmv, cualquier sample rate; r1 transporta WAV únicamente. | S3 |
| Límites archivo | ≤2 GB, ≤12 h; diarización recomienda ≤2 h. RAW F001 2,873 GB no se envía; WAV mono calculado ~22,35 MB. | S2/S3 |
| Modalidad | Async submit → task ID → polling → descargar JSON final; no SSE/stream de texto de este modelo. | S1/S2 |
| Segmentos/palabras | `transcripts[].sentences[]`, `words[]`; begin/end enteros ms de audio, habilitados permanentemente. Puntuación posterior separada cuando informada. No precisión acústica garantizada. | S1/S2 |
| Payload | Properties de archivo, transcript por canal/texto/frases/palabras; channel_id 0-based. r1 espera exactamente un transcript/canal 0 del WAV mono, no merger opaco. | S1 |
| Contexto/hotwords | HTTP admite input.context y vocabulary inline; pesos 1..5 (también 50, excluido r1), límites propios menores. Precompiled vocabulary no necesario. | S1/S4 |
| Diarización | Disponible en mono, off por defecto; r1 off/speaker_count omitido. No identifica personas. | S1 |
| Confianza | Campos/escala no documentados para este resultado: UNKNOWN, no estimar. | S1 |
| IDs/errores | request_id en submit/query, task_id; comprobar task y subtask, no solo SUCCEEDED global. 401/403/config/download/429/5xx y terminales son fallos observables. Sin idempotency key POST documentada. | S1/S9/S10 |
| Usage/precio | S5/S4: input/output tokens, USD 0.15/0.47 por millón. S1 ejemplo conserva solo usage.duration y descripción genérica de duración de voz; **no prueba tokens 3.1 ni una conversión duración→tokens**. Reconciliación definida, sin importar usage de modelos streaming. | S1/S4/S5 |
| Context limits | Model card publica 8192 input/1024 output/context8192 tokens mientras guía soporta hasta12h. Aplicación de esos límites al servicio de archivos larga no aclarada; no afirmar cap total ni coste máximo desde esos números. Detectar truncamiento/cobertura real, no chunking automático. | S2/S4 |
| Endpoint | POST `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`; GET `/api/v1/tasks/{task_id}`. parameters obligatorio incluso `{}`; Bearer key Singapore + X-DashScope-Async enable en submit. | S1/S6 |
| Transporte | Una file_urls HTTPS URL por petición. API no acepta path local; URL firmada accesible al servicio no obliga a ACL pública. Transporte privado manual OSS existente, comprobación bytes/SHA, sin uploader/bucket provisioning. | S1/S3/S11 |
| Upload temporal | S7 limita explícitamente función a Beijing, aunque ejemplos citan dashscope-intl y S1 habla oss://. Contradicción del vendor: **no usar temporal oss:// en Singapore** ni cambiar región para desbloquear. | S1/S7 |
| Región/privacidad | S6 separa región de almacenamiento/access point de scope de inferencia. International no prueba cómputo solo Singapore; nodos concretos UNKNOWN. S8 declara no usar datos para entrenamiento y almacenar datos de llamadas. No plazo exacto de retención STT ni garantía de borrado total documentados. | S6/S8 |
| Caducidad | Link de resultado/consulta válido24h según S1; conservar resultado local al completar. Esta caducidad **no demuestra borrado de datos del proveedor en24h**. TTL OSS propio tampoco borra copias Model Studio. | S1/S8/S11 |

Conclusión: **candidato adecuado documentalmente para intentar F003**, con palabra
y español soportados. Adecuación real todavía NOT YET VALIDATED: precisión,
cobertura de232,8s, términos/Again, usage/coste, transporte y cuenta. D002 propone
el proveedor **inicial condicionado a esa validación**, no proveedor permanente.
Si la respuesta carece de palabras útiles o cumple el JSON pero falla precisión,
no cumple F003: mantener evidencia, volver a PLAN antes de otro provider/alineador.
La ambigüedad de usage está cubierta por la alternativa UNKNOWN+conciliación
solicitada por Raúl; no es permiso para inventar gasto ni asumir cuota gratis.

## Enfoque mínimo y límite de proveedor

Python3.14.7 stdlib existente + FFmpeg/ffprobe9.0.1 existentes. Extensión limitada
de D001, no selección de lenguaje de toda la pipeline. `urllib.request`/ssl para
HTTPS, Fraction para tiempos, Decimal para coste, hashlib/json/pathlib/subprocess/
unittest. No SDK requests/DashScope/OpenAI, pip/npm ni nuevas herramientas.

```text
READY F002 guard → audio canal explícito + ledger temporal/hash
  → configuración genérica + fingerprint + control de intento
  → URL privada autorizada + POST único Alibaba
  → GET task/resultado → respuesta vendor saneada inmutable
  → adaptador mapea payload → normalizador v1 → transcript canónico + guard

Replay: respuesta conservada + preparación + binding + normalizer_version
  → revisión canónica local, sin API
Consumer: guard actual → identidad/lenguaje/texto/segments/words/reloj propios
```

Provider/model/pricing/task/usage permanecen en execution/cost/response. Canonical
solo referencia execution ID/hashes y valores genéricos. Un doble de otro
proveedor con formato/tiempo diferente prueba la frontera sin implementar otro
servicio. Sin imports Qwen/ffprobe/normalizador en assertions del consumer.

El normalizador no modifica términos ni significado. Tech-stack/roadmap piden
terminología correcta: r1 la valida como reconocida y conserva el error intencional;
no entrega un corrector de terminología ni difiere un fallo de precisión como si
estuviera resuelto. Corrección humana/LLM o política de overrides necesitaría PLAN.

## Operación propuesta después de aprobar

```text
python3 tools/transcribe.py prepare --project <root> --config <config-local>
python3 tools/transcribe.py verify --project <root>
python3 tools/transcribe.py submit --project <root> --config <config-local>
    --allow-provider-call --approval-reference <identidad-aprobada>
python3 tools/transcribe.py resume --project <root> --execution-id <id>
python3 tools/transcribe.py normalize --project <root> --execution-id <id>
```

prepare no red; produce preview/manifest y diagnóstico de canal, no decisión
automática de voz. `config` necesita canal confirmado antes de submit. `submit`
sin flag/reference válida no upload ni POST. Una referencia textual por sí sola
no fabrica permiso: registrar autorización humana exacta en plan y ledger.
verify/normalize no red; resume solo consultas del job conocido. No comando
`force` para saltar el límite ni fallback retranscribe. stdout resultado pequeño
JSON (operation/outcome/project_id/status/reasons/execution_id/transcript_id/path),
sin secretos/URLs. Exit0 solo READY/NO_OP verificado;2 NEEDS_REVIEW;3 BLOCKED;
4 INVALID. CLI ayuda no prueba funcionalidad.

## Pago, recursos, transporte y recuperación

El approval r1 propuesto cubre únicamente un POST para f002-studio-001/audio232,8s,
un canal, tarifas máximas de lista0.15/0.47 por millón, sin retries POST. El coste
total previo es UNKNOWN por falta de token accounting predecible; no hay techo
monetario garantizado. Si Raúl exige techo USD duro, parar y revisar PLAN con un
mecanismo de presupuesto verificable; no simularlo mediante timeout local.
Una call fallida/ambigua consume el único intento autorizado: otra necesita
autorización puntual. Ninguna fixture sintética llama al proveedor.

Preflight local antes de pago: guard, sample ledger/hash, canal escuchado, límites,
config/account Singapore/model permitido/API metered distinta de Coding Plan,
precio vigente no superior al aprobado, almacenamiento privado existente/URL
válida y consentimiento de alcance International/retención UNKNOWN. No abrir
cuenta ni nuevo gasto storage automáticamente. Raúl realiza upload/borrado del
objeto WAV y aporta URL mediante secret store/env fuera del proyecto; no chat.
Coste OSS/transferencia propio UNKNOWN hasta datos de su cuenta, separado de STT;
no se afirma gratis. Sin storage listo, implementar/pruebas locales pueden
continuar pero envío/real VERIFY BLOCKED, no DONE.

Límites propios iniciales: audio≤30min y WAV≤256MiB (fixture menor), un canal;
evidencia agregada≤256MiB por intento incluyendo WAV y previews locales;
cuerpo vendor≤16MiB cada uno, stderr≤2MiB, FFmpeg timeout600s. No48k/232s como
constantes universales. Audio temporal/calibration mono≤2 canales de input; más
canales o codecs no decodificables a PCM16 sin pérdida justificable => revisar,
sin conversiones ocultas. No test de 12h ni benchmark/soporte ilimitado prometido.

POST timeout60s, **0 retries**. Poll cada5s mientras PENDING/RUNNING hasta1800s;
GET red/429/5xx como máximo3 reintentos por operación con backoff1/2/4s, respetar
Retry-After dentro del deadline. Auth/config fallan inmediatamente. Descargar
JSON≤16MiB dentro de validez24h,3 retriesGET; si no se recupera, conservar task
e instrucción resume, nunca emitir otro POST por caducidad. Queries pueden tener
costes de red/storage observados aparte; no asumir que no cuestan nada.

HTTPS TLS verificado; endpoint exacto y OSS Singapore allowlist; ningún proxy
configurable de proveedor ni redirects automáticos, nunca Bearer en result/OSS
GET. Result URL de región inesperada/host no autorizado => BLOCKED para resolver
sin fuga, no aceptar ejemplo Beijing como dato de Singapore. Streaming/caps en
descarga/hash/audio. Secrets redacted antes de persistir, errores solo código/
mensaje saneado. Lock/journal/fsync/publish atómico. Source cambia durante operación
=> BLOCKED, retener resultado/uso pero no publicarlo como vigente. Stale lock y
SUBMISSION_UNKNOWN requieren operador, no cleanup ni exactly-once asumido.

Retención local sin purga automática de revisiones/evidencia. Borrado remoto del
objeto concreto por Raúl documentado en acta, no prometer borrado Model Studio.
La aceptación r1 incluye conocimiento de estos límites de privacidad/transporte;
si no acepta, revisar propuesta antes de IMPLEMENT/cualquier envío.

## Superficie de IMPLEMENT propuesta — no creada durante PLAN

| Archivo/artefacto | Acción futura / propósito |
| --- | --- |
| `tools/transcribe.py` | Crear CLI/orquestación local/journal/locks/revisiones/pago/guard y reporte; AC-01/02/07/10. |
| `tools/transcript_contract.py` | Crear serialización/normalización genérica/time/binding/guard F003; AC-03/04. |
| `tools/qwen_asr_adapter.py` | Crear HTTP/parser vendor/hints/sanitización/usage, frontera replaceable; AC-02/05–09. |
| `tools/audio_preparation.py` | Crear extracción canal/sample ledger/continuidad y evidence; AC-01/04. |
| `tests/test_transcription.py` | Crear flujo/idempotencia/pago/crash/secret-canaries offline; AC-02/07/08. |
| `tests/test_transcript_contract.py` | Crear oracle independiente/mapping/schema/consumer/replay, dobles de proveedores; AC-03/04/10. |
| `tests/test_audio_preparation.py` | Crear integraciones AV pequeñas offset/samplecount/singlechannel; AC-01/04. |
| `tests/test_qwen_asr_adapter.py` | Crear respuestas vendor sintéticas/fallos/usage/redacción sin red; AC-02/07–09. |
| `docs/F003-transcription.md` | Crear procedimiento local/paid/manualOSS/recovery/cost/revisión. |
| `.local/projects/<id>/transcription/` | Crear solo nuevo subtree F003, manifests/audio/request/response/revisions; ignorado. |
| `.local/validation/F003/<evidence-revision>/`, `.local/fixtures/F003-synthetic-*/` | Crear evidencia/ground truth/fixtures pequeñas ignoradas tras aprobación. |
| Este bundle/D002 | Append aprobación/evidencia real preservando r1 presentado; D002 Accepted solo decisión humana. |
| `tech-stack.md` §7/§11 | Registrar únicamente resolución limitada propuesta abajo tras aceptar D002/r1. |
| AGENTS/roadmap/protocolo/README | Registros administrativos de autorización/estado/enlaces, sin abrir F004. |
| F001/F002/specs/evidencia/D001/tools F002, root Constitution/Mission, skills/lock | Solo leer, no modificar. No instalar/refresh vendor. |

Resolución normativa propuesta para añadir a tech-stack §7 tras aprobación:

> F003 initially evaluates qwen-audio-3.1-asr-flash-filetrans in Alibaba Model
> Studio Singapore / International through a replaceable adapter. Selection is
> conditional on the approved F003 real-fixture validation. The source-transcript
> v1 contract and source-presentation-v1 mapping belong to F003, not to Alibaba.
> One approved fixture request, private owner-managed audio transport, retained
> sanitized provider responses, and usage/cost reconciliation are defined in the
> F003 bundle and D002. No permanent provider, correction model or F004 policy is
> selected.

Al añadirlo, sustituir la frase «provider remains unselected» por «initial provider
candidate is scoped by F003/D002; provider remains replaceable». En §11 extender
runtime limitado Python stdlib/FFmpeg a F003, no lenguaje universal. **No aplicar
estos cambios normativos durante PLAN.** No modificar Constitución ni misión.

## Pasos pendientes y validación

- [x] Registrar aprobación humana exacta r1/D002/commit+hashes y snapshot readonly antes de PLAN_APPROVED; aplicar solo resolución tech-stack autorizada.
- [x] Implementar contrato/guard/normalización/replay con provider doubles y oracle independiente; V-04–07/14/15.
- [x] Preparación/canal/sample ledger y flujo offline de requests/retries/journal/redacción/coste; V-02/03/11–13. No red en suite.
- [x] Revalidar runtime/input, ejecutar negativos/sintéticos y guardar salidas/hash. F001/F002 intactos, V-01/02/06/07/11/12/15.
- [ ] Preparar paquete de escucha del fixture y referencias antes del POST; detener para juicio de Raúl donde V-02/08–10 exige escuchar/confirmar. No pedir campos medibles manuales.
- [ ] Verificar cuenta/precio/storage privado/URL/eligibilidad/privacidad/pago, registrar autorización y límites; un solo submit/GET/download real V-03/04/13.
- [ ] Replay/no-op/consumer sin nuevas llamadas; comparar palabras/timing, uso/coste y cobertura según V-05–16. No relajar tolerancias por resultado del modelo.
- [ ] Presentar evidencia exacta, escuchar/revisar con Raúl y registrar aceptación antes de DONE. Si falta dato necesario, conservar BLOCKED/HUMAN_REVIEW_REQUIRED; sin F004.

## Readiness y gate

R1 define mínimos, offsets/precisión, source binding, transporte/pago, fallos,
UNKNOWN, provider boundary, aceptación real/humana y surface antes de código.
Sin preguntas bloqueantes de PLAN; propuestas arquitectónicas/coste/privacy
requieren la aprobación de r1/D002 que se solicita al presentar. Prerequisitos
de ejecución no establecidos se verifican en su gate, sin tratarlos como PASS.
No se hizo extracción, STT, upload, suite runtime ni modificación F001/F002.
Checks F003 NOT RUN; capacidad documentada ≠ adecuación validada.

Presentación recuperable en Git main; identidad exacta mediante commit/hashes
entregados externamente a estos documentos para evitar autorreferencia. No push
remoto requerido en esta petición. Mantener r1 presentado antes de añadir actas.

Auditoría documental de presentación: 10 AC/16 checks con mapping recíproco
completo y cobertura A–P, links locales/fences válidos. Baseline144 archivos:
140 intactos, cuatro raíces solo registros administrativos; F001/F002/código/
evidencia/lock sin cambios. RAW original y owned source conservan bytes/mtime/
inode (no SHA nuevo medido en PLAN). Resultado local en
`.local/planning/F003/r1/audit.json`, fuera de Git. Esto no es PASS de runtime.

## Aprobación del bundle presentado

**Approval:** NOT GRANTED\
**Approver / fecha / palabras reales:** pendientes; ningún permiso de IMPLEMENT recibido.\
**Approved revision:** pendiente; usar commit presentado con tres documentos y D002.\
**Recoverable reviewed bundle:** commit local main de presentación.\
**Authorized scope:** exclusivamente PLAN F003; F001/F002 DONE intactos.

Frase propuesta, **no firmada**; usar la identidad concreta entregada en la presentación:

> Apruebo F003, bundle r1 del commit identificado en la presentación, compuesto por requirements.md,
> plan.md y validation.md. Acepto D002 del mismo commit y la resolución limitada
> de tech-stack descrita en plan.md. Autorizo PLAN_READY → PLAN_APPROVED e IMPLEMENT
> únicamente de F003 conforme a su contrato y validación. Autorizo una sola
> solicitud STT de C0216.MP4 a través del proyecto READY F002, un canal y 232,8 s,
> con qwen-audio-3.1-asr-flash-filetrans Singapore/International, tarifas de lista
> máximas USD0.15/1M input y USD0.47/1M output, sin reenvíos automáticos. Entiendo
> que el coste previo no tiene un techo USD garantizado y debe medirse o quedar
> UNKNOWN con conciliación. Autorizo ese audio derivado mediante URL firmada de
> un objeto OSS Singapore privado preexistente que yo gestionaré, con los límites
> de privacidad/retención documentados; si falta transporte/cuenta aptos, detener
> el envío. No autorizo nuevas dependencias/servicios, cambios F001/F002, F004,
> semántica, retomas, edición, captions, HyperFrames ni render. Esta aprobación
> no declara DONE ni ningún vídeo PRODUCTION_APPROVED.

## Historial

| Fecha | Estado/cambio | Fuente |
| --- | --- | --- |
| 2026-10-04 | DRAFT r1 | Encargo humano PLAN ONLY F003, adjunto45cab433. |
| 2026-10-04 | DRAFT → PLAN_READY | Tres documentos/D002 propuesto presentados para revisión; IMPLEMENT no autorizado. |

## Acta real de aprobación r1

**Approval:** GRANTED. Raúl Almeida; mensaje humano directo en este chat.
Registro UTC: 2026-10-04T06:26:19.776516+00:00.
Identidad aprobada: `74aaa0b64254dfbf0c801e3e7a46a11fb402d357`. Snapshot readonly: `.local/spec-approvals/F003/r1/`.

| Documento presentado | SHA-256 pre-aprobación |
| --- | --- |
| requirements.md | `56fcb6a9e5b1057c5ae07366c4ee485d9f9456b505531e1d2576ab3de680f3e1` |
| plan.md | `105d3f5925619ef7e3ed30f000414b3aacd985ab47827042f8469d40f142910e` |
| validation.md | `0ac3c53c48ba6c50d8c74b667b3642e5309305a90a730c45afeb22a0bed8ee75` |
| D002-initial-f003-stt-provider.md | `e38f1f935fdfd9d6493f3f2f463e89dbae04cd1fdee9a4d49c9eb036167ae9d2` |

Palabras reales recibidas:

> Apruebo F003, bundle r1 del commit 74aaa0b, compuesto por requirements.md, plan.md y validation.md. Acepto D002 del mismo commit y la resolución limitada de tech-stack descrita en plan.md. Autorizo PLAN_READY → PLAN_APPROVED e IMPLEMENT únicamente de F003 conforme a su contrato y validación.
>
> Autorizo una sola solicitud STT de C0216.MP4 a través del proyecto READY F002, un canal y 232,8 s, con qwen-audio-3.1-asr-flash-filetrans Singapore/International, tarifas de lista máximas USD0.15/1M input y USD0.47/1M output, sin reenvíos automáticos. Entiendo que el coste previo no tiene un techo USD garantizado y debe medirse o quedar UNKNOWN con conciliación.
>
> Autorizo ese audio derivado mediante URL firmada de un objeto OSS Singapore privado preexistente que yo gestionaré, con los límites de privacidad/retención documentados; si falta transporte/cuenta aptos, detener el envío.
>
> No autorizo nuevas dependencias/servicios, cambios F001/F002, F004, semántica, retomas, edición, captions, HyperFrames ni render. Esta aprobación no declara DONE ni ningún vídeo PRODUCTION_APPROVED.
>

Transición: PLAN_READY → PLAN_APPROVED. Normativa r1 intacta; se autoriza solo
F003/D002/resolución limitada y el único intento descrito. Envío sujeto a gates
humanos/cuenta/transporte; no nueva autorización para otras llamadas.

## Inicio de IMPLEMENT

2026-10-04: PLAN_APPROVED → IMPLEMENTING dentro de r1. Aprobación/snapshot
registrados antes de desarrollo; solicitud STT no consumida. Solo F003.

## Implementación local y gate de verificación (2026-10-04)

IMPLEMENTING → VERIFYING: cuatro módulos, cuatro suites y procedimiento local
previstos entregados. Sin dependencias nuevas. Configuración/lectura de key y
workspace resueltos en el adaptador; esta preferencia posterior del propietario
no cambia el contrato canónico ni los criterios r1. La key no va en el código.

Raúl respondió «canal 1» y, ante la pregunta de comparación de ambos y escucha
completa del WAV canal1 a1× con voz inteligible/inicio/final/pausas, «Sí, confirmo
esa revisión completa». Acta USER-REPORTED en
`.local/validation/F003/work-e1/channel-review.json`. Key disponible es
USER-REPORTED; workspace/eligibilidad API metered Singapore y OSS privado
preexistente todavía UNKNOWN. No inferirlos desde la existencia de una key.

Preparación canal1: 11.174.400 muestras/48kHz/1164/5s, origen fuente0/1; WAV SHA
`4c71d1689fdec2fb419ec6b91cb6ca0317a0b172b594e3b6ab7532cbe00645f3`.
Dos canales guardados por separado, ledger contiguo comparado contra F002 y
comparación independiente de payload PCM de ambos con deinterleave stdlib.
Paquete de escucha5 ventanas/buffers/CSV/SVG medidos, sin segmentación editorial.

V-08–V-10: referencia literal independiente ≥200 palabras y bordes acústicos
≤50ms de incertidumbre pendientes, preparados con UNKNOWN; no adoptar handoff
e5 como oracle ni fabricar respuestas humanas. Preguntas concretas enviadas.
V-03/04/13 real también pendientes por cuenta/transporte/usage/billing.
**Resultado global: BLOCKED; solicitud STT consumida: 0/1.** VERIFYING no DONE
ni aceptación de evidencia completa. Continuar desde respuestas reales de esos
gates dentro de r1; no reabrir aprobación de plan ni iniciar F004.

Implementación/evidencia exactas y mapping final local en validation.md. R1
aprobado permanece readonly en snapshot/Git74aaa0b; no cambio de criterios.

Checkpoint vigente: implementación `be2a8233724fe4f94cfaf22aabb39bdcc0ef72fc`, evidencia parcial readonly
`preflight-p2`,76 tests offline PASS. La tarea de referencias sigue abierta:
paquete/plantillas entregados, contenido y bordes humanos UNKNOWN. V-02 requiere
también comparación dirigida con original antes del envío. Resultado global
BLOCKED/VERIFYING y0/1 solicitudes; acta/manifest/hash en validation.md.

## Continuación humana y preflight-p3 (2026-10-04)

Raúl aporta confirmación directa en adjunto20aac15c: escucha y comparación del
audio con el texto presentado, español/términos, presencia/orden de Again/try again,
concordancia acústica a precisión humana normal e identidad C0216 autoritativa.
Se registra USER_VERIFIED/HUMAN_VERIFIED, método listen-and-compare, sin atribuir
autoría manual nueva ni fabricar precisión. Mensaje literal/acta recuperables en
`.local/validation/F003/preflight-p3/owner-message.txt` y `human-verification.json`.
La comparación dirigida fuente/material queda confirmada; V-02 PASS junto con
la preparación y escucha completa1× ya verificadas. No se repide ese juicio.

R1 human-reference gate sigue **BLOCKED**: cinco ventanas con texto UNKNOWN,
0 palabras retenidas en ellas; recuento del texto exacto realmente revisado UNKNOWN.
Los39 controles carecen de intervalos numéricos, mínimo30/≤50ms aún no demostrado;
tres pausas también sin bounds. No afirmar que Raúl escuchó0 palabras ni calcular
el déficit de un texto no recuperado. No adoptar automáticamente citas antiguas
de reconocimiento provisional F001 como texto exacto revisado ni timing oracle.

Raúl responde: «madre mia no los tengo ahora mismo, ejecute un script de python y
eso devolvio todo con exactitud nada complicado. y si quieres esta vez manten el
documento en el proyecto porque realmente lo vamos a usar bastante».
Script/salida exactos no localizados en búsquedas de código/artefactos del proyecto.
Se conserva [documento reutilizable](../../../docs/F003-human-reference.md) con
procedencia, clips y pendientes; no se exige volver a escribir el texto revisado.

Raúl pide ubicación exacta para poner valores de producción. Se prepara archivo
externo vacío `/Users/raulalmeida/.config/editor-agentic-raul/F003.env`,0600,
F003_QWEN_WORKSPACE/DASHSCOPE_API_KEY/F003_AUDIO_URL. El adaptador existente lee
el entorno; workspace del config local permanece null para resolución por env.
Instrucciones en docs/F003-transcription.md. Ningún secreto en proyecto/Git,
ninguna carga automática/ejecución STT por completar el archivo. Confirmaciones
API metered Singapore/model-enabled/CodingPlan=false y OSS privado preexistente/
owner upload/cleanup≤24h siguen UNKNOWN. Variables no cargadas en el proceso
auditado; key existente sigue USER-REPORTED, no se niega su existencia en máquina.

Guard F002 fresco READY, muestras/hash/ledger del WAV válidos;1207 archivos
protegidos0 cambios hash/stat. P2 verificado67 archivos+6 artefactos externos,
sin cambios;76 tests offline PASS retenidos, sin nueva suite ni cambios de código.
Modelo/opciones/límites/snapshot de aprobación/budget local PASS. Documentación
oficial endpoint/precio reconsultada, dentro de tarifas aprobadas; cuenta real
no probada. No requests/attempts/stale lock ni red provider/transport/upload.

Snapshot p3 readonly, manifest SHA
`b2b76fd3b89e341e5b8d725c7ab4b3c803c3a24805570dd09bdaaf6b5d3a24dd`.
**Lifecycle VERIFYING; global BLOCKED; STT0/1.** Aprobación r1 existente permite
la única llamada si pasan todos los gates; no nuevo permiso inmediato requerido.
V-16 final todavía no procede: falta resultado/evidencia real. Sin DONE/F004/
PRODUCTION_APPROVED; F001/F002 permanecen intactos.

## Preflight-p4 — sonda de cuenta y gate de clave (2026-10-04)

El propietario (Raúl) aprobó en chat el uso del workspace free-trial `ws-tdkdn4d3hvt4t7r1`
(Singapore) para F003, verificado, y autorizó rellenar `F003.env` con los valores ya
presentes en `~/.hermes/.env`, además de obtener la referencia humana V-08–V-10 desde la
propia salida STT (listen-and-compare, no como oráculo independiente). Se registran esas
decisiones humanas; no reabren la aprobación r1 ni cambian sus criterios.

Se escribió `~/.config/editor-agentic-raul/F003.env` (0600) con `F003_QWEN_WORKSPACE`,
`DASHSCOPE_API_KEY` y `F003_AUDIO_URL` vacío (el upload OSS sigue siendo gate del propietario).
Ninguna clave se imprimió ni entró en Git; `F003.env` es externo al proyecto.

**Sonda de elegibilidad V-03 (GET, sin audio, sin coste, POST STT NO consumido):**
`GET https://{ws}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{dummy}` con la clave
`DASHSCOPE_API_KEY` de `~/.hermes/.env` → **HTTP 401 `InvalidApiKey`**. Confirmado también
en compatible-mode `/models` del host del workspace y en los endpoints nativos
`dashscope-intl` y `dashscope` (Beijing): 401 en los tres. Evidencia saneada en
`.local/validation/F003/preflight-p4/account-probe.json` (request_id, host, key_sha8; sin Bearer ni URL firmada).

Diagnóstico de la clave almacenada (sin exponerla): valor de 115 caracteres, prefijo `sk-w`,
contiene puntos/guiones/guiones bajos — forma atípica de una DashScope API key (que suele ser
`sk-`+32 hex, ~35 chars). Rechazada por Alibaba en todas las regiones. Conclusión: la clave
free-trial actualmente en `~/.hermes/.env` **no es válida** (expirada, revocada o mal copiada).

**Resultado: V-03 BLOCKED por credencial; STT 0/1 sin consumir.** No se ejecuta el POST
autorizado porque fallaría autenticación y consumiría el único intento, exigiendo nueva
autorización puntual. Se detiene aquí y se requiere del propietario una clave DashScope
free-trial válida del workspace Singapore (Model Studio console). F001/F002 DONE intactos;
sin F004 ni PRODUCTION_APPROVED.

## Preflight-p5 — CORRECCIÓN del gate de clave (2026-10-04)

**El acta p4 es FALSA y queda corregida aquí.** La conclusión "clave free-trial no
válida" fue un error del agente operador: sus sondas enviaron literalmente el prefijo
`***` en la cabecera Authorization (bug de auto-enmascarado en el script de prueba),
produciendo 401 espurios. Con `Bearer <key>` limpia la clave FreeTrailv2 del workspace
`ws-tdkdn4d3hvt4t7r1` es VÁLIDA: HTTP 200 en compatible-mode chat y en nativo
`/api/v1/services/aigc/text-generation/generation` (qwen-flash-character, usage real).
Evidencia corregida: `.local/validation/F003/preflight-p5/account-probe-corrected.json`.
POST STT sigue 0/1 sin consumir.

Hechos de cuenta verificados (probes GET/POST sin audio del fixture + log de auditoría
externo del propietario):
- La clave free-trial autentica en ws-host compatible-mode y nativo `/api/v1`.
- Modelos fuera de la cuota free → 403 `AccessDenied.Unpurchased` (no 401).
- `qwen-audio-3.1-asr-flash-filetrans` figura en la cuota habilitada del propietario
  (1M tokens, expira 2027-01-02) — tabla aportada por Raúl; elegibilidad de inferencia
  del modelo filetrans concreto queda confirmada por su acta, no por probe propio (el
  probe GET tasks dummy en ws-host devuelve 403 Unpurchased como quirk de task
  inexistente; el host intl devuelve 200 UNKNOWN para el mismo dummy).
- Limitación de transporte verificada por el log externo: la política de subida de
  DashScope rechaza claves de workspace (401) → el WAV NO puede subirse con esta clave
  por el File API/upload endpoint. El transporte aprobado r1 (OSS privado Singapore
  gestionado por el propietario, URL firmada) sigue siendo el único camino, intacto.
- `~/.config/editor-agentic-raul/F003.env` actualizado con workspace + clave válida
  (0600, fuera de Git). `F003_AUDIO_URL` sigue vacía: gate del propietario.

**Decisión del propietario sobre V-08–V-10 (registro literal, 2026-10-04):** ante la
objeción del agente de que derivar la referencia literal del propio candidato STT
invalida la independencia del WER (referencia == candidato, WER trivialmente 0),
Raúl respondió: «esto que dices ... lo vamos a hacer asi. nos va a dar mas velocidad y
realmente ya lo comprobe, creeme», citando además su comprobación previa de que la
respuesta STT es «100% identica la respuesta a lo que digo en el video». Se ejecuta
por orden expresa del owner; la referencia resultante quedará marcada
CANDIDATE_DERIVED / OWNER_OVERRIDE con la limitación registrada, nunca como
referencia independiente limpia. V-16 (aceptación humana final) sigue siendo juicio
real de Raúl sobre el paquete de evidencia.

**Estado: VERIFYING; global BLOCKED solo por transporte (F003_AUDIO_URL).**
F001/F002 DONE intactos; sin F004 ni PRODUCTION_APPROVED.

## Preflight-p6 — transporte OSS investigado, gate de cuenta pendiente (2026-10-04)

Owner autorizó instalar tooling y verificar capacidad de crear el transporte:
`aliyun-cli 3.5.1` (brew) y `ossutil 2.4.0` (CDN oficial, SHA-256 verificado
`26e51080…5a78a41d` antes de instalar). Credenciales configuradas por Raúl con
usuario RAM `power-application-user` (cuenta 5787891059913905, ap-southeast-1);
la clave raíz no toca el disco. `~/.ossutilconfig` 0600 generado desde
`~/.aliyun/config.json` sin imprimir secretos.

Sondas (todas read-only salvo un `mb` rechazado por el servicio):
- `sts GetCallerIdentity` → RAMUser válido, región correcta. Auth OK.
- `ossutil ls` / `ossutil mb oss://arsd-f003-transit --acl private` → **403
  UserDisable EC 0003-00000801**: el servicio OSS no está activado en la cuenta.
  No es problema de credencial ni de política RAM.
- `bssopenapi QueryAccountBalance` → AvailableAmount **0.00 USD**. Coherente con
  UserDisable: OSS es pay-as-you-go y requiere activación con método de pago.
- El RAM user no puede listar sus propias políticas (403 ram:ListPoliciesForUser,
  esperado en un usuario sin admin RAM).

**Conclusión:** el transporte aprobado r1 (OSS privado Singapore) está bloqueado
por un gate de cuenta del propietario: activar OSS en consola
(https://oss.console.aliyun.com → Activate Now) con método de pago/saldo. El
agente NO crea ni activa servicios de pago por su cuenta. Intento de bucket
rechazado por el servicio, ningún recurso creado, ningún coste incurrido.

Alternativa registrada para decisión del owner (NO autorizada, requeriría
enmienda de plan): ASR síncrono free-trial (`qwen-audio-3.1-asr-flash` vía
`bl speech recognize` o multimodal-generation) acepta audio sin OSS, pero exige
comprimir el WAV de 22,3 MB a ≤10 MB (mp3/opus), lo que cambia el binding r1
("transporta WAV únicamente") y necesita aprobación explícita.

**Lifecycle VERIFYING; global BLOCKED por transporte; STT 0/1 sin consumir.**
F001/F002 DONE intactos; sin F004 ni PRODUCTION_APPROVED.

## Preflight-p7 — transporte OSS resuelto; revisión material autorizada del gate de referencia (2026-10-04)

**Transporte resuelto (gates a–d de la instrucción del owner, hechos medidos):**
OSS quedó activado en la cuenta 5787891059913905: `ossutil ls` responde exit 0,
sin UserDisable. Bucket privado `arsd-f003-transit` creado en ap-southeast-1
(ACL private, Standard) bajo autorización explícita del owner en su mensaje de
hoy («Crear el bucket de tránsito una vez OSS esté activo: arsd-f003-transit,
privado, ap-southeast-1»). Subido SOLO el WAV canal 1
(SHA-256 `4c71d1689fdec2fb419ec6b91cb6ca0317a0b172b594e3b6ab7532cbe00645f3`,
22.348.844 bytes); round-trip de verificación (descarga del bucket → SHA idéntico).
El bucket contiene exactamente 1 objeto; ningún RAW/clip/sidecar. URL firmada GET
TTL 2h escrita en `F003.env` (0600) sin imprimirla; validada con el parser del
adaptador (https, host `arsd-f003-transit.oss-ap-southeast-1.aliyuncs.com`,
7199 s restantes, dentro de 1800–7200). Evidencia: `.local/validation/F003/preflight-p7/`.

**Estado local verificado:** suite 76/76 OK con Python 3.14.7 exacto (el guard
`require_runtime` rechaza 3.9/3.13; el `python3` del PATH debe ser 3.14.7).
`prepare` exit 2 NEEDS_REVIEW (comportamiento documentado), `verify` BLOCKED
TRANSCRIPT_NOT_READY (esperado). Sonda de submit con red bloqueada y referencia
UNKNOWN: STOPPED `INDEPENDENT_REFERENCE_REQUIRED` ANTES de cualquier POST;
0 intentos creados; STT 0/1 sin consumir. Precio de lista revalidado hoy por
sondeo documental: input ¥0.02/M, output ¥0.06/M — dentro del techo aprobado
USD 0.15/1M input y 0.47/1M output (`preflight-p7/pricing-revalidation.json`).

**Conflicto estructural detectado y decisión del owner (revisión material autorizada):**
`validate_reference` (r1) exige la referencia humana completa ANTES del POST,
pero el OWNER OVERRIDE registrado en p5 y reafirmado hoy deriva la referencia
DEL candidato STT (existe solo DESPUÉS del POST). Son incompatibles sin cambiar
el orden del gate. Presentado a Raúl con tres opciones; su respuesta literal
(2026-10-04, clarify): «Revisión material de plan: me autorizas explícitamente a
ajustar el orden del gate para que la referencia se derive del candidato STT
DESPUÉS del POST (marcada CANDIDATE_DERIVED/OWNER_OVERRIDE), actualizando
plan.md/validation.md y registrando tu aprobación literal. Luego ejecuto el
submit 1/1 y sigo con normalize/evaluate.» Su instrucción de sesión añade:
«V-08–V-10: la referencia humana se deriva del propio candidato STT. Es un OWNER
OVERRIDE registrado en acta; márcalo CANDIDATE_DERIVED, nunca como referencia
independiente limpia.»

**Alcance exacto de la revisión autorizada (implementación p7):**
1. `validate_reference` gana una rama explícita: solo con marcadores
   `derivation='CANDIDATE_DERIVED'` + `owner_override=true` + `candidate_seen=true`
   + `derivation_pending=false` se admite la referencia derivada; sin marcadores,
   la exigencia de independencia (`candidate_seen=false`) permanece intacta.
   NINGUNA tolerancia de contenido se relaja: ≥200 palabras, ≥30 controles,
   grupos 10+10+10, críticos again/try/again/try/again, 4 términos, bounds
   ≤50 ms, 3 pausas con núcleo >0.3 s y frases incorrecta/corregida siguen
   siendo obligatorios también en modo derivado.
2. `human_gate` pre-POST admite el estado PENDIENTE de la referencia derivada
   (marcadores + binding + `derivation_pending=true`, sin contenido todavía).
3. Nueva operación determinista `derive`: construye la referencia desde el
   transcript normalizado (ventanas fijas r1, primeros 10 léxicos, críticos,
   términos, bounds de candidato con incertidumbre 0, pausas desde gaps
   observados, frases desde runs entre pausas). Si el candidato no contiene los
   eventos exigidos (Again aislado, try again ×2, términos, ≥200 palabras),
   la derivación FALLA y se registra HUMAN_REVIEW_REQUIRED; nunca se fabrican
   palabras ni bordes.
4. Consecuencia aceptada por el owner y registrada: WER y errores de timing
   contra referencia candidate-derived son triviales (0 por construcción); su
   valor probatorio es de integridad estructural, NO de exactitud independiente.
   V-08/V-09/V-10 se marcarán CANDIDATE_DERIVED/OWNER_OVERRIDE en validation.md,
   nunca como referencia independiente limpia. V-16 sigue siendo juicio real de
   Raúl sobre el paquete completo.

Fuera de este alcance: nada de F004/semántica/edición/captions/HyperFrames/render;
F001/F002 y el bundle r1 aprobado (74aaa0b) intactos; sin retries de POST;
máximo 1 solicitud STT.

**Implementación p7 ejecutada:** `pending_derived_reference` + rama derivada en
`validate_reference` (marcadores `derivation=CANDIDATE_DERIVED` +
`owner_override=true` obligatorios; sin marcadores la independencia r1 queda
intacta) + operación determinista `derive` (falla si el candidato carece de los
eventos exigidos; nunca fabrica palabras/bordes) + 2 tests negativos nuevos.
Suite 78/78 OK (python3.14.7). `reference.json` pasado al estado PENDIENTE con
marcadores (snapshot previo readonly en preflight-p7/); `review.json` completado
con hechos de cuenta (p4/p5 + quota owner-reported), storage (p7, hechos OSS
medidos) y pricing revalidado hoy.

**Submit real ejecutado (intentos r1: 1/1 CONSUMIDO):** todos los gates locales
pasaron (approval 74aaa0b + bundle hashes, human_gate, TTL 7199 s, transport
streaming SHA exacto VERIFIED, sanitize clean). POST aceptado en el ws-host:
task_id `8d1951e0-e2be-44d2-a5fc-1540fb56d3fa`, request_id
`88aeafa9-8c3a-9867-b494-aa14ee0b605c`, PENDING, usage final reportado
duration=178 s, input 5654 / output 602 / total 6256 tokens.

**p7b — defecto de recuperación detectado, PARADA obligatoria:** el GET de
estado del adaptador r1 va al ws-host y devuelve 403 `AccessDenied.Unpurchased`
(el mismo quirk registrado en p5 para GET tasks). El job real está
**SUCCEEDED/subtask SUCCEEDED y es recuperable vía GET en `dashscope-intl`
(host International, NO Beijing)**: probe read-only HTTP 200, sin re-POST, sin
segundo cargo. Clave viva confirmada (chat compatible-mode 200). Corregir el
host del GET de recuperación es un cambio de frontera de transporte del bundle
aprobado, FUERA de la revisión material p7 autorizada: requiere autorización
explícita del owner antes de tocarlo. Evidencia completa:
`.local/validation/F003/preflight-p7/submit-and-recovery-finding.json` (sin URL
firmada ni clave). current.json BLOCKED HTTP_403 administrativo; journal del
intento preservado; ningún reenvío automático (PAID_ATTEMPT_ALREADY_CONSUMED
activo). Lifecycle VERIFYING; resultado real obtenido pero NO normalizado ni
evaluado; V-16 pendiente; F001/F002 intactos; sin F004 ni PRODUCTION_APPROVED.

## Preflight-p7c — recuperación autorizada ejecutada; hallazgo de calidad real del candidato (2026-10-04)

Raúl autorizó literalmente p7c (clarify 2026-10-04): «Autorizar p7c: corrijo el
host del GET de recuperación a dashscope-intl (International, ap-southeast-1; NO
Beijing) y amplio el allowlist Bearer a ese host oficial de Alibaba, manteniendo
el POST donde ya fue aceptado. Sin re-POST ni segundo cargo. Registro el cambio
de frontera en acta + validación. Luego resume→normalize→derive→evaluate y te
presento el paquete HUMAN_REVIEW.»

**Cambio de frontera ejecutado (mínimo, GET de recuperación únicamente):**
`recovery_endpoint()` = `https://dashscope-intl.aliyuncs.com/api/v1` (host
oficial International ap-southeast-1); allowlist Bearer ampliado con match
exacto de ese host; POST sigue en el ws-host aprobado. Test nuevo de allowlist
(intl admitido; Beijing/lookalikes rechazados sin recibir la clave). Suite
**79/79 OK**. Pre-chequeos read-only antes del fix: `file_url` echo exacto
(guard RESULT_INPUT_MISMATCH satisfecho), `transcription_url` en
`dashscope-result-sgp.oss-ap-southeast-1.aliyuncs.com` (compatible con
object_url), `vendor.job()` acepta el payload.

**Recuperación real:** `resume` → GET tasks intl 200 → SUCCEEDED/subtask
SUCCEEDED → descarga del resultado → respuesta vendor saneada retenida
(5 redacciones; canarios de clave/URL firmada: AUSENTES en todos los
artefactos) → **normalize READY**:
transcript_id `sha256:eff3ff0b7cb3921a8a540bd483da27ccddcf8002799639138c084d118cd4a30e`,
550 palabras, binding intacto. Usage real: duration 178 s, input 5654 / output
602 / total 6256 tokens; coste de lista calculado USD 0.00113104 (techo r1);
conciliación de facturación real V-13 PENDIENTE. STT sigue 1/1 (GET-only, sin
segundo cargo).

**Hallazgo de calidad real (evidencia: `preflight-p7/candidate-quality-finding.json`):**
1. **Fragmentación sub-palabra**: los word-timestamps del vendor vienen
   fragmentados (254/550 rows ≤3 chars: 'mon'/'ol'/'ito'); el texto a nivel de
   frase es limpio y correcto («si tienes un monolito … en cincuenta
   microservicios»). Quirk de representación del proveedor que rompe la
   evaluación r1 a nivel de palabra (controles de timing/WER por palabra léxica).
2. **`idempotencia` NO reconocido**: el candidato transcribió «…duplicados,
   reintentos y **en potencia** y fallos parciales». El hotword (vocabulary
   peso 1) fue enviado en la solicitud real (request.json lo contiene) y aun así
   el ASR produjo la variante «en potencia» — exactamente una de las variantes
   UNCERTAIN que el handoff F001 ya predijo. 3/4 términos presentes
   (monolito, microservicios a nivel de frase; eventos ×4); idempotencia ausente
   en el texto completo del candidato.

**Consecuencia en gates (resultado real, no inventado):** `derive` se detuvo con
`DERIVATION_EVENT_MISSING` — una referencia candidate-derived no puede contener
un término que el candidato no tiene, y fabricarlo violaría el contrato y la
honestidad de la evidencia. Por tanto V-08 (término técnico) = **FAIL real**;
V-09/V-10 = BLOCKED (la evaluación numérica r1 no puede ejecutarse sin
referencia válida; y la fragmentación rompería además los controles por
palabra); V-04 = PASS (solicitud/respuesta reales retenidas); V-05/V-12 = replay
local pendiente; V-13 = coste real registrado, conciliación de facturación
pendiente. La creencia previa «100% idéntica» (p5) queda corregida por la
evidencia real: el candidato NO es idéntico al habla en al menos un término
crítico.

**PARADA obligatoria ante el owner:** el fallo de V-08 es un resultado FAIL real
contra criterios r1. No se «arregla» con código (retrofit prohibido), ni con
otro submit (1/1 consumido; un segundo gasto exige autorización puntual nueva y
cambiar vocabulary/contexto cambiaría el fingerprint → NEW_PAID_AUTHORIZATION).
La decisión es del owner: aceptar el FAIL registrado, autorizar una revisión de
criterios vía change-control, o autorizar puntualmente una segunda ejecución con
configuración mejorada. Lifecycle VERIFYING; global BLOCKED por V-08 FAIL real;
F001/F002 intactos; sin DONE, sin F004, sin PRODUCTION_APPROVED.

## Preflight-p8 — CORRECCIÓN del acta p7c y oráculo independiente gratuito (2026-10-04)

**El acta p7c contiene dos afirmaciones falsas producidas por errores de
medición del agente y quedan corregidas aquí** (mismo procedimiento que p5
respecto de p4). El resultado FAIL de V-08 no cambia, pero su causa real es más
estrecha de lo registrado.

Error 1 — «46% de word-timestamps fragmentados»: **FALSO**. Ese recuento
incluía palabras funcionales legítimas (`de`, `no`, `y`, `el`). Medida real:
**106/550 tokens de continuación (19%)**, identificables de forma determinista
porque el vendor omite el espacio inicial en una continuación sub-palabra.

Error 2 — «la fragmentación rompe los controles de timing por palabra y hace
inviable la evaluación a nivel de palabra»: **FALSO**. La fragmentación es
**reconstruible determinísticamente** (concatenar continuaciones; no cruzar
límite de `segment_id` ni de puntuación de frase). Tras la reconstrucción
correcta: **470 palabras reales**, timing **monotónico y ordenado**, duración
mediana 280 ms, máximo 2.04 s, y solo **1/470 (0%)** palabras >1.5 s — perfil
comparable al oráculo. Las primeras reconstrucciones del agente eran las
defectuosas (llegaron a producir una «palabra» de 11,68 s fusionando tres
frases), no los datos del proveedor.

**Oráculo independiente REAL, gratuito y local (hallazgo principal de p8):**
`mlx-community/whisper-large-v3-turbo` vía `mlx_whisper 0.4.3`, ya instalado en
`/Users/raulalmeida/Workspace/MotionGraphics/.venv` y con el modelo en caché —
**nada nuevo instalado, sin red, sin coste, sin consumir presupuesto STT**.
Ejecutado sobre el MISMO WAV canal 1 (`4c71d168…`, resampleado a 16 kHz mono,
232,8 s) en **11,6 s**: 58 segmentos / 468 palabras con timestamps y
probabilidades por palabra.

**Precisión sobre su alcance (corrección de una sobre-afirmación del propio
agente):** el oráculo es **independiente pero automático**. NO satisface el
requisito literal de r1 para V-08 («un observador competente en español escucha
y aporta texto literal»): sigue sin haber referencia *humana*. Su valor real es
otro y está expresamente previsto en `tech-stack.md §7` — la **comparación de
proveedores sobre fixture real** («real-fixture comparison of technical
vocabulary, language accuracy, word timestamps»). Sirve para medir la exactitud
léxica del candidato contra un motor distinto y para desmontar el motivo por el
que se pidió el OVERRIDE p5, pero no convierte una salida de máquina en
referencia humana. Declararlo «lo que r1 exigía» habría sido falso.

**Comparación determinista medida (evidencia: `.local/validation/F003/oracle-comparison/`,
WER con la misma función `comparison_words`/`edit_alignment` del evaluator r1):**

| Ventana r1 | oracle | qwen | S | D | I | N | WER |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [0,25) | 67 | 65 | 2 | 2 | 0 | 67 | 5,97% |
| [60,85) | 57 | 57 | 1 | 0 | 0 | 57 | 1,75% |
| [90,115) | 47 | 48 | 2 | 1 | 2 | 47 | 10,64% |
| [130,155) | 46 | 47 | 2 | 1 | 2 | 46 | 10,87% |
| [195,228) | 75 | 76 | 0 | 0 | 1 | 75 | 1,33% |
| **GLOBAL** | 292 | — | 7 | 4 | 5 | 292 | **5,48%** |

El umbral de V-08 es sobre el WER global (`evaluate` acumula `totals` de todas
las ventanas): **5,48% ≤ 10% → PASS en el componente de exactitud léxica**,
medido contra oráculo independiente, no contra sí mismo. Las ventanas 2 y 3
superan individualmente el 10% (10,64% / 10,87%) y quedan registradas como
observación, no como criterio r1.

**Términos técnicos — el único fallo real que sobrevive:**

| Término | qwen (pagado) | whisper local (gratis) |
| --- | --- | --- |
| monolito | 1 | 1 |
| microservicios | 1 | 1 |
| eventos | 4 | 4 |
| **idempotencia** | **0** («en potencia») | **0** («impotencia», p=0,744) |

`idempotencia` falla en **AMBOS** modelos. No es un defecto del proveedor de
pago: es una limitación real de ASR sobre esa palabra en este audio. El handoff
F001 ya la había marcado UNCERTAIN con las variantes `diampotencia`,
`impotencia`, `bienpotencia`, `en potencia` — predicción confirmada por dos
motores independientes.

**Evidencia cruzada de otro proyecto del owner (`~/Workspace/MotionGraphics`,
coste 0 €):** su pipeline free (mismo Whisper local) produjo `diampotencia`
(p=0,663) en el mismo punto del discurso y lo resolvió con una **tabla de
correcciones de glosario escrita por un humano**:
`specs/006-arquitectura/edit.json` → `captionCorrections`
(`diampotencia`→`idempotencia`, `RP`→`ERP`, `check-out`→`checkout`). Es decir:
el karaoke/subtítulos exactos NO los produjo el modelo, los produjo una capa
determinista de corrección terminológica revisada por humano — exactamente lo
que `tech-stack.md §7` ya manda («corrected technical terminology while
preserving what was spoken») y lo que el bundle r1 de F003 **no incluye**.

**Estado corregido de V-08:** componente WER **PASS** (5,48% vs oráculo
independiente); componente de terminología técnica **FAIL real** (1 de 4
términos ausente en cualquier proveedor). V-08 global = **FAIL**, por
terminología únicamente. V-09/V-10 dejan de estar bloqueados por
«fragmentación inviable» (afirmación retirada) y pasan a depender de la
referencia y de los controles; la evaluación numérica real sigue pendiente de
una referencia válida y de la decisión del owner sobre el término.

**Consecuencia de gobierno (para el owner, no decidida por el agente):** con un
oráculo independiente disponible y gratuito, el OWNER OVERRIDE p5
(CANDIDATE_DERIVED) **deja de ser necesario** como sustituto de la
independencia; la referencia puede construirse desde el oráculo Whisper y
quedar como referencia independiente limpia. Adoptarlo cambia el binding de la
referencia y requiere aprobación explícita: el agente no lo aplica por su
cuenta.

Ninguna llamada STT adicional (1/1 consumido). Ninguna instalación nueva.
Objeto de tránsito OSS borrado (cleanup r1 ≤24 h ejecutado: bucket 0 objetos);
transcript y respuesta vendor siguen retenidos localmente. F001/F002 intactos;
sin DONE, sin F004, sin PRODUCTION_APPROVED.

## Spike-p9 — preview de revisión autorizado por el owner (2026-10-04)

Raúl autorizó literalmente un spike desechable («spike desechable me gusta eso,
el spike autorizado») con el objetivo de ver el vídeo con el texto al mismo
tiempo para corregir, sin render final, validando en Studio/navegador y dando
correcciones en lenguaje natural con tiempo aproximado. Aclaró además que 006
(MotionGraphics) y C0216 (F003) son el MISMO discurso: uno ya editado, el otro
raw.

**Vínculo de fuente verificado (medido, no asumido):** mismo discurso, distinta
captura. La fuente de 006 es `WhatsApp Video 2026-10-03 at 16.14.01.mp4`
(SHA `e72d69b6…`, 37 MB, h264 848×480 rotación −90, 25 fps, re-encode de
WhatsApp); la nuestra es `C0216.MP4` (SHA `68addbf3…`, 2.873.163.442 bytes,
Sony ZV-E10 4K portrait). Ambos duran exactamente **232,800000 s**. El vídeo
006 se montó sobre una copia comprimida de WhatsApp, no sobre el raw de
estudio; eso abarató decodificación y explica parte de su velocidad. El spike
usa nuestro WAV canal 1 real + proxy vertical ligero, nunca el 4K de 2,87 GB.

**Spike construido en `.local/spike/f003-preview/` (ignorado por git, fuera del
bundle, sin tocar F001/F002/F003 ni el RAW):**
- `build_captions.py`: reconstrucción determinista del transcript REAL F003
  (550 rows → 466 palabras; regla de continuación sub-palabra sin cruzar
  `segment_id` ni puntuación) + 149 páginas + tabla de correcciones
  terminológicas (forma D003). Cero llamadas nuevas; STT sigue 1/1.
- `build_composition.py`: composición HyperFrames de solo revisión (proxy +
  karaoke por palabra `#94a3b8`/`#f59e0b`/`#f8fafc`, `tl.set` sobre spans
  hijos, nunca sobre `.clip`).
- Proxy 540×960 25 fps con el audio del WAV canal 1 (`4c71d168…`), 60 s de
  ffmpeg local. HyperFrames 0.8.78 y gsap reutilizados de MotionGraphics:
  nada instalado.

**Validación real ejecutada:** `hyperframes lint` 0 errores; `hyperframes check`
PASS (runtime 0, layout 0/9, motion 0, contraste 26/26 WCAG AA); `snapshot` 4
fotogramas con GPU hardware. Karaoke medido por píxeles en la banda de
subtítulos: a 111,5 s → 5190 px ámbar + 7626 gris; a 112,0 s → 5486 blanco +
7158 ámbar + 158 gris. Lectura visual del fotograma 112,0 s: «reintentos y
idempotencia», con `idempotencia` en ámbar y subrayado punteado (corrección
D003 aplicada en ~111,95 s; original y timing conservados). Studio servido en
`http://localhost:3002/#project/composition`, HTTP 200, vivo en background.

**Límites honestos:** proxy CRF 30 (solo leer/escuchar, no juzgar imagen); sin
gráficos/PiP/marca/safe-zones; tiempos del vendor con su incertidumbre
(revisión de texto, no certificación de sincronía). Desechable: no es
entregable ni F004. RAW C0216 intacto (bytes y mtime sin cambios); el proxy es
copia derivada. Flujo 006 y adaptaciones propuestas:
`docs/F003-vs-MotionGraphics-diagnostico.md`. Sin DONE, sin F004, sin
PRODUCTION_APPROVED.
