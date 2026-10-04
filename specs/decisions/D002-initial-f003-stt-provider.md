# D002 — Initial F003 STT provider

**Status:** Proposed, NOT ACCEPTED\
**Date:** 2026-10-04\
**Related feature:** [F003 r1](../features/F003-time-aligned-transcription/plan.md)\
**Authority:** [Constitution](../../constitution.md), [tech-stack §7](../../tech-stack.md),
[roadmap Phase3](../../roadmap.md), [D001 accepted](D001-local-source-contract.md)

## Context

F002 delivers READY AV and an exact source clock. STT provider, timing precision,
paid calls and normalization were deferred. Provider choice affects later
consumers/recoverability/cost, so it requires a narrow decision record. The owner
requested evaluation of qwen-audio-3.1-asr-flash-filetrans Singapore/International.
Current official capability evidence, links and ambiguities are retained in the
F003 plan; documentary support is not fixture acceptance.

## Proposed decision

Use **Alibaba Cloud Model Studio qwen-audio-3.1-asr-flash-filetrans, Singapore /
International**, only as the initial F003 provider through a small replaceable
adapter, conditional on real-fixture word/text/timing validation. Keep the
canonical source-transcript v1 schema, rational source clock and normalized
UNKNOWN semantics owned by the project. No downstream consumer parses Alibaba.

Retain immutable sanitized provider response separately; replay normalization
locally without retranscription. Security requires explicit redaction of signed
transport URLs/auth before retention; keep all nonsecret recognition/usage data
and redaction provenance. This is not a promise to preserve secret wire bytes.

Limit approval to one file/canal/request for232,8s, explicit POST/journal/NO_OP,
no automatic resubmit. Pricing/actual usage/reconciliation remain execution
metadata, never domain schema. No reliable token-to-duration conversion or
hard USD upper bound has been established. If tokens absent, costs UNKNOWN
until billing reconciliation; no free-quota assumption.

Use existing private owner-managed OSS Singapore with short-lived signed HTTPS
URL for the derived audio only. No new bucket/service/uploader, permanent public
ACL or temporary oss:// fallback: upload documentation restricts the latter to
Beijing despite contradictory examples. Owner consent must include International
inference scope and UNKNOWN exact service retention; expiry24h is retrieval
availability, not proved deletion. Account/transport availability are preflight
gates, not assumed facts. Inability to meet them stops paid work.

Python3.14.7 stdlib and existing FFmpeg/ffprobe9.0.1 extend D001 narrowly to F003;
no provider SDK/dependency install or universal pipeline language decision.
Accepting D002 includes only the limited tech-stack wording proposed in plan.md;
no root amendment is applied during PLAN.

**Owner acceptance/date/trusted wording:** absent. Proposal does not authorize
IMPLEMENT, source upload or payment. Record actual decision only if received.

## Alternatives and justification

- Defer provider and draft schema only: would omit the requested concrete timing,
  transport and cost proof. Qwen has documented Spanish/word ms capabilities.
- Other cloud STT/forced alignment: plausible if real timing fails, but no candidate
  silently substituted or second service implemented in F003 r1.
- Local Whisper/Parakeet: conflicts with the cloud baseline/resource constraint;
  no install as a prerequisite.
- SDK/automatic OSS provisioning: unnecessary dependencies/infrastructure for one
  fixture. Existing private object + manual upload is the bounded initial transport.
- Public permanent URL/RAW upload/Beijing temporary storage: unnecessary exposure,
  RAW too large and region different from the requested candidate.
- Direct provider transcript everywhere: locks future consumers to vendor shape,
  usage/credentials/time semantics; normalized boundary is required.

## Consequences

Benefit: empirical Spanish/technical-word/timing proof with recoverable provenance
and no repeated paid STT for normalizer changes. Tradeoffs: account/storage setup
and owner-managed upload/cleanup, probabilistic model/backend drift, real cost
unknown before request, privacy/retention limitations and documented long-file/
token-usage ambiguity. No recurring subscription is required or authorized;
cost is metered STT plus any existing storage/transfer, observed separately.

The paid service solves unavailable cloud transcription; existing deterministic
tools cannot transcribe. It fits existing cloud STT direction and the primary
candidate requested by Raúl. Lock-in is limited by raw retention/adapter/schema.
If real fixture fails precision/coverage, keep evidence and return to PLAN for
provider/alignment revision; do not relax F003 acceptance or begin F004.

This decision selects no permanent STT service, correction model, renderer,
semantic/editorial policy or production approval. F001/F002/D001 remain intact.
