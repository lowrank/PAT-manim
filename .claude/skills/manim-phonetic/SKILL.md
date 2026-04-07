---
description: Phonetic pronunciation patterns for TTS voiceover in Manim scenes. Use when voiceover text contains math terms, proper names, acronyms, or symbols that Kokoro TTS mispronounces.
globs: ["*.py"]
---

# Manim Phonetic Pronunciation Patterns

## The Problem

Kokoro TTS (and other TTS engines) mispronounce:
- **Mathematical terms**: `liminf`, `bmod`, `vartheta`
- **Proper names**: `Yitang Zhang`, `Bombieri`, `Vinogradov`, `Kloosterman`
- **Acronyms**: `GPY`, `CRT`, `GEH` (read as words instead of letters)
- **Greek letters**: `phi` (read as "fih" instead of "fee")

## The Solution: Phonetic Text + Subcaption

Send phonetic spelling to TTS, show correct text as subtitles:

```python
from zhang_phonetics import get_phonetic_text

script = "Zhang proved that GPY needs theta > 1/2."

with self.voiceover(
    text=get_phonetic_text(script),    # TTS reads: "Jahng proved that G P Y needs theta..."
    subcaption=script,                  # Subtitles show: "Zhang proved that GPY..."
):
    self.play(FadeIn(content), run_time=2.0)
```

## Phonetic Dictionary

### Names

| Original | Phonetic |
|----------|----------|
| Yitang | Yee-tahng |
| Zhang | Jahng |
| Goldston | Gold-stone |
| Pintz | Pints |
| Yildirim | Yil-deh-rim |
| Bombieri | Bom-bee-air-ee |
| Vinogradov | Vee-no-grah-dov |
| Deligne | Deh-leen |
| Maynard | May-nard |
| Elliott | El-ee-ott |
| Halberstam | Hal-ber-stam |
| Eratosthenes | Eh-ra-tos-theh-neez |
| Dirichlet | Dee-ree-shlay |
| Kloosterman | Kloos-ter-mahn |
| Cauchy | Co-shee |
| Schwarz | Shvarts |
| Weil | Vile |

### Technical Acronyms

| Original | Phonetic |
|----------|----------|
| GPY | G P Y |
| CRT | C R T |
| GEH | G E H |
| PNT | P N T |

### Math Terms

| Original | Phonetic |
|----------|----------|
| liminf | limit infimum |
| bmod | mod |
| vartheta | theta |
| phi | fee |
| epsilon | ep-sil-on |
| ll | is much less than |
| sup | supremum |

## Convenience Wrapper

```python
from zhang_phonetics import voiceover_safe

voiceover_safe(self, "Zhang proved the GPY barrier.")
# Equivalent to:
# self.voiceover(
#     text=get_phonetic_text("Zhang proved the GPY barrier."),
#     subcaption="Zhang proved the GPY barrier.",
# )
```

## Adding New Pronunciations

Edit `zhang_phonetics.py`:

```python
PRONUNCIATIONS = {
    "NewWord": "New-fon-etic",
    ...
}
```

For regex patterns (LaTeX tokens):

```python
LATEX_PATTERNS = {
    r"\$\\newcommand\$": "new command",
    ...
}
```

## Words to Watch For

Always phoneticize these when they appear in voiceover:

- **Any non-English name** (Chinese, Italian, Russian, German, French)
- **Acronyms of 2-4 letters** (TTS reads them as words: "GPY" → "gip-ee")
- **Greek letter names** in English text (not in LaTeX math)
- **Math operator names**: `liminf`, `sup`, `inf`, `max`, `min`
- **Technical terms**: `etale`, `Kloosterman`, `Mangoldt`

## Testing Pronunciation

Render a single scene with a short test voiceover:

```bash
manim -pql storyboard.py Scene01_Intro
```

Listen to the output. If a word sounds wrong, add it to the phonetic dictionary.
