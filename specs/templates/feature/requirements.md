# FNNN — Feature requirements

**Bundle revision:** r1 (draft; use the same revision in all three files)  
**Owner:** Raúl Almeida  
**Roadmap phase / predecessor evidence:** [identify phase and required accepted artifact]  
**Related decisions:** [accepted record links, or none]

Replace bracketed prompts; remove irrelevant detail with an explicit rationale.
Lifecycle state and approval are recorded only in `plan.md`.

## Objective and user problem

[What user outcome must exist? Who needs it, and what current problem does it solve?]

## Scope and non-scope

[List the bounded delivered behavior and explicit exclusions. Do not include later
roadmap features just because a tool supports them.]

## Dependencies, inputs and outputs

[Required predecessor gates, input formats/source locations/capture context,
output artifacts and ownership. Separate source, derived artifact and evidence.
Identify unavailable inputs; a location alone does not prove recoverability.]

## Invariants and constitutional constraints

[Cite the relevant Constitution sections and root-spec constraints. Include source
preservation, timing/meaning/brand/provider boundaries where relevant. Describe
what must remain true even on failure. Tool defaults cannot waive these rules.]

## Failure behavior

[Invalid/missing/ambiguous input, unavailable tools/providers, partial work and
recovery. Describe observable behavior, preserved artifacts and when to stop for
human judgment; do not design unnecessary implementation internals.]

## Acceptance criteria

| ID | Observable condition | Success boundary / required evidence | Validation IDs |
| --- | --- | --- | --- |
| AC-01 | [testable user behavior] | [expected result; threshold if justified] | V-01 |

Cover relevant negative and boundary behavior. Define tolerances before approval;
do not claim automatic verification of an editorial judgment. Every AC needs proof
in `validation.md`, including criteria requiring human inspection.

## Questions, assumptions and deferred decisions

| Kind | Question / assumption / deferred choice | Rationale or blocking impact | Owner / resolution gate |
| --- | --- | --- | --- |
| [Blocking / Safe assumption / Deferred] | [item, or explicitly none] | [why ask, assume or defer] | [who/when] |

Ask only blocking decisions affecting behavior, architecture, acceptance, cost,
irreversible choices or editorial policy. Do not assume a product decision or
ask for facts already in the root specifications.
