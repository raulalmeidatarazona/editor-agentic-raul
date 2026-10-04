# D003 — Deterministic terminology-correction layer for transcripts

**Status:** Proposed\\\
**Date:** 2026-10-04\\\
**Related features / root documents:** [F003](../features/F003-time-aligned-transcription/plan.md),
[tech-stack §7](../../tech-stack.md), [Constitution §22/§29](../../constitution.md),
[D002 accepted](D002-initial-f003-stt-provider.md)

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
2. The layer preserves what was spoken: the original recognition and its timing
   remain recoverable alongside the correction. It rewrites text for display and
   downstream consumers; it never alters retained provider responses.
3. It never invents speech and never conceals uncertain timing. A correction
   requires an existing recognized token at a known interval; it cannot add words
   or move boundaries.
4. It is auditable per Content Project and reviewable by the owner, matching the
   proven approach already validated in production use.
5. Provider selection stays replaceable (D002). This layer is what makes the
   provider choice non-critical for terminology, instead of hunting for a model
   that gets rare terms right unaided.

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
