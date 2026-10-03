# Raúl Almeida Agentic Video Studio — Roadmap

**Version:** 0.1  
**Status:** OWNER_APPROVED foundation — F001 r1 IMPLEMENT authorized  
**Owner:** Raúl Almeida  
**Updated:** 2026-10-03  
**Priority:** Supply Chain 01 — Quick Ideas → Vertical Native

## 1. Sequencing principle

Build a working vertical slice around one real recording before expanding the
system. The objective is one production-quality short and then repeatable
production, rather than a collection of disconnected subsystems.

[constitution.md](constitution.md) defines the rules;
[mission.md](mission.md) defines the product outcome;
[tech-stack.md](tech-stack.md) records technology direction and validation gates.
This roadmap defines dependencies, proofs, and completion evidence. It does not
authorize implementation during the root-specification session.

All work serves Raúl Almeida's personal brand. AR Solución Digital is a separate
potential derivative and creates no current milestone dependency.

Each phase requires a feature specification, implementation plan, tasks, and
validation appropriate to its scope. Do not create all downstream specifications
before learning from the preceding slice. Phase numbers indicate development
order, not runtime processing order or promised dates. Most work depends on
earlier artifacts; a bounded technology investigation may move earlier if needed
to avoid investing in an unsupported assumption.

## 2. Dependency spine and quality gates

    Root specifications / conventions
      → Real RAW fixture
      → Content Project / media inspection
      → Normalized transcript
      → Retake edits / source-to-delivery timing
      → Semantic storyboard
      → Real-footage render + QA + human confirmation
      → Production hardening
      → Repeatable Studio production
      → Mobile validation
      → Audience feedback

Verify Hermes/model access and service eligibility before model-dependent work;
do not assume Coding Plan permits unattended execution. Prove HyperFrames on
the actual 16 GB Mac before expanding layouts and components.

QA and human review are present from the first rendered slice. Phases 12 and 13
harden automation and reviewer experience; they do not defer constitutional
gates. Initial checks can combine deterministic inspection and explicit human
review. A check that cannot yet be automated is a review responsibility, not an
implicit pass. Missing checks or unresolved hard failures block production
approval; technically incomplete demonstrations remain development previews.

Editorial acceptance of a preview precedes final rendering when useful. The
delivered revision receives applicable QA and explicit human confirmation before
`PRODUCTION_APPROVED`. Regeneration invalidates affected QA/approval and returns
to review. `PERFORMANCE_VALIDATED` requires later audience evidence.

## 3. Phases

### Phase 0 — Foundation / Specification

**Goal:** establish enough product and architecture direction to specify features
without reopening fundamental decisions each time.

**Deliverables:** audited `constitution.md`, `mission.md`, `tech-stack.md`, and
`roadmap.md`, plus [AGENTS.md](AGENTS.md) and the [feature development
protocol/templates](specs/README.md): feature scope, acceptance evidence,
approval gates, plan/task separation, artifact placement, and deliberate amendment
handling. The foundation and conventions received explicit owner approval on
2026-10-03, recorded in [specs/README.md](specs/README.md#phase-0-review-evidence).

**Exit:** the four documents are coherent and owner-reviewed; unresolved choices
have an assigned validation point. Conventions are sufficient to begin the first
feature specification. No application scaffold or pipeline code is required.

**Current position:** Phase 0 is OWNER_APPROVED. Raúl approved F001 bundle r1 and
authorized only F001. The physical STUDIO RAW has arrived; objective metadata,
integrity and full decoding evidence are retained. Recovery is hash-verified; setup, voice and representativeness are owner-confirmed.
Content/movement references are retained; V-01–V-09 pass. Final acceptance of
evidence e5 remains pending (HUMAN_REVIEW). [F001 plan.md](specs/features/F001-real-capture-fixture/plan.md)
records approval, identity and lifecycle. F002 is not authorized.

### Phase 1 — Real Capture Fixture

**Depends on:** Phase 0 review and the first capture-fixture specification.

**Goal:** obtain representative input from the actual STUDIO setup.

Record one short, real portrait explanation containing normal speech, pauses,
one intentional mistake, the standalone “Again” retake protocol, a corrected
take, technical terms, and natural hand movement. Include calibration movements
from Constitution Section 13, within the same recording or an accompanying
calibration fixture. Preserve the original RAW and record capture context.

Delivery compatibility and intelligible source audio matter more than insisting
on 4K. Inspect actual orientation rather than assuming the camera stores portrait
pixels. MOBILE remains an official profile, with additional fixtures and full
validation in Phase 15.

**Exit / unlock:** a stable, representative, playable vertical RAW and human
reference notes identify the intentional mistake, retake, valid speech, terms,
and calibration movements. Ingestion, STT, editing, and layouts can now be judged
against real input.

### Phase 2 — Ingestion + Media Inspection

**Depends on:** Phase 1.

**Goal:** turn the RAW into a recoverable Content Project.

Identify media; probe stream/container metadata, dimensions and rotation,
duration/frame-rate information, and audio; validate the source's suitability;
establish a project workspace and references without modifying the original.
Specify handling for missing/unreadable files, unsuitable framing, or missing
audio. Avoid unnecessary UI and product databases.

**Exit / unlock:** valid input becomes a structured Content Project; invalid or
uncertain input produces an actionable result without pretending to be ready.
The source remains recoverable for transcription and later revisions.

### Phase 3 — Transcription

**Depends on:** Phase 2 and a selected cloud STT provider after fixture comparison.

**Goal:** reliably map speech to source time.

Produce a normalized transcript with segment timestamps, word timestamps when
supported, language, optional confidence, and corrected technical terminology.
Keep the provider behind an adapter and retain the uncorrected source result.
Check the fixture against human reference notes. Where word timing is missing,
make that limitation explicit and assess whether it is adequate for retake cuts
and the initial caption pass.

**Exit / unlock:** retained speech, technical terms, and the retake marker have
usable source-time references. Provider-specific data does not define the domain
artifact. Timing adequacy is demonstrated, enabling safe edit decisions.

### Phase 4 — Retake Detection

**Depends on:** Phase 3; verify Hermes/model tool behavior and eligible provider
use before any model-dependent processing.

**Goal:** apply the initial “Again” protocol without destroying valid speech.

Identify the marker, failed take, and replacement; produce inspectable edit
instructions and apply them deterministically. Preserve the relation between
source time and edited time. Ambiguity must remain visible for review.

Validate the real intentional retake and negative cases such as ordinary use of
“again” and a recording without retakes. Repeated/nested retakes and uncertain
boundaries need explicit feature-level behavior rather than guessed deletions.

**Exit / unlock:** the fixture is cleaned without retained markers, failed takes,
or clipped valid words; the cut decisions can be inspected and the source is
recoverable. Later captions and visuals can follow the edited speech.

### Phase 5 — Semantic Storyboard

**Depends on:** Phase 4 and the model/orchestration validation gate.

**Goal:** convert the cleaned explanation into inspectable editorial intent.

Identify the hook, explanation blocks, conclusion, optional contextual CTA,
purpose of supporting visuals, and layout intent using SPEAKER, SPLIT, VISUAL,
and PIP. Maintain the distinction between semantic decisions and their rendering.
Avoid mandatory layout switching or fixed-duration editing.

**Exit / unlock:** a human can inspect the narrative and proposed visual purposes,
trace them to the source, and see technical uncertainties. The first composition
can be produced without inventing the whole visual system.

### Phase 6 — First HyperFrames Vertical Slice

**Depends on:** Phases 1–5, the permitted model-access path, and compatible local
runtime/tool versions.

**Goal:** prove one real short end to end on the target Mac.

Use the smallest meaningful sequence, for example SPEAKER → SPLIT → SPEAKER,
with real camera footage, original speech, one simple explanatory visual,
captions, basic audio, calibrated initial brand/safe-zone settings, and a final
1080 × 1920 render. Connect cloud transcript/edit timing to the composition;
do not adopt HyperFrames' local STT default.

Include a basic QA report, a watchable review artifact, and explicit human
confirmation. Record render time and peak resource use. Check A/V and caption
sync after retake edits, font/media availability, layout readability, seeking,
preview/export consistency, and a rerender from saved project artifacts.

**Exit / unlock:** RAW → checked rendered branded short works end to end. The
first major technical proof is complete. The short can receive production
approval only if every applicable constitutional requirement is actually met;
otherwise its recorded gaps guide hardening and it remains a development preview.

Do not build all layouts, a broad library, or a reviewer application to reach
this proof. If the renderer fails a material requirement, resolve that finding
through the technology decision before expanding the implementation.

### Phase 7 — Full Visual Grammar

**Depends on:** Phase 6 renderer proof and calibration footage.

**Goal:** validate SPEAKER, SPLIT, VISUAL, and PIP against real capture.

Develop the missing layouts with configured safe zones and brand rules. Check
natural movement, face/body framing, explanatory space, readable code/diagrams,
and caption placement. A video need not use every layout.

**Exit / unlock:** all four states work consistently on representative footage,
including transitions, without forcing arbitrary editorial changes. More kinds
of technical explanation can be composed safely.

### Phase 8 — Dynamic Captions

**Depends on:** Phase 6 caption baseline and Phase 7 layout validation.

**Goal:** production-grade vertical captions.

Harden synchronization, phrase grouping, technical vocabulary, brand styling,
configured safe zones, and collision prevention across the four layouts. Follow
meaning and readability; the constitutional word-count direction is a guideline.
Word-level emphasis requires demonstrated timing quality.

**Exit / unlock:** captions pass applicable automated checks and human review on
real edited recordings, including difficult technical terms and layout changes.

### Phase 9 — Visual Library v1

**Depends on:** Phase 6 reusable visual proof and real content demand.

**Goal:** prove useful reuse, rather than maximize component count.

Extract and stabilize only parts required by actual videos. Go concurrency is a
possible first domain. Candidate concepts include Goroutine, Worker, WaitGroup,
ErrGroup, Error, ContextCancellation, Timeline, and CodeHighlight; select only
what the explanation needs. Define the minimum configuration/versioning behavior
needed to preserve earlier productions while improving a component.

**Exit / unlock:** at least one component is reused across multiple real videos
or meaningfully different configurations with technical correctness and readable
output. Reuse reduces future production work.

### Phase 10 — Audio Pipeline

**Depends on:** Phase 6 original-voice baseline and representative source audio.

**Goal:** consistently clear voice-first sound.

Add only corrective processing needed by real recordings: normalization, EQ,
compression, loudness normalization, and optional subordinate music/ducking.
Use licensed assets with traceable evidence even before the fuller asset manager
exists. Musical silence is a valid choice.

**Exit / unlock:** voice stays intelligible and consistent across representative
recordings, without severe clipping or destructive over-processing. Measurement
targets and human listening checks are defined by the audio feature specification.

### Phase 11 — Asset Manager

**Depends on:** real external-asset demand from the rendered slice/audio work.

**Goal:** use supporting media without losing provenance.

Establish a small local catalog with source/item metadata, project association,
license evidence, and controlled music/SFX reuse. Verify Envato requirements
when reusing an item; manual acquisition/registration is acceptable initially.
External assets remain subordinate to explanatory clarity and reusable visuals.

**Exit / unlock:** a real asset can be selected, used, and located with its
applicable project/license evidence. Missing files or evidence are visible,
without depending on an unverified external asset API.

### Phase 12 — Automated QA

**Depends on:** the checks already operating from Phase 6 and hardened layouts,
captions, audio, and asset handling.

**Goal:** prevent broken production from silently reaching approval.

Automate constitutional hard-fail checks where technically reliable: aspect ratio,
resolution, render completion, missing media/assets, unexpected blank frames,
caption overflow/safe zones, synchronization, audio anomalies, and retake remnants.
Maintain HARD FAIL versus WARNING, and retain explicit human review for semantic
correctness or checks with insufficient automated confidence.

Exercise known faulty artifacts, not only successful videos. Specify bounded
automatic corrections and actionable unresolved failures. Optional CTA/music
or a long period without visual change must not cause forced editing.

**Exit / unlock:** known broken outputs are blocked, warnings remain advisory,
and unknown/unchecked required conditions cannot be reported as passed. Every
approval has applicable check evidence for its delivery revision.

### Phase 13 — Human Review Loop

**Depends on:** the basic review in Phase 6 and the strengthened QA gate.

**Goal:** make routine review usable by the non-technical operational reviewer.

Provide an accessible preview and interpret natural-language correction requests
with temporal context. Change the intended parts, preserve unaffected work,
regenerate, rerun affected QA, and return the new revision for review. Distinguish
explicit approval from no response. Resolve technical questions with Raúl.

Validate representative requests about code size, confusing diagrams, camera
presence, and caption placement. Select the simplest access mechanism that the
reviewer can actually use; build a UI only if repeated workflows establish a need.

**Exit / unlock:** the secondary reviewer can watch, request a normal correction,
and approve the checked result without code or timeline editing. Old approval
cannot silently carry forward to a changed revision.

### Phase 14 — Production-Ready Vertical Native

**Depends on:** Phases 6–13.

**Goal:** repeatable STUDIO production, beyond a demonstration.

Run multiple real Quick Ideas through the complete production/review pipeline,
including a correction and a meaningful component reuse. Measure active human
review/correction time, correction count, render time, AI/STT use and cost, visual
reuse, manual interventions, and automated/human QA failure rates.

The feature specification must define the representative set, sample size,
acceptable effort/cost bounds, and repeatability thresholds before declaring
success. Use earlier measurements to set realistic targets rather than treating
a successful single render as sufficient evidence.

**Exit / unlock:** repeated videos reach explicit production approval within the
agreed criteria; failures can be diagnosed and recovered from saved artifacts.
The Studio path is operationally usable, enabling meaningful Mobile comparison.

### Phase 15 — Mobile Capture Validation

**Depends on:** Phase 14 and real spontaneous MOBILE recordings.

**Goal:** make opportunity capture usable through the same production system.

Test representative variation in lighting, backgrounds, movement, orientation,
audio, and device behavior. Identify Studio assumptions that fail. Adapt capture
profiles, inspection, audio, framing, or configurable layouts rather than creating
a separate editing architecture. If footage is not recoverable to acceptable
quality, report the specific limitation and preserve the idea for another capture.

**Exit / unlock:** Studio and representative Mobile content share the production
pipeline and personal-brand language with explicit input limitations. Supply
Chain 01 is validated beyond the controlled setup.

### Phase 16 — Performance Feedback

**Depends on:** production stability and enough human-published content to assess
editorial hypotheses. Evidence gathering may start earlier; rule changes need
sufficient context and repeated signals.

**Goal:** learn from real audience behavior without building an analytics platform.

Begin with structured manual/imported performance information associated with
the published content revision and editorial hypothesis. Review retention, viewing,
engagement, and other meaningful signals in context. Track what changed and why;
do not optimize blindly toward one metric or infer causality from a single video.

**Exit / unlock:** audience evidence can inform a traceable editorial-rule change
without rewriting core architecture or weakening truthfulness, clarity, or review.
Production approval remains separate from performance validation.

## 4. Future supply chains

**Supply Chain 02 — Deep Topic → Long-Form Authority Content:** begin its detailed
specifications only after Vertical Native provides a stable production foundation.
Prove the new capture/delivery needs while reusing provider-independent artifacts,
review, QA, rendering infrastructure, and suitable visual components.

**Supply Chain 03 — Long-Form → Semantic Repurposing → Vertical Content:** depends
on a stable earlier foundation and suitable long-form sources. Specify semantic
candidate selection, context preservation, and vertical recomposition as future
work; do not implement those mechanisms now.

Neither future chain requires an upfront library expansion, database, platform,
or AR Solución Digital brand profile.

## 5. Recommended first feature specification

**Real Vertical Capture Fixture and Studio Calibration.** This comes before
ingestion implementation because representative source material determines
whether transcription, cuts, layouts, and rendering assumptions are valid.

The specification should define the short recording procedure, required retake
and technical-term content, natural movement/calibration coverage, capture context,
RAW preservation, human reference notes, fixture storage/handling conventions,
and acceptance evidence for playable portrait video and intelligible audio.
It should accommodate practical capture resolution without assuming a specific
camera metadata shape, and distinguish a development fixture from a publishable
production.

After that specification and fixture are accepted, specify **Content Project
Ingestion and Media Inspection**. Detailed transcript/edit contracts, provider
configuration, QA thresholds, safe-zone coordinates, and component APIs belong
to their own dependent features.

The foundation session delivered specifications and conventions only. The owner
then approved Phase 0 and F001 r1 and authorized only F001 IMPLEMENT. The agent
has prepared the local recording workspace; Raúl provides the physical RAW before
validation can continue. No F002, pipeline functionality, dependency installation,
agent/skill creation, STT, retake detection or video composition is authorized.
