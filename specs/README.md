# Development operating system

**Status:** Phase 0 OWNER_APPROVED — F001 r1 IMPLEMENT authorized  
**Owner:** Raúl Almeida  
**Reviewed snapshot:** 2026-10-03

This protocol makes features inspectable and reversible. It implements the
[Constitution](../constitution.md), [mission](../mission.md),
[technology boundaries](../tech-stack.md) and [roadmap](../roadmap.md).
[AGENTS.md](../AGENTS.md) is the session entry point. Specifications and evidence
are durable truth; no model-specific workflow or state-machine software is needed.

## Feature folders and authority

Use the next unused sequential ID, `F001`, `F002`, etc., with a short kebab-case
name. IDs identify features, not roadmap phase numbers. A phase can need several
features; allocate only the next authorized feature, not the entire roadmap.
Never reuse an ID; preserve history when splitting or superseding a feature.

The first feature is **`F001-real-capture-fixture`**, covering real portrait STUDIO
input and calibration under roadmap Phase 1. Ingestion follows its accepted
fixture. Its [current plan](features/F001-real-capture-fixture/plan.md) is the
only authorized feature work. Raúl approved its r1 bundle and authorized F001
IMPLEMENT; its plan records the actual approval and identity. The structure
below is the convention; merely creating files does not authorize implementation.

```text
specs/features/F001-real-capture-fixture/
    requirements.md   # WHAT, invariants, acceptance, open/deferred decisions
    plan.md           # HOW, tasks, state, approval and change history
    validation.md     # predefined proof; later execution evidence and review
```

Copy [requirements](templates/feature/requirements.md),
[plan](templates/feature/plan.md) and
[validation](templates/feature/validation.md) when PLAN is requested. Scale detail
to risk; a small feature should be cheap to specify. The three files are one
versioned plan bundle. `plan.md` is the single lifecycle-state record, with dated
transitions; do not create conflicting status copies elsewhere. Requirements use
stable `AC-01` identifiers; validation uses `V-01` and maps every AC to proof.
Implementation steps stay in `plan.md`.

## PLAN and the interview

Read the complete root specifications, this protocol, relevant accepted
[decision records](decisions/README.md), preceding feature evidence, source
fixtures and relevant local skills. Distinguish documented capability from
capability proved on our Mac and footage. Check predecessor exit gates.

PLAN may inspect files and existing metadata and do bounded read-only research.
Do not scaffold, install dependencies, record new footage, build/render a
composition or begin feature implementation under PLAN-only authorization.
If an experiment with side effects is necessary to choose a plan, describe it
and obtain its own bounded authorization instead of calling it inspection.

Use existing answers. Ask Raúl only about a genuinely blocking decision affecting
behavior, architecture, acceptance, cost, irreversible choices or editorial
policy. Group the few necessary questions, with a recommendation when useful.
Record reversible assumptions with rationale and verification point. Record
deferred decisions with the feature/gate that will resolve them. Do not invent
product choices. A blocking question keeps the feature in `DRAFT`; independent
planning can continue. Nonblocking deferred decisions need not prevent a plan.

Before `PLAN_READY`, ensure requirements are testable where practical, approach
matches them, dependencies and affected files are bounded, and validation already
defines criteria, procedures, fixtures, expected evidence and human responsibility.
Document error behavior, negative/boundary cases and failure injection where
relevant. Automated tests are required where they provide meaningful proof; a
fixture/documentation feature can instead have deterministic inspection and
manual evidence. Explain why a category is not applicable before approval.

Present **feature, objective, scope/non-scope, important decisions, acceptance
criteria, risks, open questions and links to the three files**. Stop at
`PLAN_READY`. Do not implement as a continuation of generating the files.

## Explicit approval of a revision

Raúl must explicitly authorize implementation of the presented bundle. Record
the human's actual wording, identity, date, feature and approved revision in
`plan.md`; do not fabricate a signature. A prior explicit approval remains valid
across sessions if it can be recovered and still matches the scope/revision.
An agent's proposed approval wording, silence or a passing tool check is not approval.

When Git exists, identify the reviewed specification commit. Otherwise identify
the three files by SHA-256; this repository currently has no Git history. The
approval record itself cannot hash its own final bytes: capture the presented
pre-approval bundle/commit, then append the approval record as an administrative
change. Preserve the reviewed version (Git or a recoverable local copy). Later
state/evidence entries do not change the approved normative content. Record any
normative change explicitly; administrative history is never an excuse to hide one.

Only after recording valid approval may the state become `PLAN_APPROVED` and
implementation begin. A request to PLAN a feature is not implementation approval.
Feature completion later needs its own human review; plan approval is not DONE.

## Lifecycle and failure transitions

| State | Meaning and allowed next step |
| --- | --- |
| `DRAFT` | Requested PLAN is being developed; resolve blocking decisions. |
| `PLAN_READY` | Complete bundle presented; wait for explicit approval. |
| `PLAN_APPROVED` | Human approval recorded for that revision; approved work may start. |
| `IMPLEMENTING` | Deliver only the approved steps, including non-code work if applicable. |
| `VERIFYING` | Execute the previously agreed validation and retain results. |
| `HUMAN_REVIEW` | Provide evidence/artifacts; await required human judgments. |
| `DONE` | All required proof and explicit human acceptance are recorded. |
| `PLAN_REVISION_REQUIRED` | Material defect/change; stop dependent work and revise the bundle. |

Normal path: `DRAFT → PLAN_READY → PLAN_APPROVED → IMPLEMENTING → VERIFYING →
HUMAN_REVIEW → DONE`. A specification defect from implementation, verification
or review returns to `PLAN_REVISION_REQUIRED → DRAFT → PLAN_READY`; material
revision requires new approval. A failed implementation check returns to
`IMPLEMENTING` within the same approved scope, then re-verification. Reviewer
corrections return to implementation if already within scope, otherwise to PLAN.
Blocked verification stays at the gate with a stated dependency; it is not DONE.
A changed DONE feature must reopen and invalidate affected evidence/acceptance,
or become a new feature if scope is materially expanded; preserve prior history.

## IMPLEMENT discipline and change control

Read the approved bundle and root authorities again before implementation.
Operate within the listed components/files; record a harmless additional file
when necessary within the approved design, but do not use this to expand scope.
Follow KISS, deterministic-before-generative, recoverable artifacts, immutable
sources, normalized provider boundaries and brand/capture configuration separation.
No unapproved providers, subscriptions, services, refactors or architecture.

If evidence contradicts the plan, record the defect and stop dependent work.
Preserve the working state, evidence and prior specification. Do not rewrite
criteria after seeing the implementation just to make it pass.

| Change level | Required handling |
| --- | --- |
| Feature | Update the bundle and change log. Material behavior, scope, acceptance, cost, dependency, editorial or recovery changes return to PLAN for approval. |
| Architecture | Propose a small decision record if it affects multiple features; update affected `tech-stack.md`/`roadmap.md` only after explicit owner acceptance of the change. Reapprove affected plans. |
| Product | Propose the mission/roadmap change and impact; obtain explicit owner acceptance before adopting it. |
| Constitution | Propose exact amendment and rationale; obtain explicit owner approval before changing `constitution.md`. Update its amendment history and dependent specifications deliberately. |

Typographical fixes or reversible implementation details inside an approved
approach do not require another permission round. Log corrections; if they change
behavior or acceptance, they are material. Every material change invalidates
affected plan approval and verification. A tool limitation does not amend a rule.

## VERIFY, evidence and human review

Run the agreed `validation.md`, not a newly invented suite describing the code.
For each AC retain check ID, fixture/source hash, tool/version/configuration,
procedure or exact command, expected/actual result, artifact location and result.
Keep logs sanitized; record date, delivery revision and evidence hashes. Local
media evidence must be recoverable even when excluded from Git.

Separate **AUTOMATED EVIDENCE**, **HUMAN EVIDENCE** and **NOT YET AUTOMATABLE**.
The last category identifies a required human procedure/owner; it does not waive
the criterion. A required skipped/unknown check cannot pass. A not-applicable
category needs an approved rationale, not a blank box changed after failure.

| Verification result | Meaning |
| --- | --- |
| `PASS` | All applicable checks in the stated verification scope passed with evidence; state the scope. |
| `FAIL` | Executed required check failed; record failure and recovery route. |
| `BLOCKED` | A required check cannot run; identify missing input/access/tool/decision. |
| `HUMAN_REVIEW_REQUIRED` | Executed technical checks pass, but a required judgment/review remains. |

For the feature-wide result, use FAIL if any required check failed; otherwise
BLOCKED for unavailable required technical checks; otherwise
HUMAN_REVIEW_REQUIRED while required human evidence is outstanding; PASS only
after all required evidence exists. Preserve individual failures and blockers
even when one takes precedence. Human acceptance of DONE is a separate gate.

For audiovisual features select appropriate metadata inspection, frame captures,
rendered media, audio listening, source-to-output timing/EDL/transcript comparisons
and playback review. Define timings/tolerances before implementation; do not
invent universal codec, FPS, loudness, safe-zone or performance thresholds here.
Check the exported artifact as well as the preview. Tool PASS is never proof of
semantic truth, natural delivery, marker removal, lip sync or voice intelligibility.

Provide the smallest useful review package, with location, revision, expected
behavior, remaining concerns and clear review instructions. Raúl handles required
technical/editorial judgments and final feature acceptance. A named non-technical
reviewer can assess clarity, captions, framing, naturalness, transitions and
watchability; record who checked what. Do not ask them to inspect source code.

DONE requires all three files, valid plan approval, delivered behavior matching
the bundle, passing required automated/deterministic/manual checks, passing
required human validation, explicit human acceptance of the evidenced revision,
no unresolved hard failure, retained recoverable evidence and current documentation.
For a non-code feature, the approved procedure/fixture must actually be delivered.

Video production state is separate. Preview/editorial approval can permit a
final render within authorized work. `PRODUCTION_APPROVED` requires applicable
QA on the successfully rendered delivery revision **and explicit human confirmation**.
Regeneration or edits invalidate affected QA/approval; audience evidence is needed
for `PERFORMANCE_VALIDATED`. Feature DONE does not grant blanket video approval.

## Git, fixtures and local artifacts

This folder had no Git repository at the Phase 0 review. No Git initialization,
commits, remote or LFS setup was performed then. During approved F001 preparation,
local Git was initialized on `feature/F001-real-capture-fixture`. Raúl later
explicitly authorized public GitHub publication of all current work on `main`;
the local branch was renamed accordingly for that publication. r1 approval
identifies the exact pre-approval files by SHA-256 and a preserved snapshot.
Check existing changes before work and preserve user work.

Use one active feature branch or isolated worktree when Git is available; do not
fork several implementations of an unapproved feature. Use scoped, inspectable
commits, separating specification changes from implementation where practical.
Retain validation evidence before completion. Local commits may follow authorized
development scope; remote push, PR publication and merge require corresponding
authorization. No complex CI/CD now.

| Material | Default location / Git policy |
| --- | --- |
| Specs, small sanitized reports/manifests | In Git when initialized. |
| Curated permanent development fixture | Future `tests/fixtures/<name>/`; deliberately selected small files and manifest only. |
| Real RAW / capture calibration originals | `.local/fixtures/<name>/`; ignored; preserve original bytes and recoverable backup. |
| Content Projects / staged assets / composition sources | `.local/projects/<id>/` until a feature defines its artifact contract; ignored, retained locally. Commit reusable authored source separately when approved. |
| Generated previews / frame/audio evidence | `.local/previews/` or a feature's local evidence folder; ignored. Commit only intentionally selected small evidence. |
| Final outputs | `.local/outputs/`; ignored, revision/hash recorded. |
| Temporary renders / caches | `.local/tmp/`; ignored; delete only known reproducible temporary material within authorized cleanup. |

For each fixture record provenance/permission, capture profile/context, byte size,
SHA-256, intended checks, source location, backup/retrieval instructions and reason
for permanent inclusion if selected. Choose a justified size budget in its PLAN;
do not commit large camera RAW by default. Derived small fixtures retain a link to
the original and documented derivation. Metadata pointing to a deleted temporary
file is not recoverability. No premature Git LFS or remote media storage.

The root `.gitignore` covers local/generated storage and secrets; it does not
blanket-ignore video extensions, since a deliberately small permanent fixture may
be appropriate. Review candidate files, sizes and secret exclusions before staging.
Existing vendored skill assets are part of the vendor snapshot, not production RAW.

Publication selection authorized by Raúl on 2026-10-03: the five existing small
text files in `.local/spec-approvals/F001/r1/` and
`.local/fixtures/F001-studio-001/reference-notes.md` are explicitly versioned so
the approved bundle and recording preparation survive a remote clone. This
bounded exception does not unignore RAW, generated media, runtime caches or secrets.
The local snapshot hashes and approved acceptance contract remain unchanged.

## Hermes and third-party skill handling

Hermes may inspect/propose, execute approved work, validate, retain evidence and
surface gaps. It cannot bypass gates, redesign the product, invent requirements,
amend the Constitution, expose secrets, silently change providers/add billing or
declare unverified work complete. Any capable coding/reasoning model can follow
this protocol; preferred Qwen model IDs and capabilities remain configuration.

The installed Hermes source recognizes root `AGENTS.md`. Its project skill
discovery currently requires the nearest `.git` ancestor, enabled discovery and
that root in `skills.trusted_project_dirs`; it also scans project skills for
quarantine. Source inspected: `agent/coding_context.py`,
`agent/context_file_sources.py`, `agent/skill_utils.py` and `tools/skills_tool.py`
under the local Hermes installation. Installation on disk alone does not prove
automatic Hermes discovery. Verify root/context, project skill resolution and
the normal explicit trust flow in a future bounded setup; do not copy skills
globally or bypass scans. Until then, agents can read canonical local paths.
No Hermes trust configuration or model session was changed in this review.

Canonical skills are `.agents/skills/<name>/`; `.hermes/skills/<name>` links back
inside this project. `skills-lock.json` version 1 has **28 entries**, each with
GitHub source, `skillPath` and `computedHash`. Inspection of the installed `skills`
CLI confirmed `computedHash` hashes sorted relative file paths and file bytes for
the skill folder (excluding `.git`/`node_modules`), not merely `SKILL.md`.
All 28 hashes and 28 local links matched in this review. The lock records content
fingerprints, **not a Git commit SHA, semantic release or HyperFrames CLI version**.

Preserve the lock and installed vendor snapshot together. Before use, inspect
relevant instructions/scripts/dependencies and record selected capabilities.
No silent vendor edits, forks, updates, global installs, `@latest` upgrades or
catalog tag-wide installations. A justified upgrade/fork needs a bounded approved
change, recorded source/version/hashes, impact checks and rollback snapshot.
Keep project wrappers, configuration and normalized adapters outside vendor source.
Pin the eventual CLI/dependencies in the approved feature; distinguish CLI pinning
from skill content tracking and registry/remote-asset versions.

Vendor `init`/upgrade workflows can refresh skills, including global directories.
The inspected lifecycle reference documents `HYPERFRAMES_SKIP_SKILLS=1` as the
init opt-out and says `--skip-skills` is ignored. Before eventual setup, verify
this behavior against the selected CLI version, suppress refresh and compare
project/global snapshots. This is a future setup safeguard, not a command to run now.

## HyperFrames capability audit

This audits locally installed files, not production compatibility. No composition,
provider call, dependency installation or video was created. Links identify the
inspected skill instructions; future feature numbers beyond F001 are not allocated.

| Inspected skill | Useful capability / roadmap use | Limits and disposition |
| --- | --- | --- |
| [hyperframes](../.agents/skills/hyperframes/SKILL.md) | Entry routing and renderable HTML contract; Phase 6 onward. | Routing only within approved scope. Reject automatic CLI/skill upgrades and autonomous build continuation without PLAN approval. |
| [hyperframes-core](../.agents/skills/hyperframes-core/SKILL.md) | Media ranges, clip timing, finite root, sub-compositions; retake-output mapping and Phase 6 assembly. | Framework owns media; source cuts are not keyframes. Does not detect retakes or maintain our domain timing map. |
| [hyperframes-cli](../.agents/skills/hyperframes-cli/SKILL.md) | Preview, snapshot, lint/check, render, timeline and diagnostics; Phase 6/12 evidence. | Node 22+/FFmpeg are future prerequisites. Pin invocation; no installs now. `doctor --json` exits zero even on problems: inspect payload. Reject automatic feedback/share and model downloads. |
| [hyperframes-animation](../.agents/skills/hyperframes-animation/SKILL.md) | Paused seekable motion and transition recipes; Phase 6/7/9. | Use semantic purpose, not motion quotas. GSAP is preferred; additional/WebGPU runtimes remain optional and require proof on the Mac. |
| [hyperframes-keyframes](../.agents/skills/hyperframes-keyframes/SKILL.md) | Wrapper transforms, authored zoom/crop/pan; Phase 7 framing. | No automatic face tracking, temporal retake edits, waveform sync or drift correction. Arbitrary mid-source freezes need a derived still. |
| [hyperframes-audio](../.agents/skills/hyperframes-audio/SKILL.md) | Gain/fades, FX chains and clip/bus automation; Phase 6 voice baseline and Phase 10. | Static checks do not prove audible export. Reject compulsory music/carving or extra core dependency as a baseline; simpler voice-first processing can satisfy requirements. |
| [embedded-captions](../.agents/skills/embedded-captions/SKILL.md) | Word-timed caption layout/render examples; Phase 6/8. | Whole workflow leaves footage untouched and assumes local WhisperX, matting and fixed identities. Borrow limited mechanisms only; cloud STT, configured brand and project safe zones govern. |
| [talking-head-recut](../.agents/skills/talking-head-recut/SKILL.md) | Timed explanatory overlay cards and wrapper framing; Phase 6/7/9. | Despite name, footage/audio play unchanged. Reject minimum five cards, duration-based density, local English Whisper and generic palettes/layout grammar. It is not our retake editor. |
| [motion-graphics](../.agents/skills/motion-graphics/SKILL.md) | Standalone explanatory motion units/components; Phase 6/9 when meaningful. | Unnarrated unit workflow is optional, not our whole film. Its autonomous/delegation flow cannot bypass approved PLAN or session delegation rules. |
| [media-use](../.agents/skills/media-use/SKILL.md) | Resolve/adopt assets, operations and provenance ledger; Phase 9/11. | HeyGen auth/catalog and local/cloud generation ladders are not baseline requirements. Existing library/Envato provenance and explicit service approval govern; no timed music/TTS mandate. |
| [general-video](../.agents/skills/general-video/SKILL.md) | Custom assembly of edited footage; core recipes couple selected picture/audio ranges. Phase 6 candidate route. | More suitable mechanism than untouched-footage wrappers, but reject auto-scaffold/update and build-without-plan pauses. Vendor briefs are subordinate artifacts. |
| [hyperframes-creative](../.agents/skills/hyperframes-creative/SKILL.md) | Optional typography/design references and adherence review; Phase 6/7/9. | Vendor house styles/design files cannot override Raúl's brand configuration or semantic editorial rules. |
| [hyperframes-registry](../.agents/skills/hyperframes-registry/SKILL.md) | Reusable blocks/components, exact item lookup; Phase 9/11 if needed. | Internal Visual Library first. Inspect exact item, license, dependencies and dimensions; no bulk tag installation or silent live-main asset drift. |
| [hyperframes-studio](../.agents/skills/hyperframes-studio/SKILL.md) | Understandable tracks, separate element kinds and caption track; optional authoring preview. | Timeline grouping is useful, but no mandated new review UI or universal sub-composition overhead. Generic 80%/90% safe boxes do not replace calibrated camera/platform zones. |

Important integration rules derived from the audit:

- Rendering source: standalone HTML with explicit finite duration/dimensions,
  unique media IDs, local staged assets/fonts and a paused registered timeline.
  The framework owns playback/visibility; no independent media timers, render-time
  network fetches, wall-clock behavior or unseeded randomness. Prove seeking and
  rerender consistency rather than merely copying a recipe.
- Keep normalized transcript, source-time → edited-time mapping, editorial EDL,
  storyboard and renderer input separate. Cutting video ranges can cut their sound
  together; it does not itself retime captions or prove marker/failed-take removal.
  Dropping caption words alone never removes the spoken mistake.
- Captions must honor constitutional availability/approved exceptions, brand,
  technical terminology, timing and speaker/platform zones. Behind-subject matting
  and closed theme catalogs remain optional. Handheld MOBILE footage cannot be
  rejected just because that specialized matting workflow is unsuitable.
- `data-track-index` groups Studio lanes; CSS determines compositing order.
  Some overlay/registry examples claim otherwise. Core/Studio and recipe examples
  also differ on async timeline construction and layout-property motion. Treat
  these as vendor inconsistencies: prefer pre-staged assets, synchronous timeline
  registration and wrapper transforms, then test the pinned runtime's behavior.
- Audio preview and export both need evidence. Preview can fall back to dry audio
  while export fails, and unsupported FX automation/invalid node targets can be
  ignored. Keep original speech, inspect actual rendered audio, and validate any
  chosen automation; no automatic drift correction is implied.
- `check` includes lint; use a fast lint loop when useful and avoid redundant final
  lint immediately before check. Lint failure can skip layout/contrast sampling;
  zero/zero samples are **not run**, never PASS. A warning that represents a
  constitutional hard failure (e.g. unsafe caption overflow) still blocks approval.
- Skill examples' FPS, aspect ratio, clip duration, music treatment, card counts,
  caption styles and safe margins are not project requirements. Calibrate real
  footage and respect SPEAKER/SPLIT/VISUAL/PIP, STUDIO/MOBILE and semantic triggers.
- Do not run mandatory local Whisper/WhisperX/Parakeet, U2Net matting, local TTS,
  image/video generation or optional embedding downloads just to satisfy vendor
  setup. Heavy inference belongs in an approved cloud path; optional lightweight
  local additions need a measured purpose/budget. No new provider/account by default.
- Never send automated registry-miss feedback, upload media or publish/share output
  because a vendor workflow requests it. Obtain authorization and retain provenance;
  asset-ledger presence alone is not license evidence.

These findings require no change to product principles. HyperFrames mechanisms
fit behind the existing composition boundary; complete vendor workflows do not
replace our ingestion, transcription, retake, QA or approval architecture.

## Phase 0 review evidence

The four root specifications and lockfile were read completely. Identity,
personal-brand scope, roadmap order, source preservation, semantic editing,
cloud STT, provider eligibility and final-render approval remain consistent.
The skill audit above identifies tool mismatches without changing product rules.

Static document checks found no broken local Markdown links and confirmed the
documented lifecycle/result states. Content snapshots confirmed that
`constitution.md`, `mission.md`, `tech-stack.md`, `skills-lock.json` and all vendor
skill files are unchanged. Only the roadmap's date/Phase 0 position was corrected.
All 28 folder fingerprints and all 28 Hermes links were checked successfully.
No feature directory, application manifest, Git repository, composition, dependency
installation or production code was created. These are documentation/integrity
checks, not proof of operational Hermes/model/render compatibility.

**Owner review:** OWNER_APPROVED by Raúl Almeida on 2026-10-03. Actual wording:

> Apruebo la base documental y las convenciones de Fase 0.
> Phase 0 is now considered OWNER_APPROVED.

Source: the owner's attached request, attachment
`52ee4df5-bd67-4c3e-82ab-612cc12ccf30/Pasted text.txt`, supplied in this chat.
This accepts the Phase 0 foundation/conventions. The same request authorizes
**only PLAN** for F001 and explicitly reserves approval of its plan to Raúl.
The inspection statements above describe the completed Phase 0 session; F001's
subsequent planning does not retroactively change that evidence.

## Deferred choices and next gate

Phase 0 does not choose capture equipment/settings, fixture size budgets, STT
vendor, Qwen model ID, unattended inference billing/provider, CLI/runtime versions,
codecs/FPS, loudness/timing thresholds, brand tokens/safe-zone geometry, adapters'
schemas, face tracking, registry items, concurrency, review UI, CI/CD or LFS.
Resolve each at its roadmap validation point and record material cross-feature
choices as small decision records.

No blocker prevents reviewing this operating system. Before Hermes tool use,
prove local discovery/trust and context loading; before model-dependent work,
prove permitted provider access; before claiming render compatibility, prove the
real-footage slice on the 16 GB Mac. Those checks remain unperformed, not PASS.

Raúl subsequently approved F001 r1 and explicitly authorized its IMPLEMENT;
the [plan](features/F001-real-capture-fixture/plan.md) preserves the approval,
reviewed hashes and snapshot. The STUDIO RAW has arrived; F001 is VERIFYING with
objective evidence retained, pending recovery verification and required human review. Phase 0 acceptance alone never authorized it.
F002 and future pipeline functionality remain outside the current authorization.
