# Raúl Almeida Agentic Video Studio — Mission

**Version:** 0.1  
**Status:** OWNER_APPROVED — Phase 0 acceptance recorded in specs/README.md  
**Owner:** Raúl Almeida  
**Initial scope:** Supply Chain 01 — Vertical Native  
**Updated:** 2026-10-02

## 1. Product mission

Transform Raúl Almeida's technical knowledge, experience, opinions, and ideas
into professional audiovisual content with minimal manual production work.

The desired interaction is:

    RAÚL       idea → record
    SYSTEM     recording → production
    HUMAN      review → approve

The system should carry the production burden between recording and approval:
understand the explanation, clean the recording, choose useful visuals, compose
the video, add captions, process audio, validate, and render. Human judgment
remains responsible for meaning, technical correctness, and editorial approval.

The governing principles are in [constitution.md](constitution.md). Technology
choices belong to [tech-stack.md](tech-stack.md); delivery order belongs to
[roadmap.md](roadmap.md).

## 2. Identity and audience

This product serves **Raúl Almeida's personal brand exclusively**. His knowledge,
voice, natural presentation, and point of view are central to every production.

AR Solución Digital is a separate business and brand. A future derivative may
reuse architecture, production skills, components, QA, and rendering
infrastructure, with separate identity and editorial policy. That derivative
does not drive current scope or visual decisions.

The intended audience is people interested in software engineering and practical
technical understanding, including developers and engineering leaders. Content
should make difficult ideas easier to understand without sacrificing accuracy
or inventing authority.

## 3. Users and the problem

**Primary user: Raúl Almeida.** He supplies ideas, expertise, recordings, and
editorial judgment. Production should not require him to become a timeline
editor, caption operator, asset researcher, or motion designer for every video.

**Secondary operational user: a non-technical reviewer/editor**, potentially
Raúl's wife. This person should be able to watch a preview, approve a revision,
and request changes in natural language without editing code or a professional
timeline. Technical judgments that require Raúl's expertise remain his
responsibility; the system should identify those questions clearly.

The problem is the gap between having something valuable to explain and producing
an intentional, consistent video. Manual editing, diagrams, captions, assets,
audio, platform framing, and repeated corrections consume time and discourage
spontaneous recording. The product reduces that work while preserving Raúl's
meaning and natural delivery.

## 4. Initial content domain

Initial topics include:

- software engineering and backend engineering;
- Go / Golang, concurrency, and parallelism;
- distributed systems and software architecture;
- databases and performance;
- legacy modernization;
- technical leadership;
- engineering lessons, experience, and opinions.

The domain must remain extensible to other personal-brand topics. Go concepts
can seed reusable visuals; they do not define the whole product or require a
complete Go library before production begins.

## 5. Core content supply chains

### Supply Chain 01 — Quick Ideas → Vertical Native

**First implementation priority.** A spontaneous idea or short explanation
becomes a video built for portrait viewing from the outset.

    Idea
      ↓
    Script / Bullets
      ↓
    Vertical Recording
      ↓
    Automated Production
      ↓
    Human Review / Corrections
      ↓
    Rendered, Checked, Approved Vertical Master
      ↓
    Shorts / Reels / LinkedIn

Preparation may be brief; it should support recording rather than make
spontaneous ideas wait for a large planning process. The two supported capture
profiles are **STUDIO**, for controlled capture, and **MOBILE**, for opportunity
and speed. Studio provides the first development fixture; Mobile receives real
production validation later in the roadmap.

Initial delivery is a 9:16 master at a minimum of 1080 × 1920. Capture preferences
and layout rules are governed by the Constitution. Duration follows clarity and
one primary idea, rather than a fixed target. A production-approved master is
ready for human-managed distribution; platform suitability and any variants
must be checked before publication. No universal platform acceptance is assumed.

### Supply Chain 02 — Deep Topic → Long-Form Authority Content

**Future scope.** A deeper technical topic becomes YouTube long-form or LinkedIn
long-form video, likely using horizontal, high-quality capture and richer
technical visualization.

This direction requires future specifications. Current architecture should
allow different capture and delivery profiles without making portrait layout
assumptions part of transcripts or editorial meaning.

### Supply Chain 03 — Long-Form → Content Repurposing

**Future scope.** One long-form source yields multiple semantic short candidates
that are reviewed and recomposed for vertical delivery.

    Long-Form Master
      ↓
    Semantic Short Candidates
      ↓
    Vertical Recompositions
      ↓
    Human-Approved Shorts / Reels / LinkedIn

Repurposing should retain context and meaning. It is not an instruction to crop
every source mechanically or implement clip selection now. Recoverable source
artifacts, timing, editorial intent, and reusable visuals are the compatibility
requirements for the current foundation.

## 6. First product outcome

The first implementation target is:

    ONE REAL VERTICAL RAW
            ↓
    ONE COMPLETE PIPELINE
            ↓
    ONE PRODUCTION-QUALITY SHORT

This establishes a usable path through the system. It does not require a large
visual catalog, every layout, an application UI, or every future supply chain.

An end-to-end technical proof may precede full production readiness. It must
not receive `PRODUCTION_APPROVED` while a constitutional hard failure remains
or before a human explicitly approves the checked delivery revision. Production
approval and audience performance validation are separate outcomes.

## 7. Mission-level success criteria

The primary measure is **human production work remaining after recording**.
Manual timeline editing should trend toward zero for routine content while
review and editorial judgment remain deliberate.

| Outcome | Evidence to collect |
| --- | --- |
| Low human editing effort | Active review/correction time, correction iterations, manual timeline interventions |
| Sustainable throughput | Approved videos per production period and elapsed time from RAW to approval |
| Technical correctness | Critical transcription, code, claim, and visual errors found by QA or review |
| Visual consistency | Brand and safe-zone review across videos and capture environments |
| Useful reuse | Existing components reused across different videos/configurations and work avoided |
| Natural presentation | Human review of cuts, retained gestures, voice, and delivery |
| Reliable rendering | Render completion, failed jobs, reruns, and render time on the target Mac |
| Spontaneous capture | Real Mobile ideas reaching approval and capture assumptions that prevent completion |
| Affordable operation | AI/STT cost per approved video and recurring incremental service cost |
| Evidence-based evolution | Documented editorial hypotheses and changes informed by audience behavior |

These are measurement dimensions, not invented guarantees. Feature specifications
must define counting methods and acceptance thresholds. Representative production
runs establish the initial baseline before throughput or time targets are fixed.
Audience metrics cannot override truthfulness, clarity, or human approval.

## 8. Non-goals

The initial project is not:

- a SaaS or a commercial video editor;
- a multi-user platform or a large content-management application;
- an autonomous publishing bot;
- a generic AI video generator;
- an AR Solución Digital branding project;
- a replacement for human editorial judgment;
- an implementation of long-form production or semantic repurposing.

## 9. Vision

Raúl records an idea. The system understands what he said and identifies the
semantic structure. It edits mistakes and retakes without losing valid speech.
It determines when Raúl should remain visible and when an explanation benefits
from a diagram, code visualization, comparison, animation, B-roll, or another
supporting visual.

It searches the Visual Library first, configures and composes existing parts,
and creates a missing reusable component when justified. It builds an intentional
personal-brand composition with synchronized captions and clear voice-first
audio, validates the result, and presents it to a human.

The reviewer requests corrections in natural language. The system updates the
affected production, reruns QA, and presents the changed revision for review.
The checked final render receives explicit human approval. Humans manage
publication; later, real audience evidence improves editorial rules and the
next production.

Success means recording useful ideas becomes routine because production is
reliable, understandable, and inexpensive enough to sustain.
