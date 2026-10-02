# FNNN — Validation contract and evidence

**Bundle revision:** r1  
**Requirements:** [requirements.md](requirements.md)  
**State / approval record:** [plan.md](plan.md)

Define sections below **before implementation** as part of the approved bundle.
Later append execution results and human review; do not silently weaken the contract.

## Fixtures and environment

[Required source/fixture, provenance, byte size/hash, capture context, local/backup
retrieval locations, tooling versions/configuration and resource assumptions.
Identify prerequisites not yet available; never present an unperformed check as PASS.]

## Predefined checks and AC mapping

| Check | ACs | Evidence category | Procedure / input | Expected result and boundary | Evidence retained |
| --- | --- | --- | --- | --- | --- |
| V-01 | AC-01 | [AUTOMATED EVIDENCE / HUMAN EVIDENCE / NOT YET AUTOMATABLE] | [deterministic command/test or named reviewer procedure] | [observable pass/fail condition] | [report/artifact/frames/timing/listening record] |

Every AC needs at least one check. Automated evidence includes meaningful tests
and deterministic inspection. For NOT YET AUTOMATABLE name the human owner and
procedure: the category does not waive required validation.

## Coverage and justified exclusions

| Category | Check IDs or explicit non-applicability rationale |
| --- | --- |
| Automated tests / deterministic inspection | [meaningful proof; no tests that merely mirror implementation] |
| Manual inspection / human review | [named responsibility and procedure] |
| Negative cases | [invalid/missing/ambiguous inputs] |
| Boundary cases | [relevant timing/size/format/state boundaries] |
| Failure injection | [provider/tool failure, interrupted work, recovery; if appropriate] |
| Audiovisual evidence | [metadata, export/preview frames, audio, timing and playback if relevant] |

For exclusions provide rationale in PLAN; do not change a failed required check
to N/A. Specify tolerances and editorial judgments explicitly. Select the smallest
useful human artifact rather than asking reviewers to inspect code.

## Decision rules

Required failure → FAIL. Missing required technical check/input → BLOCKED.
Technical scope passed but required human judgment outstanding →
HUMAN_REVIEW_REQUIRED. Feature-wide PASS requires all applicable checks, including
human ones, to pass with evidence. Retain individual findings. Skipped/unknown or
zero-sample checks never pass. Final feature acceptance is separate from PLAN
approval and from a video's production approval.

## Execution evidence — append after implementation

**Verification result:** NOT RUN (not PASS)  
**Delivery revision / run / date:** [actual identity]  
**Environment / tool versions:** [actual versions, no secrets]

| Check / ACs | Actual command or human procedure | Expected vs actual | Evidence location / hash | Result / reviewer |
| --- | --- | --- | --- | --- |
| [V-01 / AC-01] | [executed procedure] | [observation] | [recoverable artifact] | [PASS / FAIL / BLOCKED / HUMAN_REVIEW_REQUIRED] |

[Summarize failures, unavailable/skipped checks, warning severity, recovery actions
and verification scope. Retain sanitized outputs, fixture hashes, changed evidence
and superseded results. “Tests pass” without traceable evidence is insufficient.]

## Human review and final feature acceptance

**Review artifact / revision:** [smallest useful package and playback instructions]  
**Required technical/editorial reviewer:** [Raúl; specific judgments]  
**Additional reviewer:** [name/responsibilities if needed]  
**Actual review evidence:** [who/date/observations/result; initially pending]  
**Owner acceptance of feature:** NOT GRANTED  
**Actual acceptance wording / date / revision:** [leave unfilled until human decision]

Before DONE confirm all required checks passed, approved scope matches delivery,
no hard failure remains, evidence is recoverable and documentation is current.
A rejected review returns to implementation or PLAN according to the defect.
Record production QA/approval separately if this feature produces a video; a
feature acceptance entry cannot imply approval of every subsequent render.
