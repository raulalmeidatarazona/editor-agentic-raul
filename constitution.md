# Raúl Almeida Agentic Video Studio — Constitution

**Version:** 0.1.1  
**Status:** Active  
**Scope:** Vertical Native Supply Chain  
**Owner:** Raúl Almeida  
**Development methodology:** Spec-Driven Development (SDD)

---

# 1. Purpose of this Constitution

This document defines the non-negotiable principles, architectural boundaries,
production rules, and quality standards of Raúl Almeida Agentic Video Studio.

The project serves Raúl Almeida's personal brand exclusively. It is separate
from AR Solución Digital. A future derivative MAY reuse production architecture,
but MUST have its own brand identity and editorial configuration.

It is the highest-level specification of the project.

All future specifications, features, implementation plans, agents, skills,
prompts, components, and technical decisions MUST comply with this Constitution.

When a feature specification conflicts with this document, this document wins
unless the Constitution itself is deliberately amended.

The project follows Spec-Driven Development.

The expected hierarchy is:

    Constitution
        ↓
    Mission
        ↓
    Tech Stack
        ↓
    Roadmap
        ↓
    Feature Specification
        ↓
    Implementation Plan
        ↓
    Tasks
        ↓
    Code
        ↓
    Validation

We do not start from code.

We start from intent, constraints, contracts, and measurable outcomes.

---

# 2. Product Principle

Raúl Almeida Agentic Video Studio is not primarily a video editor.

It is an agentic content-production system that transforms Raúl Almeida's
knowledge into high-quality audiovisual content with minimal manual editing.

The system exists to make Raúl's knowledge easier to understand,
not to make the editing more noticeable.

The fundamental production model is:

    Knowledge
        ↓
    Capture
        ↓
    Understanding
        ↓
    Editorial Direction
        ↓
    Visual Explanation
        ↓
    Composition
        ↓
    Quality Assurance
        ↓
    Human Approval
        ↓
    Distribution
        ↓
    Performance Feedback
        ↓
    Learning

---

# 3. Primary Human Role

Raúl's primary responsibilities are:

- generate ideas;
- provide expertise;
- explain concepts;
- record content;
- approve important editorial decisions when necessary.

Raúl SHOULD NOT need to:

- manually edit timelines;
- create captions;
- search for every asset;
- animate diagrams manually;
- repeatedly reposition video;
- manually create platform variants;
- manually perform routine QA.

The system SHOULD convert knowledge into production-ready content.

---

# 4. Human Review Principle

The system MUST be human-in-the-loop.

Automation is responsible for production.

Humans are responsible primarily for judgment.

The desired workflow is:

    GENERATE
        ↓
    AUTOMATED QA
        ↓
    PREVIEW
        ↓
    HUMAN REVIEW
        ↓
    APPROVE
        OR
    NATURAL-LANGUAGE CORRECTION
        ↓
    REGENERATE
        ↓
    AUTOMATED QA
        ↓
    PREVIEW / HUMAN REVIEW
        ↓
    APPROVE

A reviewer SHOULD be able to request changes using natural language.

Examples:

    "The diagram at 00:23 is confusing."

    "Keep Raúl on screen longer here."

    "Remove this animation."

    "Make this code larger."

    "The captions are covering his hands."

The reviewer SHOULD NOT need to manipulate a professional video-editing
timeline for normal production.

If routine videos consistently require manual timeline editing,
the system design has failed.

---

# 5. KISS Principle

The project follows KISS aggressively.

Every dependency, service, framework, model, and abstraction MUST justify
its existence.

Do not introduce:

- unnecessary SaaS;
- unnecessary databases;
- unnecessary queues;
- unnecessary infrastructure;
- unnecessary microservices;
- unnecessary AI models;
- unnecessary UI applications;
- unnecessary abstraction layers.

A deterministic solution is preferred when it solves the problem reliably.

---

# 6. Deterministic Before Generative

The system MUST NOT use generative AI where deterministic software provides
a better, cheaper, faster, or more predictable solution.

Use AI primarily for:

- understanding;
- reasoning;
- classification;
- editorial decisions;
- planning;
- semantic segmentation;
- selecting components;
- configuring components;
- generating missing reusable components;
- interpreting natural-language feedback.

Use deterministic software primarily for:

- rendering;
- video transformations;
- audio transformations;
- timestamps;
- file operations;
- validation;
- layout constraints;
- safe zones;
- encoding;
- reusable animations;
- QA rules.

Principle:

> AI decides. Software executes.

---

# 7. Reuse Before Generation

The system follows:

    REUSE
        ↓
    CONFIGURE
        ↓
    COMPOSE
        ↓
    CREATE
        ↓
    GENERATE EXTERNALLY

Before creating a new visual, the system MUST check whether an appropriate
component already exists.

The preferred visual supply order is:

    1. Existing Visual Library component
    2. Existing component configured differently
    3. HTML / CSS / SVG / GSAP
    4. Approved external asset
    5. Generative image/video AI only when justified

Principle:

> Build once. Configure. Reuse.

Every video SHOULD improve the production capability of future videos.

---

# 8. Capture Principle

The recording is not the final composition.

It is source material.

Therefore:

> Capture for editability, not for final composition.

And:

> Capture wide; compose tight.

The capture process SHOULD preserve information rather than prematurely
discard it.

The system MAY later:

- crop;
- zoom;
- reposition;
- resize;
- replace the camera with a visual;
- place the camera inside a PiP;
- create split layouts.

Information that was never captured cannot reliably be recovered.

---

# 9. Capture Opportunity Principle

Production quality MUST NOT prevent spontaneous content creation.

The project supports at least two official capture profiles:

## STUDIO

Optimized for maximum production control.

Typical equipment:

- Sony ZV-E10;
- kit lens;
- tripod;
- Elgato Teleprompter;
- DJI Mic Mini;
- key light;
- rear/rim light;
- two RGB background lights.

## MOBILE

Optimized for speed and opportunity.

Possible contexts include:

- walking;
- travelling;
- office;
- conference;
- street;
- temporary workspace;
- spontaneous idea.

The Mobile profile MAY use:

- phone;
- portable camera;
- DJI microphone when practical;
- natural lighting;
- uncontrolled backgrounds.

Principle:

> Capture opportunity beats capture perfection.

A valuable idea MUST NOT be discarded because the studio is unavailable.

---

# 10. Environmental Independence

The physical environment is variable.

The brand language is deterministic.

Principle:

> Brand consistency must survive environmental inconsistency.

A video MUST remain recognizably part of the Raúl Almeida visual system
whether it is recorded:

- in the studio;
- outdoors;
- in an office;
- while travelling;
- at an event;
- in another country.

Brand identity MUST NOT depend exclusively on the physical background.

---

# 11. Vertical Native Capture Contract

The initial product scope is Vertical Native content.

Preferred orientation:

    9:16 portrait

Preferred capture resolution:

    4K portrait when practical

Minimum delivery resolution:

    1080 × 1920

4K capture is preferred because it provides additional room for:

- digital crop;
- digital zoom;
- reframing;
- PiP;
- composition.

4K is NOT required when it materially harms capture speed or reliability.

---

# 12. Human Safe Zone

For studio capture, Raúl SHOULD remain approximately centered horizontally.

The framing SHOULD be sufficiently wide to retain:

- head;
- shoulders;
- torso;
- natural hand gestures when practical;
- surrounding visual space.

Avoid unnecessarily tight framing.

Raúl MAY:

- gesture;
- lean slightly;
- change posture;
- move naturally.

Raúl SHOULD NOT routinely:

- leave the safe zone;
- walk out of frame;
- dramatically change camera distance.

Exact safe-zone coordinates MUST be calibrated using real camera footage
and stored as configuration rather than assumptions embedded in code.

---

# 13. Camera Calibration

Before production layouts are considered stable, the project MUST use a
real vertical calibration recording.

The calibration footage SHOULD include:

- normal speaking position;
- natural hand movement;
- slight left movement;
- slight right movement;
- normal forward/back movement;
- typical teleprompter use.

This recording SHOULD become a development fixture.

Example:

    tests/fixtures/vertical-calibration.*

Layout development SHOULD be validated against real capture footage.

---

# 14. Retake Protocol

Recording MUST remain simple.

The creator SHOULD NOT repeatedly stop recording after mistakes.

The initial verbal retake marker is:

    "Again"

Expected behavior:

    incorrect take
        ↓
    pause
        ↓
    "Again"
        ↓
    pause
        ↓
    corrected take

The editing system SHOULD identify the failed take and remove the marker.

The final output MUST NOT contain a verbal retake marker. The ordinary word
"again" used as part of valid narration is not automatically a retake marker.
Ambiguous cases MUST NOT cause valid speech to be silently deleted.

Additional voice commands SHOULD NOT be introduced until demonstrated
necessary.

---

# 15. Brand Visual System

The executable brand system MUST use deterministic design tokens.

A visual reference image MAY guide the identity, but the source of truth
for software MUST eventually be structured configuration.

Initial canonical color direction:

    CREAM
    #F2E8D0
    Base / neutral background

    FOREST
    #173F32
    Structure / architecture / authority

    OXIDE
    #B4492A
    Problem / error / contradiction / emphasis

    GOLD
    #D69B2D
    Insight / result / takeaway

    CHOCOLATE
    #493124
    Warm dark neutral

    INK
    #18201C
    High-contrast text

    WHITE
    #FAF8F2
    Light text

These values are v0.1 tokens and MAY be adjusted during visual calibration.

They MUST NOT be replaced arbitrarily on a per-video basis.

---

# 16. Semantic Color Principle

Color SHOULD communicate meaning.

Default semantic mapping:

    FOREST
    → structure
    → architecture
    → normal state
    → containers

    OXIDE
    → warning
    → error
    → problem
    → contradiction
    → important negative condition

    GOLD
    → insight
    → success
    → result
    → key takeaway

    CREAM
    → neutral surface
    → background
    → explanatory space

Visual components SHOULD consume semantic brand tokens.

They SHOULD NOT contain arbitrary LLM-generated colors.

---

# 17. Studio Background Lighting

The controlled studio uses two RGB background lights.

Initial numeric calibration targets are recorded in `tech-stack.md` under
Studio capture calibration. They are STARTING values, not brand tokens.

Physical lighting settings MUST be validated using:

- the real RGB lamps;
- the real physical background;
- the Sony ZV-E10;
- the final camera exposure;
- the real lighting setup.

Once visually calibrated, final values SHOULD be stored in configuration.

The physical RGB background is part of Studio Mode only.

It is NOT required for brand consistency.

---

# 18. Visual Grammar

Vertical Native v0.1 uses four primary visual states.

These states form the fundamental visual grammar of the editor.

## SPEAKER

Raúl is the primary visual.

Use primarily for:

- hooks;
- opinions;
- stories;
- personal experience;
- transitions;
- conclusions;
- contextual CTA.

## SPLIT

Raúl and an explanatory visual share the frame.

Typical vertical structure:

    ┌────────────────────┐
    │                    │
    │       VISUAL       │
    │                    │
    ├────────────────────┤
    │                    │
    │        RAÚL        │
    │                    │
    └────────────────────┘

Use for:

- concepts;
- simple diagrams;
- comparisons;
- supporting explanation.

## VISUAL

The explanatory visual becomes the primary screen content.

Raúl's voice continues.

Use for:

- architecture;
- code;
- concurrency;
- distributed systems;
- timelines;
- database behavior;
- detailed diagrams.

## PIP

The explanatory visual dominates while Raúl remains visible in a
picture-in-picture element.

Use when:

- the visual requires substantial space;
- maintaining human presence adds value.

---

# 19. Semantic Editing Principle

Visual changes MUST follow meaning, not arbitrary timing.

Principle:

> Visuals follow meaning, not time.

The system MUST NOT implement rules such as:

    "change visual every 2 seconds"

simply to create artificial activity.

Every significant visual SHOULD have an editorial purpose.

Valid purposes include:

- Explain
- Demonstrate
- Compare
- Orient
- Emphasize

"Make the video less boring" alone is NOT sufficient justification.

Principle:

> Every visual must earn its screen time.

---

# 20. Speaker-First Identity

Raúl's knowledge, voice, personality, and experience are the product.

Animations are supporting material.

The system MUST NOT turn every video into a motion-graphics presentation.

The visual hierarchy is:

    Raúl's idea
        ↓
    Raúl's explanation
        ↓
    Visual clarification
        ↓
    Supporting assets
        ↓
    Decorative elements

Not the reverse.

---

# 21. Code Visualization Principle

When explaining code, the system SHOULD prioritize pedagogical clarity over
literal reproduction of an IDE screen.

Principle:

> Show the concept, not necessarily the original screen.

For example, instead of showing an entire editor, the system MAY progressively
reveal:

    var wg sync.WaitGroup

then:

    var wg sync.WaitGroup

    for _, job := range jobs {
        wg.Add(1)
    }

then additional relevant lines.

Code MUST be:

- technically correct;
- readable on mobile;
- limited to relevant lines;
- visually synchronized with the explanation.

Source code recordings MAY be used as references rather than mandatory
final visuals.

---

# 22. Captions

Vertical Native videos MUST contain captions unless a future specification
explicitly defines an exception.

Captions SHOULD:

- remain synchronized;
- normally display small phrase groups;
- use no more than two lines;
- remain inside safe zones;
- avoid covering important visual information;
- use sufficient contrast;
- remain readable on mobile.

The initial target is approximately:

    2–6 visible words

when linguistically appropriate.

This is a guideline, not a grammatical constraint.

Technical terminology MUST receive additional validation.

Examples:

    WaitGroup
    errgroup
    goroutine
    PostgreSQL
    gRPC
    Symfony

Incorrect transcription of critical technical terminology is a QA failure.

---

# 23. Safe Zones

Important visual information MUST remain inside configurable safe zones.

Safe zones MUST account for:

- platform UI;
- captions;
- face/body;
- graphics;
- CTA;
- interaction controls.

Exact values MUST live in configuration.

They MUST NOT be scattered as magic numbers throughout implementation.

---

# 24. Audio

Voice is always the primary audio element.

Initial primary microphone:

    DJI Mic Mini

Camera audio MAY serve as:

- backup;
- synchronization reference.

The raw voice SHOULD be captured without destructive processing.

The production pipeline MAY perform:

    normalization
        ↓
    corrective EQ
        ↓
    compression
        ↓
    loudness normalization
        ↓
    music
        ↓
    ducking

Music is optional.

Music MUST NOT compete with speech.

Sound design MUST support comprehension rather than create unnecessary noise.

---

# 25. External Assets

Approved external asset libraries MAY provide:

- music;
- sound effects;
- icons;
- B-roll;
- illustrations;
- supporting graphics.

External assets MUST NOT replace reusable internal technical visuals when
the latter provide clearer explanations.

Asset provenance and licensing SHOULD remain traceable at project level.

---

# 26. CTA

CTA is optional.

A video MUST NOT fail QA because it does not contain a CTA.

When a CTA exists:

- maximum one primary CTA for Vertical Native v0.1;
- it SHOULD be contextual;
- it SHOULD relate naturally to the content.

Preferred:

    "Which one are you using in production?"

Over:

    "Like, comment, subscribe and follow."

The system SHOULD favor conversation and relevance over generic engagement
requests.

---

# 27. Content Principle

Vertical Native content SHOULD normally communicate one primary idea.

Principle:

    One primary idea
    +
    No unnecessary seconds
    =
    Correct duration

The system MUST NOT optimize toward a fixed duration at the expense of
clarity.

A video MAY be:

- 40 seconds;
- 70 seconds;
- 120 seconds;
- longer when justified.

Clarity determines duration.

---

# 28. Hook Principle

The viewer SHOULD encounter meaningful value immediately.

Avoid:

- unnecessary introductions;
- animated logos before content;
- long greetings;
- irrelevant setup.

Approved hook patterns MAY include:

- problem;
- question;
- contradiction;
- curiosity;
- result;
- practical observation.

Hooks MUST NOT fabricate:

- experience;
- metrics;
- results;
- customer stories;
- claims.

Authority comes from real expertise, not artificial sensationalism.

---

# 29. Technical QA

A video MUST NOT reach Production Approved state if it contains a hard failure.

Hard failures include:

- incorrect aspect ratio;
- invalid output resolution;
- failed render;
- missing media;
- unexpected blank frames;
- severe audio clipping;
- inaudible voice;
- caption overflow;
- captions outside safe zones;
- materially desynchronized captions;
- obvious critical transcription errors;
- incorrect technical terminology;
- visuals contradicting narration;
- materially incorrect code;
- cuts that remove spoken words;
- failed takes remaining;
- a verbal "Again" retake marker remaining;
- broken animation;
- missing required assets.

The system SHOULD attempt automatic correction before requesting human
intervention.

---

# 30. Editorial Warnings

Not every editorial anomaly is a hard failure.

Examples of warnings:

- long period without visual change;
- no CTA;
- no music;
- only SPEAKER layout used;
- unusually long video;
- unusually high visual density;
- potentially weak hook.

Warnings MUST NOT automatically trigger unnecessary editing.

In particular, the system MUST NOT add random B-roll or animations merely
because a timer threshold was exceeded.

---

# 31. Production Approved

A Vertical Native video MAY enter:

    PRODUCTION_APPROVED

only when:

## Content

- one clear primary idea exists;
- the opening provides immediate value;
- unnecessary intro has been removed;
- claims are not fabricated;
- conclusion is understandable.

## Video

- valid 9:16 output;
- minimum 1080 × 1920 delivery;
- crop is intentional;
- human safe zones are respected.

## Audio

- voice is intelligible;
- no severe clipping;
- loudness is consistent;
- music, when present, remains subordinate.

## Captions

- present, unless covered by the explicit exception allowed in Section 22;
- synchronized;
- readable;
- within safe zones;
- technical terminology verified.

## Editorial

- visuals follow meaning;
- visuals have purpose;
- editing is not arbitrarily hyperactive;
- brand language remains consistent;
- Raúl's explanation remains the protagonist.

## Visuals

- technically correct;
- legible;
- brand compliant;
- not unnecessarily decorative;
- Visual Library reused when appropriate.

## Code

When present:

- technically correct;
- readable on mobile;
- limited to relevant information;
- synchronized with narration.

## Technical

- no broken assets;
- no failed takes;
- no retake markers;
- no broken animation;
- no unintended blank frames;
- render completes successfully.

## Human Review

A human reviewer can reasonably conclude:

- the idea is understandable;
- Raúl appears natural;
- the video looks intentional;
- no manual timeline editing is necessary.

Approval MUST record an explicit human decision about the reviewed production
revision; the absence of a correction request is not approval.

The delivered render MUST complete successfully and pass applicable QA before
that revision enters PRODUCTION_APPROVED. An earlier preview MAY receive
editorial acceptance, but that alone is not production approval.

Changes to content, composition, assets, captions, or audio invalidate the
affected revision's QA and approval. Regenerated output MUST be checked and
reviewed again. Exact revision tracking belongs to feature specifications.

---

# 32. Performance Validation

Production approval does NOT prove editorial effectiveness.

The project distinguishes:

    PRODUCTION_APPROVED

from:

    PERFORMANCE_VALIDATED

Production Approved means:

> The video satisfies our production and editorial standards.

Performance Validated means:

> Real audience behavior provides evidence about whether our editorial
> hypotheses worked.

Post-publication signals MAY include:

- chose-to-view behavior;
- retention;
- average view duration;
- average percentage viewed;
- rewatch behavior;
- engagement;
- comments;
- shares;
- follows/subscriptions;
- retention peaks;
- retention dips.

Performance data SHOULD improve future editorial rules.

It SHOULD NOT cause blind optimization toward a single metric.

---

# 33. Learning Loop

The production system is expected to evolve.

The complete loop is:

    IDEA
      ↓
    RECORD
      ↓
    UNDERSTAND
      ↓
    EDIT
      ↓
    QA
      ↓
    HUMAN APPROVAL
      ↓
    PUBLISH
      ↓
    OBSERVE
      ↓
    LEARN
      ↓
    UPDATE RULES
      ↓
    NEXT CONTENT

Changes supported by repeated real-world evidence MAY result in amendments to:

- editorial rules;
- visual grammar;
- caption behavior;
- hook patterns;
- component selection;
- brand presentation;
- production heuristics.

Architecture SHOULD allow these rules to evolve without rewriting the
production system.

---

# 34. Architecture Independence

Editorial policy MUST be separated from rendering implementation whenever
practical.

For example:

    "Use SPLIT for this segment"

is an editorial decision.

How SPLIT is rendered is an implementation detail.

Similarly:

    "Highlight the failing worker"

is semantic intent.

Its SVG/HTML/GSAP implementation is separate.

This separation is essential for future maintainability.

---

# 35. Provider Independence

Core domain concepts SHOULD NOT depend unnecessarily on one AI provider.

Examples of provider-independent artifacts include:

- transcript;
- storyboard;
- visual specification;
- brand configuration;
- QA result;
- project metadata.

AI providers SHOULD be replaceable where practical.

The same principle applies to transcription providers.

---

# 36. Local Resource Constraint

The primary local development/production machine has approximately:

    Mac
    16 GB RAM

The architecture MUST NOT assume:

- powerful local GPU;
- local LLM inference;
- local image generation;
- local video generation;
- heavyweight local speech models.

Local resources SHOULD focus on:

- orchestration;
- code;
- browser rendering;
- FFmpeg;
- lightweight processing;
- file management.

Compute-heavy AI SHOULD generally remain cloud-based.

---

# 37. Cost Principle

Recurring infrastructure cost MUST remain intentionally low.

A new paid service MUST justify:

1. the problem it solves;
2. why existing tools cannot solve it adequately;
3. recurring cost;
4. expected benefit;
5. free/open alternative;
6. whether it introduces lock-in.

The project MUST NOT accumulate SaaS subscriptions simply because they are
convenient.

---

# 38. No Premature Platform

The initial product is the pipeline.

It is NOT:

- a SaaS;
- a multi-user application;
- a dashboard;
- a content-management platform;
- a complex web application.

The initial interface MAY consist of:

    filesystem
        +
    agent
        +
    natural language

A UI MAY be introduced later only when repeated workflows demonstrate a
clear need.

---

# 39. Content Project as the Unit of Work

The fundamental unit is a Content Project, not merely an MP4.

Conceptually:

    projects/
        <content-id>/
            idea
            script
            raw/
            transcript
            storyboard
            assets
            composition
            preview
            output
            qa
            performance

Exact filesystem structure belongs to technical specifications.

The architectural principle is that intermediate artifacts SHOULD remain
recoverable and reusable.

A project SHOULD be modifiable without reconstructing everything from zero.

---

# 40. Supply Chain v0.1

The first supported supply chain is:

    QUICK IDEA
        ↓
    CONTENT PREPARATION
        ↓
    SCRIPT / BULLETS
        ↓
    VERTICAL CAPTURE
        ↓
    INGESTION
        ↓
    TRANSCRIPTION
        ↓
    SEMANTIC ANALYSIS
        ↓
    STORYBOARD
        ↓
    VISUAL SELECTION / CREATION
        ↓
    COMPOSITION
        ↓
    CAPTIONS
        ↓
    AUDIO
        ↓
    CTA OPTIONAL
        ↓
    AUTOMATED QA
        ↓
    PREVIEW
        ↓
    HUMAN REVIEW
        ↓
    EDITORIAL ACCEPTANCE
        ↓
    FINAL RENDER
        ↓
    DELIVERY QA / HUMAN CONFIRMATION
        ↓
    PRODUCTION_APPROVED
        ↓
    DISTRIBUTION
        ↓
    PERFORMANCE ANALYSIS
        ↓
    LEARNING

---

# 41. Initial Success Criterion

The long-term target workflow is:

    RAÚL
    idea → record

    SYSTEM
    recording → finished production

    HUMAN
    review → approve

Manual editing SHOULD trend toward zero for routine Vertical Native content.

The primary operational metric is NOT:

    "Can the system render a video?"

It is:

    "How much human production work remains after recording?"

Relevant measurements SHOULD eventually include:

- human review time;
- number of correction iterations;
- render time;
- transcription cost;
- AI cost;
- percentage of reused visuals;
- automated QA failures;
- human QA failures;
- production throughput.

---

# 42. Amendment Rule

This Constitution is versioned.

It is intentionally not immutable.

However, changes MUST be deliberate.

Do not modify constitutional principles merely because a single feature is
inconvenient to implement.

A constitutional amendment SHOULD be justified by at least one of:

- a fundamental product change;
- repeated production evidence;
- repeated audience-performance evidence;
- a major technical constraint;
- a clearly superior architectural principle.

Feature implementation SHOULD conform to the Constitution.

The Constitution SHOULD NOT conform to implementation accidents.

---

# 43. Final Principle

The project optimizes for:

    KNOWLEDGE
        ↓
    CLARITY
        ↓
    CONSISTENCY
        ↓
    REUSE
        ↓
    AUTOMATION
        ↓
    SCALE

Not:

    MORE EFFECTS
        ↓
    MORE TOOLS
        ↓
    MORE COMPLEXITY

The final standard is simple:

> The system exists to make Raúl's knowledge easier to understand,
> not to make the editing more noticeable.

---

## Amendment record — 0.1.1 (2026-10-02)

- Corrected the project name and made the personal-brand boundary explicit.
- Required QA and human review after regeneration; clarified that production
  approval belongs to the successfully rendered, checked, explicitly approved
  revision, resolving the previous approval-before-final-render sequence.
- Distinguished the retake marker from ordinary narration using "again".
- Aligned the approval checklist with the caption exception already allowed
  by Section 22.
- Moved numeric studio-light calibration targets into `tech-stack.md`, retaining
  the constitutional requirement to calibrate physical lighting against footage.

The existing capture, palette, editorial, cost, resource, and visual-grammar
decisions remain in force.
