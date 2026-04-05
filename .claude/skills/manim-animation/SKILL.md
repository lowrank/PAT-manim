---
description: Best practices for writing Manim Community animations for math explainer videos. Use when creating or editing .py files that use manim, VoiceoverScene, or MathTex.
globs: ["*.py"]
---

# Manim Animation Best Practices

## Environment

- Manim Community v0.20.1 with `manim_voiceover` and custom `kokoro_mv` module (KokoroService).
- Conda environment: `my-manim-environment` (hyphens, not underscores).
- Activate: `source activate my-manim-environment`
- Render: `manim render <file>.py <SceneName> -ql --disable_caching`

## Scene Structure

- Use `VoiceoverScene` as the base class (from `manim_voiceover`).
- Initialize TTS in `construct()`: `self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))`
- Organize content into clearly commented scene blocks with `# ===` separators.
- Split scenes that overflow the screen into sub-scenes (e.g., Scene 2a, 2b).

## LaTeX and Math

- Use `MathTex` for pure math formulas, `Tex` for text with inline math.
- `Tex` is a subclass of `MathTex` — to select only pure math objects, use:
  `isinstance(child, MathTex) and not isinstance(child, Tex)`
- Use `tex_environment="flushleft"` for multi-line Tex that should be left-aligned internally.
- **LaTeX concatenation bug**: When Python implicitly concatenates raw strings like `r"\quad"` followed by `r"Q = ..."`, LaTeX sees `\quadQ` (undefined control sequence). Always add a trailing space: `r"\quad "`.

## Animation Patterns

- Use `Write()` for math equations, `FadeIn()` for text blocks.
- Use `Circumscribe()` and `Indicate()` to highlight key results.
- Use `Flash()` for intersection points or key moments.
- Pair voiceovers with animations using `with self.voiceover(text="..."):` blocks.
- Add `self.wait()` between major content transitions (see **manim-pacing** skill for specific durations).
- Clean up with `self.play(FadeOut(...))` before transitioning to new content.

## Geometric Diagrams

- Use absolute coordinates for geometry (cones, planes, dots), then reposition the group with `.next_to()`.
- **Critical**: Create dots and labels AFTER the group is positioned, otherwise they end up at wrong locations.
- For animated dots on lines, use `line.point_from_proportion()` to get points along the line.

## Boxed Theorem Cards

Use `make_theorem_card()` from `latent_utils`:

```python
from latent_utils import make_theorem_card
card, rect, content = make_theorem_card(text1, text2, color=GREEN, buff=0.3)
# Animate: self.play(FadeIn(content), Create(rect))
```

## Proof Roadmaps

- Use `RoundedRectangle` boxes with color-coded steps.
- Add `Arrow` objects between steps for flow.
- Animate step-by-step with `FadeIn(step, shift=RIGHT * 0.3)`.

## Color Conventions

| Purpose | Color |
|---------|-------|
| Step 1 / titles | BLUE |
| Step 2 / Gram | TEAL |
| Step 3 / Krein | GOLD |
| Step 4 / result | GREEN |
| Warnings / problems | YELLOW / RED |
| Notes / secondary | GREY_B |
| Examples | YELLOW |
