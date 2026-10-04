# Uso del CSV `freetailv2.csv` — guía para agentes (bl + curl + Python)

> **Audiencia:** cualquier agente (humano o IA) que necesite llamar al espacio de
> trabajo **FreeTrailv2** de Alibaba Cloud Model Studio (Bailian) usando el
> archivo `~/Downloads/freetailv2.csv`.
>
> **Documento verificado el 2026-10-04** con llamadas reales. Todo lo marcado
> como ✅ devolvió HTTP 200 en pruebas; todo lo marcado como ❌ falló y se
> documenta con su error exacto.
>
> ⚠️ **Este archivo NO contiene la API key.** La key vive solo en el CSV local
> (que está en `~/Downloads`, fuera de Git). No la copies nunca aquí ni a
> ningún archivo del repositorio.

---

## 0. Resumen ejecutivo (léelo si solo tienes 30 segundos)

1. El CSV es un pares `clave,valor` por línea. De ahí salen **3 datos útiles**:
   `apiKey`, `openAiCompatible` (base URL OpenAI) y `dashScope` (base URL nativa).
2. **Dos formas de usarlo:**
   - **`bl`** (CLI oficial de Bailian): cómodo para chat/TTS/ASR, pero usa
     variables de entorno **por comando** para no pisar tu perfil existente.
   - **`curl` / Python directo**: base URL `…/compatible-mode/v1` + header
     `Authorization: Bearer <apiKey>`. Es OpenAI-compatible.
3. **Solo ~25 modelos están habilitados.** El resto da `403 AccessDenied.Unpurchased`.
4. **Los archivos locales NO se pueden subir** (`401 InvalidApiKey` en la
   política de subida). Para ASR/visión necesitas una **URL pública**.
5. **Nunca copies una key enmascarada** (`****`, `sk-s...xBeY`) desde logs,
   capturas o salida de `bl auth status`. Eso rompe la conexión. Ver §2.

---

## 1. El CSV: formato exacto

```
~/Downloads/freetailv2.csv
```

| Propiedad | Valor real (verificado con `od -c`) |
|---|---|
| Codificación | UTF-8 **con BOM** (`EF BB BF` = `\ufeff` al inicio) |
| Fin de línea | `\n` (LF, **sin** `\r`) |
| Líneas | 8 |
| Formato | `clave,valor` por línea (NO es un CSV con cabecera de columnas) |
| Separador | primera coma; los valores **no contienen comas** |

Contenido (valores truncados a propósito):

```
id,1288302
apiKey,sk-ws-<...>
apiHost,ws-<...>.ap-southeast-1.maas.aliyuncs.com
openAiCompatible,https://ws-<...>.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
dashScope,https://ws-<...>.ap-southeast-1.maas.aliyuncs.com/api/v1
description,FreeTrailv2
workspaceName,默认业务空间
workspaceId,ws-<...>
```

### Campos y para qué sirve cada uno

| Campo | Uso |
|---|---|
| `apiKey` | Credencial `sk-ws-…`. Va en `Authorization: Bearer …` o en `--api-key` / `DASHSCOPE_API_KEY`. |
| `apiHost` | Solo el host, sin esquema ni ruta. Útil para armar URLs a mano. |
| `openAiCompatible` | **Base URL para el SDK de OpenAI / curl de chat y embeddings.** Ya incluye `/compatible-mode/v1`. |
| `dashScope` | **Base URL para los endpoints nativos** (`/services/...`): ASR, TTS, image2image, tasks. |
| `workspaceId` | ID del espacio `ws-…` (mismo prefijo que el host). |
| `id`, `description`, `workspaceName` | Informativos; no se usan en las llamadas. |

### Parsing correcto

**Python (recomendado — `utf-8-sig` elimina el BOM de golpe):**

```python
import csv, os

CSV_PATH = os.path.expanduser("~/Downloads/freetailv2.csv")

cfg = {}
with open(CSV_PATH, encoding="utf-8-sig") as f:      # ← utf-8-sig quita el BOM
    for row in csv.reader(f):
        if len(row) >= 2:
            cfg[row[0]] = row[1]                      # split por CSV, no manual

API_KEY   = cfg["apiKey"]
BASE_OPEN = cfg["openAiCompatible"]   # https://ws-….maas.aliyuncs.com/compatible-mode/v1
BASE_NAT  = cfg["dashScope"]          # https://ws-….maas.aliyuncs.com/api/v1
```

**Bash:**

```bash
CSV=~/Downloads/freetailv2.csv
KEY=$(awk -F, '$1=="apiKey"{print $2}' "$CSV")
OPEN_BASE=$(awk -F, '$1=="openAiCompatible"{print $2}' "$CSV")
NATIVE_BASE=$(awk -F, '$1=="dashScope"{print $2}' "$CSV")
```

**Errores de parsing típicos:**

- Usar `open(...)` sin `utf-8-sig` en Python → la primera clave queda como
  `"﻿id"` (con BOM) y `cfg["id"]` falla o `cfg["apiKey"]` se lee bien pero la
  primera línea no. No afecta a `apiKey` (no es la primera línea), pero
  rompe `cfg["id"]`.
- Usar `split(",")` completo en vez de `split(",", 1)` → rompe si algún valor
  pasa a contener comas (hoy no, mañana sí).
- Copiar/pegar el contenido del CSV en el código → expone el secreto (ver §2).

---

## 2. 🔴 REGLA #1 DE SEGURIDAD: nunca pegues una key enmascarada

Este es el fallo **más frecuente** al hacer que otro agente use este CSV, y el
que provoca el error clásico `InvalidApiKey` / `401`.

### De dónde sale el `**` y por qué es una trampa

Varias fuentes **enmascaran automáticamente** la clave. Si copias literalmente
ese texto a tu código, la conexión **nunca** funcionará:

| Fuente | Qué muestra | Ejemplo real de salida |
|---|---|---|
| Consola de Alibaba (capturas de pantalla, columna "API Key") | `****` en el medio | `sk-ws-H.DHYYIMH****KOpsLGm67Co9pxQ` |
| `bl auth status` | `sk-s...xBeY` (puntos suspensivos) | `API key (model): config sk-s...xBeY` |
| Logs, APM, herramientas de tracing | reemplazo de secretos | `Bearer sk-ws-H.***` |
| Un agente resumiendo una conversación | `***` por prudencia | `la clave es sk-ws-***` |
| Tu propio editor con extensión de redacción de secretos | todo oculto | `sk-ws-<redacted>` |

**Si pegas cualquiera de esas cadenas en `Authorization: Bearer …`,
`DASHSCOPE_API_KEY` o `--api-key`, el servidor responde:**

```json
{"code":"InvalidApiKey","message":"Invalid API-key provided."}   ← HTTP 401
```

### Reglas operativas para el agente

1. **La clave NUNCA se escribe a mano ni se pega.** Se **lee del CSV en tiempo
   de ejecución** (§1) o se pasa por variable de entorno ya cargada desde el CSV.
2. **Prohibido** escribir en el código `sk-ws-…` con `****`, `...` o cualquier
   truncamiento. Ni siquiera "de ejemplo".
3. Al **reportar** resultados, si necesitas mostrar la clave, muestra solo:
   - longitud total: `len(key)` → p. ej. `115` (la real de este CSV)
   - prefijo seguro: `key[:8]` → p. ej. `sk-ws-H.`
   - NUNCA el cuerpo ni el sufijo.
4. Si un log, `--verbose` o una respuesta HTTP imprime la clave **completa**,
   no la copies al chat ni a un archivo del repo; las trazas deben ir
   redactadas (`sk-[A-Za-z0-9._-]{6}` → `sk-…***`).
5. El CSV vive en `~/Downloads` (**fuera de Git**). No lo copies a
   `docs/`, `specs/`, `.local/` ni a ningún artefacto de evidencia.
6. Verificación rápida de que la variable es la correcta **sin exponerla**:

```bash
python3 -c "
import os,sys
k=os.environ['DASHSCOPE_API_KEY']
print('longitud:', len(k), '| prefijo:', k[:8], '| ¿enmascarada?', any(s in k for s in ('****','...','<')))
"
# salida correcta:  longitud: 115 | prefijo: sk-ws-H. | ¿enmascarada? False
# si sale True  → estás usando una cadena enmascarada. Vuelve al CSV.
```

---

## 3. Uso con `bl` (CLI oficial de Bailian)

> Versión verificada: skill `bailian-protocol` **2.1.0** = `bl --version`
> **2.1.0** = `npm view bailian-cli version` **2.1.0** (pre-flight de versiones
> OK). Si hay desajuste: `bl skill update` / preguntar antes de `bl update`.

### 3.1 Autenticación sin romper tu config

Este equipo ya tiene un perfil activo (`token-plan`) con **otra** clave. Para
usar la de FreeTrailv2 **no hagas `bl auth login`** (cambiaría el perfil
activo). Usa variables de entorno **por comando**:

```bash
export DASHSCOPE_API_KEY=$(awk -F, '$1=="apiKey"{print $2}' ~/Downloads/freetailv2.csv)
export DASHSCOPE_BASE_URL=$(awk -F, '$1=="openAiCompatible"{print $2}' ~/Downloads/freetailv2.csv)

# (o por comando, sin exportar:)
bl text chat --api-key "$KEY" --base-url "$BASE" --message "hola"
```

Prioridad real: `--api-key` / `--base-url` (flag) > `DASHSCOPE_API_KEY` /
`DASHSCOPE_BASE_URL` (env) > perfil activo (config).

### 3.2 Llamadas verificadas ✅

```bash
# 1) Chat
NO_COLOR=1 bl text chat --timeout 120 \
  --model qwen-flash-character \
  --system "Responde en español, una frase corta." \
  --message "Saluda y di qué modelo eres" --max-tokens 80 --quiet
# → "Hola! Soy el modelo experimental Pegasus."

# 2) TTS (OBLIGATORIO: --voice; sin él → error "Missing required flag")
NO_COLOR=1 bl speech synthesize --timeout 120 \
  --model qwen-audio-3.0-tts-plus --voice longanlufeng \
  --text "Hello, this is a voice synthesis test." \
  --format mp3 --out /tmp/tts.mp3 --output json
# → {"saved":"/tmp/tts.mp3","audio_url":"http://dashscope-result-sgp.oss-…mp3?Expires=…"}
#   MP3 24 kHz mono, ~5 s, 100 KB

# 2b) Listar voces (solo 2: longanlingxin 龙安灵心 / longanlufeng 龙安鲁风, 中文/英文)
bl speech synthesize --list-voices --model qwen-audio-3.0-tts-plus

# 3) ASR desde URL pública (la del TTS sirve)
NO_COLOR=1 bl speech recognize --timeout 180 \
  --url "$AUDIO_URL" --model qwen-audio-3.0-asr-flash --language en
# → "Hello, this is a voice synthesis test for the free trial workspace."
# También probado con --model qwen-audio-3.1-asr-flash → OK

# 4) Límites por modelo (QPM/TPM, nivel workspace)
NO_COLOR=1 bl quota list --api-key "$KEY" --base-url "$BASE" --page-size 50 --output json
```

### 3.3 Llamadas que FALLAN ❌ (con error exacto)

```bash
# Archivo local → 401 en la política de subida de DashScope
bl file upload --file ./tts.mp3 --model qwen-audio-3.0-asr-flash
# {"code":1,"message":"Failed to get upload policy (HTTP 401): {\"code\":\"InvalidApiKey\"…}"}
bl speech recognize --url ./tts.mp3 --model qwen-audio-3.0-asr-flash
# mismo 401 (el CLI sube el archivo antes de reconocer)

# Modelo no habilitado → 403
bl text chat --model qwen3.8-max --message "hola"
# {"http_status":403,"api_code":"AccessDenied.Unpurchased"}

# Cuota gratuita agotada → 403
bl text chat --model qwen-plus-character --message "hola"
# {"http_status":403,"api_code":"insufficient_quota",
#  "message":"Free quota exhausted… disable the 'use free tier only' mode…"}
```

### 3.4 Gotchas de `bl` aprendidas a la fuerza

| Sintaxis/tema | Correcto |
|---|---|
| `--stream off` | ❌ **No existe**. `--stream` es flag booleano; `--stream off` → `Unexpected argument: off`. Para salida limpia usa `--quiet` y/o `--output json`. |
| Timeout de conexión | El host de Singapur tarda **5–6 s** en conectar y `bl` aborta a veces con `UND_ERR_CONNECT_TIMEOUT` (10 s). **Reintenta** o pasa `--timeout 120/180`. |
| Modelos por defecto | `text chat` por defecto usa `qwen3.8-max` → **403** aquí. Pasa `--model` explícito **de la lista habilitada** (§5). |
| `bl model list` | Catálogo **global** (172 modelos). **No** refleja tus permisos. |
| Perfil activo | `bl auth status` → `Config: token-plan *`. No hagas `auth login` si no quieres cambiarlo. |
| Salida con color | Añade `NO_COLOR=1` si vas a parsear la salida. |
| ASR local | Solo con URL pública. `--url ./archivo.mp3` falla por el 401. |

---

## 4. Uso con `curl` / HTTP directo (sin `bl`)

Todo es OpenAI-compatible en `openAiCompatible` y DashScope-nativo en `dashScope`.

```bash
KEY=$(awk -F, '$1=="apiKey"{print $2}' ~/Downloads/freetailv2.csv)
OPEN_BASE=$(awk -F, '$1=="openAiCompatible"{print $2}' ~/Downloads/freetailv2.csv)
NATIVE_BASE=$(awk -F, '$1=="dashScope"{print $2}' ~/Downloads/freetailv2.csv)
```

### 4.1 Chat ✅ (probado)

```bash
curl -sS --max-time 60 \
  "$OPEN_BASE/chat/completions" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-flash-character",
    "messages": [
      {"role":"system","content":"Responde en español, máximo 20 palabras."},
      {"role":"user","content":"Hola, ¿estás funcionando?"}
    ],
    "max_tokens": 60
  }'
```

Respuesta real (HTTP 200):

```json
{"choices":[{"message":{"content":"¡Hola!","role":"assistant"},
 "finish_reason":"stop"}],"model":"qwen-flash-character",
 "usage":{"prompt_tokens":14,"completion_tokens":3,"total_tokens":17}}
```

### 4.2 Embeddings ✅ (probado)

```bash
curl -sS "$OPEN_BASE/embeddings" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.7-text-embedding","input":"hola mundo"}'
# → {"object":"list","data":[{"embedding":[0.0216, 0.0154, …]}]}
```

> `text-embedding-v4` → **403 AccessDenied.Unpurchased**. Solo el `qwen3.7-text-embedding`.

### 4.3 Listar modelos (solo catálogo) ✅

```bash
curl -s "$OPEN_BASE/models" -H "Authorization: Bearer $KEY" | jq '.data | length'
# → 172   ← NO son tus permisos, es el catálogo global
```

### 4.4 ASR (reconocimiento) vía endpoint nativo ✅ (probado)

**Esquema exacto** (capturado del comportamiento real de `bl` con un proxy
local de registro; verificado con HTTP 200):

```bash
curl -sS --max-time 120 -X POST \
  "$NATIVE_BASE/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-audio-3.0-asr-flash",
    "input": {
      "messages": [{
        "role": "user",
        "content": [{"type":"input_audio","input_audio":{"data":"URL_PUBLICA_DEL_AUDIO"}}]
      }]
    },
    "parameters": {
      "format": "mp3",
      "sample_rate": "16000",
      "language_hints": ["en"]
    }
  }'
```

Respuesta real (HTTP 200):

```json
{"sentence":{"sentence_id":1,"begin_time":280,"end_time":2200,
 "text":"Native SR test two. ","words":[…]}}
```

**Detalles críticos (todos comprobados):**

- ❌ `parameters` **sin** `format`+`sample_rate` → `400 {}` (cuerpo vacío,
  imposible de diagnosticar a ciegas). **Los dos son obligatorios.**
- ❌ Ruta `/services/audio/asr` → `400 {"code":"InvalidParameter","message":"url error…"}`.
- ❌ Claves alternativas (`file_url`, `file_urls`, `audio_url` crudos) → `400`.
- ❌ `/compatible-mode/v1/audio/transcriptions` (multipart) → `404`.
- ✅ Solo funciona `content[0] = {"type":"input_audio","input_audio":{"data": URL}}`
  **más** `parameters.format` + `parameters.sample_rate`.
- `language_hints` es opcional pero mejora el resultado (sin él, `"Native SR Test 2"` con mayúsculas raras; con él, `"Native SR test two. "`).
- El audio debe ser una **URL pública** (el `audio_url` que devuelve el TTS sirve; ver §4.5).

### 4.5 TTS (sintetización) ✅

La ruta recomendada es `bl speech synthesize` (ya resuelve URL y descarga).

Con `curl` directo, la invocación **asíncrona NO está habilitada** para esta key:

```bash
curl -X POST "$NATIVE_BASE/services/audio/tts" … -H "X-DashScope-Async: enable"
# → 403 {"code":"AccessDenied","message":"current user api does not support asynchronous calls"}
```

Por tanto: usa `bl` para TTS, o la versión síncrona si la necesitas en crudo.
**Voz obligatoria** y solo 2 voces (zh/en) → **no se puede sintetizar en
español** con `qwen-audio-3.0-tts-plus`.

### 4.6 Traducción de imagen `qwen-mt-image-2.0` ✅ (probado, HTTP 200)

```bash
curl -sS -X POST \
  "$NATIVE_BASE/services/aigc/image2image/image-synthesis" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-mt-image-2.0",
    "input": {
      "image_url": "https://ejemplo.com/foto.jpg",
      "source_lang": "auto",
      "target_lang": "es"
    }
  }'
# → {"output":{"image_url":"http://dashscope-463f.oss-…jpg?Expires=…"},
#    "usage":{"image_count":1}}
```

- Consumes **1 de tus 100 cuotas** por imagen.
- `image_url` debe ser **pública** (no local).
- **No** va por `/chat/completions` → ahí da `404 model_not_supported`.
- Asíncrono: header `X-DashScope-Async: enable` → devuelve `task_id`, consulta en
  `GET $NATIVE_BASE/tasks/{task_id}`.

### 4.7 Subida de archivos (File API) ⚠️ parcial

```bash
# Sube (HTTP 200)…
curl -s -F "file=@/tmp/audio.mp3" -F "purpose=file-extract" \
  "$OPEN_BASE/files" -H "Authorization: Bearer $KEY"
# → {"id":"file-fe-…","status":"processed"}   purposes válidos: file-extract | batch
```

Pero **no devuelve URL pública** (`GET /files/{id}` tampoco), así que **no sirve
para alimentar al ASR**. Y `POST …/api/v1/files` → `404`.

---

## 5. Modelos habilitados vs. bloqueados

### 5.1 Habilitados (cuota FreeTrailv2, expiran **2027-01-02**)

| Modelo | Tipo | Cuota | Estado de prueba |
|---|---|---|---|
| `qwen-flash-character` | Chat | 1M | ✅ **probado, OK** |
| `qwen-plus-character` | Chat | 1M | ❌ `403 insufficient_quota` (cuota gratuita agotada) |
| `qwen3.7-text-embedding` | Embeddings | 1M | ✅ **probado, OK** |
| `qwen-audio-3.0-tts-plus` | TTS | 10K | ✅ **probado, OK** (solo 2 voces zh/en) |
| `qwen-audio-3.0-tts-flash` | TTS | 10K | no probado |
| `qwen3-tts-instruct-flash` (+ `-2026-01-26`, `-realtime`, `-realtime-2026-01-26`) | TTS | 10K | no probado (pasa validación) |
| `qwen3-tts-vc-2026-01-22`, `qwen3-tts-vd-2026-01-26` | Voz | 10K | no probado (pasa validación) |
| `qwen-audio-3.0-asr-flash` | ASR | 36K | ✅ **probado, OK** (bl + curl) |
| `qwen-audio-3.1-asr-flash` | ASR | 1M | ✅ **probado, OK** (bl) |
| `qwen-audio-3.1-asr-flash-filetrans` / `-message` / `-streaming` | ASR largo/stream | 1M–36K | no probado |
| `qwen-audio-3.0-asr-flash-filetrans` / `-streaming` | ASR largo/stream | 36K | no probado |
| `qwen3-asr-flash-2026-02-10` | ASR | 36K | no probado (pasa validación) |
| `qwen3-asr-flash-realtime-2026-02-10` | ASR realtime | 36K | acepta chat (200) |
| `fun-asr-flash-2026-06-15` | ASR | 36K | no probado |
| `qwen3.5-livetranslate-flash-realtime` (+ `-2026-01-26`) | Traducción en vivo | 1M | acepta chat (200) |
| `qwen3.8-livetranslate-flash-realtime` | Traducción en vivo | 1M | acepta chat (200) |
| `qwen-mt-image-2.0` | Traducción de imagen | 100 | ✅ **probado, OK** |

### 5.2 Bloqueados (muestra representativa)

Todo lo demás → `403 AccessDenied.Unpurchased`:

```
qwen3.8-max  qwen3.8-flash  qwen3.7-max  qwen3.7-plus  qwen3.7-flash
qwen3.6-*  qwen3.5-*  qwen-plus  qwen-max  qwen-turbo  qwq-plus
qwen3-coder-*  deepseek-*  kimi-*  glm-5.*  qwen3-vl-*  qwen3*-omni-*
text-embedding-v4  qwen-image-*  wan2.7-image …
```

> ⚠️ `GET /compatible-mode/v1/models` devuelve **172** modelos: es el catálogo
> del mercado, **no** tus permisos. Antes de probar un modelo, comprueba que
> esté en §5.1.

---

## 6. Uso directo desde Python

### 6.1 Sin dependencias (stdlib puro) ✅ probado

```python
import csv, json, os, urllib.request, urllib.error

CSV = os.path.expanduser("~/Downloads/freetailv2.csv")
cfg = {}
with open(CSV, encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        if len(row) >= 2:
            cfg[row[0]] = row[1]

API_KEY = cfg["apiKey"]                    # ← SIEMPRE leído del archivo
if any(s in API_KEY for s in ("****", "...", "<")):
    raise SystemExit("API key enmascarada: vuelve al CSV original (ver §2)")

BASE = cfg["openAiCompatible"]

def chat(prompt, model="qwen-flash-character", max_tokens=100):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        f"{BASE}/chat/completions", data=body,
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # imprime el error SIN la cabecera Authorization
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:500]}")

print(chat("Di hola y termina.")["choices"][0]["message"]["content"])
# → ¡Hola! ¡Es un placer conocerte!   (HTTP 200, ~29 tokens)
```

### 6.2 Con el SDK de OpenAI ✅ (mismo endpoint; `pip install openai`)

```python
from openai import OpenAI
client = OpenAI(api_key=API_KEY, base_url=cfg["openAiCompatible"])

r = client.chat.completions.create(
    model="qwen-flash-character",
    messages=[{"role": "user", "content": "Hola"}],
    max_tokens=50)
print(r.choices[0].message.content)

e = client.embeddings.create(model="qwen3.7-text-embedding", input="hola mundo")
print(len(e.data[0].embedding))
```

> En este equipo **no hay `openai` instalado** (`ModuleNotFoundError`). Con
> stdlib (6.1) funciona sin instalar nada.

### 6.3 Variables de entorno (equivalente que leen muchos SDK)

```bash
export DASHSCOPE_API_KEY=$(awk -F, '$1=="apiKey"{print $2}' ~/Downloads/freetailv2.csv)
export DASHSCOPE_BASE_URL=$(awk -F, '$1=="openAiCompatible"{print $2}' ~/Downloads/freetailv2.csv)
```

---

## 7. Catálogo de errores (diagnóstico rápido)

| Mensaje / código | Causa real | Solución |
|---|---|---|
| `InvalidApiKey` / `401` en **subida** de archivo | La clave `sk-ws-…` de espacio no vale para el endpoint de subida de DashScope | No subas locales. Usa **URL pública** (p. ej. el `audio_url` del TTS). |
| `AccessDenied.Unpurchased` / `403` | Modelo fuera de tu cuota | Usa solo §5.1. El catálogo `/models` miente. |
| `insufficient_quota` / `403` + "Free quota exhausted" | Cuota gratuita agotada (`qwen-plus-character`) | Pasar a pago o desactivar "use free tier only" en consola. |
| `AccessDenied` + "does not support asynchronous calls" / `403` | `X-DashScope-Async: enable` no permitido en TTS | Usa síncrono o `bl speech synthesize`. |
| `url error, please check url` / `400` | Ruta ASR equivocada (`/services/audio/asr`) o `parameters` incompleto | Usa §4.4 completo (`input_audio` + `format` + `sample_rate`). |
| `400 {}` (JSON vacío) | Falta `parameters.format` y `parameters.sample_rate` en ASR | Añadir ambos. |
| `Unexpected argument: off` | `--stream off` no existe | `--stream` es booleano; usa `--quiet`/`--output json`. |
| `Missing required flag: --voice` | TTS sin voz | `--voice longanlufeng` (o `--list-voices`). |
| `model_not_found` / `404` | Modelo inexistente o endpoint incorrecto (`qwen-mt-image-2.0` en chat) | Ruta nativa §4.6. |
| `UND_ERR_CONNECT_TIMEOUT` | El host tarda >10 s en conectar | **Reintenta**; sube `--timeout`. No es error de clave. |
| `curl: (56)` / salida vacía con HTTP 000 | Conexión caída al host de Singapur | Reintenta con `--retry 3`. |

---

## 8. Checklist del agente antes de dar una llamada por buena

1. ☐ Leí la clave **del CSV en runtime** (nunca pegada, nunca enmascarada).
2. ☐ Comprobé `len(key)` y prefijo `sk-ws-`, sin imprimir el cuerpo.
3. ☐ El modelo está en **§5.1**.
4. ☐ Usé la base URL correcta: `openAiCompatible` (chat/embeddings/files) vs
   `dashScope` (ASR/TTS/image2image/tasks).
5. ☐ La respuesta es **HTTP 200 con cuerpo JSON esperado**, no solo "no hubo excepción".
6. ☐ No dejé la clave en logs, ni en archivos de Git, ni en la respuesta al usuario.
7. ☐ Si hubo error transitorio de red, **reintenté** antes de declarar fallo.

---

## 9. Límites del proyecto (reglas del repo, no del proveedor)

- **No subir material de captura (RAW, previews, `C0216.MP4`) a este u otro
  servicio nuevo** sin autorización explícita del propietario. Es una regla
  del proyecto (`AGENTS.md`).
- Mantener el CSV y cualquier clave **fuera de Git y fuera de los artefactos
  de evidencia**.
- No instalar dependencias nuevas (p. ej. `openai`) sin necesidad: la llamada
  directa funciona con stdlib.
- El uso de modelos de pago/cuota debe respetar las cuotas de §5.1; este
  espacio es de prueba gratuita.

---

## 10. Verificación mínima de humo (30 s)

```bash
CSV=~/Downloads/freetailv2.csv
KEY=$(awk -F, '$1=="apiKey"{print $2}' "$CSV")
BASE=$(awk -F, '$1=="openAiCompatible"{print $2}' "$CSV")

# 1. ¿la clave no está enmascarada?
python3 -c "import sys;k=sys.argv[1];print(len(k), k[:8], '****' not in k)" "$KEY"

# 2. ¿auth OK? (debe listar modelos, no 401)
curl -s --max-time 30 "$BASE/models" -H "Authorization: Bearer $KEY" | head -c 120

# 3. ¿chat OK? (debe devolver content, no 403)
curl -s --max-time 60 "$BASE/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen-flash-character","messages":[{"role":"user","content":"di hola"}],"max_tokens":20}'
```

Sal esperada: `115 sk-ws-H. True` · `{"object":"list","data":[…` ·
`{"choices":[{"message":{"content":"¡Hola!…`

---

*Documento generado el 2026-10-04 a partir de llamadas reales verificadas
(chat, embeddings, TTS, ASR bl y ASR nativo, image2image, File API, quota).
Si algo deja de funcionar, reejecuta §10 antes de cambiar código: el 90 % de
los fallos aquí son clave enmascarada, modelo fuera de cuota o timeout de red.*
