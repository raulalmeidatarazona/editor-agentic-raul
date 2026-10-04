# Raúl Almeida Agentic Video Studio — Tech Stack

**Version:** 0.2  
**Status:** OWNER_APPROVED architectural direction; runtime unvalidated  
**Owner:** Raúl Almeida  
**Documentation checked:** 2026-10-04  
**Target environment:** macOS, approximately 16 GB RAM

## 1. Responsibility and authority

This document records technology roles, selection rationale, replaceability,
and evidence needed before implementation relies on them. It complements
[mission.md](mission.md) and remains subordinate to [constitution.md](constitution.md).
[roadmap.md](roadmap.md) schedules the validation work.

The current product is Raúl Almeida's personal-brand production pipeline.
AR Solución Digital is a separate potential derivative, not the current brand
configuration or an implementation requirement.

Approval here permits a technology to be considered for its stated role. It does
not establish that a particular version, account, model, integration, or real
recording has passed a runtime test. No dependencies are installed by this
specification foundation.

## 2. Decision vocabulary

- **Core:** a required capability or architectural contract. Replacing its
  implementation must preserve that capability and constitutional behavior.
- **Preferred:** the initial implementation choice, subject to evidence.
- **Optional:** use only when a concrete production need justifies it.
- **Replaceable:** isolate vendor/tool details so replacement does not rewrite
  core content artifacts. This can also describe a Preferred choice.
- **Experimental:** a candidate requiring a bounded proof before production use.

| Role | Direction | Classification | Rationale / boundary |
| --- | --- | --- | --- |
| Production orchestration | Hermes Agent by Nous Research | Preferred; Replaceable | Skills, reasoning, tools, and file operations; durable artifacts remain outside agent memory |
| Coding/reasoning access | Alibaba Cloud Coding Plan | Preferred for permitted interactive work; Replaceable; conditional | Initial provider target; service restrictions prevent assuming unattended production eligibility |
| Composition/rendering | HyperFrames, initially through its CLI | Preferred; Replaceable behind composition boundary | HTML-based source, preview, checks, and local rendering |
| Visual primitives | HTML, CSS, SVG | Preferred | Readable, configurable technical visuals with low complexity |
| Styling and motion | Tailwind CSS; GSAP | Preferred | Consistent styling and controlled motion where needed |
| Additional animation | Lottie, Anime.js, Web Animations API | Optional | Only where they simplify an actual visual requirement |
| 3D | Three.js | Optional; Experimental until fixture-tested | Only if SVG and simpler motion cannot explain the concept adequately |
| Deterministic media operations | FFmpeg; ffprobe | Core tooling direction | Media inspection, transformations, encoding, and audio/video handling |
| Speech-to-text | Cloud STT behind a provider adapter | Core capability; vendor Replaceable and unselected | Avoid local heavyweight inference; normalize timestamps and terminology |
| Content persistence | Local files within a Content Project | Preferred | Recoverable intermediate artifacts without a new application database |
| External media | Existing Envato Elements subscription | Optional; Replaceable | Supporting assets with project-level provenance and license evidence |
| UI visuals | Existing FlyonUI Pro license | Optional; Replaceable | Application/dashboard visuals when useful; not required for diagrams or a review UI |
| Brand behavior | Structured configuration, e.g. future `brand/brand.json` | Core architectural direction | Components consume shared tokens rather than scattered constants |
| Heavy generative media / hosted rendering | Individually selected cloud services | Optional; Experimental | Require production benefit, affordability, and explicit validation |

“Core tooling direction” does not make a software vendor constitutionally
immutable. A replacement needs an explicit technical decision and evidence.
Remotion is superseded as the preferred renderer; it is not a parallel baseline.
Reconsider rendering tools only if the HyperFrames proof reveals a material gap.

## 3. Agent and orchestration

Hermes Agent is the preferred initial environment for executing production
procedures, reasoning over transcripts, creating storyboards, invoking tools,
manipulating project files, coordinating stages, and interpreting feedback.
Its official documentation describes skills, terminal/file tools, and custom
model-provider integration. These are documented surfaces, not evidence that
our video workflow is already implemented. See the [skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills),
[tool registry](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools),
and [provider documentation](https://hermes-agent.nousresearch.com/docs/integrations/providers).

Before relying on Hermes, validate one permitted interactive session using the
selected model, tool invocation, bounded file edits, an external command, and
saved artifacts recoverable in a later session. Failure handling, retries,
resume behavior, and correction loops require project-level specifications.
Do not assume a transaction system or durable production state machine exists
because the agent supports tools or persistent memory.

Agent memory may support operation; the Content Project is the source of truth
for production decisions and artifacts. Agent-created knowledge must not
silently amend the Constitution, brand policy, or approval rules.

Conceptual responsibilities to evaluate in feature specifications are:

| Possible skill | Responsibility to validate |
| --- | --- |
| `video-director` | Semantic structure, editorial purpose, storyboard and layout intent |
| `video-editor` | Retake cleanup and edit instructions that preserve valid speech |
| `technical-visualizer` | Correct, legible explanations using reusable visual components |
| `asset-manager` | Asset selection, local references, provenance and license evidence |
| `video-qa` | Applicable checks, evidence, warnings and unresolved review questions |

These names are conceptual boundaries, not implemented skills or a requirement
for five independently running agents. Avoid a monolithic skill; also avoid
premature delegation infrastructure.

## 4. Model provider and Coding Plan constraint

Alibaba Cloud Coding Plan is the initial target for interactive coding/reasoning.
Its documentation lists model families including Qwen, GLM, Kimi, and MiniMax,
and publishes a Hermes integration guide. Exact models, endpoints, quotas, and
account availability must be rechecked at implementation. [Coding Plan overview](https://www.alibabacloud.com/help/en/model-studio/coding-plan),
[Hermes integration](https://www.alibabacloud.com/help/en/model-studio/hermes-agent).

**Material finding:** the Coding Plan documentation restricts its key to
interactive use in programming tools and excludes automated scripts, application
backends, and other non-interactive scenarios. Hermes compatibility does not
establish eligibility for an unattended video-production pipeline. Use the plan
only within documented permitted use. Before automating model calls, establish
an eligible API service, or obtain explicit provider clarification for the
intended workflow. A metered API is a candidate, not a selected or budget-approved
fallback. This remains an implementation gate, not a reason to change the
provider-independent domain. [Usage restrictions](https://www.alibabacloud.com/help/en/model-studio/coding-plan).

Model and provider choices must live in environment/provider configuration.
Transcripts, storyboards, visual intent, and QA artifacts must not require an
Alibaba response shape. Benchmark candidates later on instruction following,
tool use, code correctness, valid artifact generation, latency, cost, and
correction iterations. Visual understanding and image/video generation are
different capabilities; family names do not establish either capability.
Generative media requires a separately verified tool/service when justified.

## 5. Composition and rendering

HyperFrames is the preferred primary composition system. Its documentation
describes ordinary HTML composition source, timed media, preview, CLI checks,
and render operations; its project model supports seekable compositions and
reusable parts. Start at the CLI boundary; SDK/Player integration is optional.
[Developer guide](https://hyperframes.heygen.com/developers),
[project model](https://hyperframes.heygen.com/concepts).

Local rendering does not consume HeyGen credits according to the
[official quickstart](https://hyperframes.heygen.com/quickstart). This does not
make agent inference, STT, generated media, or optional hosted services free.
The [official CLI repository](https://github.com/heygen-com/hyperframes/blob/main/packages/cli/README.md)
lists Node.js 22 or later and FFmpeg as requirements. Verify and pin the actual
compatible runtime/tool versions during implementation; browser provisioning
and local resource use remain part of the proof.

Prefer HTML/CSS/SVG and GSAP for technical explanation. Tailwind is the preferred
styling helper where useful, rather than an obligation to introduce a larger
application framework. Lottie, Anime.js, Web Animations API, and Three.js need
a concrete reason. Do not use 3D for a concept adequately explained with SVG
and GSAP. Motion must be controllable by composition time and behave consistently
in preview and rendering; validate the selected animation integration.

The decisive proof uses real footage, original speech, one explanatory visual,
captions, and a 1080 × 1920 render. Check video seeking, edit boundaries, A/V sync,
caption timing, safe zones, font availability, preview/export consistency,
rerender behavior, peak memory, and render time on the 16 GB Mac. Documentation
support alone is not a successful production proof. HyperFrames checks supplement
project QA; they do not establish technical truth or human approval.

## 6. Media processing and timing

Use FFmpeg for deterministic encoding, cropping, resizing, audio extraction,
transformations, and muxing. Use ffprobe to inspect containers, streams, dimensions,
rotation/orientation metadata, duration, frame-rate information, and audio
properties. [FFmpeg reference](https://ffmpeg.org/ffmpeg.html),
[ffprobe reference](https://ffmpeg.org/ffprobe.html).

Ingestion should preserve the original recording and produce derived artifacts
for processing. Detect rotated footage and variable frame rates rather than
assuming stored pixel dimensions describe the viewing orientation. Features
will specify any normalization needed; silent upscaling does not prove usable
image quality.

Editing creates a delivery timeline different from the source timeline. Preserve
the relationship between them so captions, visuals, and audio follow retained
speech after retakes are removed. Deterministic software applies validated edit
instructions; AI may propose them. Exact time representations, boundary tolerances,
frame-rate policy, codec settings, and mappings belong in feature specifications.

## 7. Speech-to-text

**Amended 2026-10-04** under the Architecture row of the change-control table,
after explicit owner acceptance (see the amendment record at the end of this
document and [D003](specs/decisions/D003-terminology-correction-layer.md)).

No STT engine is a baseline *requirement*. The baseline requirement is the
provider-independent contract: `source-transcript v1` plus the
`source-presentation-v1` clock, reached through a small replaceable adapter, so
no downstream consumer parses a vendor. Which engine produced a given
transcript is recorded per Content Project and is a configuration choice, never
an architectural assumption. This keeps Constitution §35 (provider independence)
and §36 (never assume heavyweight local speech models) both satisfied: a machine
without any local speech model still works through the cloud adapter, and a
machine that already has one is not forced to pay or to transport audio.

Engine selection is by measured evidence on the real fixture, not by price tier
or by novelty. The comparison recorded for the C0216 fixture (232.8 s, F003
preflight-p8) is the reference case:

| | local Whisper (mlx, large-v3-turbo) | cloud qwen-audio-3.1-asr-flash-filetrans |
| --- | --- | --- |
| cost | 0 | USD 0.00113 |
| wall time | 11.6 s | ~10 s job, plus private object transport and its gates |
| words | 468 | 470 after deterministic sub-word reconstruction |
| mutual WER | 5.48% global across the five r1 windows | — |
| `idempotencia` | missed (`impotencia`) | missed (`en potencia`) |

Both engines miss the same rare technical term, so neither buys terminology
accuracy. Local ASR, when already installed, is therefore the preferred path for
iteration, preview and cross-checking, because it removes paid transport,
signed-URL TTL windows, account activation and per-call authorization from the
inner loop. Cloud STT remains fully supported and is the recorded provider for
the F003 canonical transcript, whose request, sanitized response, usage and cost
are retained for audit.

Terminology correctness is never expected from the engine. It is produced by the
deterministic, human-reviewed correction layer defined in D003, applied after
normalization and before any consumer. Corrections are data owned by a reviewer,
they change text only, and they never move a boundary, invent a word or delete
one; the recognized text and its timing stay recoverable. This is how
`tech-stack` §7's existing requirement — "corrected technical terminology while
preserving what was spoken" — is actually met.

The review that produces those corrections is visual, not transcript-reading:
the owner plays an assembled preview with per-word karaoke in the browser
timeline, reads and listens at once, and states corrections in natural language
with approximate time. No final render is required for that review.

F003 initially evaluated qwen-audio-3.1-asr-flash-filetrans in Alibaba Model
Studio Singapore / International through a replaceable adapter. Selection was
conditional on the approved F003 real-fixture validation; that validation is
recorded in the F003 plan. The `source-transcript v1` contract and the
`source-presentation-v1` mapping belong to F003, not to Alibaba. One approved
fixture request, private owner-managed audio transport, retained sanitized
provider responses, and usage/cost reconciliation are defined in the F003 bundle
and D002. No permanent provider is selected, and no F004 policy is selected
here.

The normalized format must support:

- segment timestamps and text;
- word timestamps when available;
- confidence when available, without fabricating missing values;
- language;
- corrected technical terminology while preserving what was spoken;
- a recoverable relationship to the original source timing and provider result.

Select an engine through a real-fixture comparison of technical vocabulary,
language accuracy, word timestamps, price, latency, and API simplicity. Recording
language is not assumed from the language of these documents. Corrections to
recognized terminology must not manufacture speech or conceal uncertain timing;
they are applied by the D003 layer, never by editing the canonical transcript or
by asking the model to "get it right".

**Integration finding (amended 2026-10-04):** HyperFrames' documented
transcription command uses local Parakeet when installed and falls back to
Whisper, and it also documents import of subtitle/transcript files. Two points
still hold and one is corrected. Still holding: renderer-specific import formats
are lossy, so the domain transcript must remain richer than any of them, and the
renderer's default engine must not become this project's canonical provider by
accident. Corrected: the earlier claim that a local engine is "unsuitable as the
baseline STT path" is withdrawn. The measured C0216 comparison (preflight-p8)
shows a local Whisper run matching the paid cloud transcript at 5.48% mutual WER
at zero cost and zero transport, and both engines miss the same rare term. Local
ASR is therefore suitable for iteration, preview and cross-check; the canonical
transcript records whichever engine was actually used.
[HyperFrames audio/transcription guide](https://hyperframes.heygen.com/guides/voice-and-audio).

## 8. Brand configuration and studio capture calibration

Structured brand configuration should eventually control colors, semantic
colors, typography, code theme, captions, spacing, diagrams, transitions, CTA
presentation, and safe zones. `brand/brand.json` is an example, not a schema
commitment. The palette in Constitution Sections 15–16 remains authoritative;
do not duplicate its constants across components.

Camera/human safe zones and platform occlusion zones are distinct calibration
concerns. Both are configurable and validated against real footage and intended
delivery contexts. Neither receives invented pixel coordinates here.

The studio's two RGB lights have the following **starting calibration targets**,
moved from Constitution Section 17 without changing their values:

| Light | Direction | Hue | Saturation | Brightness |
| --- | --- | --- | --- | --- |
| A | Forest / Teal | 155° | 65% | 35% |
| B | Oxide / Warm | 18° | 70% | 30% |

These are physical-light settings, not software color tokens. Calibrate against
the actual lamps, background, Sony ZV-E10, exposure, and complete lighting setup.
Store validated results in capture configuration. They apply only to STUDIO;
MOBILE brand consistency comes from composition, not reproducing the background.

## 9. Visual Library

Build reusable, configurable parts just in time for real videos. Possible future
domains are `architecture/`, `golang/`, `distributed-systems/`, `database/`, `ui/`,
and `generic/`; these are a taxonomy direction, not folders to scaffold now.

Examples of future concepts:

| Domain | Illustrative concepts |
| --- | --- |
| Architecture | LoadBalancer, ApiGateway, Microservice, Database, Cache, MessageQueue, EventBus |
| Go | Goroutine, Channel, WaitGroup, ErrGroup, Mutex, WorkerPool |
| Distributed systems | CircuitBreaker, Retry, Backpressure, Replication, Sharding |
| Databases | Query, Index, Transaction, Lock |
| UI | Dashboard, Terminal, Browser, CodeEditor, Metrics |
| Generic | Timeline, Comparison, Flow, Counter, Callout, CodeHighlight |

Semantic intent and reusable component behavior should be separate from a
specific renderer. This does not require dual renderer implementations or a
universal component framework. Define the minimum useful component contract in
the feature that needs it. Correctness, readability, configuration, and proven
reuse matter more than catalog size.

## 10. Assets and optional UI components

Use the existing [Envato Elements subscription](https://elements.envato.com/)
when music, SFX, B-roll, icons, or illustrations improve a specific production.
Prefer internal technical visuals for explanations they express more clearly.

Keep asset origin, item reference, local file, license evidence, and association
to each Content Project traceable. Envato documents separate licenses for
separate end uses; cached files alone are not license evidence for another video.
Verify applicable terms when acquiring/reusing assets. Start with manual acquisition
and evidence capture if necessary; no automated download or registration API is
assumed. [Envato license creation](https://help.elements.envato.com/hc/en-us/articles/360000621763-Create-new-license).

[FlyonUI Pro](https://flyonui.com/pro) is available under an existing license,
but optional. It may simplify dashboards, SaaS screens, metrics, tables, admin
screens, or application mockups; technical diagrams generally remain HTML/SVG/CSS
with GSAP. Validate any selected component's dependencies, license applicability,
and render behavior before incorporating it. Ownership of a license does not
justify introducing a dashboard or extra runtime dependencies.

## 11. Modular architecture and recoverable artifacts

Prefer small contracts around the following responsibilities:

| Responsibility | Architectural role |
| --- | --- |
| Capture | Studio/Mobile source and calibration context |
| Ingestion | Media validation and Content Project creation |
| Transcript | Provider-independent speech and source timing |
| Editorial analysis | Retakes, meaning, technical questions and editorial intent |
| Storyboard | Inspectable narrative blocks and layout intent |
| Visual specification | Explanation requirements separate from rendering mechanics |
| Visual Library | Selection/configuration of reusable concepts |
| Asset management | Local references, provenance and license evidence |
| Composition | Bind edited footage and visuals to delivery time |
| Captions | Validated spoken text, grouping, timing and collision handling |
| Audio | Clear original voice and optional subordinate supporting sound |
| QA | Hard failures, warnings, evidence and human-only judgments |
| Render | Preview and checked delivery artifacts |
| Human feedback | Explicit approval and scoped revision requests |
| Performance feedback | Imported/manual audience evidence and editorial learnings |

These are responsibilities, not microservices. Begin with local files and
ordinary tool invocations. No new product database, queue, web API, hosted worker,
or review application is selected. An orchestration tool's own internal storage
does not become the product's domain database.

Features must define schemas, filesystem conventions, source/delivery timing,
revision tracking, retry limits, selective regeneration, and error behavior.
Store enough input/output and configuration context to investigate a production
and resume it; do not promise identical AI outputs on reruns. Deterministic
render execution and preservation of the approved source revision are the goals.

F002 uses Python 3.14.7 with the standard library and the existing FFmpeg/ffprobe
9.0.1 tools for local ingestion and inspection. Its versioned JSON source and
inspection contracts, owned byte-identical source copy, and source-presentation-v1
clock are defined by the accepted F002 bundle and D001. This does not select a
universal pipeline language, STT provider, normalization policy or renderer API.

Owner acceptance: F002 r1 / ae36327, explicitly including
[D001](specs/decisions/D001-local-source-contract.md); recorded in
[the F002 plan](specs/features/F002-content-project-ingestion/plan.md).

F003 r1 / 74aaa0b and [D002](specs/decisions/D002-initial-f003-stt-provider.md)
extend the existing Python 3.14.7 standard-library and FFmpeg/ffprobe 9.0.1
runtime narrowly to F003 preparation, cloud adapter and normalized transcription.
Raúl explicitly approved this limited resolution; no universal language decision
or new dependency installation is authorized.

## 12. Local resources, security, and cost

The baseline Mac has approximately 16 GB RAM. Local work includes orchestration,
the required runtimes, browser rendering, FFmpeg, lightweight scripts, and file
operations. Cloud services handle heavy AI. Local LLMs, Whisper, Stable Diffusion,
generative video, and powerful GPUs are not baseline requirements. Bound browser
and render concurrency through measurement; no concurrency count is fixed here.

No API keys, tokens, or credentials may enter the repository, project artifacts,
or committed logs. Use environment configuration or the tool's supported external
secret mechanism. A future `.env.example` documents names and placeholders only.
Exact provider settings and RAW retention/cloud-upload handling belong to the
relevant feature specifications.

Prefer existing subscriptions, open-source tools, and deterministic local
processing. Measure per-video AI/STT use and render resources. Distinguish
existing subscription cost from incremental cost and subscription quotas from
available runtime capacity. New recurring services must satisfy Constitution
Section 37; model fallback must not silently introduce a paid service or
unbounded retry cost.

## 13. Validation gates and deferred decisions

| Gate | Required evidence | Scheduled by roadmap |
| --- | --- | --- |
| Representative input | Real portrait fixture, actual audio, retake and calibration movement | Phase 1 |
| STT fit | Technical terms and usable source timing; word-timing limitations explicit | Phase 3 |
| Model/orchestration fit | Permitted provider use, selected account/model, tools and recoverable artifacts | Before model-dependent work in Phases 4–5 |
| Renderer fit | Real-footage vertical short, correct media/timing and acceptable resources | Phase 6 |
| Review integrity | Approval bound to checked delivery revision; corrections rerun QA and review | Minimal in Phase 6; hardened in Phases 12–13 |
| Repeatability | Multiple real videos with measured effort, cost and failures | Phase 14 |

Pending technology choices are not blockers to reviewing these root documents.
They become blockers when an implementation depends on them. Deferred decisions
include STT vendor, model IDs and benchmarks, eligible production API billing,
runtime/version pins, programming language for later glue code beyond F002, transcript/edit schemas,
codecs/frame rate/loudness targets, brand typography and safe-zone values,
component APIs, QA tolerances, reviewer access mechanism, and platform variants.

No evidence currently justifies a different personal-brand mission or a broader
platform. Runtime suitability of the chosen stack remains to be demonstrated.

---

## Amendment record — 0.2 (2026-10-04)

Approved by Raúl Almeida, literal: «es momento de hacer KISS el proyecto, asi que
D003 aprovado y listo modificalo para continuar, modificar el tech-stck,
aplicatodo lo necesario para avanzar con KISS». Recorded under the Architecture
row of the change-control table in `specs/README.md`, which requires explicit
owner acceptance before root documents change and requires affected plans to be
reapproved.

- §7 rewritten. Cloud STT is no longer the baseline requirement; the baseline
  requirement is the provider-independent transcript contract. Engine choice
  becomes measured configuration per Content Project. The prior claim that a
  local engine is unsuitable is withdrawn on measured evidence.
- Grounding evidence: F003 preflight-p8 real-fixture comparison on C0216
  (232.8 s). Local Whisper 0 EUR / 11.6 s / 468 words vs cloud qwen filetrans
  USD 0.00113 / 470 words; mutual WER 5.48% global across the five r1 windows;
  both engines miss `idempotencia`.
- §7 now names the D003 correction layer as the mechanism that actually delivers
  "corrected technical terminology while preserving what was spoken", and the
  visual review over an assembled browser preview as the way corrections are
  produced.
- Constitution untouched. §7 was worded so local ASR stays optional and never a
  requirement, keeping §36 ("MUST NOT assume heavyweight local speech models")
  intact, and §35 (provider independence) is reinforced rather than relaxed.
- §12 unchanged: no new dependency is added to the baseline, and nothing here
  authorizes installing a speech model on a machine that lacks one.

Not authorized by this amendment: any new feature implementation, F004
(retake detection), semantic storyboarding, captions or rendering. Those follow
their own PLAN → approval → IMPLEMENT gates.
