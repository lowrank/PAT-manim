---
description: Latent Seminar branding, prelude animation, and video styling conventions. Use when creating a new Latent Seminar video or editing the prelude sequence.
globs: ["*.py"]
---

# Latent Seminar Branding & Style

## Brand Identity

- **"Latent"** is rendered in black (invisible against default background) with BOLD weight.
- **"Seminar"** is rendered in `SEMINAR_BLUE = "#6fa8dc"` with BOLD weight.
- The reveal effect: "Latent" appears letter-by-letter (invisible), then "Seminar" appears in blue. A glow pulse reveals "Latent" via a blue outline stroke.

## Prelude Animation

Use the `LatentPrelude` mixin from `latent_utils.py`:

```python
from latent_utils import LatentPrelude, SEMINAR_BLUE

class MyScene(LatentPrelude, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))
        self.play_prelude()  # default settings
        # ... rest of the animation
```

### Prelude Sequence (default timing ~6s total)

1. Music starts (`prelude_music.mp3`, ~5s with 2s fade-out starting at 3s)
2. "Latent" appears letter-by-letter (0.6s)
3. 0.5s pause
4. "Seminar" appears letter-by-letter (0.7s)
5. Glow pulse: blue outline on "Latent" fades in and out (1.5s, `there_and_back`)
6. Hold 1.4s (syncs with music fade)
7. Dissolve upward (1.0s)
8. Brief pause (0.3s)

### Prelude Music

Generated from source audio with:
```bash
ffmpeg -i "Amazing Grace - Casa Rosa.mp3" -t 5 -af "afade=t=out:st=3:d=2" -y prelude_music.mp3
```

### Design Decisions (User Preferences)

- **No particles** — rejected as too ugly
- **No sweep light bar** — rejected
- **No stagger dissolve** — rejected
- Keep it simple: letter-by-letter + glow pulse + dissolve

## Video Structure Convention

Every Latent Seminar video should follow this structure:

1. **Prelude** — Latent Seminar branding (~6s)
2. **Title Card** — Paper title, author, journal, year
3. **Motivation** — The big question / why this matters
4. **Proof Roadmap** — Visual overview of the proof steps
5. **Preliminaries** — Key definitions for a graduate audience
6. **Main Content** — Proof steps, each as a scene/sub-scene
7. **Application** — Concrete worked example
8. **Summary** — Recap with key takeaway

## Audience

- Target: **general graduate students** (not specialists)
- Add intuition, analogies, and worked examples
- Explain every step; don't skip "obvious" details
- Use visual aids (diagrams, color coding, highlights)
