# F002 — Operación local de ingestión e inspección

Python 3.14.7 estándar y FFmpeg/ffprobe 9.0.1 existentes. No instalar dependencias.
Fuente integrada AV, copia byte-exacta independiente, metadata/tiempos y diagnóstico;
ninguna transcripción, extracción para STT, edición o normalización de media.

## Uso

Desde este repositorio, sustituye ruta e ID por los reales:

```sh
python3 tools/ingest.py ingest \
  --source '/ruta/local/Grabación original.mp4' \
  --project-id 'mi-grabacion-001' \
  --profile STUDIO
python3 tools/ingest.py verify --project '.local/projects/mi-grabacion-001'
python3 tools/ingest.py inspect --project '.local/projects/mi-grabacion-001'
```

IDs en minúsculas, letras/dígitos/guiones, máximo 64 caracteres. No se cambia el
nombre/ruta del original; `raw/source` es una copia con procedencia en project.json.
`--expected-sha256` verifica una identidad conocida, sin fijar valores en el código.
Opciones de referencia: `--fixture-id`, `--feature-revision`, `--recovery-location`,
`--evidence-manifest-sha256`. `--limitation` registra hechos declarados sin inferir
calidad de voz. Perfil UNKNOWN es válido si todavía no fue declarado.

Raíz por defecto `.local/projects` resuelta desde este repositorio. Si configuras
`--projects-root`, usa almacenamiento local y confirma que la carpeta esté excluida
de cualquier Git antes de ingerir; no publicar RAW/proyectos/logs por defecto.

## Resultado y recuperación

Stdout JSON, códigos: **0 READY**, **2 NEEDS_REVIEW**, **3 BLOCKED**, **4 INVALID**.
La ayuda es solo ayuda. READY confirma input técnico, no voz comprensible ni
encuadre/calidad de producción. Revisa `report.md` de la inspección referida en
`current.json`; no confíes en un snapshot READY antiguo: ejecuta verify de nuevo
inmediatamente antes de consumirlo. El lector no modifica el proyecto.

Múltiples streams: elegir explícitamente, sin adivinar el micrófono:

```sh
python3 tools/ingest.py inspect --project '.local/projects/mi-grabacion-001' \
  --video-stream 0 --audio-stream 2
```

Si Raúl confirma la vista correcta ante metadata ausente/conflictiva, guardar un
override de vista en grados **positivos antihorarios** (0, 90, -90, 180):

```sh
python3 tools/ingest.py inspect --project '.local/projects/mi-grabacion-001' \
  --display-rotation -90 --override-reason 'Vista confirmada en reproductor' \
  --override-reviewer 'Raúl Almeida'
```

Solo usar ese comando después de obtener el juicio real. No resuelve SAR, codec,
audio o tiempo desconocidos ni aplica giro/crop al RAW. La matriz reportada y el
tag original siguen visibles. Matrices se extraen en convención antihoraria;
el antiguo tag `rotate` se interpreta en convención horaria en este adaptador.
Tags arbitrarios o una vista contradictoria necesitan juicio humano; no afirman
orientación física de cámara. Raster almacenado y geometría display son distintos.

Segundo ingest idéntico produce NO_OP y conserva revisión/mtime/procedencia.
Cambio de contenido/contexto usa nuevo ID; cambio de elección/override usa inspect.
inspect sin opciones reutiliza las de última revisión completa cuando se conserva.
Artefactos derivados perdidos se regeneran desde copia poseída; si se pierde también
el registro de opciones, volver a aportar la selección/override humano explícito.

Fuente alterada: parar, localizar copia con identidad original y decidir recuperación
explícita; no actualizar el expected hash ni sobrescribir automáticamente. Un fallo
retiene staging/revisión, invalida readiness y no restaura un READY anterior.

BUSY puede ser writer activo o lock tras interrupción. Lee `.locks/<id>.lock`,
comprueba que su PID/run ya no está activo, identifica/conserva staging, y solo
entonces retira ese lock concreto por decisión explícita. No borrar locks por edad
ni directorios ajenos. Después vuelve a ejecutar inspect o ingest según el punto
de fallo. Timeouts de comando: 600 s por defecto, configurable 1–3600 s mediante
`--command-timeout-seconds`; ninguna repetición automática.

## Frontera de datos y tiempos

project.json posee identidad/contexto; inspections contienen derivados versionados;
current.json apunta a la revisión y hashes. [Contrato v1](../specs/features/F002-content-project-ingestion/requirements.md)
define null+motivos, extensiones, serialización y todos los bindings.

Reloj `source-presentation-v1`: cero en primer PTS presentado del vídeo elegido;
`t = PTS × time_base − origin_media_s`, racional exacto `n/d`. Audio puede tener
offset negativo/positivo. No es fecha, DTS, timecode Sony, índice/FPS ni timeline
editada. El consumidor independiente recibe fuente relativa/hash, streams,
properties, origen/offsets/intervalos y readiness; no parsea ffprobe ni elige STT.

La integridad se verifica en cada consumo; cambios externos después de verify
siguen siendo responsabilidad de comprobar estabilidad durante esa operación.
La copia de trabajo en el Mac no sustituye un backup independiente del disco.

## Pruebas y fixture real

```sh
python3 -m unittest discover -s tests -v
```

Las pruebas crean clips técnicos 1–3 s y fallos solo en copias temporales/locales
ignoradas. Los clips no reemplazan la aceptación real C0216.MP4 ni validan el MOBILE
candidato. Sus comandos/properties/hashes permanecen bajo `.local/fixtures/F002-synthetic-*/`.
[validation.md](../specs/features/F002-content-project-ingestion/validation.md) define
el procedimiento real y gates humanos; F002 DONE requiere aceptación expresa.
