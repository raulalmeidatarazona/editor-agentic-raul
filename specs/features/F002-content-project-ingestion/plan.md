# F002 — Content Project Ingestion and Media Inspection

**Documento:** plan — CÓMO entregar la frontera de ingestión\
**Bundle revision:** r1\
**Lifecycle state:** HUMAN_REVIEW\
**Owner:** Raúl Almeida\
**Scope:** [requirements.md](requirements.md)\
**Proof contract:** [validation.md](validation.md)\
**Decisión propuesta incluida:** [D001](../../decisions/D001-local-source-contract.md)

## Autorización y predecesor

Raúl confirmó F001 DONE/e5/cierre 7e0bc22 y autorizó **PLAN ONLY** para F002 en
el adjunto 09eb3b1a-f082-4d19-b2fb-5bdcac283c62/Pasted text.txt. Este permiso
autoriza estos documentos y la inspección de antecedentes; no implementación.
F001 r1, identidad, actas y limitaciones se conservan sin modificaciones.

Se leyeron completamente los cuatro specs raíz, AGENTS.md, protocolo, bundle
F001 y validación final relevante, aceptación e5, probe retenido, decisiones y
templates. No hay ADR aceptado previo. Las referencias históricas en raíces
que reservan F002 se superan solo para PLAN por este mensaje humano nuevo.
No se usan skills de vídeo: no hay autoría, edición ni render en esta feature.

## Enfoque arquitectónico y flujo

Propuesta D001: código pequeño local con Python stdlib, copia byte-exacta y JSON
v1 propios. FFprobe/FFmpeg son herramientas detrás del inspector, no contrato
dominio. Sin agente/modelo/Hermes de producción en runtime; no necesitamos probar
provider access para este trabajo determinista.

```text
Ruta RAW + ID + contexto declarado + opciones
  → preflight/lock/hash/espacio
  → copia staging + hash independiente + origen estable
  → manifest source autoritativo
  → probe/inventario/selección
  → decode completo + recorrido PTS + normalización
  → contrato/reporte/artefactos con hashes
  → publicación local atómica, resultado READY o no listo

Reinspección: owned RAW + manifest + opciones retenidas → nueva revisión
Consumo: guard de integridad/revisión → contrato mínimo, sin STT
```

Separación mínima: entry CLI/copia/publicación, inspección de media y contrato/
guard. No framework/package scaffold. Contexto capture se declara separado;
marca, safe zones y significado no son responsabilidad del inspector. No editar,
remuxear, extraer audio ni crear proxies para resolver límites del RAW.

## Interfaz propuesta — solo después de aprobar

```text
python3 tools/ingest.py ingest --source <ruta-local> --project-id <id>
    [--projects-root <directorio-local>] [--profile STUDIO|MOBILE|UNKNOWN]
    [--expected-sha256 <hash>] [--fixture-id <id>] [--feature-revision <revision>]
    [--recovery-location <ruta>] [--evidence-manifest-sha256 <hash>]
    [--limitation <texto>] [--video-stream <indice>] [--audio-stream <indice>]
python3 tools/ingest.py inspect --project <raiz>
    [--video-stream <indice>] [--audio-stream <indice>]
    [--display-rotation <0|-90|90|180> --override-reason <texto>
     --override-reviewer <nombre>]
python3 tools/ingest.py verify --project <raiz>
```

ingest/inspect admiten `--command-timeout-seconds <1..3600>` (default 600);
los caps de evidencia/logs permanecen los definidos abajo. `--display-rotation`
usa grados positivos antihorarios; no es el signo de un constructor de matriz.

`projects-root` por defecto `.local/projects` del repositorio resuelto, no del
CWD accidental. Source y project reciben rutas absolutas o relativas resueltas
por operador; nombres/espacios/Unicode se manejan como argumentos, sin shell.
Primer ingest con override de display no necesario: si hay revisión pendiente,
resolver con inspect tras juicio humano. inspect sin opciones de selección/override
reutiliza opciones de última revisión completa, o selección única si no existe;
opción explícita las sustituye y crea revisión. No cambiar silenciosamente pista.

Stdout = resultado JSON pequeño `{operation, outcome, project_id, status,
reasons, project_path, inspection_path}`; strings/paths nullable. outcome
`CREATED/NO_OP/REINSPECTED/VERIFIED/REJECTED`. Exit 0 solo resultado READY/no-op
verificado; 2 NEEDS_REVIEW, 3 BLOCKED, 4 INVALID. Mensajes de ayuda no implican
validación. Verify es guard de lectura: no cambia contenido de proyecto; cuando
detecta un snapshot READY stale, devuelve BLOCKED/INVALID y explica diferencia.
El consumidor usa ese resultado fresco; no hay daemon que garantice el filesystem.
Reingest que encuentre derivados dañados no es NO_OP: devuelve no listo y señala
inspect para regenerar; solo esa operación explícita publica otra revisión.

## Superficie exacta de IMPLEMENT propuesta

No crear ninguno de estos archivos/carpeta de código/media durante PLAN.

| Archivo / artefacto | Acción después de aprobación | Propósito |
| --- | --- | --- |
| `tools/ingest.py` | Crear | CLI, source copy/hash, manifest, locks, transacción, revisión, reporte y exit codes. AC-01/02/07–10. |
| `tools/media_inspection.py` | Crear | Adaptador local ffprobe/FFmpeg, inventario/selección, scan/display/tiempo. AC-03–05/09. |
| `tools/content_contract.py` | Crear | Serialización/tipos v1, bindings y guard; sin modelo/STT. AC-06/10. |
| `tests/test_ingestion.py` | Crear | Integración filesystem/CLI, idempotencia, fallos y recuperación no destructiva. |
| `tests/test_media_inspection.py` | Crear | Casos reales pequeños de stream/display/tiempo + respuestas de herramienta controladas. |
| `tests/test_content_contract.py` | Crear | Versionado/paths/hashes/unknowns y consumidor mínimo independiente del normalizador. |
| `tests/support_media.py` | Crear | Generación local reproducible de fixtures sintéticos pequeños y dobles de fallo, sin F001 mutation. |
| `docs/F002-ingestion.md` | Crear | Procedimiento operador, estados, comandos, recuperación y frontera JSON. |
| Este bundle | Añadir acta/progreso/evidencia | Preservar normativa r1 presentada antes de aprobación. |
| D001 | Registrar aceptación real si recibida | Propuesta no se convierte en aceptada por generar código. |
| `tech-stack.md` §11/§13 | Modificar solo tras aceptación explícita D001 | Registrar resolución limitada de lenguaje/contrato, con texto propuesto abajo; no nueva dirección de renderer/STT. |
| `AGENTS.md`, `roadmap.md`, `specs/README.md`, `README.md` | Actualizar solo registros de autorización/progreso/uso | Alinear gate F002 tras aprobación y entrega; no cambiar políticas ni normativa F001. |
| `.local/projects/F002-studio-001/` | Crear | Proyecto resultante de copiar RAW F001; fuente + revisiones requeridas, no directorios futuros. |
| `.local/fixtures/F002-synthetic-*/` | Crear después de aprobar | Casos AV sintéticos de validation.md, ignorados, con comandos/hashes. |
| `.local/validation/F002/<run-id>/` | Crear | Evidencia real/negativa, hashes, frames mínimos/reporte/revisión humana. |
| `.local/projects/.staging/`, `.locks/`, `.failures/` | Crear según necesidad | Trabajo parcial diagnosticable; no servicio ni eliminación automática. |
| RAW/recovery/artefactos F001, skills, lock, Constitution/Mission | Solo leer | Predecesor inmutable; ninguna modificación prevista. |

La actualización arquitectónica propuesta añade a tech-stack §11, con enlace a
D001, exactamente esta resolución de alcance:

> F002 uses Python 3.14.7 with the standard library and the existing FFmpeg/ffprobe
> 9.0.1 tools for local ingestion and inspection. Its versioned JSON source and
> inspection contracts, owned byte-identical source copy, and source-presentation-v1
> clock are defined by the accepted F002 bundle and D001. This does not select a
> universal pipeline language, STT provider, normalization policy or renderer API.

En §13, «programming language for glue code» queda como «programming language for
later glue code beyond F002». Esta es la única resolución normativa raíz propuesta;
no se modifica ahora ni se considera adoptada sin aprobación explícita D001.

## Dependencias, versiones y coste

Inspección de PLAN encontró `/opt/homebrew/bin/python3` **3.14.7** y
`/opt/homebrew/bin/ffmpeg`, `ffprobe` **9.0.1**. Es disponibilidad/versión, no
prueba de compatibilidad de código aún inexistente. Implementar/probar con esas
versiones sin instalar/actualizar; registrar versión y configuración efectiva.
Racional: `fractions.Fraction`; SHA: `hashlib`; JSON/files/subprocess/unittest
stdlib. No pip/npm/package manifest. D001 explica por qué no Shell/Node/Go.

Probe documental: [ffprobe](https://ffmpeg.org/ffprobe.html) ofrece inventario,
JSON y recorrido de frames; [FFmpeg](https://ffmpeg.org/ffmpeg.html) ofrece selección
de streams/decodificación. Adaptador y tests deberán probar convenciones reales
de la versión instalada, especialmente signo de rotación y timestamps.

Presupuesto local: una copia RAW adicional de 2.873.163.442 bytes y hasta **512 MiB**
de evidencia por inspección; preflight exige ambos disponibles en destino para
F001, y `source.bytes + 512 MiB` en general. Copy/hash/scan streaming, sin cargar
RAW o todos los frames en RAM. Cap agregado de evidencia 512 MiB por inspección,
probe JSON 16 MiB y logs stderr 2 MiB por comando; TSV streaming dentro del cap
agregado, resúmenes de delta sin almacenar todos los frames en RAM.
Alcanzar límite => BLOCKED/LIMIT_EXCEEDED, nunca PASS silencioso. Execution anota
truncamiento. Timeouts por proceso 600 s, configurable explícitamente 1–3600 s;
sin retry automático. Hash/copy verifican IO/error/cambio y tiempo de ejecución,
sin benchmarks de producción inventados. Una sola operación por ID en este
filesystem local; no validar filesystems remotos ni power-loss recovery universal.

No auth, cloud, provider, modelo, audio upload, servicio nuevo ni gasto recurrente.
El único coste incremental esperado es espacio/IO/CPU local. Source-only copia
no es backup independiente frente a fallo del disco del Mac.

## Errores, riesgos y recuperación

Aplicar estados/códigos de requirements.md, sin fallback READY. Locks/staging
solo afectan proyectos F002, no F001. Stale lock: reportar PID/run/contexto;
operador confirma ausencia del proceso y conserva staging antes de retirar su
lock concreto. No borrar por TTL ni autolimpiar evidencia. Fallo de copy conserva
original y parcial identificado; repetición produce intento nuevo. Fallo de inspect
conserva fuente/manifest/revisiones previas, puntero no listo; nuevo inspect revalida.

Para recuperación de owned RAW: detener, localizar copia hash-equivalente y
presentar identidad; el procedimiento manual documentado no reemplaza bytes sin
decisión explícita. No cambiar expected hash. Tests de corrupción solo sobre
copias sintéticas/temporales identificadas, nunca realfixture/recovery.

Riesgos pendientes de prueba: demuxer edit lists/PTS faltante, convenciones de
matriz/tag, límites de IO/espacio, cambio externo concurrente, precisión de duración
de último frame. R1 define cuándo detener/revisar en vez de inventar. Si F001 no
puede cumplir este contrato tal como está definido, registrar mismatch y volver
a PLAN si cambia normativa; no relajar tiempos/display para aceptar el resultado.

## Observabilidad y evidencia

Cada intento: source/project/revision IDs, versiones, argv sin entorno/tokens,
UTC start/end, hashes/stats antes/después, códigos/timeout, acciones/resultado,
evidencia local y límites. Logs no contienen env ni auth. Probe/paths absolutos
locales no se suben como material público por defecto. Reporte pequeño para
Raúl: fuente/hash, selección, raster/display, reloj/offsets, readiness/motivos,
limitaciones, recuperación y tabla V/AC; no solicitar inspección de código.

Hash manifest de paquete de evidencia (sin incluirse a sí mismo), Git commit de
implementación y revisión de inspección enlazados en validation.md. F001 e5 ya
aceptada es comparación/procedencia, no sustituto de validar F002 real.

## Pasos incrementales — pendientes, no ejecutar durante PLAN

- [x] Registrar aprobación real de r1 + D001, commit/hashes previos y snapshot; solo entonces PLAN_APPROVED. Actualizar resolución raíz limitada.
- [x] Implementar tipos v1/serialización y guard con casos inválidos independientes. AC-06/10, V-06/12.
- [x] Implementar copy/hash/provenance/lock/atomic publication y CLI sin sobrescritura. AC-01/02/07/09, V-01/02/07/09/13.
- [x] Implementar inspector/selección/rotación/reloj/scan/decode y límites. AC-03–05/09, V-03–05/10/11.
- [x] Crear solo muestras sintéticas necesarias y ejecutar negativos/failure injection definidos; corregir defectos dentro de r1, no redefinir criterios.
- [ ] Ingerir RAW F001 real, inspeccionar independientemente y ejecutar V-01–V-14, incluyendo regeneración/guard/consumer. Conservar fuente/evidencia.
- [ ] Presentar reporte/frames y revisar display con Raúl; añadir resultados/limitaciones, esperar aceptación exacta de entrega antes de DONE. Sin F003.

## Readiness del PLAN y presentación

R1 define alcance, contratos, campos desconocidos, copia/identidad, raster/display,
PTS y offsets, fallos/transacciones, idempotencia/regeneración, consumer boundary,
superficie de implementación y prueba real/negativa/humana antes de código.
Predecesor satisfecho por F001 DONE; runtime/espacio/lectura se revalidarán en
IMPLEMENT. Preguntas bloqueantes: ninguna. Decisiones nuevas: propuestas D001/r1
para aceptación, no hechos aceptados. Todos los checks F002 están NOT RUN.

El commit de presentación y hashes pre-aprobación se entregan junto a estos
archivos. Las actualizaciones de acta/estado no deben hash-earse a sí mismas ni
cambiar normativa; Git preserva exactamente la versión presentada. Esta sesión
se detiene en PLAN_READY.

Auditoría documental previa a presentación: 10 AC y 14 checks con mapping
bidireccional completo; enlaces locales de los cuatro documentos resueltos y
fences Markdown cerrados. Esto prueba coherencia del PLAN, no comportamiento
de ingestión ni PASS de F002. La comprobación de integridad de antecedentes
comparó 45 archivos raíz/F001/lock/evidencia: todos con SHA-256 idéntico antes y
después de PLAN. Bytes/mtime del RAW sin cambio; Git no muestra cambios en archivos
preexistentes. No se ejecuta suite, decode ni probe nuevo del RAW durante PLAN.

## Aprobación del bundle presentado

**Approval:** NOT GRANTED\
**Approver / fecha / palabras reales:** pendientes; no hay decisión recibida.\
**Approved revision / identidad:** pendiente de aprobación; usar commit presentado
o hashes pre-aprobación, no bytes con acta posterior.\
**Recoverable reviewed bundle:** commit de presentación en Git local `main`.\
**Alcance actualmente autorizado:** solo PLAN F002; F001 permanece DONE.

Frase propuesta para Raúl, todavía no firmada:

> Apruebo F002, bundle r1 presentado en el commit indicado, compuesto por
> requirements.md, plan.md y validation.md. Acepto expresamente D001 en ese mismo
> commit y la resolución limitada de tech-stack descrita en plan.md. Autorizo
> PLAN_READY → PLAN_APPROVED e IMPLEMENT únicamente de F002 conforme a ese
> contrato y validación. No autorizo F003, dependencias nuevas, STT, edición,
> retake detection, HyperFrames ni render; F001 permanece intacto y su aceptación
> no cambia. Esta aprobación no declara ningún vídeo PRODUCTION_APPROVED.

Sustituir «commit indicado» por la identidad presentada. Aceptación de este PLAN
no equivale a DONE; requiere ejecución y aceptación humana de evidencia posterior.

## Historial

| Fecha | Estado / cambio | Decisión/evidencia |
| --- | --- | --- |
| 2026-10-03 | DRAFT, r1 | Petición adjunta del propietario: PLAN ONLY F002 tras cierre F001 7e0bc22. |
| 2026-10-03 | DRAFT → PLAN_READY | Tres documentos + D001 propuesto preparados para presentación. No código, instalaciones, proyecto/media ni checks F002 ejecutados. |

## Aprobación real de r1 y D001 — acta administrativa

**Approval:** GRANTED. Raúl Almeida, mensaje directo en este chat.

Fecha de registro UTC: 2026-10-03T19:40:26.578743Z. Commit aprobado: `ae36327768a4186009a92619ef8e4b1bf379d8a8`.
Los campos anteriores NOT GRANTED pertenecen a la presentación histórica; este
registro los sustituye administrativamente, sin cambiar la normativa aprobada.

> Apruebo F002, bundle r1 del commit ae36327, compuesto por requirements.md, plan.md y validation.md. Acepto expresamente D001 del mismo commit y la resolución limitada de tech-stack descrita en plan.md. Autorizo PLAN_READY → PLAN_APPROVED e IMPLEMENT únicamente de F002 conforme a ese contrato y validación. No autorizo F003, dependencias nuevas, STT, edición, detección de retomas, HyperFrames ni render. F001 permanece intacto. Esta aprobación no declara ningún vídeo PRODUCTION_APPROVED.

Identidad exacta pre-aprobación:

```text
cc2469e1fcdf2b6ccbfcb42ad0c26bea9bad203e9e228c8f4f918122cc1be6ce  requirements.md
df6bbb5bc76611ec05cfccab03a226e11ce22e5ccceaca6b282d6ae3ef292b54  plan.md
a2ab20714962d9f67a023099ac793cdb603f0051f0de92abba93f45e41611753  validation.md
49535e195f9ba6b5f36fa9e99f3b7782d8b6889ab256e7e71a0864715fa29bfc  D001-local-source-contract.md
```

Snapshot readonly: `.local/spec-approvals/F002/r1/`, además del commit Git.
Transición: PLAN_READY → PLAN_APPROVED. Alcance: IMPLEMENT/VERIFY solo F002.
D001 y la resolución limitada raíz están aceptados explícitamente; F003 continúa
fuera de autorización. Aceptación final F002 y PRODUCTION_APPROVED no concedidas.

## Inicio de IMPLEMENT y corrección tipográfica

Aprobación r1/D001 registrada antes de código. PLAN_APPROVED → IMPLEMENTING.
Se crean únicamente los ocho archivos de código/pruebas/procedimiento previstos.

Errata de ejemplo: `F002-studio-001` en plan/validación es el rótulo de feature;
el ID de proyecto ejecutable es `f002-studio-001`, conforme a la gramática normativa
minúscula de requirements.md. No cambiar esa gramática ni añadir normalización
silenciosa de IDs. Es corrección de capitalización del ejemplo, no cambio de
comportamiento, scope, criterios o tolerancias; originales presentados preservados.

## Inicio de VERIFY

IMPLEMENTING → VERIFYING. Código y procedimiento previstos implementados;
42 pruebas pasan con salida retenida en `.local/validation/F002/e1/unittest.log`.
La validación real F001 y el gate humano se ejecutan a continuación; todavía
no hay aceptación de evidencia ni DONE.

## VERIFY → HUMAN_REVIEW — entrega e1

Fecha UTC 2026-10-04T05:11:54.432452+00:00. Implementación `3e53205bcfd55570968f891a5bd972d5fe6bc621`; 43 tests y 15 escenarios
de fallo PASS. V-01–V-13 completos técnicamente; V-04 conserva juicio humano
pendiente y V-14 aceptación pendiente. [Matriz actual](validation.md#ejecución-e1--acta-administrativa-actual-2026-10-04).

Paquete: `.local/validation/F002/e1/review.md`; manifest e1 SHA-256
`3dd9201577a3e23cae128760a6ad217e48e24bb46d1e0acaf82d1fc93f71d35c`. Proyecto real `f002-studio-001`, inspection
`inspections/d48b0e46-af7e-405e-a5ee-0d703d53bcb0/inspection.json`, SHA-256
`d08658c3542e2a7d10b1093a0de5e464752fd6cbca14588cc816b323478b428f`. Input READY, feature HUMAN_REVIEW.

Paso de ingestión/regeneración/consumer cumplido técnicamente; sus referencias
a V-14 y el último checkbox humano quedan abiertos hasta decisión real del owner.
Normativa y bundle r1 exacto intactos/recuperables. F001/RAW/evidencia aceptada
sin cambios. La corrección de copia entra en r1 y no cambia ningún contrato;
reinspección con versión final y repetición final verificadas.

**Acceptance:** NOT GRANTED; no DONE. Se detiene para V-04/V-14 conforme al
contrato aprobado, sin pedir aprobación otra vez del PLAN ni avanzar a F003.
