---
title: Braid Docs
hide:
  - navigation
  - toc
---

<div class="braid-hero" markdown>

<span class="braid-hero__eyebrow">Protocol &amp; Product Docs</span>

# Braid Docs

<p class="braid-hero__lead">Braid is the accountability layer for software work. It records what happened, who did it, what shaped the work, and what was vouched for — across both humans and agents.</p>

<div class="braid-hero__actions" markdown>
[Get started](getting-started/introduction.md){ .md-button .md-button--primary }
[Read the protocol](protocol/overview.md){ .md-button }
</div>

</div>

<h2 class="hub-section-title">Explore the docs</h2>

<div class="grid cards" markdown>

-   :material-rocket-launch-outline:{ .lg .middle } __Getting Started__

    ---

    What Braid is, why it exists, and how to send your first events.

    [:octicons-arrow-right-24: Start here](getting-started/introduction.md)

    <span class="page-count">3 pages</span>

-   :material-shape-outline:{ .lg .middle } __Concepts__

    ---

    The vocabulary: braids, threads, contributors, events, reviews, decisions.

    [:octicons-arrow-right-24: Learn the model](concepts/braids.md)

    <span class="page-count">6 pages</span>

-   :material-sitemap-outline:{ .lg .middle } __Protocol__

    ---

    The wire contract — entity relations, the `WorkEvent` envelope, and capture.

    [:octicons-arrow-right-24: Read the protocol](protocol/overview.md)

    <span class="page-count">5 pages</span>

-   :material-map-marker-path:{ .lg .middle } __Walkthroughs__

    ---

    Concrete event stories: humans, agents, sub-agents, review and promote.

    [:octicons-arrow-right-24: Follow a story](stories/human-thread.md)

    <span class="page-count">4 pages</span>

-   :material-book-open-variant:{ .lg .middle } __Reference__

    ---

    Payload-kind catalog, glossary, and frequently asked questions.

    [:octicons-arrow-right-24: Look it up](reference/payload-kinds.md)

    <span class="page-count">3 pages</span>

-   :material-cog-outline:{ .lg .middle } __Operations__

    ---

    Keeping docs in sync with the proto, and deploying this site.

    [:octicons-arrow-right-24: Operate the docs](keeping-docs-current.md)

    <span class="page-count">2 pages</span>

</div>

<h2 class="hub-section-title">Start with the model</h2>

<div class="grid cards" markdown>

-   __Entity relations__

    ---

    How braids, threads, contributors, events, reviews, and decisions fit
    together.

    [:octicons-arrow-right-24: See the chart](protocol/entity-relations.md)

-   __Event stories__

    ---

    Which events get sent while humans and agents work, and why each one
    matters to a future reviewer.

    [:octicons-arrow-right-24: Walk through work](protocol/event-stories.md)

-   __WorkEvent reference__

    ---

    The canonical event envelope, its required fields, and every payload kind.

    [:octicons-arrow-right-24: Read the reference](protocol/work-event.md)

</div>

!!! info "Source of truth"
    The proto is the canonical wire contract:
    [`Prototype/api/proto/braid/work/v1/work.proto`](https://github.com/braidkit/Prototype/blob/main/api/proto/braid/work/v1/work.proto).
    These docs explain the shape and intent of that contract; they do not replace it.
