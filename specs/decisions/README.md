# Lightweight architectural decisions

Use a decision record only when a choice materially affects multiple features,
provider/renderer boundaries, recoverability, cost or accepted architecture.
Ordinary coding choices and bounded feature decisions belong in that feature's
three files. No decision records have been created by this Phase 0 session.

Name records `D001-short-name.md`, with the next unused ID. Keep them small; link
the feature and authoritative root documents. A proposal does not authorize
implementation or amend the Constitution. Owner acceptance is required before a
material architectural choice is adopted. Accepted records cannot override higher
authority; update affected root documents and reapprove affected plans explicitly.

```markdown
# DNNN — Decision title

Status: Proposed / Accepted / Superseded
Date: [date]
Related features / root documents: [links]

## Context
[The concrete problem, constraints and evidence.]

## Decision
[The bounded choice; actual owner approval/date/source when Accepted.]

## Alternatives
[Only plausible alternatives and why they were not chosen.]

## Consequences
[Tradeoffs, costs, validation, affected specs/features and recovery implications.]
```

Preserve accepted history. A later change creates a superseding record and links
both ways; do not rewrite old decisions to suggest they were always different.
Record constitutional amendment approval separately and follow its amendment
procedure. Do not generate speculative downstream ADRs now.
