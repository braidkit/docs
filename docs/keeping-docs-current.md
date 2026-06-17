# Keeping Docs Current

The proto remains the source of truth. Docs explain the model, but they should
not silently invent protocol facts.

## Source of truth markers

Protocol pages should link back to:

```text
Prototype/api/proto/braid/work/v1/work.proto
```

When a page describes field-level behavior, include the `Prototype` commit it
was reviewed against.

## PR rule

When a `Prototype` PR changes protocol semantics, the author should do one of:

- update this docs site in the same workstream, or
- add a short "docs not needed" reason to the PR.

## CI

This repo runs:

```sh
mkdocs build --strict
```

That catches broken links, missing pages, and malformed docs structure. Mermaid
diagrams are kept in Markdown so they are easy to review and update.

## Later automation

If drift becomes painful, add a small script that pulls selected facts from
`work.proto` into generated reference snippets. Keep narrative docs human-written.

