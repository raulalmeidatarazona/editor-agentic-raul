# F003 — Contrato de validación y evidencia

**Bundle revision:** r1\
**Requirements:** [requirements.md](requirements.md)\
**Estado/aprobación:** únicamente en [plan.md](plan.md)

Definido antes de código/pago. Todas las pruebas de F003 están **NOT RUN**.
Documentación oficial en PLAN y evidencia aceptada F001/F002 no son PASS F003.

## Input real, entorno y procedencia

Raíz `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/projects/f002-studio-001/`:
usar guard READY F002 y owned `raw/source`, nunca el MP4 original como bypass.
Identidades source/project/inspección y streams en requirements.md son expected
fixtures, no constantes del código general. Source2.873.163.442bytes/SHA
`68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`.
Reloj `source-presentation-v1`, clock ID
`77eb1d8cc14a3c1171c6fee14801c9a124a1f08d4844dc47f687ae103ce68d99`,
audio/vídeo0→1164/5s, origen0, audio stream1/48kHz/2canales/layoutUNKNOWN.

F001 original `.local/fixtures/F001-studio-001/raw/C0216.MP4`, recovery
`/Volumes/PortableSSD/videos/raw/C0216.MP4`, identidad/recuperación aceptadas e5;
no exige reconectar ese disco para transcribir el owned source. F001 e5 manifest
`accd69f2e0e5c70451b60f1fa6f364837e9fa03ce4bb52141003592ea0027696`;
F002 e1 manifest `3dd9201577a3e23cae128760a6ad217e48e24bb46d1e0acaf82d1fc93f71d35c`.
Son referencias a evidencia previa, no nuevas mediciones de este turno.

Runtime previsto Python3.14.7 estándar/FFmpeg+ffprobe9.0.1 existente; revalidar
versiones, espacio/acceso y código aprobado antes de IMPLEMENT. Sin install.
Cloud prerequisites no verificados: cuenta/key/workspace Singapore aptos para
API metered, modelo permitido, OSS privado existente gestionado por Raúl, URL
firmada y aceptación de scope/retención. No llamar API para descubrir elegibilidad
durante PLAN. Missing => BLOCKED en validación dependiente, nunca PASS.

## Referencias humanas reales y procedimiento de escucha

Notas e5 conservadas `.local/fixtures/F001-studio-001/evidence/reference-notes-e5-approved.md`:
español natural de arquitectura/modernización, voz inteligible con ruido/posible
eco; cuatro términos confirmados monolito/microservicios/eventos/idempotencia.
Los tiempos del handoff son **aproximados**, no oracle de precisión por palabra.

| Región fuente aproximada e5 | Referencia de contenido para revisar, no etiqueta que produzca F003 |
| --- | --- |
| 01:08–01:16 | Monolito/microservicios; localizar ocurrencias por escucha real. |
| 01:19–01:24 y 01:31–01:38 | Eventos; referencia técnica y afirmación intencionalmente incorrecta. |
| 01:31.5–01:38.7 | Raúl confirma afirmación de garantía de no procesar dos veces; transcript debe conservar lo dicho, sin corregir la arquitectura. |
| 01:38.7–01:40.3 → 01:40.3–01:40.8 → 01:40.8–01:42.7 | Pausa → Again aislado → pausa confirmados; límites exactos a observar, no cargar estos tiempos como texto/timing canónico. |
| 01:42.7–01:53.8 | Raúl confirma corrección sobre ausencia de garantía de una única vez. Cerca01:52 reconocimiento de idempotencia UNCERTAIN; palabra realmente usada USER-REPORTED, ubicarla por escucha, no fijar ese instante por suposición. |
| 02:14–02:26 | Raúl confirma narración «try again, try again»; parejas aproximadas02:17.3–02:18.0 y02:18.4–02:19.1. |
| 00:09.7–00:10.4 / 00:37.2–00:40.9 | Pausas candidatas del handoff; la existencia de una pausa natural está confirmada, sus bordes todavía no son ground truth. |
| Principio /03:26–03:36 /03:37–03:47.4 | Palabras completas al inicio/final, resumen/cierre; comprobar ausencia de truncamiento de texto. |

Durante IMPLEMENT, antes de enviar, preparar solo audio local derivado y paquete
de escucha: canal0/1, WAV final, snippets de esas regiones con buffers2s, y windows
fijas **[0,25), [60,85), [90,115), [130,155), [195,228)** segundos fuente.
Snippets son evidencia local únicamente, no cortes de producción ni uploads
individuales; offsets racionales/sample counts/hashes documentados. Registrar
full playback a1× del WAV para elegir canal y comprobar que conversión no pierde
voz; comparación dirigida con audio original en los extremos/eventos.

Referencia de texto sin ver el resultado candidato: observador competente en
español escucha windows fijas y transcribe literalmente. Agente prepara campos
medibles/artefactos; Raúl confirma frases dudosas y juicios de fidelidad. Ground
truth antes de comparar/candidato para evitar corregir la referencia hacia el
modelo. Mínimo **200 palabras** conjuntamente, cubrir todos los eventos críticos;
si windows contienen menos, ampliar desde228s hacia atrás, preservando selección
original y procedimiento. No escoger solo frases donde el modelo acierta.

Reference timing: localizar onset/offset audible con escucha repetible a1× y
waveform local de PCM (stdlib/SVG, sin nueva dependencia ni ASR). Mantener tabla
por palabra de intervalos de posible borde, revisor/método, razón/incertidumbre.
Bounds acústicos no son determinísticamente medibles solo por nivel de energía;
pedir juicio de Raúl para ambiguos, sin exigir que rellene SHA/offsets/duración.
Necesarias **30 palabras de control**: diez primeras palabras léxicas audibles
de cada window [0,25), [90,115), [195,228), más las cinco palabras críticas
Again + try/again + try/again y cuatro términos (si coinciden, cuentan una vez;
total mínimo30). No abandonar controles mal reconocidos; contar omisión como fallo.
Cada borde reference requiere incertidumbre≤50ms; si no establecible, check
temporal BLOCKED/humano pendiente, no sustituir por tiempos del handoff.

## Tolerancias y fronteras fijadas antes del resultado

- Identidad, bytes, SHA/bindings, core JSON, rational mapping, PTS/offsets,
  samples, orden, separación vendor/domain y byte-identical replay: **exactos**.
- Extraer mono a sample rate nativo: sample count exacto, primer PTS exacto y
  continuidad; duración exacta por muestras. Provider original_duration_ms admite
  ±(1ms+1sample) por su representación, no para esconder word endpoints inválidos.
- Fidelidad natural: WER≤**10%** en las≥200 palabras de referencia; comparison
  Unicode NFC/casefold, eliminar puntuación, colapsar espacios, preservar acentos,
  números y negaciones. Registrar S/D/I/N por distancia Levenshtein independiente;
  ninguna normalización de comparación reescribe transcript. Raúl debe además
  confirmar representación suficiente, afirmación errónea/corrección distinguibles
  como texto y ninguna negación crítica perdida. WER por sí solo no basta.
- Vocabulario: las cuatro palabras confirmadas por F001 se evalúan, al menos una
  ocurrencia audible localizada de cada una reconocida exactamente (casefold/NFC).
  No suministrar reference frases completas en hints. Si el término/posición sigue
  inaudible/ambiguo, solicitar juicio y mantener check pendiente; nunca inventarlo.
- Palabras críticas: Again aislado y dos parejas try again reconocidas en orden,
  completas, con word timestamps conocidos. Grafía case-insensitive/puntuación
  aparte; «Thank you»/traducción/omisión o una pareja perdida = FAIL.
- Timing: para cada borde comparado, error conservador = máxima distancia al
  extremo del intervalo de incertidumbre reference. Controles: p95 de errores
  onset y offset≤**200ms** (nearest-rank, índice ceil(0.95×N)), máximo≤**300ms**. Cinco palabras críticas: **cada**
  onset/offset≤**150ms** conservadores. No declarar sample precision del modelo
  por tener integer ms. Son mínimos F003 para poder estudiar sincronía/retomas;
  F004/captions deben validar límites de corte/producción por su cuenta.
- Drift: comparar mediana de errores firmados del primer y último grupo de diez
  controles (puntos medios reference): diferencia absoluta≤**100ms**. Todas las
  palabras/segments deben cumplir bounds/monotonicidad estructurales globales.
  No ajustar offset para mejorar resultados. Cualquier threshold incumplido FAIL.
- Pausas: dos buffers alrededor de Again y una pausa natural confirmada no
  contienen palabras alucinadas dentro de su núcleo observado. El margen de
 150ms de los bordes humanos se excluye solo de esta prueba de silencio; no
  amplía tolerancia de timing ni elimina palabras del transcript. Si pausa sin
  núcleo restante, elegir otra pausa natural audible, registrar el motivo.

## Checks predefinidos y matriz AC

| Check | AC | Categoría | Procedimiento / resultado exigido | Evidencia |
| --- | --- | --- | --- | --- |
| V-01 | AC-01 | DETERMINISTIC | Guard F002 real inmediatamente antes de preparar/enviar/consumir. Fuente/manifest/inspection/clock coinciden con aceptados; no path bypass. Después hashes/stats F001 y todo subtree F002 preexistente idénticos. | baseline/final hashes/stats, guard/output/binding, implementación commit. |
| V-02 | AC-01/04 | DETERMINISTIC + HUMAN | Scan audio independiente/comparación F002; WAV samples/counts/PTS/hash/duration exactos, canal explícito y escucha completa1× confirmada por Raúl. Dos canales evaluados sin asumir DJI, no procesamiento. | preparación/argv/version/sample ledger, WAV/previews hash, acta canal/escucha. |
| V-03 | AC-01/08 | DETERMINISTIC + HUMAN | Preflight local, consentimiento/eligibilidad/cuenta/región/config/precio; Raúl confirma objeto privado existente/TTL/cleanup. URL en env, GET streaming hash exacto del WAV, un archivo/canal autorizado enviado. Ningún RAW/publicACL/Beijing/uploader. | URL-free transport manifest/hash, account eligibility report sin key, autorización, price snapshot, cleanup act. |
| V-04 | AC-02 | REAL PROVIDER + DETERMINISTIC | Único POST autorizado y task GET/result real; IDs ligados, un result/subtask SUCCEEDED/canal0; preservar recognition/usage y redacción antes de write. SHA/campos concuerdan con respuesta en memoria. | request/execution/envelope/redaction/result hashes y timings, terminal/status/report. |
| V-05 | AC-02/03 | AUTOMATED / REAL REPLAY | Normalizar respuesta real dos veces misma versión: transcript byte-idéntico; quitar solo transcript en copia de test, replay sin red recupera igual. Nuevo normalizer version-ID crea revisión, conserva response/audio/anteriores. | canonical hashes/comparison, no-network stub counters, revision manifests. |
| V-06 | AC-03/04/07 | AUTOMATED | Guard/schema rejects fuente/clock/inspection/hash/version/path/tamper/NaN/floats/null sin motivo; no confianza/idioma defaults. Missing word times conserva ausencias pero no READY. Artefactos ajenos/parciales/current stale no válidos. | casos JSON independientes, exit/status/reasons, hash snapshots. |
| V-07 | AC-04 | AUTOMATED / AV INTEGRATION | AV pequeñas con offset audio positivo/negativo y video PTS no cero/VFR; oracle Fraction externo. Word crossing segment se preserva, no duplicación/clamp; word fuera vídeo => review. Nonmonotonic/duplicate IDs/zero duration/out-ofbounds/gap/priming no resuelto bloquean. | comandos/samples/hashes/reloj esperado vs actual, boundary/failure table. |
| V-08 | AC-05 | HUMAN + DETERMINISTIC | Windows/reference sin ver candidato≥200 palabras; WER≤10% y las cuatro palabras técnicas según procedimiento. Raúl confirma habla suficiente/negaciones/as-spoken, voz completa inicio/final, sin modelo corrector. | reference hash/procedencia, WER S/D/I/N, término/time table, audio+acta. |
| V-09 | AC-04/05/06 | HUMAN + DETERMINISTIC | Escucha dirigida [90,115) y pausas: error original y corrección preservados textualmente, Again como palabra; onset/offset≤150ms cada uno, pausas sin alucinación en núcleo observado. Sin decisiones de retoma/corte. | snippet/hash/offset, referencia incertidumbre/bordes, errors table y revisión. |
| V-10 | AC-04/05/06 | HUMAN + DETERMINISTIC | Ambos try again [130,155) reconocidos, cada borde≤150ms. Controles≥30/onset+offset p95≤200ms/max300ms y drift≤100ms; timestamps completos, source bounds globales. | audio/references/control tables/errores/drift, playback act; no time correction. |
| V-11 | AC-07/08 | AUTOMATED / FAILURE INJECTION | Offline401/403/429/5xx/connection timeout/FAILED/CANCELED/UNKNOWN/file-download failure/multiple-partial/empty/malformed/truncated/limit/IO/diskfull/tooltimeout; no READY/old fallback. Crash antes/tras POST y antes de guardar task: SUBMIT_INTENT impide repetir. Segundo writer BUSY/stale lock preservado. | mocked HTTP count/journal/reasons/recovery snapshots, source before/after. |
| V-12 | AC-02/07 | AUTOMATED + REAL LOCAL | Submit real repetido mismo fingerprint NO_OP sin red/mtime; resume conocido GET solamente; source/revision/config/channel/hints/provider change exige nuevo permiso, no POST implícito. Version-only normalize no call. Failed/ambiguous attempt requiere autorización adicional. | counters/actions/NO_OP hashes/stats, fingerprint differential matrix. |
| V-13 | AC-08/09 | AUTOMATED + REAL ACCOUNTING | Secret-canaries en headers/URLs/echoes/errors/unknown nested fields no persistidos/stdout/Git. Usage real/IDs/prepared duration/pricing exactos. Si tokens, fórmula Decimal independiente; si duration-only, total/min/hora UNKNOWN y conciliación Alibaba con provenance/no atribución falsa de agregado. | sanitized cost.json/price snapshot, scan/rejection table, billing reconciliation/redacted receipt. |
| V-14 | AC-03/06/10 | AUTOMATED / INDEPENDENT CONSUMER | Lector JSON/hashlib/Fraction independiente obtiene texto/lenguaje/word intervals/clock/source/execution opaque; no import vendor/parser/normalizer. Doble de otro provider normalizado igual interfaz. Retiene todos los tokens Again/try again como texto sin etiquetas retake/error/semantic/caption/EDL. | consumer output/core-key audit/double format+unit test, no F004 implementation. |
| V-15 | AC-01/03/10 | DETERMINISTIC / SCOPE | Runtime/source guard y hashes de antecedentes sin cambios; Git exclusion de media/project/response/credentials, scope diff solo autorizado. F003 derivado separado, no skill refresh/newdependencies/F004. | exclusion/diff/versions/hash report y registry de artefactos. |
| V-16 | AC-05/06/09/10 | HUMAN | Raúl revisa mínimo package exacto y audio a1×: fidelidad/términos/palabras/precisión/UNKNOWN/coste/limitaciones. Juicio expreso y aceptación de eN/r1/implementation/source/transcript hash antes de DONE. | owner/date/palabras reales, tabla V/AC y manifest/hash delivery. |

## Cobertura A–P solicitada

| Objetivo | Checks |
| --- | --- |
| A READY F002 → adapter real | V-01–04 |
| B respuesta conservada | V-04 |
| C regeneración sin pago | V-05/12 |
| D source binding | V-01/06/14 |
| E reloj explícito | V-02/07/14 |
| F orden/bounds | V-06/07/10 |
| G español | V-08/16 |
| H vocabulario | V-08 |
| I Again aislado | V-09 |
| J try again válido | V-10 |
| K sin clasificación | V-14/15 |
| L fallo no READY | V-06/11 |
| M idempotencia | V-05/12 |
| N secrets ausentes | V-03/11/13/15 |
| O uso/coste real | V-13/16 |
| P consumer mínimo independiente | V-14 |

## Negativos, oráculos y exclusiones

Suite `python3 -m unittest discover -s tests -v` tras aprobación, **red desactivada**.
Reutilizar solo lectura fixtures sintéticas F002 pertinentes; nuevas muestras
1–3s,≤2MiB cada archivo/≤20MiB agregado, AV/tonos técnicos con versiones/comandos/
hashes en almacenamiento ignorado. Tonos no sustituyen español humano ni precisión
real. Doubles identificados como GENERATED TEST DATA, nunca respuesta de Alibaba
real. Casos necesarios para V-06/07/11/12/13 cubren rutas/unknown/time/discontinuidad,
retries/pago/caps, archivos corruptos y fuente cambiante solo en copias sintéticas.

Oracle independiente calcula Fraction/Decimal/Levenshtein/hash desde entradas
retenidas sin importar funciones de normalización/adapter que está probando.
Response tests incluyen segundos decimales de provider ficticio, ms exactos Qwen,
usage duration-only/tokens válidos/missing/negativos, punctuation null vs vacío,
layout UNKNOWN, text mismatch y speaker no solicitado. No fixtures pagadas extras.

Full real guard/preparación/provider/replay/listening y medición de precisión son
obligatorios; tests sintéticos o exit0 no los sustituyen. No render AV final: no
se edita vídeo. Evidencia audiovisual es WAV local/snippets/onda/tablas y escucha
real, con voice/tempo/inicio/final preservados. No evaluar lip-sync editado,
captions, retake correctness, producción, MOBILE real o infraestructura distribuida.
Estas exclusiones no permiten declarar precisión acústica por un CLI exitoso.

## Resultados, incertidumbre y gate humano

Reglas SDD: required check fallido => FAIL; técnico requerido ausente => BLOCKED;
técnica completa pero juicio/aceptación pendiente => HUMAN_REVIEW_REQUIRED.
PASS global solo todos requeridos completos con evidencia, incluidos humanos.
Unknown/skipped/zero sample nunca es PASS de una medición requerida.

La rama explícita de V-13 puede **pasar honestidad/observabilidad** con coste
numérico UNKNOWN si uso insuficiente, registro de conciliación (consulta/fuente,
fecha, qué no se pudo atribuir) y aceptación del límite por Raúl; no pasa una
medición de coste exacto ni se registra USD0. Si existe uso suficiente, omitir
cálculo sí es fallo. No completar V-13 con solo una intención futura de reconciliar.
Confianza/detected language/backend revision pueden seguir UNKNOWN porque no
son mediciones necesarias; word timing/critical text/ground truth no pueden.

Si palabra/evento/borde de referencia necesita juicio, preparar evidencia y
pregunta concisa, detener dependientes hasta respuesta. No pedir manualmente
metadata/hashes/source offsets determinísticos ni reutilizar la aceptación F001
como si aceptara salida STT. Ningún valor generado es firma de Raúl.

Paquete mínimo `.local/validation/F003/eN/`: report.md con source/transcript hash,
implementation commit/r1 identity, matriz V/AC, word/text/timing review table,
WAV/snippets/ground truth, provider-response/replay hashes, secret scan, coste
total/min/hora o UNKNOWN+conciliación, límite de inferencia/retención y cleanup.
Manifest de hashes excluye su propio archivo; revisión eN se congela antes de
pedir aceptación. Guard/transcript READY es técnico; feature DONE solo tras
aceptación humana de esta evidencia, nunca PRODUCTION_APPROVED/F004.

## Evidencia de ejecución — pendiente

**Verification result:** NOT RUN (not PASS)\
**Delivery revision/run/fecha:** ninguna implementación ni ejecución F003.\
**V-01–V-16 / AC-01–AC-10:** NOT RUN; append comandos/procedimientos, expected/actual,
artefactos/hash, resultado y revisor después de aprobar IMPLEMENT.\
**Owner acceptance of feature:** NOT GRANTED.\
**Actual human evidence / wording / revision:** pendientes.

Auditoría documental de PLAN se registra aparte; no es suite runtime ni VERIFY.
Cambios materiales a tolerancias/transporte/coste/contrato invalidan aprobación,
exigen nueva revisión antes de dependientes. No empezar F004 tras crear el bundle.

## Checkpoint real de IMPLEMENT/VERIFY — preflight-p1 (2026-10-04)

Implementación: `62f659334c060de022ec8cbf9419b3e2f008e58f`; aprobación r1/D002 exacta en74aaa0b/snapshot readonly.
Evidence partial frozen: `.local/validation/F003/preflight-p1/report.md`, manifest
SHA `775d755fdf00f9dd3d417308ad53b9011e7701cd59e3d7df455e13cd436f21d2`. No es entrega final eN ni aceptación de F003.

**Lifecycle: VERIFYING; global verification: BLOCKED.** Suite75 tests PASS con
red bloqueada (socket.create_connection y OpenerDirector.open); runtime
Python3.14.7/FFmpeg+ffprobe9.0.1 existentes. Git diff/scope/exclusion revisados,
sin nuevas dependencias, cambios F001/F002 ni F004.

Auditoría1207 archivos protegidos:0 diferencias bytes/SHA/stat, incluyendo RAW
original/owned source, F001/F002/specs/evidencia y vendor/lock/código antecedente.
Guard real F002 READY. Fuente SHA `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`.
WAV canal1 SHA `4c71d1689fdec2fb419ec6b91cb6ca0317a0b172b594e3b6ab7532cbe00645f3`,
11.174.400 muestras/48kHz/1164/5s, origen0/1. Ledger comparado frame por frame,
continuidad exacta y payload de ambos canales idéntico a deinterleave independiente
del PCM stereo original. Bits/velocidad/muestras conservados; layout/micrófono no inferidos.

Raúl seleccionó «canal 1» y confirmó «Sí, confirmo esa revisión completa» ante
comparación de ambos/canal1 completo1×/voz/inicio/final/pausas. USER-REPORTED,
acta channel-review.json. Falta referencia literal independiente≥200 palabras,
bordes humanos≤50ms y revisión dirigida de extremos/eventos contra source;
plantillas UNKNOWN/paquetes preparados, preguntas enviadas. Key disponible
USER-REPORTED; workspace/API metered Singapore/OSS privado existente/URL UNKNOWN.
Ningún upload, transport GET o POST; **intentos consumidos0/1**.

| Check | Resultado actual | Límite / evidencia |
| --- | --- | --- |
| V-01 | PASS | Fresh real F002 guard and 1207 protected files unchanged in bytes/hash/stat. |
| V-02 | HUMAN_REVIEW_REQUIRED | Native samples/PTS/continuity/hash exact; independent PCM comparison and full1x selected-channel review confirmed. Directed source event/extreme comparison remains part of final reference review. |
| V-03 | BLOCKED | Key available USER-REPORTED; metered API workspace/region eligibility and private existing OSS/URL/cleanup prerequisites UNKNOWN. No transport GET or POST. |
| V-04 | BLOCKED | No real provider request or retained real result; 0/1 submissions. |
| V-05 | BLOCKED | Synthetic byte-identical replay/new revision pass; real retained response absent. |
| V-06 | PASS | Offline schema/guard/tamper/unknown/time/closed core and stale input tests pass; real transcript not created. |
| V-07 | PASS | Retained native AV positive/negative offset, nonzero video PTS/VFR, Fraction oracle, crossing/outside-video and discontinuity negatives. |
| V-08 | BLOCKED | Independent literal reference >=200 words before candidate and real WER/technical terms judgments pending; no candidate-derived reference. |
| V-09 | BLOCKED | Real acoustic bounds <=50ms uncertainty and candidate Again/error/correction/pause evidence unavailable. |
| V-10 | BLOCKED | Real try-again/control/drift evidence unavailable; numerical evaluator tested with synthetic oracle only. |
| V-11 | PASS | Offline auth/rate/server/timeout/status/partial/malformed/caps/tool/IO/crash/locks and conservative paid intent tests pass. |
| V-12 | BLOCKED | Synthetic NO_OP/no-network/mtime, GET-only recovery and new recognition authorization tests pass; real repetition absent. |
| V-13 | BLOCKED | Offline secret-canaries, transport safety and Decimal/UNKNOWN usage tests pass; real usage and billing reconciliation not available. |
| V-14 | PASS | Independent JSON/hashlib/Fraction wire consumer and second-provider decimal double; no vendor fields/editorial classifications in domain. |
| V-15 | PASS | Existing Python3.14.7/FFmpeg9.0.1, 1207-file preservation audit, only authorized text/code changed; local artifacts/media excluded. |
| V-16 | BLOCKED | No complete real evidence package, numerical acoustic verification, accounting or explicit final acceptance. No DONE. |

El evaluator sintético prueba WER/Levenshtein, límites/p95/drift/pausas y no
reescribe el texto. No es precisión del fixture real ni aceptación de términos/
negaciones/Again. Double de provider distinto/consumer prueban el contrato,
no implementan otro servicio. Usage/cost real y conciliación no disponibles:
UNKNOWN, no USD0 ni V-13 completo por intención futura.

AC-01 tiene guard/preparación/preservación demostrados y gate humano dirigido
pendiente; AC-02/03/04/07/08/10 tienen cobertura offline local, pero entrega real
AC-02 y replay real pendientes. AC-05/06/09 pendientes de speech/timing/accounting
real. Ningún AC globalmente aceptado como DONE. La matriz r1 original permanece
intacta y se completará con evidencia real sin rebajar tolerancias.

Owner acceptance F003: NOT GRANTED. No transcript técnico READY real, no DONE,
no PRODUCTION_APPROVED ni autorización F004.

## Checkpoint vigente preflight-p2 (2026-10-04)

Implementación vigente `be2a8233724fe4f94cfaf22aabb39bdcc0ef72fc` (incluye62f6593). Se añade el guard explícito
de comparación dirigida contra audio original antes del POST, ya exigido por r1,
y prueba negativa; ningún criterio/tolerancia ha cambiado. Suite final completa:
**76 tests PASS con red bloqueada**,17,122s. Snapshot anterior p1 intacto.

Snapshot vigente `.local/validation/F003/preflight-p2/`, manifest SHA
`7c1566ecdfc8857321cab1a5ea82d37a6befd11d48f76de077851fc4cf219923`; mismo mapping V/AC y resultado **BLOCKED** de p1.
V-02 sigue HUMAN_REVIEW_REQUIRED para la comparación dirigida original/extremos/
eventos; canal1 y escucha completa1× están confirmados. V-03/04/05/08/09/10/12/13/16
conservan los pendientes reales indicados, no se convierten en PASS por tests.
Scope/Git exclusion de media, proyectos, evidencia y credenciales PASS; fixtures
sintéticas retenidas≤2MiB por archivo y agregado845139bytes≤20MiB.

**STT consumidos0/1; lifecycle VERIFYING; F001/F002 intactos; aceptación F003
NOT GRANTED.** Esperar referencia humana/preflight de cuenta y OSS dentro de r1.

## Continuación verificada — preflight-p3 (2026-10-04)

Acta humana adjunto20aac15c retenida literalmente, junto con respuestas sobre
script no disponible ahora y ubicación de configuración. Evidencia readonly
`.local/validation/F003/preflight-p3/`, manifest SHA
`b2b76fd3b89e341e5b8d725c7ab4b3c803c3a24805570dd09bdaaf6b5d3a24dd`.
Implementación be2a823 intacta; aprobación r1/74aaa0b intacta. P1/P2 sin cambios.

| Parte evaluada | Resultado / evidencia actual |
| --- | --- |
| Juicios humanos presentados | USER_VERIFIED/HUMAN_VERIFIED: listen-and-compare por Raúl; fidelidad/contexto/orden/palabras y fuente confirmados. No autoría manual independiente ficticia. |
| V-02 | PASS: preparación/PCM/ledger/preservación/canal1/full1× previos más confirmación nueva de revisión dirigida del material fuente. Exactitud de word boundaries se evalúa aparte. |
| Referencia pre-candidato V-08 | BLOCKED:5 textos de ventanas siguen null;0 palabras retenidas en esas ventanas; ≥200 requeridas. Recuento del texto exacto que el humano revisó UNKNOWN, no0. Script/salida/identidad no recuperados; no requerir reescritura manual. |
| Bordes V-09/V-10 | BLOCKED:0 de39 controles preparados con intervalos numéricos; mínimo30 y≤50ms exigidos.3 pausas sin bounds. Confirmación humana cualitativa aceptada sin fabricar milisegundos. |
| V-01 / V-15 preservación | PASS fresco: guard F002 READY/WAV válido;1207 archivos protegidos0 diferencias hash/stat. |
| Aprobación/modelo/config/budget local | PASS: snapshot exacto; modelo/región/scope/opciones/límites correctos;0 attempts y0 stale lock. Documentación oficial endpoint/precio reconsultada dentro de tarifas aprobadas. |
| V-03 cuenta/OSS | BLOCKED:eligibilidad API metered Singapore/model-enabled/CodingPlan=false/workspace/OSS privado existente y gestión≤24h UNKNOWN. Key/workspace/URL no cargados en proceso auditado; no prueba de ausencia en máquina. Plantilla externa0600 preparada, sin valores. |
| Suite y checkpoints |76 tests offline PASS retenidos; p2 integridad67 archivos+6 artefactos externos PASS. No código de producto nuevo ni rerun de suite. |
| V-04/05/08/09/10/12/13/16 real | BLOCKED: resultado real/transcript/replay/WER/timing/usage/billing/aceptación final ausentes. Juicio nuevo no los sustituye. |

V-06/07/11/14 conservan los PASS offline p2 y sus límites. No F004/semántica,
no red provider/transport/upload; STT consumidos0/1. Coste total/min/hora real
UNKNOWN, no USD0. Documento reutilizable solicitado por Raúl en
[docs/F003-human-reference.md](../../../docs/F003-human-reference.md), sin
transcripción generada atribuida al revisor ni cambio de aceptación/tolerancias.

**Global BLOCKED; lifecycle VERIFYING; final owner acceptance NOT GRANTED.**
R1 ya autoriza la única ejecución condicionada; aún faltan datos de referencia y
cuenta/transporte, no una nueva autorización genérica. V-16 requiere evidencia
real congelada y aceptación distinta antes de DONE; todavía no corresponde pedirla.

## Checkpoint preflight-p7c — STT real ejecutado; V-08 FAIL real (2026-10-04)

La única solicitud STT r1 fue consumida (POST aceptado, 1/1). Transporte OSS
resuelto (bucket privado `arsd-f003-transit`, WAV canal 1 SHA `4c71d168…`,
URL firmada TTL 2h). Recuperación vía host International autorizado por el owner
(p7c). Transcript real normalizado READY:
`sha256:eff3ff0b7cb3921a8a540bd483da27ccddcf8002799639138c084d118cd4a30e`,
550 palabras, usage 6256 tokens (duration 178 s), coste de lista USD 0.00113104.
Respuesta vendor saneada retenida; canarios de clave/URL firmada AUSENTES.
Estado completo y hallazgo de calidad en plan.md preflight-p7/p7b/p7c y
`.local/validation/F003/preflight-p7/candidate-quality-finding.json`.

| Check | Resultado real | Límite / evidencia |
| --- | --- | --- |
| V-03 | PASS (transporte) | OSS activo; bucket privado Singapore; URL firmada TTL 2h verificada por el parser (1800–7200 s); transport streaming SHA exacto VERIFIED. Elegibilidad cuenta: auth 200 (p5), quota owner-reported. |
| V-04 | PASS | Solicitud/respuesta reales retenidas (request.json, provider-response.json, execution.json). POST aceptado; job SUCCEEDED/subtask SUCCEEDED recuperado por GET intl. |
| V-05 | PASS | Replay real ejecutado: normalize repetido con red bloqueada desde la respuesta retenida → transcript byte-idéntico (SHA `8251cdda…` antes y después). Sin segunda llamada ni cargo. |
| V-08 | **FAIL real** | 3/4 términos técnicos presentes a nivel de frase (monolito, microservicios, eventos×4); **idempotencia NO reconocido** → candidato dice «en potencia» (variante ya predicha UNCERTAIN por el handoff F001). WER independiente no aplicable: la referencia candidate-derived no puede contener un término ausente en el candidato. |
| V-09 | BLOCKED | Sin referencia válida no se ejecuta la evaluación numérica; además los word-timestamps vienen fragmentados (254/550 ≤3 chars), lo que rompe los controles por palabra léxica. Again aislado SÍ presente (~100.7 s). |
| V-10 | BLOCKED | try again ×2 presentes (~137.5/138.6 s); misma limitación de fragmentación/controles que V-09. |
| V-12 | PASS (propiedad de seguridad) | Re-submit con red bloqueada → PAID_ATTEMPT_ALREADY_CONSUMED, cero llamadas de red: nunca un segundo POST. El NO_OP por fingerprint idéntico no aplica tras la revisión p7c (adapter_version cambió); la suite offline cubre esa ruta. |
| V-13 | PARTIAL | Usage/coste real registrados (Decimal, techo r1). Conciliación de facturación real (invoice/billing) PENDIENTE; no USD0 por intención. |
| V-16 | BLOCKED | Sin aceptación humana final; V-08 FAIL real requiere decisión del owner antes de cualquier DONE. |

V-01/02/06/07/11/14/15 conservan sus PASS previos (guard/preservación/suite/
contracto/runtime). Suite 79/79 OK en Python 3.14.7.

**Corrección de creencia previa:** el acta p5 citaba «100% idéntica la respuesta
a lo que digo en el video» (owner-reported). La evidencia real la corrige: el
candidato difiere del habla en al menos un término crítico (idempotencia →
«en potencia»). No se declara PASS sobre esa base.

**Global BLOCKED por V-08 FAIL real; lifecycle VERIFYING; owner acceptance NOT
GRANTED.** Un FAIL real contra r1 no se corrige con código (retrofit prohibido)
ni con otro submit (1/1 consumido; nueva configuración cambiaría el fingerprint
→ NEW_PAID_AUTHORIZATION). Decisión del owner: (i) aceptar el FAIL registrado,
(ii) revisión de criterios vía change-control, o (iii) autorización puntual de
una segunda ejecución con configuración mejorada. Sin DONE, sin F004, sin
PRODUCTION_APPROVED; F001/F002 intactos.
