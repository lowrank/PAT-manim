---
description: API reference for latent_utils.py — the shared utility library for Latent Seminar Manim videos. Use when importing or calling functions from latent_utils.
globs: ["*.py"]
---

# latent_utils.py — Shared Library Reference

## Installation

The library lives at the project root as `latent_utils.py`. Import what you need:

```python
from latent_utils import (
    center_mathtex,
    make_content_group,
    make_theorem_card,
    LatentPrelude,
    clear_screen,
    SEMINAR_BLUE,
)
```

## API

### `SEMINAR_BLUE`

```python
SEMINAR_BLUE = "#6fa8dc"
```

The signature blue used for Latent Seminar branding.

---

### `center_mathtex(group) -> VGroup`

Centers standalone `MathTex` items within a VGroup horizontally (`.set_x(0)`), while leaving `Tex` items at their left-aligned position. Only acts on direct children.

```python
group = VGroup(tex_header, mathtex_eq, tex_note).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
center_mathtex(group)  # only mathtex_eq gets centered
```

---

### `make_content_group(*items, reference=None, buff_between=0.3, buff_below=0.5, aligned_edge=LEFT, center_math=True) -> VGroup`

Builds a left-aligned, horizontally-centered content block in one call.

```python
group = make_content_group(
    header, explanation, equation, note,
    reference=title,       # placed below this mobject
    buff_between=0.3,      # vertical spacing
    buff_below=0.5,        # gap below reference
)
```

Equivalent to:
```python
group = VGroup(header, explanation, equation, note)
group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
group.next_to(title, DOWN, buff=0.5)
group.set_x(0)
center_mathtex(group)
```

---

### `make_theorem_card(*content_items, color=GREEN, buff=0.3, corner_radius=0.1, stroke_width=2.5, content_buff=0.2) -> tuple[VGroup, SurroundingRectangle, VGroup]`

Creates a boxed theorem/equation card. Returns `(card, rect, content)`.

```python
card, rect, content = make_theorem_card(
    eq_line1, eq_line2,
    color=GREEN,
    buff=0.3,
)

# Animate:
self.play(FadeIn(content), Create(rect))
self.play(Circumscribe(card, color=GREEN, time_width=2))
```

For single-item cards:
```python
card, rect, _ = make_theorem_card(equation, color=TEAL, buff=0.2, stroke_width=2)
```

---

### `LatentPrelude` (mixin class)

Adds `play_prelude()` to any VoiceoverScene. Use as a mixin (first in MRO):

```python
class MyScene(LatentPrelude, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))
        self.play_prelude()                    # all defaults
        self.play_prelude(music_file="my.mp3") # custom music
        # ... rest of animation
```

Parameters (all optional with defaults):
- `music_file="prelude_music.mp3"` — path to opening music clip
- `font_size=60` — branding text size
- `letter_time=0.08` — seconds per character
- `latent_run_time=0.6` — duration for "Latent" animation
- `seminar_run_time=0.7` — duration for "Seminar" animation
- `pause_between=0.5` — pause after "Latent" before "Seminar"
- `glow_run_time=1.5` — glow pulse duration
- `hold_after_glow=1.4` — hold until music fades
- `dissolve_run_time=1.0` — fade-out duration
- `post_wait=0.3` — pause after dissolve

---

### `clear_screen(scene, run_time=0.5)`

Fades out all mobjects currently on screen.

```python
clear_screen(self)         # from inside a scene
clear_screen(self, 0.3)   # faster fade
```

## Complete Example

```python
from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
from latent_utils import (
    center_mathtex, make_content_group, make_theorem_card,
    LatentPrelude, clear_screen, SEMINAR_BLUE,
)

class MyProofVideo(LatentPrelude, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))
        self.play_prelude()

        title = Text("My Theorem", color=BLUE, font_size=40).to_edge(UP, buff=0.5)
        eq = MathTex(r"E = mc^2", font_size=36, color=GREEN)
        card, rect, _ = make_theorem_card(eq, color=GREEN)
        note = Tex(r"A famous result.", font_size=26, color=GREY_B)

        group = make_content_group(card, note, reference=title)
        card.set_x(0)

        with self.voiceover(text="Here is the theorem."):
            self.play(Write(title))
            self.play(FadeIn(eq), Create(rect))
            self.play(FadeIn(note))

        clear_screen(self)
```
