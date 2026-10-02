# F001 — Real Vertical Capture Fixture and Studio Calibration

**Documento:** requirements — QUÉ debe existir  
**Bundle revision:** r1  
**Owner:** Raúl Almeida  
**Roadmap:** Fase 1 — Real Capture Fixture  
**Predecesor:** Fase 0 OWNER_APPROVED, [decisión registrada](../../README.md#phase-0-review-evidence)  
**Decisiones arquitectónicas relacionadas:** ninguna; no hay ADR aceptados  
**Estado y aprobación:** únicamente en [plan.md](plan.md)

## Objetivo y problema

Obtener una pequeña muestra real y recuperable del STUDIO de Raúl, con voz,
retoma y movimientos conocidos. Permitirá evaluar ingestión, STT, edición y
layouts con evidencia del equipo real en vez de supuestos. Es un fixture de
ingeniería de su marca personal, no un vídeo terminado ni una prueba de producción.

## Alcance y fundamento

| Requisito | Qué debe proporcionar F001 | Razón en las especificaciones raíz |
| --- | --- | --- |
| R-01 | Captura real de Raúl en STUDIO, pensada para vista vertical, con encuadre amplio. | Constitución §§8–13; roadmap Fase 1. |
| R-02 | Explicación natural de una idea, pausas y vocabulario técnico realmente pronunciado. | Constitución §§20, 22, 27; misión §§4–6; roadmap Fases 1/3. |
| R-03 | Un error intencional, pausa, marcador aislado «Again», pausa y toma corregida; también «again» dentro de narración válida. | Constitución §14; roadmap Fases 1/4. El contraste evita referencias que enseñen a borrar cualquier aparición de la palabra. |
| R-04 | Postura normal, manos y pequeños desplazamientos izquierda/derecha y adelante/atrás; teleprompter cuando sea habitual. | Constitución §§12–13; roadmap Fases 1/7. |
| R-05 | Original con vídeo reproducible y voz original inteligible; propiedades y orientación observadas. | Constitución §§11, 24, 36; tech stack §6; roadmap Fases 1/2. |
| R-06 | Notas humanas que distingan intención, hechos de la toma y mediciones; referencia de los eventos en tiempo de fuente. | Constitución §§14, 35, 39; roadmap Fase 1 y dependencia de STT/edición. |
| R-07 | RAW sin edición, identidad por hash y recuperación comprobable; almacenamiento local ignorado. | Constitución §§8, 39; tech stack §§6, 11; protocolo de fixtures en specs/README.md. |
| R-08 | Evidencia mínima y decisión humana sobre representatividad; sin atribuir resultados a funciones futuras. | Constitución §§4–6; tech stack §13; protocolo VERIFY/DONE. |

Quedan fuera: software de ingestión/Content Project, modelos/proveedores, STT,
detección o eliminación de retomas, cortes, captions, mezcla correctiva, export,
HyperFrames, tracking, detección automática de zonas, calibración final de layouts,
UI, CI/CD, servicios nuevos, LFS, publicación y F002. No se exige que el RAW
cumpla el checklist de un vídeo PRODUCTION_APPROVED: debe conservar el error y
el marcador deliberados que una feature posterior tendrá que eliminar.

## Lo conocido, lo provisional y lo pendiente

### KNOWN CONSTITUTIONAL REQUIREMENTS

- Perfil STUDIO de referencia: Sony ZV-E10, objetivo kit, trípode, Elgato
  Teleprompter, DJI Mic Mini, luz principal, trasera/rim y dos luces RGB.
  Se registrará el equipo efectivamente utilizado, sin inventar conexiones.
- Capturar para editabilidad: aproximadamente centrado, cabeza, hombros, torso,
  manos naturales cuando sea práctico y espacio alrededor. No cerrar el plano
  para simular un crop final.
- Vista vertical 9:16; 4K cuando sea práctico, sin exigirlo a costa de fiabilidad.
  La entrega futura mínima 1080 × 1920 no obliga a que el RAW almacene sus píxeles
  en ese orden ni demuestra de antemano la calidad de un reencuadre.
- Voz original como elemento principal; no procesarla destructivamente ni añadir
  música/captions a la muestra. El marcador de retoma no es narración válida.

### CONFIGURABLE STARTING ASSUMPTIONS

- Una toma continua principal; como máximo una segunda toma corta de calibración
  si no resulta práctico incluir los movimientos en la primera. Ambas, si existen,
  serán del mismo montaje y conservarán su contexto. No es un corpus de grabaciones.
- Unos **90–150 segundos** totales como orientación práctica para explicación,
  contraste de retoma y movimientos. No es límite de aceptación ni objetivo del
  vídeo final: prima cubrir los comportamientos sin alargar artificialmente.
- Buffers silenciosos de unos 3–5 segundos al principio/final y pausas cómodas
  alrededor del marcador, sin temporizador ni duración obligatoria.
- Ruta más simple: voz del DJI en una pista del archivo de cámara, comprobada
  mediante escucha. No se presume que la existencia de una pista pruebe su origen.
  Si la configuración real solo entrega voz en un archivo separado, conservarlo
  y presentar el ajuste al PLAN antes de aceptar un contrato distinto.
- Idioma habitual elegido por Raúl y anotado. El ejemplo de plan.md está en
  español; el idioma de documentación no impone idioma al producto.
- Los targets RGB de tech-stack §8 son puntos de partida existentes, no valores
  finales: A 155°/65%/35%, B 18°/70%/30%. Se anotarán los ajustes reales o «desconocido».

### MEASUREMENTS TO COLLECT

Nombre, bytes, SHA-256, duración, streams elegidos, codec, dimensiones almacenadas,
aspectos SAR/DAR si se informan, tags/matriz/rotación si existen, frame rates
reportados, sample rate, canales y propiedades de audio disponibles. Observar
cómo aparece en el reproductor y qué orientación de vista corresponde a la toma.
Medir/anotar el encuadre visible y sus limitaciones durante los movimientos;
no derivar coordenadas de zonas, zoom o crop finales en F001.

La ausencia de metadatos de rotación no significa que la cámara estuviera
horizontal. Un RAW almacenado horizontal o mostrado de lado puede ser válido
si la vista vertical correcta queda inequívocamente identificada con contexto
y observación humana, para que F002 pueda tratar el comportamiento real.

### OWNER DECISIONS

Raúl aprobará este PLAN, elegirá idea/idioma, comprobará físicamente el montaje,
ajustes y uso habitual del teleprompter, designará una copia recuperable disponible
y decidirá si el resultado representa su STUDIO. No se le pide fijar ahora FPS,
exposición, distancia, encuadre geométrico ni presupuesto de un nuevo servicio.

### DEFERRED DECISIONS

Normalización de orientación/FPS y contratos de Content Project: F002. STT e
idioma/términos reconocidos: Fase 3. Límites de corte/retoma y su precisión: Fase 4.
Zonas, zoom, crop, layouts/configuración de marca final: Fases 6–7. Captions,
audio procesado y tolerancias de producción: sus features. Ninguno es criterio F001.

## Inputs, outputs y conservación

Inputs futuros: grabación física de Raúl, copia original desde la cámara/tarjeta,
contexto real, notas de escucha/visualización y herramientas ya disponibles.
La inspección de PLAN no encontró RAW ni fixtures previos en este proyecto.

Outputs después de aprobar/ejecutar F001:

| Tipo | Ubicación/contenido | Autoridad |
| --- | --- | --- |
| RAW SOURCE | `.local/fixtures/F001-studio-001/raw/<nombre-original>`; una toma principal y solo una auxiliar si hace falta. | Bytes originales; nunca un export o vídeo recortado. |
| REFERENCE NOTES | `reference-notes.md` en ese fixture; formato en plan.md. | Observaciones humanas del contenido, eventos e intención; no transcript generado. |
| MEASURED MEDIA METADATA | `evidence/ffprobe.json`, `source.sha256`, `decode.log` y versiones/resultados de inspección. | Lo observado por herramientas; no valores deseados ni configuración inventada. |
| Referencia de entrega | Tabla de identidad/evidencia en validation.md, con rutas, hashes, backup y aceptación. | Identifica exactamente el fixture aceptado para otra sesión. |
| FUTURE DERIVED ARTIFACTS | No existen en F001: normalizados, transcripts, EDL, captions, composiciones y outputs. | Se crearán en sus features, separados del RAW. |

La raíz relativa anterior se resuelve dentro de este repositorio. Al entregar,
registrar rutas absolutas reales. Preservar nombre original, hash tras importación
y hash después de inspección; conservar y verificar una copia recuperable en la
tarjeta original o almacenamiento existente distinto del directorio de trabajo.
No formatear/borrar la tarjeta hasta disponer de esa recuperación. No contratar
almacenamiento ni subir RAW a servicios para cumplir F001.

El conjunto completo queda fuera de Git por `/.local/`. En Git solo podrán ir
los tres documentos y el resumen pequeño y saneado de evidencia. No se selecciona
un fixture de vídeo permanente para Git en F001; no se crea `tests/fixtures/`
ni se introduce presupuesto arbitrario de bytes para cámaras. Se registra el
tamaño real y la capacidad disponible antes de copiar, sin recomprimir para caber.

## Comportamiento ante fallos

Archivo ausente/vacío, corrupción o falta de voz: no aceptar. Inspección no
ejecutable o identidad/orientación no resoluble: BLOCKED. Recibir un archivo no
autoriza sobrescribir un original existente. Un hash cambiado exige investigar
y recuperar desde copia verificada; no reemplazar el hash esperado para ocultarlo.

Contenido o movimientos incompletos: señalar exactamente lo ausente; repetir la
toma necesaria con un nuevo identificador y conservar la anterior. No subsanar
mediante edición, doblaje ni generación. Registrar equipo ausente/cambiado; si
altera la representatividad o el contrato, volver al PLAN, no declararlo STUDIO
equivalente automáticamente. Si hay una limitación menor compatible con todos los
AC, registrarla y pedir el juicio final de Raúl.

## Criterios de aceptación

| ID | Condición observable / frontera | Requisitos | Validación |
| --- | --- | --- | --- |
| AC-01 | Original/es no vacíos, identidad por SHA-256 estable antes/después de checks y copia recuperable con hash coincidente y ruta/instrucciones de acceso. | R-07 | V-01, V-10 |
| AC-02 | La toma principal contiene vídeo real y audio con voz; se decodifican completos los streams elegidos de cada toma requerida sin errores y se puede reproducir el contenido. | R-05 | V-02, V-03, V-05 |
| AC-03 | Duración positiva y dimensiones conocidas; información FPS/audio y orientación almacenada/de vista observadas. Vista vertical 9:16 identificable, con cualquier rotación necesaria anotada, sin alterar el RAW. | R-01, R-05 | V-02, V-04 |
| AC-04 | Voz original comprensible en reproducción normal durante toda la explicación, incluidas palabras críticas; sin clipping/distorsión/dropouts que impidan evaluarla. | R-05 | V-05 |
| AC-05 | Explicación natural de una idea, pausas, al menos tres términos técnicos pertinentes y palabras completas al inicio/final; notas de lo efectivamente dicho. | R-02, R-06 | V-06 |
| AC-06 | Un error identificable seguido de pausa → «Again» aislado → pausa → corrección. También una aparición de «again» en una frase válida, marcada explícitamente como NO RETOMA; intervalos aproximados en tiempo de fuente. | R-03, R-06 | V-07 |
| AC-07 | Raúl centrado en postura normal y encuadre amplio útil; cabeza/hombros/torso y gestos de manos observables, movimientos leves izquierda/derecha y adelante/atrás identificados. Uso habitual de teleprompter mostrado o no-aplicabilidad documentada. | R-01, R-04 | V-08 |
| AC-08 | Notas registran fecha con zona horaria, STUDIO, equipo/micrófono/ruta de voz, idioma, ajustes conocidos/desconocidos, luces, posición y uso de teleprompter, permiso/procedencia y limitaciones. Intención no se presenta como medición. | R-01, R-06 | V-09 |
| AC-09 | Raúl confirma que imagen/voz/movimientos representan el montaje real y son útiles para evaluar ingestión/STT/edición/layouts; limitaciones de detalle/framing están visibles sin prometer crops futuros. | R-04, R-05, R-08 | V-08, V-09 |
| AC-10 | Paquete local y resumen identifican una entrega inequívoca, evidencia recuperable y resultados por AC; las funciones futuras figuran NOT YET VALIDATED y Raúl acepta la revisión exacta. | R-06, R-07, R-08 | V-10 |

## Preguntas, supuestos y decisiones pendientes

El mínimo de tres términos es cobertura pequeña y explícita de este fixture para
el vocabulario técnico; no define una regla editorial de futuros vídeos. Pausas,
duración y movimientos no reciben umbrales artificiales ni tolerancias de corte.

No hay preguntas bloqueantes para preparar este PLAN: el perfil y los objetivos
ya están definidos. Idea/idioma exactos, ajustes físicos observados y ubicación
del backup son decisiones de ejecución de Raúl, recogidas antes de aceptar el
fixture; no se rellenan ahora como hechos. Los supuestos reversibles anteriores
se verifican durante la toma. Un cambio de perfil, audio separado exclusivo o
imposibilidad de recuperación sí bloquea la ejecución/aceptación correspondiente
y requiere resolver el contrato; no convierte a una feature futura en requisito.
