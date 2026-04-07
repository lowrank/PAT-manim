"""
Phonetic pronunciation dictionary .

Usage:
    from BoundedGapPrimeNumbers-Phonetics import get_phonetic_text, get_subcaption

    script = "Zhang proved that GPY needs theta > 1/2."
    with self.voiceover(
        text=get_phonetic_text(script),
        subcaption=get_subcaption(script),
    ):
        self.play(...)
"""

import re


# ── Phonetic replacements ─────────────────────────────────────────────

PRONUNCIATIONS = {
    # Names
    "Yitang": "Yee-tahng",
    "Zhang": "Jahng",
    "Goldston": "Gold-stone",
    "Pintz": "Pints",
    "Yildirim": "Yil-deh-rim",
    "Bombieri": "Bom-bee-air-ee",
    "Vinogradov": "Vee-no-grah-dov",
    "Deligne": "Deh-leen",
    "Maynard": "May-nard",
    "Elliott": "El-ee-ott",
    "Halberstam": "Hal-ber-stam",
    "Eratosthenes": "Eh-ra-tos-theh-neez",
    "Dirichlet": "Dee-ree-shlay",
    "Kloosterman": "Kloos-ter-mahn",
    "Cauchy": "Co-shee",
    "Schwarz": "Shvarts",
    "Weil": "Vile",
    "Polymath": "Pol-ee-math",

    # Technical terms
    "GPY": "G P Y",
    "CRT": "C R T",
    "GEH": "G E H",
    "PNT": "P N T",
    "BV": "B V",

    # Math notation spoken
    "liminf": "limit infimum",
    "bmod": "mod",
    "mathbb": "",
    "vartheta": "theta",
    "Lambda": "Lambda",
    "phi": "fee",
    "epsilon": "ep-sil-on",
    "Rightarrow": "implies",
    "exists": "there exists",
    "forall": "for all",
    "mid": "divides",
    "cong": "is congruent to",
    "ll": "is much less than",
    "sup": "supremum",
}

# Words to keep in subcaption but replace in TTS
# These are LaTeX-like tokens that appear in voiceover text
LATEX_PATTERNS = {
    r"\$\\liminf\$": "limit infimum",
    r"\$\\theta\$": "theta",
    r"\$\\delta\$": "delta",
    r"\$\\rho\$": "rho",
    r"\$\\psi\$": "psi",
    r"\$\\alpha\$": "alpha",
    r"\$\\beta\$": "beta",
    r"\$\\pi\$": "pi",
    r"\$\\phi\$": "fee",
    r"\$\\Lambda\$": "Lambda",
    r"\$\\vartheta\$": "theta",
    r"\$\\mathbb\{Z\}\$": "the integers Z",
    r"\$\\mathbb\{F\}\$": "the field F",
}


def get_phonetic_text(text: str) -> str:
    """Convert text to phonetic spelling for TTS pronunciation."""
    result = text

    # Apply direct word replacements
    for word, phonetic in PRONUNCIATIONS.items():
        result = result.replace(word, phonetic)

    # Apply LaTeX pattern replacements
    for pattern, replacement in LATEX_PATTERNS.items():
        result = re.sub(pattern, replacement, result)

    return result


def get_subcaption(text: str) -> str:
    """Return the original text for subcaption display."""
    return text


def voiceover_safe(self, text: str, **kwargs):
    """Convenience wrapper for voiceover with phonetic text and subcaption.

    Usage:
        voiceover_safe(self, "Zhang proved the GPY barrier.")
    """
    return self.voiceover(
        text=get_phonetic_text(text),
        subcaption=get_subcaption(text),
        **kwargs,
    )
