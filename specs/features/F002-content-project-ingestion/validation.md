# F002 — Contrato de validación y evidencia

**Bundle revision:** r1\
**Requirements:** [requirements.md](requirements.md)\
**Estado/aprobación:** [plan.md](plan.md)

Definido antes de implementación. Ningún check F002 está ejecutado ni PASS.
La evidencia F001 citada es predecesor aceptado, no resultado de código F002.

## Fixtures, entorno y oráculos

Primario real obligatorio: F001-studio-001, C0216.MP4:

- `/Users/raulalmeida/Workspace/editor-agentic-raul/.local/fixtures/F001-studio-001/raw/C0216.MP4`
- **2.873.163.442 bytes**, SHA-256
  `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`.
- Recovery F001: `/Volumes/PortableSSD/videos/raw/C0216.MP4`, lectura/hash equivalente
  verificada en F001 el 2026-10-03; no es una nueva verificación F002 ni dependencia
  operativa del proyecto. Conectar/montar PortableSSD si hace falta recuperar.
- F001 DONE/e5/cierre 7e0bc22; manifest e5 SHA-256
  `accd69f2e0e5c70451b60f1fa6f364837e9fa03ce4bb52141003592ea0027696`.
- [Tabla F001 aceptada](../F001-real-capture-fixture/validation.md) y probe retenido
  en `.local/fixtures/F001-studio-001/evidence/ffprobe.json`: 232,800 s, vídeo stream
  0 H.264 3840×2160, SAR 1/1, 25/1 reportado, time_base 1/25000, matriz −90°;
  audio stream 1 pcm_s16be, 48 kHz/2 canales/time_base 1/48000; stream 2 data rtmd.
  Audio layout UNKNOWN. Vista vertical erguida confirmada. Cadencia se medirá en
  F002; el 25/1 de metadata no demuestra CFR.

Tools propuestos/ya disponibles: Python 3.14.7 stdlib, ffprobe/FFmpeg 9.0.1,
shasum existente como oráculo externo de hashing. Sin instalaciones ni services.
Registrar versión/configuración efectiva, fecha, implementación commit, opciones,
identidad del proyecto/inspección y manifest de cada paquete de evidencia.

El operador ejecutará un probe fresco externo al código de normalización:

```text
ffprobe -v error -show_format -show_streams -of json <owned-source>
shasum -a 256 <original-F001>
shasum -a 256 <owned-source>
ffmpeg -nostdin -hide_banner -v error -xerror -err_detect explode
    -i <owned-source> -map 0:<video-elegido> -map 0:<audio-elegido> -f null -
```

No ejecutar estos ejemplos durante PLAN. Usar argumentos reales sin shell/env
injection; capturar exit code inmediatamente. Timing con ffprobe `-show_frames`
y PTS/duración/time_base, exportado por stream a TSV, comparado también por cálculo
racional independiente de `tools/media_inspection.py`. Hash F001 es expected
fixture identity como parámetro/test, nunca literal de lógica general de ingestión.

## Muestras negativas y de borde — propuestas, aún inexistentes

Crear tras aprobación con FFmpeg existente y stdlib, locales/ignoradas. Vídeo
testsrc con patrón asimétrico/rotulado y tonos generados son muestras técnicas,
no sustitutos de la voz de Raúl ni input primario. Duración **1–3 s**, raster
**160×90/90×160**, máximo **2 MiB por archivo** y **20 MiB en total**. Manifest
incluye comando, versión, propósito, propiedades/procedencia/hashes. No Git media.

| Grupo | Casos mínimos | Necesidad |
| --- | --- | --- |
| S-01 AV simple | Vídeo portrait 90×160 + audio, sin sidecar/rotation, otro nombre con Unicode/espacios y otro codec soportado (p.ej. MPEG-4 + AAC), profile MOBILE declarado. | Probar genericidad/copia/paths, no validar el MOBILE real ni su calidad. |
| S-02 Inventario | Sin audio, audio sin vídeo, múltiples vídeo, múltiples audio, attached picture + vídeo real; índices explícitos e inválidos. | F001 solo tiene un AV; probar resolución de ambigüedad y errores reales. |
| S-03 Display | Sin rotation + portrait y landscape; 0/±90/180 con marcador visual asimétrico; SAR 2/1; tag/matriz conflicto, reflexión/rotación no ortogonal. | Evitar error landscape por raster/rotación y probar signo/SAR/conflictos. Casos imposibles de generar con tool se prueban con JSON controlado del adaptador, identificado como tal. |
| S-04 Tiempo | PTS video no cero, audio antes/después de video, inicio negativo donde el contenedor lo preserve, VFR con deltas conocidos, B-frame DTS≠PTS, audio/sample rate distinto y duration de contenedor ausente. | Probar reloj/offsets sin fixture origin=0/cadencia nominal única. Verificar propiedades efectivas del generado antes de usarlo como oracle. |
| S-05 IO/estado | Archivo vacío/random/truncado y copias temporales corruptibles; input no legible con doble IO si permisos del operador invalidan chmod; source changes/IO fail/timeout/JSON malformado/disk full por doubles. | Ejercitar fallos sin dañar RAW real ni llenar disco. |

Respuestas ffprobe controladas adicionales: null/N/A/0/0, layout ausente, bitrate
ausente, codec/dimensiones/sample rate/canales/timebase ausentes, duration ausente
con y sin fallback válido, PTS faltante/duplicate/nonmonotonic/best-effort only,
version/paths/binding corruptos. No llamarles mediciones de media real. Las pruebas
de VFR/rotación básica/offsets requieren al menos un archivo AV real pequeño;
un mock no sustituye esas integraciones ni la captura F001.

## Checks predefinidos y matriz AC

| Check | AC | Categoría | Procedimiento y resultado exigido | Evidencia retenida |
| --- | --- | --- | --- | --- |
| V-01 | AC-01/02 | AUTOMATED / DETERMINISTIC EVIDENCE | Ingest real F001 hacia F002-studio-001 con expected SHA, profile STUDIO y referencias e5. Preflight/version/espacio, origen/copy SHA y bytes independientes; resultado READY, estructura mínima y source ID correctos, sin literales Sony/hash/ruta en código general. | argv/options/version, hashes origen/copy, tree/bytes, manifest/current/inspection/report. |
| V-02 | AC-01/02 | AUTOMATED / DETERMINISTIC EVIDENCE | Stats bytes/mtime y hashes del RAW F001 antes/después de toda suite. Confirmar owned source inode/copia independiente y SHA igual; validar fixture/notes/specs F001 sin cambios. Decode streams elegidos completo exit 0/error log vacío y conteos frame >0. | source stat/hash before/after, F001 document hash comparison, decode/scan exit/log/counts. |
| V-03 | AC-03 | AUTOMATED / DETERMINISTIC EVIDENCE | Probe fresco externo sobre owned source; comparar todos los campos normalizados con esa salida, además con referencia e5. Para F001 valores listados arriba; layout null NOT_REPORTED, rtmd inventariado/no elegido, codec/PTS/timebases fieles. Renombrar entrada pequeña y variar codec/perfil sin cambiar lógica. | fresh probe + comparison table de paths/expected/actual, synthetic manifests. |
| V-04 | AC-03/04 | DETERMINISTIC + HUMAN EVIDENCE | F001 raster3840×2160 vs display2160×3840/aspect9/16, matriz −90 preservada. Capturar un frame reducido con autorrotación de owned source en 30 s; contrastar con frame e5/revisión previa y revisar upright con Raúl en V-14. No confundir width/height ni inferir física. | normalized display/raw matrix, frame local derivado con hash/argv, comparación de raster/display y acta. |
| V-05 | AC-05 | AUTOMATED / DETERMINISTIC EVIDENCE | Recorrido completo PTS reales F001 stream0/1; cálculo independiente Fraction de origen0, audio offset0, ends1164/5; timebases/clock ID reproducibles. Conteos concuerdan exactamente con scan externo independiente; 5820 frames vídeo es referencia reportada F001, no sustituto de contar. Discrepancia con referencia se investiga y registra antes de PASS. Cadencia de PTS medida explícitamente. | frames.tsv/hash, summary counts/PTS/deltas, calculator independiente y comparison. |
| V-06 | AC-06 | AUTOMATED EVIDENCE | Roundtrip JSON/canonical bytes, null+motivos, ratios/ticks sin pérdida, version/kind desconocidos rechazados, keys/path traversal/escaped symlinks/bad bindings detectados; extension namespace inocuo no altera readiness. Independent reader no importa normalizador/validador interno para assertions. | unittest output/cases, JSON cases/versioning/serialization/hashes. |
| V-07 | AC-02/07 | AUTOMATED EVIDENCE | Segundo ingest real idéntico NO_OP y todos los hashes/mtime de proyecto sin cambios; alias de mismo source pequeña no altera provenance; mismo ID con bytes/contexto distinto rechaza y archivos previos intactos. Hash esperado erróneo en muestra falla antes de READY. | snapshots antes/después/exit/outcome/hash; conflicto/noop reports. |
| V-08 | AC-08 | AUTOMATED / DETERMINISTIC EVIDENCE | inspect explícito F001 crea revisión nueva; normalizado byte-idéntico mismas versiones/opciones, manifest/RAW/previa intactos. Solo sobre proyecto sintético: retirar derivados y origen externo sin tocar authoritative F001, verificar no READY, regenerar owned copy y operar tras mover raíz del proyecto; paths relativos válidos. | old/new inspection hashes, guard/error/recovery logs, relocation/provenance check. |
| V-09 | AC-09 | AUTOMATED EVIDENCE | Missing/empty/unreadable/random/truncated inputs, unavailable ffprobe, nonzero probe/decode, malformed JSON, timeout/output cap, IO/copy/rename/disk-full doubles. No resultado READY, fuente sin cambios y diagnóstico concreto/exit conforme al contrato. | tabla casos/codes/snapshots/staging; test outputs y failures. |
| V-10 | AC-04/05 | AUTOMATED / DETERMINISTIC EVIDENCE | S-03/S-04 reales + doubles: verificar fórmula SAR/rotation, los cuatro giros, signo con patrón visual; missing/conflict/no orthogonal; tiempos no cero/audio lead lag/negative, VFR/B-frames, extent fallback válido y unknown. Comparar racionales exactos con timeline generada/fresh scan externo. | fixture commands/hash, display frames, PTS oracle/case table, required blocked/review results. |
| V-11 | AC-03/09 | AUTOMATED EVIDENCE | S-02: no vídeo/audio INVALID, varios requieren revisión, selección explícita resuelve, wrong index INVALID, attached pic excluido. Optional metadata null no bloquea, necesaria ausente bloquea. Nunca inferir voice origin/layout/language. | inventory/selection/unknown reasons cases+exit, invalid/review/ready result table. |
| V-12 | AC-01/06/10 | AUTOMATED EVIDENCE | Consumer smoke independiente con JSON/pathlib/Fraction/hashlib sobre F001 resultante obtiene solo contrato: RAW relative/hash, streams/properties, clock/offset/intervals/display/readiness. Rechaza tampered revision/source/version/path. Usa guard vigente y prueba rehash requerido; ningún STT/provider/extracción/transcript. git check-ignore/list tracked: RAW/proyectos/media excluidos. | consumer result/case table, exclusion report, entrega/JSON hashes. |
| V-13 | AC-09 | AUTOMATED EVIDENCE | Sobre proyectos sintéticos: change source durante copy/inspect y owned RAW después de READY; fallo/inyección/kill después de copiar, antes del commit y después de pointer BLOCKED. Segundo writer BUSY, stale lock no eliminado por TTL; recuperación explícita conserva origen y revisiones. Guard impide consumo de READY stale, reinspección fallida no restaura old READY. | failure-point matrix, guard/integrity report, before/after source/manifests, locks/staging/recovery logs. |
| V-14 | AC-04/10 | HUMAN EVIDENCE | Raúl revisa reporte mínimo/revisión/hash y frame V-04 (vídeo visualizado localmente si frame/vista conflictivos), entiende original vs copy, raster/display y origen/offset; confirma vista F001 correctamente presentada y límites/diagnósticos. Aceptación expresa del paquete exacto tras todos los checks. No reabrir contenido/setup/retomas F001. | acta owner/date/revision y aceptación literal; manifesto hashes y matriz final V/AC. |

La suite usa `python3 -m unittest discover -s tests` tras aprobación. Ejecutar
checks realfixture aparte con argv/run retenidos: unittest de muestras no satisface
V-01–V-05/V-07/V-08/V-12 reales. Corregir software hasta cumplir r1; si falla la
especificación, registrar mismatch/PLAN_REVISION_REQUIRED en vez de reducir criterios.

## Cobertura A–K solicitada

| Objetivo | Checks |
| --- | --- |
| A ingest realfixture | V-01 |
| B preservación de identidad | V-01/02/07 |
| C SHA coincide F001 | V-01/02 |
| D propiedades deterministas | V-03/11 |
| E raster/display | V-04/10/14 |
| F source-time | V-05/10/12 |
| G repetición/idempotencia | V-07 |
| H authoritative source sin modificación | V-02/07/09/13 |
| I regeneración derivada | V-08 |
| J fallos no falso válido | V-06/09/11/12/13 |
| K frontera F003 sin implementarla | V-12/14 |

## Tolerancias y límites definidos previamente

Bytes/SHA/canonical JSON/PTS/ratios/offsets/IDs y binding: coincidencia **exacta**.
Duración decimal F001/probe: comparación racional con precisión declarada de
metadata (seis decimales => ±1 microsegundo para esa comparación textual); cálculo
de PTS/time_base/extents exacto. Discrepancias container/stream-vs-scan aplican
la frontera de requirements.md (máximo un frame observado/una muestra audio),
con NEEDS_REVIEW si excede; no una tolerancia universal para edición o STT.
Matrices ortogonales: coeficientes enteros fijos exactamente correspondientes,
sin redondear ángulo arbitrario. SAR/aspect derivados racionales exactos.

Frames V-04/V-10 solo evidencia de orientación/sentido de giro, reducidos localmente
y sin evaluación de producción/crop/safe zone. Muestra F001 a 30 s ± un frame
presentado es suficiente para reconocer vista de la misma escena; no exactitud
de corte prometida. Audio listening nueva no exigida: no audio transformado y
copy SHA idéntico preserva la revisión completa VLC1× aceptada en F001. Si cambia
contenido o aparece conflicto no cubierto por identidad, detener y resolver.

## Cobertura y exclusiones justificadas

| Categoría | Cobertura / rationale |
| --- | --- |
| Tests/inspección automática | V-01–13; integración real independiente, contratos, IO/transacción y cases negativos; no solo asserts de constantes. |
| Revisión humana | V-04/14, Raúl sobre geometría y paquete exacto; no exigir repetir la entrevista F001. |
| Negativos/bordes/failure injection | S-01–05 + V-06–13; únicamente proyectos/copias sintéticos para modificaciones intencionales. |
| Audiovisual | Full decode y timestamps, frame upright/display, revisión F001 válida retained + inspección visual actual. No render export: no vídeo transformado de entrega. |
| F003/producción/provider | No STT, upload, modelo, EDL, retakes, composición, captions, audio processing, lipsync de entrega, performance/render QA; inexistentes/fuera de F002. |
| Mobile real / quality / plataformas | Compatibilidad de contrato probada con sample sintético sin Sony, no representatividad ni producción MOBILE; futura feature. |
| Infrastructure / security services | No CI/CD, cloud, DB/API, network/multiwriter distribuido ni pruebas destructive de disco; no necesidad aprobada. |

Una categoría excluida no reemplaza required check. UNKNOWN/NOT RUN/skip/zero
frames nunca PASS. Todas las pruebas negativas requieren el comportamiento de
rechazo/revisión esperado, no «el programa falló» sin código/evidencia.

## Reglas de decisión SDD

FAIL si cualquier required check ejecutado falla; luego BLOCKED por cualquier
check técnico obligatorio indisponible; luego HUMAN_REVIEW_REQUIRED si técnica
completa y juicio/aceptación pendiente; PASS global solo toda prueba/humano cumplida.
Retener motivos individuales. Input READY no es resultado PASS de la feature.
La aceptación final exige PLAN válido, entrega r1, evidencia recuperable,
normativa intacta, todos AC/checks satisfechos y palabras reales de Raúl.

## Evidencia de ejecución — pendiente de aprobación/implementación

**Verification result:** NOT RUN (not PASS)\
**Delivery revision / run / date:** ninguno; no código/proyecto F002 creado.\
**Runtime compatibility:** NOT YET VALIDATED; solo disponibilidad/versiones vistas.\
**Estado:** exclusivamente en plan.md.

| Checks / AC | Ejecución y resultado |
| --- | --- |
| V-01–V-14 / AC-01–AC-10 | NOT RUN; append después de implementación aprobada: comando/procedimiento, expected/actual, artifact path/hash, resultado/revisor. |

## Gate humano y aceptación final

**Review package:** futuro report.md de inspección + frame local + tabla V/AC,
Git revision y manifest/hash de artefactos/source/revisión.\
**Revisor técnico y owner:** Raúl Almeida.\
**Actual human evidence:** pendiente; nadie revisó entrega F002 inexistente.\
**Owner acceptance of feature:** NOT GRANTED.\
**Actual acceptance wording/date/revision:** pendiente.

Antes de DONE presentar scope/límites y evidencia, luego registrar aceptación de
esa revisión específica. No pedir aprobación de feature por anticipado. Conservar
revisiones anteriores y sus hash; cambios materiales requieren PLAN nuevo, cambios
de output invalidan QA/aceptación afectadas. Ni r1 ni F002 DONE autoriza F003 o
PRODUCTION_APPROVED.

## Ejecución e1 — acta administrativa actual (2026-10-04)

Los campos NOT RUN y gate futuro anteriores pertenecen a r1 presentado. Este
registro los sustituye administrativamente sin cambiar contrato/criterios/tolerancias.

**Verification result:** HUMAN_REVIEW_REQUIRED.
**Approved bundle:** r1 / ae36327768a4186009a92619ef8e4b1bf379d8a8; D001 aceptada.
**Implementation commit:** `3e53205bcfd55570968f891a5bd972d5fe6bc621`. Python 3.14.7 stdlib y FFmpeg/ffprobe 9.0.1.
**Evidencia:** `.local/validation/F002/e1/`, fecha UTC 2026-10-04T05:11:54.432452+00:00.
**Manifest SHA-256:** `3dd9201577a3e23cae128760a6ad217e48e24bb46d1e0acaf82d1fc93f71d35c` (`evidence-e1.sha256`, 394 artefactos/referencias).
**Revisión real final:** `inspections/d48b0e46-af7e-405e-a5ee-0d703d53bcb0/inspection.json`; SHA-256 `d08658c3542e2a7d10b1093a0de5e464752fd6cbca14588cc816b323478b428f`.
**Manifest source SHA-256:** `7350428f4c3b7f5ffbf685c4d39a7fad52aae527a4ae08070189442c6aefa3ce`.
**Input state:** READY; no equivale a DONE.

| Check | Resultado | Evidencia / alcance |
| --- | --- | --- |
| V-01 | PASS | Copia real READY; identidad/refs e5, runtime y preflight. `ingest-execution.json, preflight-capacity.json, consumer-result.json` |
| V-02 | PASS | Bytes/mtime/hash originales y 64 archivos protegidos sin cambios; 6 frames e5 idénticos, inode independiente; decode completo sin errores. `baseline.json, preservation-comparison.json, F001-accepted-frame-preservation.json, external-decode-execution.json` |
| V-03 | PASS | Metadata normalizada/UNKNOWN comparada campo a campo con probe externo y e5; data 2 rtmd en probe, no seleccionado. `metadata-comparison.json, environment.json, synthetic-inventory.json` |
| V-04 | HUMAN_REVIEW_REQUIRED | Geometría técnica/frame byte-idéntico PASS; confirmación actual de vista por Raúl pendiente en V-14. `frame-comparison.json, frame-030s.png, metadata-comparison.json` |
| V-05 | PASS | Recorridos completos independientes y TSV idéntico; vídeo 5820/audio 11155, origin/audio offset 0, ends1164/5, clock exacto. `timing-comparison.json, external-frames.tsv` |
| V-06 | PASS | Versiones/keys/UNKNOWN/ratios/canonical JSON/paths/bindings/extensiones y guard. `unittest.log, test-case-mapping.json` |
| V-07 | PASS | Segundo ingest con versión final NO_OP; todos hashes/tamaños/mtime intactos; alias/conflictos/hash erróneo en suite. `repeat-before.json, repeat-after.json, repeat-comparison.json, unittest.log` |
| V-08 | PASS | Reinspección nueva con mismas opciones/versiones: JSON byte-idéntico; fuente/manifest/previas intactos; pérdida/move/origen ausente en sintético. `regeneration-comparison.json, unittest.log` |
| V-09 | PASS | Entradas inválidas/fallos herramientas/JSON/timeout/cap/IO/rename/disco; códigos y preservación de fuentes según contrato. `failure-matrix.json, negative/, unittest.log` |
| V-10 | PASS | Giros reales contrastados con píxeles/SAR; VFR/B-frames/audio lead/lag/inicio no cero; negatives/fallback con doubles identificados. `environment.json, synthetic-inventory.json, test-case-mapping.json, unittest.log` |
| V-11 | PASS | Sin AV/múltiples/selección explícita/attached pic y metadata desconocida requerida/opcional. `test-case-mapping.json, unittest.log` |
| V-12 | PASS | Consumidor stdlib independiente tras guard fresco; binding/hashes/paths, cero providers/F003; proyectos/RAW/evidencia ignorados. `consumer-result.json, guard-execution.json, exclusion-result.json, implementation-scope-check.json` |
| V-13 | PASS | Mutaciones/interrupción SIGKILL real/lock BUSY sin TTL/recuperación explícita/guard frente a fuente alterada o revisión incompleta. `failure-matrix.json, negative/, unittest.log` |
| V-14 | HUMAN_REVIEW_REQUIRED | Paquete exacto presentado; confirmación de vista/límites y aceptación final pendiente. `review.md; acta futura fuera del e1 congelado` |

| AC | Resultado |
| --- | --- |
| AC-01 | PASS |
| AC-02 | PASS |
| AC-03 | PASS |
| AC-04 | HUMAN_REVIEW_REQUIRED |
| AC-05 | PASS |
| AC-06 | PASS |
| AC-07 | PASS |
| AC-08 | PASS |
| AC-09 | PASS |
| AC-10 | HUMAN_REVIEW_REQUIRED |

43 tests PASS, 15 casos de fallo con snapshots/logs, geometría/timing reales
comparados independientemente, NO_OP y regeneración byte-idéntica probados.
RAW F001: 2.873.163.442 bytes, mtime_ns 1791032763000000000 y SHA-256
68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc intactos.
64 archivos protegidos y 6 frames aceptados conservan sus hashes. No nueva
verificación del backup externo; la referencia sigue siendo la aceptada en F001.

Correcciones retenidas transparentemente: copia detenida cuando source cambia
después de cada bloque (regresión pasa); muestra temporal final 1–3 s en vez de
span anterior 4 s; oracle independiente ajustado para comparar selection.basis
y codec tag rtmd sin inventar codec name ausente. Historial no contado como PASS
y ninguna normativa reducida. Ver review.md/environment.json/failure-matrix.json.

**Review package:** `.local/validation/F002/e1/review.md` y frame-030s.png;
manifest de identidad arriba. **Owner acceptance:** NOT GRANTED.
**Human judgment:** V-04/V-14 pendientes; agente observó frame erguido y su hash
es idéntico al frame aceptado e5, sin sustituir la confirmación actual de Raúl.
No reabrir setup/contenido/voz F001 ni usar MOBILE real. Sin F003/dependencias/
STT/edición/retomas/composición/render/PRODUCTION_APPROVED. Estado en plan.md.

## Aceptación e1 y cierre — acta final (2026-10-04)

**Verification result:** PASS. **Owner acceptance:** GRANTED, Raúl Almeida,
mensaje directo en este chat; registro UTC 2026-10-04T05:58:57.210474+00:00.
La evidencia e1 pendiente anterior es el snapshot presentado, sin cambios;
este registro completa el juicio/aceptación, sin alterar r1 ni tolerancias.

**Accepted bundle:** r1 `ae36327768a4186009a92619ef8e4b1bf379d8a8` / D001 aceptada.
**Accepted implementation:** `3e53205bcfd55570968f891a5bd972d5fe6bc621`.
**Accepted evidence:** e1; manifest SHA-256
`3dd9201577a3e23cae128760a6ad217e48e24bb46d1e0acaf82d1fc93f71d35c` (394 artefactos/referencias).
**Accepted inspection SHA-256:** `d08658c3542e2a7d10b1093a0de5e464752fd6cbca14588cc816b323478b428f`.
**Accepted RAW SHA-256:** `68addbf384db8927b05eea36873bc46dc3409ccad998427ba9c43d19ae427bcc`.
**Human act / final matrix:** `.local/validation/F002/closure-e1/acceptance-e1.md`
y `final-results.json`; mensaje literal `owner-message.txt`, SHA-256 `f1962760af832eba101d2e91b5ad20b922bbff6fa1a653d31893bde1d3af886d`.
**Closure manifest SHA-256:** `f62462818dca0fba677d1d7aeef5c02927d6a3398e2e7a6d7c6626072e007367` (`closure-e1.sha256`).

### Palabras reales de Raúl

> Confirmo que en frame-030s.png la vista está erguida y correctamente
> presentada en vertical.
>
> Entiendo y acepto la distinción entre raster almacenado 3840×2160 y
> presentación vertical derivada 2160×3840 mediante la transformación de
> orientación, así como que el reloj source-presentation-v1 comienza en el
> primer PTS presentado del vídeo y no representa fecha ni timecode de cámara.
>
> Confirmo la vista erguida/vertical y acepto F002, evidencia e1 identificada
> en validation.md, conforme al bundle r1 ae36327 y la implementación 3e53205.
> Acepto sus límites y autorizo HUMAN_REVIEW → DONE.
>
> No autorizo F003 ni declaro un vídeo PRODUCTION_APPROVED.

### Matriz final V / AC

| Checks | Resultado final | Evidencia |
| --- | --- | --- |
| V-01/02/03/05/06/07/08/09/10/11/12/13 | PASS | Técnica e1 congelada; matriz por check en acta e1 anterior. |
| V-04 | PASS | Raúl confirma frame-030s.png erguido/vertical y entiende raster/display/transformation; acta literal arriba. |
| V-14 | PASS | Raúl acepta e1/r1/implementación exactos, reloj y límites, y autoriza cierre; acta literal arriba. |
| AC-01–AC-10 | PASS | Matriz técnica e1 + V-04/V-14 humanos; final-results.json identifica cada criterio. |

Comprobación de cierre: 394 hashes e1 intactos; código idéntico a 3e53205;
guard fresco READY. Se mantienen 43 tests y 15 escenarios de fallo PASS,
NO_OP/regeneración y preservación de F001; no nueva ejecución de inspección/media.
**Lifecycle:** HUMAN_REVIEW → DONE, registrado en plan.md. Ningún check pendiente.
No se modifica el paquete e1 congelado, el r1 aprobado, RAW ni F001.
Los límites aceptados persisten; F003 y PRODUCTION_APPROVED no autorizados.
