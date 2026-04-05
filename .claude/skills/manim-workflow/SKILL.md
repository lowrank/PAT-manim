---
description: Three-stage model pipeline for producing Latent Seminar Manim videos. At each stage, ask the user which model to use. Use when starting a new Manim video project or handing off between stages.
globs: ["*.py"]
---

# Manim Video Production Workflow

## Overview

Latent Seminar videos are produced in three stages. **At the start of each stage, ask the user which model they want to use.** The recommended defaults are listed below, but the user always chooses.

## Stage Transitions

**IMPORTANT:** Before starting each stage, present the user with a model choice. Example:

> "Ready for Stage 1 (Draft). Which model would you like to use?"
> - Gemini Flash 2.5 (Recommended for drafting)
> - Claude Sonnet 4.5
> - Claude Opus 4.6
> - (or type your own)

Do the same before Stage 2 and Stage 3.

## Stage 1: Draft

**Recommended model:** Gemini Flash 2.5 (fast iteration, cheap tokens)

**Goal:** Get a working Manim script with correct structure and content, fast.

**What to do:**
- Describe the animation concept, target audience, and desired duration.
- Produce a working Manim script with basic animations and scene flow.
- Iterate 2-3 times until the structure, scene order, and mathematical content are roughly correct.
- Don't worry about Latent Seminar conventions, layout polish, or voiceover quality yet.

**Focus on:**
- Correct math and definitions
- Scene ordering and logical flow
- Basic animations that convey the right ideas
- Getting the content complete (nothing missing)

**Don't worry about (yet):**
- `latent_utils.py` integration
- Prelude animation
- Voiceover TTS pitfalls
- Precise layout, centering, font sizes
- Color conventions

**Output:** A rough but functional `.py` file that renders without errors.

## Stage 2: Rewrite & Polish

**Recommended model:** Claude Sonnet 4.5 (balance of quality and speed)

**Goal:** Rewrite the draft to follow all Latent Seminar conventions and polish the code.

**What to provide:**
- The draft `.py` file from Stage 1
- All skills from `.claude/skills/` (they load automatically if working in the `latent-seminar` repo)

**What to do:**
- Rewrite imports to use `latent_utils.py` (`center_mathtex`, `make_content_group`, `make_theorem_card`, `LatentPrelude`, etc.)
- Add the `LatentPrelude` mixin and `self.play_prelude()` call
- Reorganize into clean scene blocks with `# ===` separators
- Apply layout patterns: `.arrange(DOWN, aligned_edge=LEFT)` + `.set_x(0)` + `center_mathtex()`
- Replace manual `SurroundingRectangle` with `make_theorem_card()`
- Write voiceover text following TTS rules (avoid "A" as variable, avoid "eigenvalue", spell out math)
- Apply color conventions (BLUE for titles, TEAL for Gram, GOLD for Krein, GREEN for results, etc.)
- Apply font size conventions
- Split scenes that overflow the screen
- Add pedagogical elements: worked examples, analogies, intuition, verification, insights

**Output:** A polished `.py` file following all conventions.

## Stage 3: Final Review

**Recommended model:** Claude Opus 4.6 (highest quality, careful review)

**Goal:** Final pass for accuracy, quality, and correctness.

**What to check:**
- Mathematical accuracy of all formulas and statements
- Voiceover text reads naturally when spoken aloud
- No LaTeX concatenation bugs (e.g., `r"\quad"` + `r"Q"` producing `\quadQ`)
- Geometric diagrams: dots/labels created AFTER group positioning
- Screen overflow: every scene fits without clipping
- Font sizes and buff values are consistent
- All `self.wait()` calls provide appropriate pacing
- TTS mispronunciation rules are followed
- Author names and dates are correct
- Pedagogical quality: examples are illuminating, analogies are accurate, insights are genuine

**What to do:**
- Read through the entire script carefully
- Fix any issues found
- Test render: `source activate my-manim-environment && manim render <file>.py <Scene> -ql --disable_caching`
- Verify 0 errors in the render output
- Watch the rendered video if possible to check timing

**Output:** The final production-ready `.py` file.

## Project Folder Lifecycle

1. **Create** a new folder under `/home/lowrank/workplace/work/manim-videos/<ProjectName>/`
2. **Copy** into it: `kokoro-v1.0.onnx`, `voices-v1.0.bin`, `prelude_music.mp3`, `latent_utils.py`
   - `kokoro_mv` is a site-package in `my-manim-environment`, no copy needed
3. **Work** in the project folder through all 3 stages
4. **Do NOT** automatically copy source files to `latent-seminar/` — wait for the user to decide
5. **Do NOT** automatically delete the project folder — the user will clean up when ready

## Render Command

```bash
source activate my-manim-environment && cd /home/lowrank/workplace/work/manim-videos/<ProjectName> && manim render <file>.py <SceneName> -ql --disable_caching
```

## Conda Environment

- Name: `my-manim-environment` (hyphens)
- Activate: `source activate my-manim-environment`
- Manim Community v0.20.1
- Includes: `manim_voiceover`, `kokoro_mv` (KokoroService)
