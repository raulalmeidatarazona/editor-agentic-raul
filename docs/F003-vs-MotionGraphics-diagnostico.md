# Diagnóstico del flujo 006 (MotionGraphics) y adaptaciones a este proyecto

**Fecha:** 2026-10-04\\
**Estado:** diagnóstico documental. No autoriza implementación ni cambia ninguna
especificación raíz. Las propuestas finales requieren aprobación del owner.\\
**Fuente analizada:** `/Users/raulalmeida/Workspace/MotionGraphics`, iteración 006
(`edicion-006-arquitectura.mp4`, 160,84 s, 1080×1920 a 25 fps).\\
**Método:** lectura directa de ficheros y medición. Nada de este documento viene
de inferencia: cada afirmación tiene su archivo y línea.

> Nota de integridad: cuatro subagentes encargados de mapear 006 devolvieron
> contenido fabricado (mencionaban «Azure Speech to Text» cuando el script usa
> `mlx_whisper`; colores negro/blanco en el QA de karaoke cuando son
> `#94a3b8`/`#f59e0b`/`#f8fafc`; versiones de dependencias inventadas; y scripts
> `hf6:preview`/`hf6:studio` que no existen en `package.json`). Se descartaron
> sus cuatro informes y todo lo que sigue se verificó leyendo los archivos.

---

## 1. Vínculo real entre ambos proyectos

Mismo discurso, distinta captura. Medido:

| | MotionGraphics 006 | editor-agentic-raul F003 |
| --- | --- | --- |
| Archivo | `WhatsApp Video 2026-10-03 at 16.14.01.mp4` | `C0216.MP4` |
| SHA-256 | `e72d69b6…2033d604` | `68addbf3…19ae427bcc` |
| Bytes | 37.288.406 | 2.873.163.442 |
| Vídeo | h264 848×480, rotación −90, 25 fps, 1,22 Mbps | h264 3840×2160, rotación −90, 25 fps |
| Audio | AAC 62 kbps | PCM 2 canales |
| Duración | **232,800000 s** | **232,800000 s** |

Confirmado por el owner: uno está editado, el otro está raw, y es el mismo
discurso. Consecuencia inmediata: 006 se montó sobre un **re-encode de WhatsApp
a 480p**, no sobre el raw de estudio. Decodificar 37 MB no es lo mismo que mover
2,87 GB en 4K, y eso explica parte de su velocidad. Su README lo declara
explícitamente: «La imagen visible original es 480×848… la demo conserva esa
resolución y no pretende recuperar detalle perdido».

**Adaptación:** nosotros trabajaremos siempre con un proxy ligero derivado del
raw, nunca con el 4K directo, ni para preview ni para iterar. El raw solo se
toca en el render final de entrega.

---

## 2. El pipeline real de 006, paso a paso

Los nueve pasos están documentados en `docs/one-shot-prompt.md` §3 y confirmados
en el código:

| # | Paso | Comando | Escribe | Coste real |
| --- | --- | --- | --- | --- |
| 1 | Ingest | `scripts/ingest_006.py` | `analysis/006/metadata.json`, `assets/source.mp4` (CRF 0, GOP 25, autorotate), `assets/source-pip.mp4` | ffmpeg local |
| 2 | Transcripción | `scripts/transcribe_006.py` | `analysis/006/transcript.raw.json` | **mlx_whisper local, 0 €** |
| 3 | Especificación | manual + `edit.json` | `specs/006-arquitectura/{spec.md,edit.json}` | humano |
| 4 | Build | `scripts/build_006.py` | `videos/006-arquitectura/{index.html,style.css,compositions/*.html}`, `analysis/006/timeline.json`, máster de audio | Python local |
| 5 | Check | `npx hyperframes@0.8.79 check --json` | `analysis/006/check.json` | navegador headless |
| 6 | Render | `node scripts/render_006.mjs` | `out/edicion-006-arquitectura.mp4` | render local |
| 7 | Verificación | `scripts/verify_006.py` | `analysis/006/verification.json` (14 puertas) + SHA-256 | ffprobe/PIL |
| 8 | QA de fotogramas | `diag_layout_006.mjs`, `verify_karaoke_006.mjs` | `analysis/006/qa-v3/`, contact sheets | puppeteer 25.12.0 |
| 9 | Docs | manual | `spec.md`, `verification.md`, `edit.json` | humano |

Transcripción exacta (`scripts/transcribe_006.py`):

```python
result = mlx_whisper.transcribe(
    str(AUDIO), path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
    language="es", word_timestamps=True, verbose=False,
    condition_on_previous_text=False,
)
```

Ninguna llamada de pago, ninguna subida, ninguna URL firmada, ningún bucket. El
modelo ya está en caché en `.cache/huggingface/hub` (1,5 GB).

**Adaptación:** esta es la diferencia de coste estructural más grande entre los
dos proyectos y es la que hay que decidir (ver §7).

---

## 3. Cómo se producen los timestamps exactos (el bloque que pediste)

### 3.1 Origen del timing

`mlx_whisper` con `word_timestamps=True` devuelve, por palabra, `start`/`end` en
segundos de la **fuente** y una `probability`. En `analysis/006/transcript.raw.json`:
58 segmentos, 467 palabras, **0 palabras sin timestamp**, probabilidad presente
en 467/467 con media 0,9646.

### 3.2 Ajustes de frontera documentados (`build_006.py` 187-202)

Whisper asigna a veces silencio con gap 0 entre palabras. El script corrige
**cinco** fronteras concretas, con condición explícita de tiempo y texto:

```python
if 186.15 < cw['start'] < 186.95 and cw['word'].strip() == 'sofisticada,':
    cw['end'] = 186.85
elif 186.85 < cw['start'] < 187.0 and cw['word'].strip() == 'debería':
    cw['start'] = 187.65
elif 113.85 < cw['start'] < 114.1 and cw['word'].strip() == 'Y':
    cw['start'] = 114.15
elif 138.85 < cw['start'] < 139.1 and cw['word'].strip() == 'pero':
    cw['start'] = 139.38
elif 152.95 < cw['start'] < 153.2 and cw['word'].strip() == 'y':
    cw['start'] = 153.26
```

Son cinco ajustes en 467 palabras (1%), escritos a mano, condicionados y
comentados como «Documented boundary adjustments». No hay un corrector
automático genérico: hay una lista corta y auditable.

**Adaptación:** esto es exactamente la forma D003 que proponemos. Una lista
corta, en datos, con condición de tiempo y texto, revisada por humano. No un
modelo de corrección, no una regla mágica.

### 3.3 Guardia dura: nunca cortar dentro de una palabra (`build_006.py` 207-209)

```python
for w in words:
    if w['end'] > w['start'] and (w['start'] < a < w['end'] or w['start'] < b < w['end']):
        raise ValueError(f"Cut inside word in {c['id']}: a={a:.3f}, b={b:.3f}, word={w}")
```

Si un corte de montaje cae dentro del intervalo de una palabra, el build
**falla**. Esto es lo que garantiza que los subtítulos no queden desincronizados
tras cortar: el corte se mueve, no el subtítulo.

**Adaptación alta prioridad:** nuestro F003 no tiene esta guardia. Es la regla
más valiosa de todo el flujo 006 y es trivial de portar. Debería ser un criterio
de F004 (edición), no de F003 (transcripción).

### 3.4 Re-mapeo de tiempo fuente → tiempo salida (`build_006.py` 215-223)

```python
start = f(c['fromFrame']) + w['start'] - a
end   = f(c['fromFrame']) + min(w['end'], b) - a
captions.append({'text': text, 'start': round(start, 4),
                 'end': round(max(end, start + 0.04), 4),
                 'clip': c['id'], 'sourceStart': w['start']})
```

Tres cosas importantes:

- el tiempo se re-mapea al clip de destino (`fromFrame`) y se recorta al
  intervalo del clip (`min(w['end'], b)`);
- se impone una **duración mínima de 0,04 s** para que ninguna palabra tenga
  ventana nula;
- se conserva `sourceStart`, el tiempo original en la fuente, **junto** al tiempo
  de salida.

**Adaptación crítica:** conservar ambos tiempos es lo que hace posible aplicar
una corrección dicho «en más o menos este segundo» sobre el vídeo ya montado y
que siga funcionando si el montaje cambia. Nuestro contrato `source-transcript v1`
ya tiene el reloj `source-presentation-v1` para esto; el spike lo respeta.

### 3.5 Correcciones terminológicas (`build_006.py` 211-214)

```python
text = w['word'].strip()
for corr in E['captionCorrections']:
    if abs(w['start'] - corr['sourceStart']) < 0.2 and text == corr['original']:
        text = corr['replacement']
```

El match es por **ventana de tiempo ±0,2 s y texto exacto**, no por posición ni
por índice. Las tres entradas reales de `specs/006-arquitectura/edit.json`:

| `sourceStart` | `original` | `replacement` | `reason` |
| --- | --- | --- | --- |
| 18.44 | `RP` | `ERP` | «Acrónimo de software empresarial en el discurso.» |
| 28.5 | `check-out` | `checkout` | «Término técnico de comercio electrónico.» |
| 111.88 | `diampotencia` | `idempotencia` | «Propiedad clave de sistemas distribuidos mal transcrita por Whisper.» |

La corrección toca **solo el texto**. El timing no se modifica en ningún momento.
Eso cumple literalmente `tech-stack.md §7`: «corrected technical terminology
while preserving what was spoken».

**Adaptación:** es la forma exacta de D003. Tres correcciones en un vídeo de
160 s. La tabla vive en `edit.json` (datos del proyecto), no en código.

### 3.6 Agrupación en cajas legibles en móvil (`build_006.py` 225-249)

```python
if pending and (len(' '.join(x['text'] for x in pending + [w])) > 28 or len(pending) >= 4
                or w['clip'] != pending[-1]['clip'] or w['start'] - pending[-1]['end'] > 0.45):
```

Cuatro criterios de corte de línea: más de 28 caracteres, más de 4 palabras,
cambio de clip, o hueco mayor de 0,45 s. Además corta siempre tras puntuación de
frase. Resultado en 006: 123 páginas. En nuestro spike, con el mismo criterio
sobre el transcript real: 149 páginas sobre 232,8 s.

Esto cumple Constitution §22 («2–6 visible words… no more than two lines») sin
necesidad de reglas adicionales.

### 3.7 Cómo el timing por palabra dirige la animación

`build_006.py` 605-641, función `build_subcomp`. Por cada página de subtítulo
que solapa la escena:

```python
rel_start = max(0.0, pg['start'] - scene_start_master)
rel_end   = min(scene_duration, pg['end'] - scene_start_master)
rel_dur   = max(0.2, rel_end - rel_start)
...
word_id = f'{scene_id}-cap-{cap_idx}-w{wi}'
word_spans.append(f'<span class="caption-word" id="{word_id}">{esc(w["text"])}</span>')
w_start = max(rel_start, min(scene_duration, w['start'] - scene_start_master))
w_end   = min(scene_duration, w['end'] - scene_start_master)
if w_end > w_start:
    karaoke_js.append(
        f'  tl.set("#{word_id}", {{color: "#f59e0b"}}, {w_start:.4f});\n'
        f'  tl.set("#{word_id}", {{color: "#f8fafc"}}, {w_end:.4f});'
    )
karaoke_js.insert(0, f'  tl.set("#{scene_id}-cap-{cap_idx} .caption-word", {{color: "#94a3b8"}}, {rel_start:.4f});')
```

El karaoke son **dos `tl.set()` de color por palabra**, más uno para poner toda
la caja en pendiente al abrirse. Tres estados, solo color:

- `#94a3b8` pendiente (gris pizarra)
- `#f59e0b` actual (ámbar)
- `#f8fafc` dicha (blanco)

Sin `font-weight`, sin `transition`, sin fade, sin escala. `one-shot-prompt.md`
§7 lo explica: «sin `font-weight`, sin `transition` (reevaluan y rompen la
reproducibilidad al hacer seek)». Por eso el seek es determinista y por eso el
render con `--workers 1` reproduce exactamente lo mismo.

Los `tl.set` van sobre los **spans hijos**, nunca sobre `.caption-box` (que
lleva `class="clip"`): el runtime es dueño de la visibilidad de los clips.
Eso coincide con la regla `gsap_animates_clip_element` de HyperFrames.

La caja se coloca con atributos de tiempo declarativos:

```html
<div id="{scene}-cap-{i}" class="clip caption-box"
     data-start="{rel_start:.4f}" data-duration="{rel_dur:.4f}" data-track-index="3">
```

**Adaptación:** este mecanismo se puede copiar literalmente. Nuestro spike ya lo
hace y pasó `hyperframes check` con contraste 26/26 AA.

---

## 4. Estructura de la composición (HyperFrames)

`videos/006-arquitectura/index.html` es la raíz: un `div#root` con
`data-composition-id="main"`, `data-width="1080"`, `data-height="1920"`,
`data-duration="160.8400"`, `data-fps="25"`. Dentro:

- seis hosts de escena con `data-composition-src="compositions/<id>.html"`,
  `data-start`/`data-duration` contiguos sin solapes, `data-track-index="1"`;
- `<audio id="master" class="clip" src="assets/master.wav" data-track-index="4">`;
- `window.__timelines.main = gsap.timeline({paused: true})`.

Cada escena es un archivo HTML propio (`friccion.html`, `frontera.html`,
`idempotencia.html`, `reintentos.html`, `preguntas.html`, `regla.html`), con el
vídeo de fondo, los gráficos y **su propia pista de subtítulos** dentro.

Los subtítulos viven dentro de cada escena (track 3) y no en la raíz, porque sus
tiempos son relativos a la escena. Eso es lo que permite que cada escena se
pueda mover sin recalcular los subtítulos.

**Adaptación:** en F004 la pista de subtítulos debe ser relativa a escena, no
absoluta. Nuestro spike, al no tener escenas, usa tiempos absolutos; es correcto
para un spike de revisión de una sola pieza, y habría que cambiarlo al introducir
escenas.

---

## 5. QA: cero escucha humana

Ninguna puerta de 006 requiere que alguien escuche nada. Todo es medición:

- `verify_006.py` → `analysis/006/verification.json`: **14 puertas en true**
  (`deliverable_stable_during_audit`, `source_unchanged`, `dimensions`, `fps`,
  `frames`, `duration`, `decode`, `codecs`, `color`, `lufs`, `peak`,
  `audio_matches_prepared_mix`, `no_black_frames`, `engine_check_passed`).
- `check.json` → `hyperframes check --json`: `ok: true`, `strict: false`, con
  **7 warnings** (`composition_file_too_large` ×1 y `timeline_track_too_dense` ×6).
  Los warnings no bloquean; los errores sí.
- `verify_karaoke_006.mjs` → puppeteer headless: carga cada escena, busca el
  timeline GSAP por `window.__sceneId`, hace `tl.time(t, false)` y lee
  `getComputedStyle(el).color` de cada `.caption-word`. Muestrea **1 de cada 4
  palabras** en el punto medio de su ventana, más un instante en cada hueco de
  más de 0,4 s (marcado `<hueco>`) para comprobar que no queda ámbar donde no
  hay subtítulo. El objetivo declarado es «100 % de palabras correctas».
- `diag_layout_006.mjs` → mide huecos de la tarjeta PiP: ≥32 px en reposo y
  ≥21 px en pleno tween.
- `faces.json` → geometría facial (YuNet según `one-shot-prompt.md` §3.1) para
  decidir el recorte vertical del PiP.
- Contact sheets y fotogramas `render-*.jpg` para revisión visual rápida.

**Adaptación alta prioridad:** esta es la segunda diferencia estructural más
grande. Nuestro F003 pedía escucha humana con bordes de incertidumbre ≤50 ms
como requisito **previo** al submit. 006 no pide escucha en ninguna puerta: mide
píxeles, colores, LUFS, peak, decodificación, ausencia de fotogramas negros y
estabilidad del entregable durante la auditoría. La escucha humana queda para el
juicio editorial del owner, no como oráculo de timing.

---

## 6. El bucle de corrección humano (lo que tú describiste)

Confirmado en el código y en los docs, y coincide exactamente con lo que
contaste: el texto **no** se perfecciona antes de montar.

1. Se transcribe (Whisper local, gratis, 12 s).
2. Se monta el vídeo con subtítulos y karaoke.
3. El owner **mira** el vídeo con las palabras y escucha a la vez.
4. Detecta errores leyendo, no leyendo transcripts.
5. Los comunica en lenguaje natural con tiempo aproximado: «son estas palabras
   en lugar de estas en más o menos este segundo».
6. Eso se convierte en entradas de `captionCorrections` (datos en `edit.json`).
7. Se regenera el build; el timing no cambia nunca.

`one-shot-prompt.md` §8 lo consagra como línea roja: «Correcciones de
transcripción documentadas (`RP→ERP`, errores evidentes, tecnicismos)». Y §1
pide que el flujo salga «en una sola pasada, sin pausas de aprobación» hasta el
entregable, para que la revisión humana caiga **sobre el vídeo**, no sobre
artefactos intermedios.

**Adaptación:** esto invierte el orden de nuestro F003 r1, que exige referencia
humana literal antes del POST. El spike ya implementa el orden correcto y está
corriendo en `http://localhost:3002/#project/composition`.

---

## 7. Decisiones que necesita el owner

Ninguna de estas la tomo yo. Cada una cambia una especificación raíz o el
presupuesto.

### 7.1 D003 v2 — capa de corrección terminológica alimentada por revisión visual

Ya propuesta como D003; con lo que contaste, cambia de forma. La corrección no
sale de una escucha previa: sale de ver el montaje en Studio y decir la
corrección en lenguaje natural. La tabla `captionCorrections` es la **salida** de
esa revisión, no un requisito de entrada. Requiere: aceptar D003, y decidir si
la capa vive en F003 (normalización) o en la feature de captions/F004.

### 7.2 Revisión de `tech-stack.md §7` (STT local vs nube)

§7 dice hoy: «Cloud STT is required for the baseline; no local Whisper
installation». Esa regla se escribió antes de tener estas mediciones:

| | Whisper local (mlx) | qwen filetrans (nube, pagado) |
| --- | --- | --- |
| Coste | 0 € | USD 0,00113 por 232,8 s |
| Tiempo | 11,6 s | ~10 s de job + transporte OSS + gates |
| Palabras | 468 | 470 (tras reconstrucción) |
| WER mutuo | — | **5,48%** global sobre las 5 ventanas r1 |
| `idempotencia` | falla (`impotencia`, p=0,744) | falla (`en potencia`) |
| Transporte | ninguno | bucket privado + URL firmada TTL |
| Iteraciones | ilimitadas | 1 autorizada |

Los dos fallan el mismo término. La nube no aporta ventaja en terminología sobre
este fixture. Hay tensión real con Constitution §36 (no asumir modelos de voz
pesados en local), aunque el modelo ya está en caché y ocupa 1,5 GB.

Propuesta probable: **local para iterar y previsualizar, nube para el transcript
canónico auditado** — o directamente local como baseline y nube como verificación
cruzada. Requiere aprobación explícita y enmienda de tech-stack §7; no lo aplico
por mi cuenta.

### 7.3 Guardia «nunca cortar dentro de una palabra»

Portarla como criterio medible de la feature de edición (F004). Es la regla más
barata y de mayor valor de todo 006.

### 7.4 Puertas de QA sin escucha humana

Sustituir el requisito de escucha humana con bounds ≤50 ms por QA medido
(karaoke por píxeles/colores, LUFS, peak, decode, black frames, layout). La
escucha humana queda para el juicio editorial del owner en V-16, que es donde
pertenece según Constitution §4.

### 7.5 Un prompt one-shot para nuestra cadena

`one-shot-prompt.md` es la razón por la que 006 sale de una pasada: 109 líneas
con pipeline exacto, constantes visuales, zonas en píxeles, estructura narrativa,
geometría del PiP, reglas de karaoke, líneas rojas y gates. Cuando tengamos un
máster aceptado, escribir el equivalente para Vertical Native es lo que convierte
el pipeline en reutilizable (Constitution §7: build once, configure, reuse).

---

## 8. Lo que NO se debería copiar

- **Ajustes de frontera hardcodeados en el script de build** (los cinco `elif`
  de `build_006.py` 187-202). Funcionan, pero mezclan datos de corrección con
  código de montaje. En nuestro proyecto van en la tabla de datos (D003), con
  razón y revisor, no en `if/elif`.
- **Trabajar sobre un re-encode de WhatsApp a 480p.** Fue lo que hizo 006 rápido
  y es justo lo que pierde la calidad del raw de estudio. Nosotros iteramos con
  proxy y entregamos desde el raw.
- **Aceptar warnings de densidad de timeline** (seis `timeline_track_too_dense`)
  como normales a partir de la iteración 1. Para un spike está bien; para un
  máster de entrega, las escenas deben ser sub-composiciones.

---

## 9. Evidencia del spike que ya está corriendo

`.local/spike/f003-preview/` (ignorado por git, fuera del bundle, sin tocar
F001/F002/F003 ni el raw):

- `build_captions.py` → `captions.json`: 149 páginas, 466 palabras
  reconstruidas desde 550 rows del transcript **real** de F003, 1 corrección
  aplicada (`en potencia` → `idempotencia` en 111,95 s).
- `build_composition.py` → composición HyperFrames con karaoke idéntico al de
  006 (mismos tres colores, mismos `tl.set` sobre spans hijos).
- Proxy 540×960 25 fps con el audio del WAV canal 1 (`4c71d168…`), 60 s de
  ffmpeg local. HyperFrames 0.8.78 y gsap **reutilizados** de MotionGraphics:
  nada instalado.
- Validación: `lint` 0 errores; `check` PASS (runtime 0, layout 0/9, motion 0,
  contraste 26/26 AA); 4 snapshots con GPU hardware.
- Karaoke medido por píxeles: a 111,5 s → 5190 px ámbar + 7626 gris; a 112,0 s →
  5486 blanco + 7158 ámbar + 158 gris. Lectura visual del fotograma 112,0 s:
  «reintentos y idempotencia», con `idempotencia` en ámbar y subrayado punteado.

Límites honestos: proxy CRF 30 (solo para leer y escuchar), sin gráficos, PiP,
marca ni safe-zones de producción, y tiempos por palabra con la incertidumbre
del vendor. Es desechable: no es entregable ni F004.

Instrucciones de uso y de cómo darme correcciones en lenguaje natural:
`.local/spike/f003-preview/README.md`.
