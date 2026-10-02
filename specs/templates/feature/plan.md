# FNNN — Feature plan

**Bundle revision:** r1  
**Lifecycle state:** DRAFT  
**Owner:** Raúl Almeida  
**Scope:** [requirements.md](requirements.md)  
**Proof contract:** [validation.md](validation.md)

This file owns state, tasks and approval. A template is not an approved plan.

## Architectural approach and data flow

[Explain the simplest approach satisfying requirements, affected components and
source → derived artifact → evidence flow. Cite root constraints/accepted decisions.
Keep provider-independent domain data and brand/capture configuration boundaries.]

## Change surface and dependencies

| File / component / local artifact | Create / modify / inspect | Purpose and related AC |
| --- | --- | --- |
| [bounded path] | [action] | [reason] |

[Tools, dependency/CLI versions to pin, relevant local skills/references and
selected mechanisms; no implicit vendor refresh. Note external services, auth,
documented permitted usage, cost and existing approvals. Identify necessary setup
such as local Git/Hermes discovery when relevant. No install during PLAN.]

## Risks, errors and recovery

[Failure behavior, recovery/rollback if relevant, immutable source/backup locations,
resource/cost exposure and open limitations. Explain when a defect returns to PLAN.]

## Observability and evidence

[What sanitized diagnostics identify failures? Where are run/version/configuration,
source hashes and small reports retained? Link media evidence to recoverable local
locations; do not record secrets or rely only on conversation memory.]

## Incremental implementation steps

- [ ] [Deliver one bounded increment; link relevant AC and validation check.]
- [ ] [Run the predefined validation, document actual evidence, prepare human review.]

[Add only needed steps. Non-code capture/procedure features still need delivery,
inspection and human review; no production-code requirement is implied.]

## PLAN readiness and presentation

[Summarize objective, scope, important decisions, ACs, risks and open questions.
Confirm the three files agree, dependencies are satisfied or explicitly gated and
validation is predefined. Set PLAN_READY only when presented for human approval.
Stop there: do not implement while waiting.]

## Approval of the presented bundle

**Approval:** NOT GRANTED  
**Approver / date:** [leave unfilled until actual human approval]  
**Human wording / trusted source:** [actual quote and message reference]  
**Approved revision:** [reviewed Git commit or three pre-approval SHA-256 values]  
**Recoverable reviewed bundle:** [Git or local snapshot location]  
**Authorized scope / exclusions:** [explicit scope and any approval conditions]

Appending this approval record is administrative; it does not authorize changes
to normative content. See the protocol's revision rule to avoid self-hashing.
Honor recovered valid approval without another permission round. A material
revision requires a new record; retain the old one and mark it superseded.

## State and change history

| Date | From → to / bundle change | Reason, human decision and evidence reference |
| --- | --- | --- |
| [date] | [DRAFT; later transition] | [actual event, not a predicted approval] |

Record mismatches and changed requirements/approach/validation explicitly. Material
changes go to PLAN_REVISION_REQUIRED and back through PLAN approval. Invalidate
affected evidence. Do not quietly alter the specification to fit existing work.
Record final human acceptance in `validation.md` and link it here before DONE.
