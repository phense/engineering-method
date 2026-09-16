---
name: visual-placeholders
description: "Use as a supporting skill when documentation needs screenshots, diagrams, or other images that do not exist yet or must be reproducible: insert standardized placeholder callouts with stable IDs, alt text, captions and capture instructions, and keep the asset manifest in step. Not for producing the images, for UML architecture analysis, or for decorative illustration."
---

# Visual Placeholders

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Text and image must say the same thing. A placeholder is a contract: it states
what the reader must see, where in the text it belongs, and how to produce the
image later so that it proves exactly that.

## Trigger

Use while drafting any chunk where a screenshot or diagram would let the
reader confirm a state faster than words, when the interface is not available
to capture, when images will be produced by someone else, or when the image
must be regenerated for every version.

## Do not use for

- Creating or editing image files; capture and drawing happen outside this
  skill following the manifest instructions.
- Architecture or design diagrams that answer engineering questions; those
  belong to `architecture-modeling` under `docs/uml/`.
- Images without a claim: if the caption cannot state what the reader learns,
  do not add the image.

## When an image earns its place

Add a placeholder when the image confirms a result after a step block,
locates an element that words locate poorly, shows a structure with more than
about five related parts, or compares states. Do not add one for every step;
a task chunk normally has one to three.

## Callout syntax

Insert the callout at the exact position in the text, as its own paragraph:

```markdown
> **[IMAGE A-012 | screenshot]** Settings page with the **API keys** tab
> selected and one key listed.
> Alt: The Settings page shows the API keys tab with one key named Production.
> Capture: Sign in as an administrator, open Settings from the gear icon in the
> top-right corner, select the API keys tab, ensure exactly one key exists,
> capture the full page at 1440 px width, highlight the Generate key button.
```

Rules:

- `A-<number>` is a stable ID that never changes; the number is not an order.
- Kind is one of screenshot, diagram, video, table-image, icon.
- The first line is the caption the reader will see: it states the fact the
  image proves, using glossary terms and exact interface labels.
- Alt text states the same fact in one sentence of at most about 150
  characters for readers who cannot see the image. It may start with the kind
  ("Screenshot of ..."), never with "Image of", and never repeats the caption
  word for word or names the file.
- Introduce the image in the preceding sentence and refer to it by ID or
  figure number, never as "above" or "below".
- Capture instructions are precise enough for another person: role, path,
  required state, element to highlight, size, and anything to mask.
- For diagrams, give the elements, relationships and reading direction, or
  point to a text source such as a Mermaid file that will render the image.

## Asset manifest

Every callout has one row in `docs/writing/<doc-id>/assets.md` from the
installed [asset manifest template](../../templates/documentation/assets.md),
and the chunk lists the asset ID in its `assets` frontmatter field. Update the
manifest in the same change as the callout. When an asset is captured, the
row moves to captured, the callout is replaced by the image reference with the
same caption and alt text, and the placeholder ID stays in an HTML comment
beside the image for later regeneration.

## Completion

Placeholders are complete for a scope when every callout has an ID, kind,
caption, alt text and capture instructions; every ID appears in the manifest
and in the chunk frontmatter; and no image lacks a claim the text also makes.

## Common mistakes

- Captions that name the screen instead of the fact to be observed.
- Alt text duplicating the caption word for word without the observable fact,
  or omitting alt text altogether.
- Capture instructions that assume the capturer knows the product.
- Renumbering asset IDs when chapters are reordered.
