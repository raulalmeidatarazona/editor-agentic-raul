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
