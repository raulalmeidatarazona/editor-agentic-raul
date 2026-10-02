# F001 — Real Vertical Capture Fixture and Studio Calibration

**Documento:** plan — CÓMO obtener el fixture  
**Bundle revision:** r1  
**Lifecycle state:** PLAN_READY  
**Owner:** Raúl Almeida  
**Scope:** [requirements.md](requirements.md)  
**Proof contract:** [validation.md](validation.md)

## Autorización y enfoque

La aprobación de Fase 0 está [registrada](../../README.md#phase-0-review-evidence).
El mismo mensaje pide «Proceed ONLY with the PLAN phase» para F001 y prohíbe
implementar, grabar en nombre de Raúl, crear composiciones o instalar dependencias.
Este documento define trabajo futuro; ninguna tarea de entrega se ha ejecutado.

La solución es una grabación real, copias de archivos y Markdown con inspección
manual/determinista. No construimos el futuro Content Project ni un esquema de
media. Raúl graba; después de aprobación, el agente inspecciona copias sin cambiar
los originales y prepara evidencia para Raúl. No se necesitan modelo, API, skill
de producción, proveedor ni coste recurrente nuevo.

Flujo futuro: cámara/tarjeta → copia RAW local + recuperación conservada → notas
humanas y mediciones independientes → resumen de identidad/evidencia → revisión
de Raúl. F002 consume el fixture aceptado; F001 no empieza F002.

## Cambio previsto y herramientas

| Ubicación / componente | Acción futura | Propósito |
| --- | --- | --- |
| Los tres archivos de esta feature | Completar historial, evidencia y aceptación después de ejecución. | SDD; no cambiar criterios silenciosamente. |
| `.local/fixtures/F001-studio-001/raw/` | Copiar originales, conservando nombres y bytes. | AC-01–03. |
| `.local/fixtures/F001-studio-001/reference-notes.md` | Escribir notas del material real con el formato siguiente. | AC-05–09. |
| `.local/fixtures/F001-studio-001/evidence/` | Guardar probe, hashes, logs y observaciones. | AC-01–04/10. |
| Tarjeta/almacenamiento existente designado por Raúl | Conservar una copia verificable y anotar recuperación. | AC-01. |

No crear esas rutas locales durante PLAN. Un reemplazo usa `F001-studio-002`,
sin sobreescribir una toma ni su evidencia. No crear carpetas de F002, software,
scripts de validación, fixtures binarios para Git ni nuevas dependencias.

Herramientas aprobadas por tech-stack y encontradas en la inspección de PLAN:
`/opt/homebrew/bin/ffmpeg` y `ffprobe`, ambos **9.0.1**, y
`/usr/bin/shasum`. Se comprobaron ubicación/versión, no se inspeccionó media
inexistente. Se usarán comandos existentes, documentados en validation.md, más
el reproductor local disponible. Registrar de nuevo versión efectiva al validar;
no actualizar herramientas automáticamente. Las skills HyperFrames no son
necesarias: su auditoría existente no convierte capture/calibration en render.

No hay ADR previo que modifique este alcance. La preparación local Git prevista
por el protocolo se resolverá como paso de preparación antes de IMPLEMENT si
el repositorio sigue sin inicializar; no añade remoto, LFS ni configuración Hermes
a la captura. Ningún check del fixture depende de Git o de descubrimiento de skills.

## Procedimiento de grabación para Raúl — después de aprobar el PLAN

**Resultado buscado:** una toma de referencia de aproximadamente 90–150 segundos,
con una explicación y pequeños movimientos. No hace falta actuar ni producir un
vídeo perfecto. Lee este procedimiento; los comandos de inspección son trabajo
posterior del agente.

1. **Prepara tu STUDIO habitual.** Usa el montaje de referencia Sony ZV-E10,
   objetivo kit, trípode, DJI Mic Mini y luces reales; usa Elgato Teleprompter si
   normalmente lo utilizas. Comprueba físicamente que el montaje vertical es
   estable y compatible. Si algo no puede usarse, anótalo antes de grabar; no
   fuerces el montaje ni compres equipo para cumplir este ejemplo.
2. **Elige un encuadre amplio y comprueba el sonido.** Aproximadamente centrado,
   cabeza, hombros y torso visibles y margen para manos/movimiento. Elige los
   ajustes que funcionen con tu cámara: 4K si es práctico, o la alternativa
   fiable de tu montaje. Verifica que el micrófono real se escucha en la cámara;
   no asumas que una pista con sonido es el DJI. No fijamos focal, FPS, exposición,
   distancia ni coordenadas. Guarda las lecturas conocidas para las notas.
3. **Empieza la toma y deja unos segundos de margen.** Mira a cámara/teleprompter
   como lo harías al explicar una idea. Haz una pausa natural antes de hablar.
4. **Explica una sola idea técnica.** Habla con tus palabras e incluye al menos
   tres términos relevantes. El ejemplo de abajo utiliza `goroutine`, `WaitGroup`
   y `errgroup`; no necesitas recitar una lista. Incluye una pausa normal de
   pensamiento que no sea una retoma.
5. **Introduce un error controlado y corrígelo sin detener la cámara.** Di una
   afirmación que puedas identificar después como equivocada; pausa; di únicamente
   **«Again»**; pausa; vuelve a decir la afirmación correctamente. No añadas otros
   comandos de voz ni hagas varias retomas deliberadas. El error permanecerá en
   el RAW, identificado como material de prueba, nunca como afirmación publicable.
6. **Di «again» dentro de una frase válida.** Por ejemplo, al explicar un retry:
   «En inglés lo llamamos “try again”: volver a intentarlo». Continúa normalmente;
   no lo aísles como un comando y no reinicies la frase. En las notas esa aparición
   quedará marcada **NARRACIÓN VÁLIDA — NO RETOMA**. Si tu idioma habitual permite
   una frase más natural, úsala y registra las palabras reales.
7. **Haz la calibración sin cambiar cámara ni luces.** Vuelve a postura normal,
   gesticula con las manos como al explicar; desplázate ligeramente a la izquierda,
   vuelve al centro, a la derecha y al centro. Inclínate/acércate ligeramente y
   vuelve; sepárate/inclínate ligeramente atrás y vuelve. Mantén cada posición
   el tiempo suficiente para poder verla y anuncia brevemente el movimiento.
   No busques los límites extremos ni salgas deliberadamente del plano. Muestra
   unos segundos de lectura normal con teleprompter si es tu uso habitual.
8. **Termina con una frase completa y unos segundos de margen.** No cortes la
   grabación mientras pronuncias la última palabra. Comprueba reproducción y
   escucha antes de desmontar/formatear la tarjeta.
9. **Conserva el original y anota lo ocurrido.** Copia el archivo tal como lo creó
   la cámara, sin exportar desde un editor ni enviarlo por una vía que recomprima.
   Conserva la tarjeta u otra copia recuperable. Escribe los datos/contexto reales
   y señala aproximadamente dónde están el error, el marcador, la corrección, la
   frase válida con «again» y los movimientos.

Si separar los movimientos ayuda, usa **una sola toma auxiliar de unos 20–40
segundos**, además de la principal. Conserva el mismo montaje, registra su propio
archivo/contexto y anuncia los movimientos con voz. La duración es orientativa.
Un cambio de cámara/luces entre tomas debe quedar explícito: no se considera una
calibración del mismo montaje por omisión.

### Guion opcional para una idea concreta

Este ejemplo sirve para recordar el contraste; se puede adaptar sin perder los
comportamientos requeridos. No impone idioma ni el texto exacto de futuras pruebas.

> Una goroutine permite ejecutar una tarea de forma concurrente. Cuando varias
> deben terminar antes de continuar, podemos coordinarlas con un WaitGroup.
>
> **Error intencional:** «WaitGroup devuelve el primer error de las goroutines».
> [Pausa] **Again** [Pausa].
> **Corrección:** «WaitGroup espera a que las goroutines terminen; no devuelve
> sus errores. Para agrupar tareas y recibir un error podemos utilizar errgroup».
>
> Repetir una operación es una decisión distinta: en inglés decimos «try again»,
> volver a intentarlo. Esa frase es parte de la explicación, no una retoma.

Después resume la idea con tus palabras y realiza los movimientos. Las notas
reflejarán lo que realmente dijiste, incluso si cambiaste o abandonaste el guion.

## Formato mínimo de reference-notes.md — crear tras grabar

Es Markdown humano, no un esquema/API. «Desconocido» es válido para ajustes no
observados; nunca sustituye la identidad del archivo o un evento obligatorio.
Los tiempos son aproximados desde el inicio de cada archivo RAW, no timecode de
entrega ni límites de corte frame-exactos.

```markdown
# F001-studio-001 — Notas de referencia

Fecha/hora y zona horaria: [real]
Grabado por / permiso de uso local de desarrollo: [Raúl / decisión real]
Perfil: STUDIO
Idea e idioma(s) hablados: [reales]
Equipo: [cámara, objetivo, trípode, teleprompter usado/no usado y motivo]
Micrófono y ruta de voz/pista: [dispositivo real, conexión observada; no inferir]
Ajustes conocidos: [resolución seleccionada, FPS seleccionado, focal/exposición
si se conocen; desconocido cuando corresponda]
Luces y entorno: [key/rim/RGB, lecturas conocidas, cambios, fondo, observaciones]
Postura / montaje / orientación intencionada: [descripción; sin coordenadas finales]

| Rol | Nombre original / ruta absoluta | Bytes | SHA-256 | Recuperación: ubicación y acceso |
| --- | --- | --- | --- | --- |
| Principal [auxiliar solo si existe] | [archivo real] | [medidos] | [real] | [tarjeta/copia verificada] |

## Hechos del contenido: tiempo de fuente aproximado mm:ss–mm:ss

| Archivo | Intervalo aproximado | Tipo | Palabras/acción realmente observadas |
| --- | --- | --- | --- |
| [real] | [real] | Narración válida / pausa normal | [resumen] |
| [real] | [real] | Error intencional | [afirmación equivocada] |
| [real] | [real] | Pausa → marcador aislado → pausa | [Again] |
| [real] | [real] | Toma corregida | [palabras reales] |
| [real] | [real] | NARRACIÓN VÁLIDA — NO RETOMA | [frase completa que contiene again] |
| [real] | [real] | Calibración | [postura/manos/izquierda/derecha/adelante/atrás/teleprompter] |

Términos técnicos realmente pronunciados: [lista con grafía de referencia]
Orientación observada: [píxeles, tags/matriz si hay; reproducción; corrección
de vista necesaria si no se autorrota, confirmada visualmente, no aplicada al RAW]
Observaciones y limitaciones: [visibilidad, voz, gesto, lectura, resolución, etc.]
Evidencia medida: [rutas a probe, hashes y logs; no confundir con ajustes elegidos]
Revisión de Raúl: [fecha/observaciones; no inventar aceptación]
```

## Riesgos, recuperación y evidencia

- Rotación ausente o diferente entre archivo y player: conservar metadata y vista
  observada; resolver la referencia con Raúl. No normalizar el original en F001.
- Sonido de cámara en vez del DJI, saturación o pérdida de voz: escuchar la toma
  completa y señalar el problema; corregir captura y crear una nueva toma si falla.
- Movimientos cortados o lectura poco representativa: señalar los momentos y
  repetir solo la toma necesaria; no inventar zonas ni corregir con digital crop.
- Copia incompleta, disco lleno o hash divergente: detener validación, mantener la
  fuente/tarjeta y recuperar una copia verificada. No borrar tomas como rollback.
- Error del guion confundido con consejo: marcarlo como ERROR INTENCIONAL en las
  notas; separar la corrección y la narración válida. No generar un transcript.

Registrar comandos reales, versiones, código de salida, logs, bytes/hashes y
revisión humana. Los datos de media quedan en `.local/`; el resumen pequeño de
validation.md conserva identidad y resultados para futuras sesiones. No secretos,
subidas a nube ni herramientas que alteren RAW. No prometemos sincronía, crops o
producción final a partir de estas comprobaciones.

## Pasos de ejecución — todos pendientes

- [ ] Confirmar aprobación explícita de r1 y resolver preparación local del repositorio conforme al protocolo, sin remoto/LFS ni servicios.
- [ ] Raúl verifica montaje/contexto y graba la toma principal; auxiliar solo si hace falta. AC-04–09.
- [ ] Copiar RAW sin transformación, registrar identidad y recuperación; completar notas reales. AC-01/08.
- [ ] Ejecutar V-01–V-04 sin modificar fuentes; conservar probe/logs/versión. AC-01–03.
- [ ] Escuchar/ver y anotar V-05–V-09 con Raúl. AC-04–09.
- [ ] Completar V-10, presentar fixture/evidencia y obtener aceptación expresa; solo entonces DONE. AC-10.

## Auditoría de especificación y presentación del PLAN

Revisión de PLAN, realizada 2026-10-03: R-01–R-08 tienen fundamento explícito;
AC-01–AC-10 tienen checks previos; ninguno depende de F002/STT/render. Los tres
archivos usan r1 y el mismo almacenamiento/alcance. El procedimiento es una toma
principal, con una auxiliar opcional; los campos vacíos son de ejecución futura,
no decisiones de producto ocultas. No se fijaron coordenadas, zoom/crop o ajustes
finales. No se grabó, instaló ni implementó. No se introduce un ADR o arquitectura
nueva. El fixture aceptado desbloqueará F002 y proporcionará referencias para las
features posteriores, sin probar sus algoritmos.

Presentación: objetivo = fixture real; alcance = captura/notas/mediciones; decisiones
= un original principal, contraste de «again», movimientos, copias recuperables;
aceptación = AC-01–AC-10; riesgos = orientación, voz, framing y recuperación;
preguntas bloqueantes = ninguna para PLAN. Falta aprobación expresa de este bundle.

## Aprobación del bundle presentado

**PLAN approval:** NOT GRANTED  
**Revisión presentada:** r1 de requirements.md, plan.md y validation.md  
**Approver / fecha / palabras de aprobación:** pendientes de decisión de Raúl  
**Approved revision / SHA-256 del bundle:** pendiente; registrar las tres huellas del bundle revisado antes de añadir el acta de aprobación  
**Copia recuperable del bundle aprobado:** pendiente de aprobación; conservar snapshot/Git según el protocolo  
**Alcance que se solicita aprobar:** procedimiento F001 y checks acordados; no F002 ni pipeline

La aprobación de Fase 0 y la orden de crear este PLAN no aprueban F001 IMPLEMENT.
Al recibir aprobación real, identificar/conservar el bundle presentado, registrar
la frase humana y solo entonces pasar a PLAN_APPROVED. Una revisión material
volverá a PLAN; las anotaciones administrativas no pueden encubrir cambios.

## Historial de estado y cambios

| Fecha | Transición / cambio | Evidencia |
| --- | --- | --- |
| 2026-10-03 | Inicio DRAFT, r1 | Petición expresa del propietario: solo PLAN para F001; predecesor OWNER_APPROVED. |
| 2026-10-03 | DRAFT → PLAN_READY | Bundle completo, auditado y presentado; implementación/aprobación aún pendientes. |

La aceptación final se registrará en validation.md; no existe entrega del fixture
ni revisión humana de media todavía. Detenerse aquí esperando al propietario.
