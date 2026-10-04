# D003 — Deterministic terminology-correction layer for transcripts

**Status:** Accepted — owner approval below\\\
**Date:** 2026-10-04 (accepted 2026-10-04)\\\
**Related features / root documents:** [F003](../features/F003-time-aligned-transcription/plan.md),
[tech-stack §7](../../tech-stack.md), [Constitution §22/§29](../../constitution.md),
[D002 accepted](D002-initial-f003-stt-provider.md),
[diagnóstico 006](../../docs/F003-vs-MotionGraphics-diagnostico.md)

## Owner feedback that reshapes this decision (literal, 2026-10-04)

> «prefiero corregir viendo y escuchando el video con los subtitulos ya puestos
> para leer y escuchar a la vez, nisiquiera tiene que estar el video renderizado
> con que pueda validarlo en el studio en el navegador en el timeline sin
> problema le doy al play y en lenguaje natural digo lo que se debe correr y el
> tiempo aproximado»

Consequence: the correction table is the OUTPUT of a visual review over an
assembled preview, never a pre-condition for assembling it. The text is not
finalized before montage. This inverts the r1 assumption that a literal human
reference must exist before the provider call.

The validated mechanism for that review already runs as the p9 spike:
HyperFrames Studio over a proxy, karaoke per word, corrected words visually
marked. The owner plays it, reads and listens at once, and dictates corrections
in natural language with approximate time ("son estas palabras en lugar de estas
en más o menos este segundo"). The agent turns that into table entries.

## Context

F003 spent its single authorized paid STT request on the real C0216 fixture and
obtained a genuine, retained result. Measured against an independent local
oracle (Whisper large-v3-turbo, 0 EUR, 11.6 s), lexical accuracy is good: global
WER 5.48% across the five r1 windows, threshold 10%.

One r1 criterion still fails, and the cause is not the provider. The spoken term
`idempotencia` was misrecognized by every engine tested on this recording:

| Engine | Output | Evidence |
| --- | --- | --- |
| qwen-audio-3.1-asr-flash-filetrans (paid, hotword weight 1 sent) | `en potencia` | F003 p7c/p8 |
| Whisper large-v3-turbo (local, free) | `impotencia` (p=0.744) | p8 oracle |
| Whisper large-v3-turbo (owner's MotionGraphics pipeline) | `diampotencia` (p=0.663) | `specs/006-arquitectura` |

The F001 handoff had already predicted this exact word and these exact variants
as UNCERTAIN. Sending hotwords did not fix it. Three independent runs confirm
that rare technical vocabulary is not reliably recoverable by the acoustic model
alone, regardless of price.

The owner's other project already solved this at zero cost, and solved it
without a better model: `MotionGraphics/specs/006-arquitectura/edit.json` carries
a human-authored `captionCorrections` table
(`diampotencia`→`idempotencia`, `RP`→`ERP`, `check-out`→`checkout`), each entry
with `sourceStart`, `original`, `replacement` and `reason`. That deterministic,
reviewed layer is what produced exact karaoke captions.

Constitution §22 states that incorrect transcription of critical technical
terminology is a QA failure, and §29 lists it among hard failures blocking
PRODUCTION_APPROVED. tech-stack §7 already requires the normalized format to
support "corrected technical terminology while preserving what was spoken" and
warns that "corrections to recognized terminology must not manufacture speech or
conceal uncertain timing".

The F003 r1 bundle has no such layer. It treats the provider output as needing
to be terminologically correct on its own, which the evidence shows is not
achievable. This is a specification gap, not an implementation defect.

## Proposed decision

Introduce a **deterministic, human-reviewed terminology-correction layer** in
the provider-independent transcript domain, applied after normalization and
before any consumer (captions, semantic analysis, editing):

1. Corrections live in configuration/data, never in provider or editorial code.
   Each entry carries: source interval, recognized text, corrected text, reason,
   and the human who approved it.

   Proven schema (verbatim from `MotionGraphics/specs/006-arquitectura/edit.json`,
   three real entries): `sourceStart` (seconds in the SOURCE clock), `original`
   (exact recognized token), `replacement`, `reason`. Proven match rule
   (`build_006.py:211-214`): `abs(w['start'] - corr['sourceStart']) < 0.2 and
   text == corr['original']` — a time window plus exact text, never an index or
   a position. This project adds `reviewer` and keeps both source and output
   clocks, per `source-presentation-v1`.
2. The layer preserves what was spoken: the original recognition and its timing
   remain recoverable alongside the correction. It rewrites text for display and
   downstream consumers; it never alters retained provider responses. Matching
   the proven implementation, a correction changes text ONLY; it never moves a
   boundary.
3. It never invents speech and never conceals uncertain timing. A correction
   requires an existing recognized token at a known interval; it cannot add words
   or move boundaries.
4. It is auditable per Content Project and reviewable by the owner, matching the
   proven approach already validated in production use.
5. Provider selection stays replaceable (D002). This layer is what makes the
   provider choice non-critical for terminology, instead of hunting for a model
   that gets rare terms right unaided.
6. The review that produces the table is VISUAL, over an assembled preview with
   per-word karaoke in a browser timeline (HyperFrames Studio). No final render
   is required for the owner to review. Corrected words are visibly marked so the
   owner sees what the layer already changed.

Ownership and feature boundary must be assigned by the owner: the layer is
arguably part of F003's normalization surface or a new feature preceding
captions/F004. This record does not decide that; it proposes the architectural
shape and requires explicit acceptance before adoption.

## Alternatives and justification

- **Switch to a better ASR model.** Rejected: three engines already disagree on
  this word, and the owner's free pipeline reached the same result. Cost rises,
  the failure class remains.
- **Raise hotword/vocabulary weight and re-run the paid call.** Rejected as a
  solution: hotwords were already sent and did not work; a second paid run
  consumes new budget and changes the request fingerprint, requiring separate
  authorization, with no evidence it would succeed.
- **Relax the V-08 terminology criterion.** Rejected: it retrofits acceptance
  criteria to excuse a real defect, which project rules forbid, and Constitution
  §22/§29 treat wrong technical terminology as a hard QA failure for good
  reason — captions would ship the error.
- **Manual correction per video with no stored layer.** Rejected: not reusable,
  not auditable, contradicts Constitution §7 (build once, configure, reuse).

## Consequences

Benefits: terminology becomes deterministically correct and auditable; provider
choice stops being a correctness bottleneck; the owner's proven workflow is
adopted instead of reinvented; future features (captions, retake detection)
inherit corrected text without each re-solving the problem.

Costs and risks: the correction table is human-maintained work per project; a
wrong correction silently changes meaning, so entries need reason + reviewer and
must not touch timing; the layer must be tested to prove it cannot add words or
shift boundaries; the canonical transcript changes, so a new normalization
version is required and prior revisions must remain immutable.

Validation implications: F003's V-08 terminology component cannot pass on
provider output alone. Either this layer is adopted and V-08 is re-evaluated
against corrected output, or V-08 is recorded as a real, permanent FAIL with the
reason documented. The measured WER component (5.48%) is unaffected.

Affected specifications: tech-stack §7 (already anticipates corrected
terminology), the F003 feature files if the layer lands there, and the future
captions/semantic features. No constitutional amendment is proposed.

## Acta real de aceptación (2026-10-04)

Owner approval, literal: «es momento de hacer KISS el proyecto, asi que D003
aprovado y listo modificalo para continuar, modificar el tech-stck, aplicatodo
lo necesario para avanzar con KISS, en el studio todo esta bien continua. que
sigue todo esta aprovado modificalo tienes mi aprovacion YOLO»

Scope the owner accepted here, recorded precisely so the blanket wording is not
over-read:

- D003 moves Proposed → Accepted.
- `tech-stack.md` §7 is amended accordingly (Architecture row of the
  change-control table: root documents updated after explicit owner acceptance).
- The layer is implemented as project code with tests, and F003's V-08
  terminology component is re-evaluated against corrected output, which is the
  first of the two paths this record already defined.

Not accepted by this wording, and therefore not done:

- No constitutional amendment. `constitution.md` §36 and §22 are untouched, and
  §7 is amended so that it stays compatible with §36 ("MUST NOT assume
  heavyweight local speech models") by keeping local ASR optional, never
  required.
- No new feature is implemented. F004 (retake detection, roadmap Phase 4) still
  requires its own PLAN and explicit approval of that revision; the SDD sequence
  is PLAN → approval → IMPLEMENT and a blanket authorization does not skip the
  PLAN gate.
- F003 is not DONE. V-16 remains the owner's real acceptance of the evidence
  package.

Implementation delivered under this acceptance:
`tools/terminology_correction.py` + `tests/test_terminology_correction.py`, and
the per-project table at
`.local/projects/f002-studio-001/transcription/terminology-corrections.json`
(data, outside Git-tracked specs, reviewed by the owner).
