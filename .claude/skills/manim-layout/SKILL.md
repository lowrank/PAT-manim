---
description: Layout patterns for centering, alignment, and handling screen overflow in Manim scenes. Use when positioning content groups, math equations, or splitting scenes.
globs: ["*.py"]
---

# Manim Layout & Centering Patterns

## The Standard Content Block Pattern

Content blocks should be **centered on screen** but **internally left-aligned**:

```python
group = VGroup(header, explanation, equation, note)
group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
group.next_to(title, DOWN, buff=0.5)
group.set_x(0)          # center the whole block horizontally
center_mathtex(group)    # center only MathTex items within
```

Or use the helper:
```python
from latent_utils import make_content_group
group = make_content_group(header, explanation, equation, note, reference=title)
```

## How `.set_x(0)` Works

- `.set_x(0)` centers a mobject's **bounding box** horizontally on the scene.
- Applied to a VGroup, it shifts the entire group so its center is at x=0.
- This preserves internal left-alignment from `.arrange(aligned_edge=LEFT)`.

## `center_mathtex()` — Selective Centering

- Single-line `MathTex` formulas should be centered on the scene (`.set_x(0)` per item).
- `Tex` text items should remain left-aligned within the group.
- `center_mathtex(group)` does this automatically by checking:
  `isinstance(child, MathTex) and not isinstance(child, Tex)`
- This works because `Tex` is a subclass of `MathTex` in Manim's class hierarchy.

## Handling Screen Overflow

When content doesn't fit on screen, split into sub-scenes:

```python
# Scene 2a: First half of content
# ... show and FadeOut

# Scene 2b: Second half of content
# ... show and FadeOut
```

Rules:
- Keep the **title persistent** across sub-scenes (don't FadeOut the title between parts).
- FadeOut the content group at the end of each sub-scene.
- Use consistent `buff` values within a scene family.

## Centering Boxed Equations

Boxed equation cards (from `make_theorem_card`) should be centered independently:

```python
card, rect, content = make_theorem_card(eq1, eq2, color=GREEN)

all_content = VGroup(header, card, note).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
all_content.next_to(title, DOWN, buff=0.5).set_x(0)
card.set_x(0)  # center the card independently within the group
```

## Side-by-Side Arrangements

For items that should appear in a row (e.g., two matrices):

```python
row = VGroup(matrix_X, matrix_Y).arrange(RIGHT, buff=1.0)
```

Then include the row as a single item in the vertical group.

## Title Positioning

Titles go at the top edge:
```python
title = Text("Step 1: ...", font_size=36, color=BLUE).to_edge(UP, buff=0.5)
```

Content is placed below:
```python
content.next_to(title, DOWN, buff=0.5)
```

## Common `buff` Values

| Context | Recommended `buff` |
|---------|-------------------|
| Between title and content | 0.4 - 0.5 |
| Between items in a group | 0.25 - 0.35 |
| Between major sections | 0.5 - 0.7 |
| Inside boxed cards | 0.2 - 0.3 |
| Side-by-side items | 0.4 - 1.0 |

## Font Size Conventions

| Element | Font Size |
|---------|-----------|
| Scene title | 40-44 |
| Section header | 30-32 |
| Body text (Tex) | 28-30 |
| Main equations (MathTex) | 32-38 |
| Notes / secondary text | 26-28 |
| Labels on diagrams | 22-26 |
| Photo / caption labels | 22-24 |
| Final boxed result | 42-48 |
| Diagram vertex labels | 22-24 |
| Diagram dot radius | 0.09 |
