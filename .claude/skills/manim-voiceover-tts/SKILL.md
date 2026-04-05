---
description: Workarounds for KokoroService TTS mispronunciations and voiceover best practices. Use when writing voiceover text in Manim scripts.
globs: ["*.py"]
---

# Manim Voiceover & TTS Pitfalls

## TTS Engine

- Uses `KokoroService` from custom `kokoro_mv` module.
- Voice: `af_heart`, Language: `en-us`
- Initialize: `self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))`

## Known Mispronunciations — MUST AVOID

### The letter "A" as a variable name
- **Problem**: TTS reads the single letter "A" as the article "a" (uh/ay), not as "the matrix A".
- **Fix**: Use other letters for matrix variables in voiceover text: X, Y, Z, W, M.
- Example: Instead of "matrix A", say "matrix W" or "matrix M".

### The word "eigenvalue"
- **Problem**: TTS mispronounces any word with the prefix "eigen" — including "eigenvalue", "eigenvector", "eigenspace", etc.
- **Fix**: Use alternatives:
  - "eigenvalue" → "spectral value", "value in the spectrum", or just "spectrum"
  - "eigenvector" → "characteristic vector"
  - "eigenspace" → "characteristic subspace"
- Example: Instead of "the eigenvalues are nonnegative", say "every value in its spectrum is nonnegative".
- Example: Instead of "pick the eigenvector entry", say "pick the characteristic vector entry".

### Ordinals: "i-th", "k-th", etc.
- **Problem**: TTS reads "i-th" as three separate letters "i t h" instead of the ordinal.
- **Fix**: Rephrase to avoid the ordinal entirely.
- Example: Instead of "the i-th bit", say "bit i" or "the bit at position i" or "coordinate i".
- Example: Instead of "the k-th entry", say "entry k" or "the entry at position k".

### Names
- **Always verify author names.** For Helton's theorem, the first name is **John**, not William.
- When unsure about a name, look it up before writing voiceover text.

## Voiceover Writing Style

- Write in natural spoken English, not mathematical notation.
- Spell out math: "X 1 transpose X 2" not "$X_1^T X_2$".
- Use spaces between variable names: "X 1" not "X1".
- Spell out operations: "times", "plus", "minus", "transpose", "inverse".
- Read matrices by entries: "the matrix 2, 1, 1, 2" not "the matrix [[2,1],[1,2]]".
- Use "succeeds or equals zero" for $\succeq 0$ (positive semidefinite).
- Use "nonnegative" not "non-negative" (TTS handles single words better).

## Voiceover + Animation Sync

```python
with self.voiceover(
    text="Step one is the Gram representation..."
):
    self.play(Write(title))
    self.play(FadeIn(content))
    self.wait(0.5)
    self.play(Write(equation))
```

- Place animations inside the `with self.voiceover():` block.
- The voiceover auto-waits until speech finishes.
- Add `self.wait()` calls between animation groups for pacing (see **manim-pacing** skill for specific durations).
- Add a scene-end pause (`self.wait(1.5)`) AFTER the voiceover block before `clear_screen()`.

## Voiceover Text Formatting

- Use plain strings, not raw strings (no LaTeX in voiceover text).
- Use Python string concatenation for long voiceovers:
  ```python
  text="First sentence. "
       "Second sentence. "
       "Third sentence."
  ```
- Keep individual voiceover blocks to 3-5 sentences max.
