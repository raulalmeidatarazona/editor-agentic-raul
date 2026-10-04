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
- [x] Preparar paquete de escucha del fixture y referencias antes del POST; detener para juicio de Raúl donde V-02/08–10 exige escuchar/confirmar. No pedir campos medibles manuales.
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
