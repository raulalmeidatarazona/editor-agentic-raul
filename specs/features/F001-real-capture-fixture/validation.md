# F001 — Contrato de validación y evidencia

**Bundle revision:** r1  
**Requirements:** [requirements.md](requirements.md)  
**Estado y aprobación:** [plan.md](plan.md)  
**Definido antes de grabar:** 2026-10-03

## Fixture y entorno

Fuente futura: toma principal STUDIO y, solo si se necesita, una auxiliar de
calibración. Ubicación canónica `.local/fixtures/F001-studio-001/`, relativa a
este repositorio; registrar rutas absolutas, nombres originales, bytes y hashes
reales al entregar. Si una toma se sustituye, usar un nuevo ID y conservar la
relación/historial. Todas las tomas incluidas deben satisfacer los checks que
les corresponden, no solo la principal.

Se encontraron ffprobe/FFmpeg 9.0.1 y shasum durante PLAN; no se instaló nada.
Ninguna inspección de media se ha ejecutado: no existe el fixture. Captura,
ubicación del backup, hashes, tiempos de contenido y revisión humana están
pendientes de ejecución. Comprobar disponibilidad/versiones de nuevo al validar.

## Checks predefinidos y correspondencia con aceptación

| Check | AC | Categoría | Procedimiento / expectativa | Evidencia a conservar |
| --- | --- | --- | --- | --- |
| V-01 | AC-01 | AUTOMATED / DETERMINISTIC EVIDENCE | Cada RAW es archivo regular no vacío; medir bytes y SHA-256 tras copiar; comparar con fuente/copia de recuperación y repetir hash al terminar checks. Todos coinciden. | Nombres/rutas/bytes, source.sha256 inicial/final y hash/ubicación de recuperación. |
| V-02 | AC-02/03 | AUTOMATED / DETERMINISTIC EVIDENCE | Probe exitoso; identificar vídeo real y pista de voz, duración positiva, dimensiones y datos FPS/audio. Registrar ausencias/campos no informados; no inventar valores. | ffprobe.json, streams seleccionados y resumen de propiedades. |
| V-03 | AC-02 | AUTOMATED / DETERMINISTIC EVIDENCE | Decodificar completos los streams seleccionados de cada toma con herramientas existentes; salida 0 y ningún error de decodificación. Probe/primer frame no bastan. | Comando, versión, exit code y decode.log. |
| V-04 | AC-03 | DETERMINISTIC + HUMAN EVIDENCE | Contrastar dimensiones/SAR/DAR/rotación disponible con montaje y vista humana. Identificar de forma inequívoca la vista vertical 9:16 y registrar comportamiento real del player. Puede requerir orientación de referencia externa al RAW; no exigir tag de rotación. | Campos medidos, descripción de vista/corrección necesaria, observación y confirmación de Raúl. |
| V-05 | AC-02/04 | HUMAN EVIDENCE | Reproducir y escuchar la explicación completa a velocidad normal con Raúl: voz original comprensible, sin distorsión/dropouts impeditivos; verificar origen conocido de la pista. | Player/archivo/pista revisados, fecha/revisor y observaciones de audio con momentos problemáticos si existen. |
| V-06 | AC-05 | HUMAN EVIDENCE | Verificar idea, entrega natural, pausa normal, tres términos técnicos realmente pronunciados y palabras completas al inicio/final. | Notas con términos, resumen e intervalos aproximados de fuente. |
| V-07 | AC-06 | HUMAN EVIDENCE | Escuchar error → pausa → Again aislado → pausa → corrección; contrastar con frase válida que contiene again. Notas identifican ambos usos sin ambigüedad. | Archivo/intervalos/palabras de error, marcador, corrección y NO RETOMA. |
| V-08 | AC-07/09 | HUMAN EVIDENCE | Ver postura normal, manos, izquierda/derecha y adelante/atrás y retorno al centro; evaluar encuadre útil y representatividad. Teleprompter usado si habitual; si no, registrar motivo real. | Intervalos por movimiento, partes visibles/limitaciones, uso/no-aplicabilidad y juicio de Raúl. |
| V-09 | AC-08/09 | HUMAN EVIDENCE | Revisar notas/contexto: equipo real, mic/ruta, fecha/zona, idioma, luces/ajustes conocidos o desconocidos, procedencia/permiso y limitaciones; Raúl confirma STUDIO representativo. | reference-notes.md y confirmación humana vinculada a hashes. |
| V-10 | AC-01/10 | DETERMINISTIC + HUMAN EVIDENCE | Revisar paquete local y resumen por AC, lectura/hash de copia recuperable, rutas de recuperación y exclusión de RAW de Git. Raúl acepta expresamente el fixture exacto; futuras funciones siguen NOT YET VALIDATED. | Tabla de identidad/resultados, recuperación verificada, alcance/fecha/frase de aceptación. |

No hay criterio de duración fija, 4K obligatorio, loudness numérico, tolerancia de
STT, crop digital o render. La ausencia de una propiedad opcional como bitrate
no es un fallo por sí sola: registrarla. No disponer de dimensiones, duración,
pistas o referencia de orientación suficiente sí bloquea su check obligatorio.

## Procedimientos deterministas — ejecutar solo después de aprobación

El agente operador sustituirá los valores por datos reales. Estos ejemplos son
comandos manuales, no software F002 ni scripts creados en F001. Guardar comando,
versión, stdout/stderr y código de salida en evidence/ sin secretos. Ninguno
escribe media de salida ni modifica el archivo fuente.

```sh
CAPTURE_RAW='/ruta/absoluta/.local/fixtures/F001-studio-001/raw/nombre-original.MP4'
test -f "$CAPTURE_RAW" && test -s "$CAPTURE_RAW"
wc -c < "$CAPTURE_RAW"
shasum -a 256 "$CAPTURE_RAW"
ffprobe -v error -show_format -show_streams -of json "$CAPTURE_RAW"
```

En la salida de probe registrar format/stream duration cuando estén disponibles,
width/height, sample_aspect_ratio/display_aspect_ratio, avg_frame_rate/r_frame_rate,
codec y tags/side_data de rotación/matriz si hay; para audio, codec, sample_rate,
channels/channel_layout cuando estén informados. La duración seleccionada debe
ser positiva y coherente con reproducción. FPS reportado no demuestra CFR; la
normalización temporal queda para F002. No convertir ausencia de rotation en
«0 grados confirmado» sin contrastar la imagen/contexto.

Decodificación completa, después de identificar los índices de vídeo real y voz
en probe; no asumir que el primer stream de audio es el micrófono deseado:

```sh
CAPTURE_VIDEO_INDEX='indice_real_del_stream_de_video'
CAPTURE_AUDIO_INDEX='indice_real_del_stream_de_voz'
ffmpeg -nostdin -hide_banner -v error -xerror -err_detect explode \
  -i "$CAPTURE_RAW" -map "0:${CAPTURE_VIDEO_INDEX}" \
  -map "0:${CAPTURE_AUDIO_INDEX}" -f null -
CAPTURE_DECODE_STATUS=$?
shasum -a 256 "$CAPTURE_RAW"
```

Conservar el exit code inmediatamente tras la decodificación, antes del comando
siguiente, además del log. Repetir para cada toma. Comparar hashes de cada fuente
y de su backup sin cambiar nombres/bytes para forzar una coincidencia. No basta
decir «hay una copia»: debe ser localizable y leíble, con hash coincidente. Una
herramienta no disponible o fallo de codec se informa con su salida; no instalar,
reconvertir ni rebajar aceptación automáticamente.

No se requieren capturas de pantalla, audio extraído ni proxy para pasar F001:
el RAW reproducible y las notas/checks son el paquete humano mínimo. Un pequeño
frame de evidencia, si resulta útil dentro de la ejecución aprobada, puede formar
parte de esos checks; no convertirlo en una composición o prueba de reframing.

## Cobertura negativa, límites y fallos

| Tipo | Cobertura acordada para F001 |
| --- | --- |
| Negativo semántico | La frase válida con again y una pausa normal contrastan con la retoma en V-06/07. Se valida la referencia humana, no un detector inexistente. |
| Archivo inválido / voz ausente | V-01–03/05 detectan archivo vacío, error de lectura/decodificación, ausencia de streams o voz ininteligible; bloquear aceptación, preservar originales. |
| Límites de orientación | V-04 contempla píxeles horizontales, autorrotación o metadata ausente; contexto+observación pueden resolver la vista. Conflicto no resoluble queda BLOCKED. |
| Límites de captura | V-06/08 revisan inicio/final de palabras, alcance natural de manos/movimientos y detalle visible. Sin probar zoom/crop finales. |
| Recuperación | V-01/10 comprueban lectura/hash de la copia existente. Diferencia o ausencia impide aceptar. No destruir ni interrumpir una copia para provocar fallos. |
| Tests de aplicación / failure injection destructiva | No aplican: no hay software/pipeline en F001. No fabricar corrupción, cortes o audio eliminado para probar funciones futuras. Los comportamientos ante fallos están predefinidos. |

## NOT YET VALIDATED — fuera de aceptación F001

STT y términos reconocidos automáticamente; detección de retomas/ambigüedad y
límites de corte; sincronía tras edición; captions; composición/render HyperFrames;
tracking o reframing digital; detección de safe zones y layouts finales; mezcla,
normalización/loudness de entrega; performance de render y calidad publicable.
No son «checks F001 pendientes» ni N/A añadidos para ocultar fallos: están fuera
de alcance desde PLAN. El fixture aporta casos para evaluarlos después.

## Reglas de decisión

Cada AC requiere sus evidencias. Criterio ejecutado que falla → FAIL. Inspección
requerida no ejecutable/identidad no resoluble → BLOCKED. Técnica disponible pero
juicios humanos pendientes → HUMAN_REVIEW_REQUIRED. PASS global solo con todos
los checks aplicables y humanos aprobados; conservar cada fallo/bloqueo individual.
Unknown/skipped nunca significa PASS. No aceptar por tener MP4 o probe exitoso.

DONE requiere aprobación previa del PLAN, entrega correspondiente a r1, evidencia
recuperable y aceptación expresa de Raúl vinculada a archivo/s y SHA-256. Es
aceptación de un fixture de desarrollo, no PRODUCTION_APPROVED de un vídeo.

## Evidencia de ejecución — todavía pendiente

**Verification result:** NOT RUN (no es PASS)  
**Fixture entregado / fecha / hashes:** pendientes; no se ha grabado ni recibido media  
**Checks V-01–V-10:** todos NOT RUN; no sustituir este estado por PASS al crear los documentos

Tras ejecución añadir, sin alterar el contrato previo:

| Campo de identidad | Valor real |
| --- | --- |
| Fixture ID / rol / nombre original | Pendiente |
| RAW absoluto / bytes / SHA-256 antes y después | Pendiente |
| Backup / hash / instrucciones y fecha de lectura | Pendiente |
| Notas / metadata / logs y versiones | Pendiente |

| Check / AC | Procedimiento real, fecha y operador | Esperado vs observado | Evidencia recuperable / hash | Resultado |
| --- | --- | --- | --- | --- |
| V-01–V-10 / AC correspondientes | Pendiente; completar una fila por check | Pendiente | Pendiente | NOT RUN |

No hay identidad autoritativa del RAW hasta que se complete esta tabla y Raúl
acepte la revisión. Después, un agente debe verificar archivo/hash contra esta
identidad, no escoger «el MP4 más nuevo». Cambiar el RAW invalida evidencia y
aceptación; registrar nueva toma y repetir checks afectados.

## Revisión humana y aceptación final

**Paquete mínimo:** RAW local identificable + reference-notes.md + resumen de checks.  
**Revisor requerido:** Raúl, para contenido/voz, montaje, retoma, movimientos y representatividad.  
**Revisor adicional:** opcional para claridad/escucha, sin sustituir el juicio de Raúl.  
**Observaciones / fecha / decisión reales:** pendientes.  
**Owner acceptance of feature:** NOT GRANTED.  
**Frase de aceptación / fixture ID / hashes / revisión:** pendientes.

Si el contenido o la toma fallan, corregir mediante nueva captura dentro de scope
y volver a verificar. Si el contrato debe cambiar, volver a PLAN. No pasar a
DONE ni comenzar F002 por una aprobación de PLAN o ausencia de comentarios.
