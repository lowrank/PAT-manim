---
description: Pedagogical guidelines for making Manim math videos accessible to graduate students. Use when writing voiceover text, choosing examples, or deciding what to explain in detail.
globs: ["*.py"]
---

# Manim Pedagogy — Graduate-Level Accessibility

## Target Audience

General graduate students — not specialists in the specific field. They have mathematical maturity (linear algebra, analysis, basic algebra) but may not know the specialized topic.

## Core Principles

### 1. Intuition Before Formalism

Always state the idea in plain language before showing the formula.

**Bad:**
```python
# Jump straight to the formula
eq = MathTex(r"Q(X) = V(X)^T M_Q V(X)")
```

**Good:**
```python
# Explain the idea first
intuition = Tex(r"\textbf{Key Idea:} Rewrite $Q(X)$ as a \textit{quadratic form} in noncommuting monomials.")
# Then the analogy
analogy = Tex(r"Analogy: just as $ax^2 + bxy + cy^2 = [x, y]^T \begin{bmatrix} a & b/2 \\ b/2 & c \end{bmatrix} [x, y]$")
# Then the formula
eq = MathTex(r"Q(X) = V(X)^T M_Q V(X)")
```

### 2. Worked Examples After Every Definition

Every abstract definition or theorem should be followed by a concrete, small-dimensional example.

- Use 2x2 or 3x3 matrices when possible.
- Show specific numerical values.
- Walk through the computation step by step.

**Example pattern:**
```
Definition -> Example label -> Specific instance -> Step-by-step computation -> Checkmark
```

### 3. Analogies to Familiar Concepts

Connect unfamiliar concepts to things graduate students already know:

| Unfamiliar | Analogy |
|------------|---------|
| Gram representation | "Like writing a quadratic form as x^T A x" |
| Ghost matrices | "Like the null space — perturbations that don't change the output" |
| Krein's theorem | "A cousin of the Hahn-Banach theorem" |
| Affine plane of Gram matrices | "Like a coset in group theory: a fixed element plus a subspace" |
| Cholesky factorization | "Like taking a square root of a matrix" |

### 4. Step-by-Step Verification

After deriving a formula, show that it actually works by expanding or plugging in numbers.

```python
# Show the formula
eq = MathTex(r"V^T M_Q V = Q")
# Then verify
verify = MathTex(r"= X_1 X_2 + X_2^T X_1^T + X_1 X_1^T + 2\,X_2^T X_1^T X_1 X_2 = Q \;\checkmark")
```

Always end verification with a green checkmark (`\checkmark`) for visual confirmation.

### 5. Numerical Checks

After abstract results, plug in concrete matrices to build confidence.

```python
num_label = Tex(r"\textbf{Numerical check} ($2 \times 2$ matrices):", color=YELLOW)
# Show specific matrix values
# Compute step by step
# Show final result is PSD with checkmark
```

### 6. Geometric Pictures

When a concept has geometric content, add a visual diagram:

- **Cones** for PSD matrices (triangle/polygon shape)
- **Lines/planes** for affine spaces
- **Dots** for intersection points
- **Animated dots** sliding along planes to show search for intersection

### 7. Proof Roadmaps

Before a multi-step proof, show a visual roadmap so the audience knows where they're going:

- Color-coded boxes for each step
- Arrows between steps showing logical flow
- Brief 1-line description in each box
- Animate step-by-step appearance

### 8. Highlight the "Aha" Moments

Use visual emphasis to draw attention to surprising or key insights:

- `Circumscribe(mob, color=GREEN)` for key results
- `Indicate(mob, color=ORANGE)` for important terms
- `Flash(dot, color=GREEN)` for geometric breakthroughs
- Colored boxes (`make_theorem_card`) for theorem statements

### 9. Point Out What's Surprising

Explicitly call out when results are counterintuitive or surprising:

- "Surprisingly, the answer is no" (Motzkin counterexample)
- "This polynomial is invisible in commutative algebra!" (commutator squared)
- "Noncommutativity is a feature, not a bug"

### 10. Voiceover Pacing

See the **manim-pacing** skill for detailed timing guidelines. Key points:

- Use named pause durations (PAUSE_ELEMENT, PAUSE_KEY_RESULT, etc.) for consistent rhythm.
- One concept per voiceover block; don't rush multiple ideas into a single block.
- Step through examples one piece at a time in the voiceover text, not all at once.
- Scale pauses by importance: definitions get shorter pauses, key results get longer ones.

## Scene Content Checklist

For each major concept in the video, verify you have:

- [ ] Plain-language intuition or motivation
- [ ] Formal definition or statement
- [ ] At least one concrete example (small matrices, specific numbers)
- [ ] Verification or numerical check where applicable
- [ ] Analogy to a familiar concept (if one exists)
- [ ] Visual emphasis on key results
- [ ] Appropriate pauses for digestion

## Anti-Patterns to Avoid

- **Definition dumping**: Don't list 5 definitions in a row without examples.
- **Notation overload**: Introduce notation gradually, not all at once.
- **Skipping "obvious" steps**: What's obvious to a specialist isn't obvious to a general grad student.
- **Abstract-only proofs**: Every abstract argument should be grounded with at least one concrete instance.
- **Wall of text**: Break content into sub-scenes; split when things get crowded.
