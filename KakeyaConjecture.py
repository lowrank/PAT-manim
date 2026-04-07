"""
Kakeya Conjecture Proof — Latent Seminar
Based on Wang-Zahl (2025): "Volume estimates for unions of convex sets,
and the Kakeya set conjecture in three dimensions"
"""

from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
from latent_utils import (
    center_mathtex,
    make_content_group,
    make_theorem_card,
    LatentPrelude,
    clear_screen,
    SEMINAR_BLUE,
)

# ── Named pauses (manim-pacing skill) ──
PAUSE_BRIEF = 0.5
PAUSE_ELEMENT = 1.0
PAUSE_READ = 1.5
PAUSE_ABSORB = 2.0
PAUSE_KEY_RESULT = 3.0
PAUSE_BREATHE = 3.5
PAUSE_SCENE_END = 1.5
PAUSE_FINALE = 4.0


class KakeyaProof(LatentPrelude, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))

        # === Prelude ===
        self.play_prelude()

        # === Title Card ===
        self._title_card()

        # === Motivation ===
        self._motivation()

        # === Proof Roadmap ===
        self._proof_roadmap()

        # === Preliminaries: Kakeya Sets ===
        self._prelim_kakeya_sets()

        # === Preliminaries: Wolff Axioms ===
        self._prelim_wolff_axioms()

        # === Step 1: Sticky vs Non-Sticky ===
        self._step1_sticky()

        # === Step 2: Multi-Scale Analysis ===
        self._step2_multiscale()

        # === Step 3: The Factoring Lemma ===
        self._step3_factoring()

        # === Step 4: High Density Lemma ===
        self._step4_high_density()

        # === Step 5: Self-Improving Iteration ===
        self._step5_iteration()

        # === Summary ===
        self._summary()

    # ──────────────────────────────────────────────
    # Title Card
    # ──────────────────────────────────────────────
    def _title_card(self):
        title = Tex(
            r"The Kakeya Set Conjecture in $\mathbb{R}^3$",
            font_size=38,
            color=BLUE,
        )
        title.to_edge(UP, buff=0.6)

        authors = Tex(
            "Based on Wang \\& Zahl (2025)", font_size=28, color=GREY_B
        )
        authors.next_to(title, DOWN, buff=0.4)

        journal = Tex(
            "To appear in JAMS", font_size=24, color=GREY_B
        )
        journal.next_to(authors, DOWN, buff=0.3)

        with self.voiceover(
            text="Welcome to Latent Seminar. "
            "Today we explore a breakthrough result in geometric measure theory: "
            "the proof of the Kakeya set conjecture in three dimensions, "
            "by Hong Wang and Joshua Zahl."
        ):
            self.play(Write(title))
            self.play(FadeIn(authors))
            self.play(FadeIn(journal))

        self.wait(PAUSE_SCENE_END)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Motivation: Needle Rotation Problem
    # ──────────────────────────────────────────────
    def _motivation(self):
        # --- Part A: The original Kakeya problem ---
        title = Tex(r"\text{The Needle Rotation Problem}", font_size=38, color=BLUE)
        title.to_edge(UP, buff=0.5)

        hist_header = Tex(
            r"\textbf{1917.} Soichi Kakeya asked:",
            font_size=28,
        )
        hist_body = Tex(
            r"What is the \textit{smallest area} region in the plane",
            font_size=28,
        )
        hist_body2 = Tex(
            r"in which a unit needle can be rotated by 180 degrees?",
            font_size=28,
        )

        # Visual: needle rotating inside a triangle
        tri = Polygon(
            LEFT * 1.5, RIGHT * 1.5, UP * 2.6,
            color=TEAL, fill_opacity=0.15, stroke_width=2,
        )
        tri_label = Tex("Deltoid", font_size=24, color=TEAL)
        tri_label.next_to(tri, DOWN, buff=0.2)

        needle_anim = VGroup()
        for angle in [0, PI/8, PI/4, 3*PI/8, PI/2, 5*PI/8, 3*PI/4, 7*PI/8]:
            line = Line(ORIGIN, RIGHT, color=SEMINAR_BLUE, stroke_width=2)
            line.rotate(angle, about_point=ORIGIN)
            line.scale(1.0)
            line.shift(UP * 0.5)
            needle_anim.add(line)
        needle_anim.next_to(hist_body2, DOWN, buff=0.4)

        example_box = Tex(
            r"$\bullet$ Unit disk: area $\pi \approx 3.14$ \quad (works, but not minimal)",
            font_size=24,
            color=GREY_B,
        )
        example_box2 = Tex(
            r"$\bullet$ Deltoid (3-cusped hypocycloid): area $\pi/8 \approx 0.39$",
            font_size=24,
            color=GREY_B,
        )
        example_box.next_to(needle_anim, DOWN, buff=0.4)
        example_box2.next_to(example_box, DOWN, buff=0.2)

        all_content = VGroup(
            hist_header, hist_body, hist_body2,
            needle_anim, example_box, example_box2,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(0)
        center_mathtex(all_content)

        with self.voiceover(
            text="The story begins in 1917, when the Japanese mathematician "
            "Soichi Kakeya posed a deceptively simple question. "
            "What is the smallest area region in the plane "
            "in which a unit line segment, think of it as a needle, "
            "can be rotated by 180 degrees? "
            "The unit disk obviously works, with area pi. "
            "But it is not minimal. "
            "A three-cusped hypocycloid called a deltoid "
            "also allows the needle to turn, with much smaller area pi over eight."
        ):
            self.play(Write(title))
            self.play(FadeIn(hist_header))
            self.play(FadeIn(hist_body))
            self.play(FadeIn(hist_body2))
            self.play(Create(needle_anim))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(example_box))
            self.play(FadeIn(example_box2))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: Besicovitch's shocking construction ---
        title2 = Tex(r"\text{Besicovitch's Surprise (1919)}", font_size=38, color=BLUE)
        title2.to_edge(UP, buff=0.5)

        shock_header = Tex(
            r"\textbf{Shockingly,} Besicovitch proved (1919):",
            font_size=28,
        )
        shock_body = Tex(
            r"For any $\varepsilon > 0$, there exists a Kakeya set in $\mathbb{R}^2$",
            font_size=28,
        )
        shock_eq = MathTex(
            r"\text{with area } < \varepsilon!",
            font_size=34,
            color=YELLOW,
        )
        shock_eq.next_to(shock_body, DOWN, buff=0.2)

        intuition = Tex(
            r"\textbf{Idea:} Overlap many thin triangles cleverly",
            font_size=26,
            color=TEAL,
        )
        intuition2 = Tex(
            r"$\phantom{\bullet}$\;so their total area is small but every direction is covered",
            font_size=26,
            color=GREY_B,
        )

        # Visual: overlapping thin triangles
        tri_group = VGroup()
        for i in range(8):
            angle = i * PI / 8
            tri_small = Polygon(
                ORIGIN,
                RIGHT * 1.2,
                RIGHT * 1.2 + UP * 0.15,
                color=SEMINAR_BLUE, fill_opacity=0.1, stroke_width=1,
            )
            tri_small.rotate(angle, about_point=ORIGIN)
            tri_group.add(tri_small)
        tri_group.next_to(intuition2, DOWN, buff=0.4)

        all_content2 = VGroup(
            shock_header, shock_body, shock_eq,
            intuition, intuition2, tri_group,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="But just two years later, Besicovitch delivered a stunning surprise. "
            "He proved that for any positive epsilon, no matter how small, "
            "there exists a Kakeya set in the plane with area less than epsilon. "
            "The idea is to overlap many thin triangles in a clever arrangement, "
            "so that their total area becomes arbitrarily small, "
            "yet every direction is still covered. "
            "This construction is now called a Besicovitch set."
        ):
            self.play(Write(title2))
            self.play(FadeIn(shock_header))
            self.play(FadeIn(shock_body))
            self.play(Write(shock_eq))
            self.play(Circumscribe(shock_eq, color=YELLOW, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition))
            self.play(FadeIn(intuition2))
            self.play(Create(tri_group, lag_ratio=0.1))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

        # --- Part C: Dimension is the right question ---
        title3 = Tex(r"\text{The Right Question: Dimension}", font_size=38, color=BLUE)
        title3.to_edge(UP, buff=0.5)

        dim_header = Tex(
            r"Besicovitch sets can have \textbf{Lebesgue measure zero}.",
            font_size=28,
        )
        dim_body = Tex(
            r"So area/volume is the wrong measure of size.",
            font_size=28,
            color=GREY_B,
        )

        dim_body2 = Tex(
            r"\textbf{Better question:} What is the \textit{fractal dimension}?",
            font_size=28,
            color=TEAL,
        )

        dim_eq = MathTex(
            r"\dim_H(K) = \text{Hausdorff dimension of } K",
            font_size=30,
        )
        dim_eq2 = MathTex(
            r"\dim_M(K) = \text{Minkowski (box-counting) dimension}",
            font_size=30,
        )

        conjecture_header = Tex(
            r"\textbf{Kakeya Conjecture.} Every Kakeya set in $\mathbb{R}^n$ has",
            font_size=28,
        )
        conjecture_eq = MathTex(
            r"\dim_H(K) = \dim_M(K) = n",
            font_size=36,
            color=GREEN,
        )
        conjecture_eq.next_to(conjecture_header, DOWN, buff=0.2)

        status = Tex(
            r"$n=2$: proved by Davies (1971) \quad $n \geq 3$: open for decades",
            font_size=24,
            color=GREY_B,
        )

        all_content3 = VGroup(
            dim_header, dim_body, dim_body2,
            dim_eq, dim_eq2,
            conjecture_header, conjecture_eq, status,
        )
        all_content3.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content3.next_to(title3, DOWN, buff=0.5)
        all_content3.set_x(0)
        center_mathtex(all_content3)

        with self.voiceover(
            text="This raises a natural question. "
            "If Besicovitch sets can have arbitrarily small area, "
            "and even Lebesgue measure zero, "
            "then area is the wrong way to measure their size. "
            "The right question is about fractal dimension. "
            "The Hausdorff dimension and the Minkowski dimension, "
            "also called the box-counting dimension, "
            "capture how densely a set fills space at small scales. "
            "The Kakeya conjecture asserts that every Kakeya set "
            "in R n must have full dimension n. "
            "In other words, even though the set can have measure zero, "
            "it cannot be thin in the fractal sense. "
            "This was proved in two dimensions by Davies in 1971, "
            "but remained open in three and higher dimensions for over fifty years."
        ):
            self.play(Write(title3))
            self.play(FadeIn(dim_header))
            self.play(FadeIn(dim_body))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(dim_body2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(dim_eq))
            self.play(FadeIn(dim_eq2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(conjecture_header))
            self.play(Write(conjecture_eq))
            self.play(Circumscribe(conjecture_eq, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(status))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

        # --- Part D: Why analysts care ---
        title4 = Tex(r"\text{Why Do Analysts Care?}", font_size=38, color=BLUE)
        title4.to_edge(UP, buff=0.5)

        conn_header = Tex(
            r"The Kakeya problem is deeply connected to \textbf{harmonic analysis}.",
            font_size=28,
        )

        conn1 = Tex(
            r"$\bullet$ \textbf{Fourier restriction:} How well does $\hat{f}$ restrict to curved surfaces?",
            font_size=24,
        )
        conn1b = Tex(
            r"$\phantom{\bullet}$\;The restriction conjecture implies the Kakeya conjecture",
            font_size=24,
            color=GREY_B,
        )
        conn2 = Tex(
            r"$\bullet$ \textbf{Bochner-Riesz multipliers:} Convergence of Fourier series",
            font_size=24,
        )
        conn3 = Tex(
            r"$\bullet$ \textbf{Wave equations:} Dispersive estimates and local smoothing",
            font_size=24,
        )
        conn4 = Tex(
            r"$\bullet$ \textbf{Number theory:} Connections to the Riemann zeta function",
            font_size=24,
        )

        insight_box = Tex(
            r"\textbf{Key insight:} Tubes in physical space $\leftrightarrow$ Wave packets in frequency space",
            font_size=26,
            color=TEAL,
        )

        all_content4 = VGroup(
            conn_header, conn1, conn1b, conn2, conn3, conn4, insight_box,
        )
        all_content4.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content4.next_to(title4, DOWN, buff=0.5)
        all_content4.set_x(0)
        center_mathtex(all_content4)

        with self.voiceover(
            text="You might wonder why harmonic analysts care so much "
            "about a geometric problem about rotating needles. "
            "The answer is that the Kakeya problem is deeply connected "
            "to several central questions in analysis. "
            "The Fourier restriction conjecture, which asks how well "
            "the Fourier transform of a function can be restricted to curved surfaces, "
            "actually implies the Kakeya conjecture. "
            "So does the Bochner-Riesz conjecture about convergence of Fourier series. "
            "There are also connections to dispersive estimates for wave equations, "
            "and even to number theory and the Riemann zeta function. "
            "The key insight is that tubes in physical space "
            "correspond to wave packets localized in frequency space. "
            "Understanding how tubes overlap is the same as understanding "
            "how waves interfere with each other."
        ):
            self.play(Write(title4))
            self.play(FadeIn(conn_header))
            self.play(FadeIn(conn1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(conn1b))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(conn2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(conn3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(conn4))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(insight_box))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

        # --- Part E: The Heisenberg group obstacle ---
        title5 = Tex(r"\text{The Heisenberg Group Obstacle}", font_size=38, color=BLUE)
        title5.to_edge(UP, buff=0.5)

        heis_header = Tex(
            r"\textbf{Why is $n=3$ so hard?} A counterexample in $\mathbb{C}^3$:",
            font_size=28,
        )

        heis_eq = MathTex(
            r"H = \left\{(z_1, z_2, z_3) : |z_1|^2 + |z_2|^2 - |z_3|^2 = 1\right\}",
            font_size=30,
            color=TEAL,
        )

        heis_body = Tex(
            r"$\bullet$ $H$ contains \textbf{many complex lines} through every point",
            font_size=26,
        )
        heis_body2 = Tex(
            r"$\bullet$ These lines form a Kakeya-type set with $\mu \approx \delta^{-1}$",
            font_size=26,
        )
        heis_body3 = Tex(
            r"$\bullet$ But $\Delta_{\max} \lessapprox 1$ — it satisfies the Wolff axioms!",
            font_size=26,
            color=YELLOW,
        )

        punch = Tex(
            r"\textbf{The real line $\mathbb{R}$ is not a subring of $\mathbb{C}$.}",
            font_size=26,
            color=GREEN,
        )
        punch2 = Tex(
            r"This algebraic structure is what makes the complex case fail.",
            font_size=24,
            color=GREY_B,
        )

        all_content5 = VGroup(
            heis_header, heis_eq, heis_body, heis_body2, heis_body3,
            punch, punch2,
        )
        all_content5.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content5.next_to(title5, DOWN, buff=0.5)
        all_content5.set_x(0)
        center_mathtex(all_content5)

        with self.voiceover(
            text="So why is dimension three so much harder than dimension two? "
            "One clue comes from a complex analogue of the problem. "
            "In complex three-space, there is a surface called the Heisenberg group, "
            "defined by the equation mod z one squared plus mod z two squared "
            "minus mod z three squared equals one. "
            "This surface contains infinitely many complex lines through every point. "
            "Taking delta neighborhoods of these lines gives a set of tubes "
            "that satisfies the Wolff axioms, "
            "yet has multiplicity of order delta to the minus one. "
            "This is a genuine counterexample in the complex setting. "
            "The reason this cannot happen in real three-space "
            "is that the real line is not a subring of the complex numbers. "
            "The algebraic structure of the complex numbers "
            "is what allows the Heisenberg group to exist. "
            "Any proof in R cubed must somehow rule out this algebraic pathology."
        ):
            self.play(Write(title5))
            self.play(FadeIn(heis_header))
            self.play(Write(heis_eq))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(heis_body))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(heis_body2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(heis_body3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(punch))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(punch2))

        self.wait(PAUSE_BREATHE)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Proof Roadmap
    # ──────────────────────────────────────────────
    def _proof_roadmap(self):
        title = Tex(r"\text{Proof Roadmap}", font_size=40, color=BLUE)
        title.to_edge(UP, buff=0.5)

        steps = [
            ("Step 1", "Sticky vs. Non-Sticky", TEAL),
            ("Step 2", "Multi-Scale Analysis", GOLD),
            ("Step 3", "Factoring Lemma", ORANGE),
            ("Step 4", "High Density Lemma", PURPLE),
            ("Step 5", "Self-Improving Iteration", GREEN),
        ]

        boxes = VGroup()
        arrows = VGroup()
        for i, (label, desc, color) in enumerate(steps):
            step_label = Text(label, font_size=22, color=color, weight=BOLD)
            step_desc = Tex(desc, font_size=24)
            step_group = VGroup(step_label, step_desc).arrange(DOWN, buff=0.1)
            box = SurroundingRectangle(
                step_group, color=color, buff=0.2, corner_radius=0.1, stroke_width=2
            )
            full_step = VGroup(box, step_group)
            boxes.add(full_step)

        boxes.arrange(DOWN, buff=0.4)
        boxes.next_to(title, DOWN, buff=0.5)
        boxes.set_x(0)

        for i in range(len(boxes) - 1):
            arrow = Arrow(
                boxes[i].get_bottom(),
                boxes[i + 1].get_top(),
                buff=0.1,
                color=GREY_B,
                stroke_width=2,
            )
            arrows.add(arrow)

        with self.voiceover(
            text="Here is our roadmap. "
            "The proof has five key steps. "
            "First, we distinguish between sticky and non-sticky arrangements of tubes. "
            "Second, we analyze the structure at multiple scales. "
            "Third, we introduce the factoring lemma, which organizes tubes into convex clusters. "
            "Fourth, we prove the high density lemma for Frostman sets of tubes. "
            "And fifth, we run a self-improving iteration that drives the exponent to zero."
        ):
            self.play(Write(title))
            for i, box in enumerate(boxes):
                self.play(FadeIn(box, shift=RIGHT * 0.3))
                if i < len(arrows):
                    self.play(GrowArrow(arrows[i]))
                self.wait(PAUSE_BRIEF)

        self.wait(PAUSE_READ)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Preliminaries: Tubes and Volume
    # ──────────────────────────────────────────────
    def _prelim_kakeya_sets(self):
        # --- Part A: Discretization ---
        title = Tex(r"\text{Discretization: From Sets to Tubes}", font_size=38, color=BLUE)
        title.to_edge(UP, buff=0.5)

        why_header = Tex(
            r"\textbf{Why discretize?} The original problem is about sets of measure zero.",
            font_size=28,
        )
        why_body = Tex(
            r"We replace it with a quantitative, finite version:",
            font_size=28,
            color=TEAL,
        )

        bullet1 = Tex(
            r"$\bullet$ A $\delta$-tube $T$ = $\delta$-neighborhood of a unit line segment",
            font_size=26,
        )
        bullet2 = Tex(
            r"$\bullet$ In $\mathbb{R}^3$: $|T| \approx \delta \times \delta \times 1 = \delta^2$",
            font_size=26,
        )
        bullet3 = Tex(
            r"$\bullet$ $\mathbb{T}$ = set of $\delta$-tubes in the unit ball $B_1$",
            font_size=26,
        )
        bullet4 = Tex(
            r"$\bullet$ Typical case: $|\mathbb{T}| \approx \delta^{-2}$ (one per direction)",
            font_size=26,
            color=GREY_B,
        )

        all_content = VGroup(
            why_header, why_body,
            bullet1, bullet2, bullet3, bullet4,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(0)
        center_mathtex(all_content)

        # Right side: animated tube visualization
        tube_demo = VGroup()
        # Start with a line segment
        line_seg = Line(LEFT * 1.5, RIGHT * 1.5, color=WHITE, stroke_width=3)
        line_label = Tex(r"Line segment", font_size=22, color=WHITE)
        line_label.next_to(line_seg, DOWN, buff=0.2)
        line_group = VGroup(line_seg, line_label)

        # The tube (thickened version)
        tube_shape = Rectangle(
            width=3.0, height=0.4,
            color=SEMINAR_BLUE, fill_opacity=0.3, stroke_width=2,
        )
        tube_shape.move_to(line_seg)
        tube_label_side = Tex(r"$\delta$", font_size=22, color=SEMINAR_BLUE)
        tube_label_side.next_to(tube_shape, RIGHT, buff=0.1)
        len_label_side = Tex(r"$1$", font_size=22, color=WHITE)
        len_label_side.next_to(tube_shape, DOWN, buff=0.3)
        tube_group = VGroup(tube_shape, tube_label_side, len_label_side)

        # Unit ball with multiple tubes
        ball = Circle(radius=1.2, color=GREY_B, fill_opacity=0.05, stroke_width=1.5)
        ball_label = Tex(r"$B_1$", font_size=20, color=GREY_B)
        ball_label.next_to(ball, DOWN, buff=0.1)
        tubes_in_ball = VGroup()
        for angle in [0, PI/6, PI/3, PI/2, 2*PI/3, 5*PI/6]:
            t = Rectangle(
                width=2.0, height=0.12,
                color=SEMINAR_BLUE, fill_opacity=0.15, stroke_width=1,
            )
            t.rotate(angle)
            tubes_in_ball.add(t)
        full_demo = VGroup(ball, tubes_in_ball, ball_label)

        tube_demo.add(line_group, tube_group, full_demo)
        tube_demo.arrange(DOWN, buff=0.5)
        tube_demo.set_x(2.8)
        tube_demo.to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text="To tackle the Kakeya conjecture, we first need to discretize it. "
            "The original problem is about sets of measure zero, "
            "which are hard to work with directly. "
            "So we replace it with a quantitative, finite version. "
            "Instead of exact line segments, we work with delta tubes. "
            "A delta tube is simply the delta neighborhood of a unit line segment. "
            "In R cubed, each tube has cross-section delta by delta "
            "and length one, so its volume is approximately delta squared. "
            "We consider a collection of such tubes inside the unit ball. "
            "In the typical case, we have about delta to the minus two tubes, "
            "which corresponds to roughly one tube in each delta-separated direction."
        ):
            self.play(Write(title))
            self.play(FadeIn(why_header))
            self.play(FadeIn(why_body))
            self.play(FadeIn(bullet1))
            self.wait(PAUSE_ELEMENT)
            # Show line → tube animation
            self.play(Create(line_seg), FadeIn(line_label))
            self.wait(PAUSE_BRIEF)
            self.play(
                Transform(line_seg, tube_shape),
                FadeIn(tube_label_side),
                FadeIn(len_label_side),
                FadeOut(line_label),
                run_time=1.0,
            )
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet3))
            # Show tubes inside ball
            self.play(Create(ball), FadeIn(ball_label))
            self.play(
                *[FadeIn(t, shift=RIGHT * 0.2) for t in tubes_in_ball],
                lag_ratio=0.15,
            )
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet4))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: The volume bound goal ---
        title2 = Tex(r"\text{The Volume Bound}", font_size=38, color=BLUE)
        title2.to_edge(UP, buff=0.5)

        goal_header = Tex(
            r"\textbf{Goal:} Lower bound the volume of the union:",
            font_size=28,
        )

        goal_eq = MathTex(
            r"\Big| \bigcup_{T \in \mathbb{T}} T \Big| \geq \delta^{\varepsilon} \cdot |\mathbb{T}| \cdot |T|",
            font_size=34,
            color=GREEN,
        )

        intuition_header = Tex(
            r"\textbf{Intuition:} If tubes point in different directions,",
            font_size=28,
        )
        intuition_body = Tex(
            r"they should overlap \textit{as little as possible}.",
            font_size=28,
            color=TEAL,
        )

        equiv_header = Tex(
            r"\textbf{Equivalently,} bound the \textbf{multiplicity} $\mu$:",
            font_size=28,
        )
        equiv_eq = MathTex(
            r"\mu(\mathbb{T}) = \frac{|\mathbb{T}| \cdot |T|}{\left| \bigcup T \right|} \lessapprox 1",
            font_size=34,
            color=GOLD,
        )

        note = Tex(
            r"$\mu \approx 1$ means tubes are essentially disjoint",
            font_size=24,
            color=GREY_B,
        )
        note2 = Tex(
            r"$\mu \gg 1$ means heavy overlap — this is what we must rule out",
            font_size=24,
            color=YELLOW,
        )

        all_content2 = VGroup(
            goal_header, goal_eq,
            intuition_header, intuition_body,
            equiv_header, equiv_eq, note, note2,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        # Visual: disjoint vs overlapping tubes
        # Left: disjoint tubes (good case)
        disjoint_label = Tex(r"$\mu \approx 1$", font_size=24, color=GREEN)
        disjoint_tubes = VGroup()
        for i, angle in enumerate([0, PI/5, 2*PI/5, 3*PI/5, 4*PI/5]):
            t = Rectangle(
                width=1.5, height=0.15,
                color=SEMINAR_BLUE, fill_opacity=0.3, stroke_width=1.5,
            )
            t.rotate(angle)
            disjoint_tubes.add(t)
        disjoint_group = VGroup(disjoint_tubes, disjoint_label)
        disjoint_label.next_to(disjoint_tubes, DOWN, buff=0.2)

        # Right: overlapping tubes (bad case)
        overlap_label = Tex(r"$\mu \gg 1$", font_size=24, color=RED)
        overlap_tubes = VGroup()
        for i, angle in enumerate([0, PI/12, PI/6, PI/4, PI/3]):
            t = Rectangle(
                width=1.5, height=0.15,
                color=RED, fill_opacity=0.25, stroke_width=1.5,
            )
            t.rotate(angle)
            t.shift(DOWN * 0.1 * i)  # slight offset to show bunching
            overlap_tubes.add(t)
        overlap_group = VGroup(overlap_tubes, overlap_label)
        overlap_label.next_to(overlap_tubes, DOWN, buff=0.2)

        comparison = VGroup(disjoint_group, overlap_group)
        comparison.arrange(RIGHT, buff=1.5)
        comparison.set_x(0)
        comparison.to_edge(DOWN, buff=0.5)

        vs_label = Tex(r"vs", font_size=28, color=GREY_B)
        vs_label.move_to(midpoint(disjoint_group.get_right(), overlap_group.get_left()))

        with self.voiceover(
            text="Our goal is to prove a lower bound on the volume of the union of all tubes. "
            "If the tubes point in well-separated directions, "
            "we expect them to overlap as little as possible, "
            "so the union should have volume close to the sum of individual volumes. "
            "It is often more convenient to think about this in terms of multiplicity. "
            "The multiplicity mu is the total tube volume divided by the union volume. "
            "If mu is approximately one, the tubes are essentially disjoint. "
            "If mu is much larger than one, there is heavy overlap. "
            "Our task is to rule out heavy overlap under suitable hypotheses. "
            "This is the core challenge of the Kakeya problem."
        ):
            self.play(Write(title2))
            self.play(FadeIn(goal_header))
            self.play(Write(goal_eq))
            self.play(Circumscribe(goal_eq, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition_header))
            self.play(FadeIn(intuition_body))
            # Show disjoint tubes
            self.play(
                *[Create(t) for t in disjoint_tubes],
                lag_ratio=0.1,
            )
            self.play(FadeIn(disjoint_label))
            self.wait(PAUSE_ELEMENT)
            # Show overlapping tubes
            self.play(
                *[Create(t) for t in overlap_tubes],
                lag_ratio=0.1,
            )
            self.play(FadeIn(overlap_label), FadeIn(vs_label))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(equiv_header))
            self.play(Write(equiv_eq))
            self.play(Circumscribe(equiv_eq, color=GOLD, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(note))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(note2))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Preliminaries: Wolff Axioms
    # ──────────────────────────────────────────────
    def _prelim_wolff_axioms(self):
        # --- Part A: What are the Wolff Axioms? ---
        title = Tex(r"\text{The Wolff Axioms}", font_size=38, color=BLUE)
        title.to_edge(UP, buff=0.5)

        why_header = Tex(
            r"\textbf{The problem:} Tubes can overlap \textit{a lot} if we allow it.",
            font_size=28,
        )

        bad_example = Tex(
            r"\textbf{Trivial counterexample:} Put all $\delta^{-2}$ tubes inside one slab.",
            font_size=26,
            color=YELLOW,
        )
        bad_result = MathTex(
            r"\Big| \bigcup T \Big| \approx \delta \quad \text{(tiny!)}",
            font_size=30,
            color=RED,
        )

        need_header = Tex(
            r"\textbf{We need an anti-clustering hypothesis.}",
            font_size=28,
            color=TEAL,
        )

        all_content = VGroup(
            why_header, bad_example, bad_result, need_header,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(-1.5)
        center_mathtex(all_content)

        # Visual: thin slab with many tubes bunched inside
        slab = Rectangle(
            width=2.5, height=0.5,
            color=YELLOW, fill_opacity=0.1, stroke_width=2, stroke_color=YELLOW,
        )
        slab_label = Tex(r"Slab of width $\delta$", font_size=20, color=YELLOW)
        slab_label.next_to(slab, DOWN, buff=0.15)
        slab_tubes = VGroup()
        for i in range(12):
            t = Rectangle(
                width=2.2, height=0.04,
                color=RED, fill_opacity=0.35, stroke_width=1,
            )
            t.shift(UP * (0.2 - i * 0.035))
            slab_tubes.add(t)
        slab_group = VGroup(slab, slab_tubes, slab_label)
        slab_group.set_x(3.2)
        slab_group.to_edge(DOWN, buff=0.8)

        # Arrow showing tiny union volume
        union_arrow = MathTex(
            r"\text{Union volume} \approx \delta",
            font_size=24,
            color=RED,
        )
        union_arrow.next_to(slab_label, DOWN, buff=0.3)

        with self.voiceover(
            text="Before we can state the theorem precisely, "
            "we need to understand why some hypothesis is necessary. "
            "The problem is that tubes can overlap a lot if we allow it. "
            "Here is a trivial counterexample. "
            "Take all delta to the minus two tubes and put them inside one thin slab. "
            "Then the union has volume only about delta, which is tiny. "
            "So we need an anti-clustering hypothesis "
            "that prevents tubes from bunching up too much."
        ):
            self.play(Write(title))
            self.play(FadeIn(why_header))
            self.play(FadeIn(bad_example))
            self.play(Write(bad_result))
            self.play(Circumscribe(bad_result, color=RED, time_width=2))
            # Show slab animation
            self.play(Create(slab), FadeIn(slab_label))
            self.play(
                *[FadeIn(t, shift=RIGHT * 0.3) for t in slab_tubes],
                lag_ratio=0.08,
            )
            self.play(FadeIn(union_arrow))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(need_header))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: The precise definition ---
        title2 = Tex(r"\text{The Convex Wolff Axiom}", font_size=38, color=BLUE)
        title2.to_edge(UP, buff=0.5)

        hist = Tex(
            r"Introduced by Tom Wolff (1995), refined by Katz and Tao.",
            font_size=26,
            color=GREY_B,
        )

        defn_header = Tex(
            r"\textbf{Density of tubes in a convex set $K$:}",
            font_size=28,
        )
        defn_eq = MathTex(
            r"\Delta(\mathbb{T}, K) = \frac{\sum_{T \subset K} |T|}{|K|}",
            font_size=32,
            color=TEAL,
        )

        intuition = Tex(
            r"$\bullet$ $\Delta(\mathbb{T}, K)$ = fraction of $K$ covered by tubes inside it",
            font_size=26,
        )
        intuition2 = Tex(
            r"$\bullet$ $\Delta(\mathbb{T}, B_1) \approx \delta^{-2} \cdot \delta^2 / 1 = O(1)$",
            font_size=26,
            color=GREY_B,
        )

        max_header = Tex(
            r"\textbf{Maximal density over all convex sets:}",
            font_size=28,
        )
        max_eq = MathTex(
            r"\Delta_{\max}(\mathbb{T}) = \max_{K \text{ convex}} \Delta(\mathbb{T}, K) \lessapprox 1",
            font_size=32,
            color=GREEN,
        )

        note = Tex(
            r"This is the \textit{Katz-Tao Convex Wolff Axiom}.",
            font_size=26,
            color=GREY_B,
        )

        all_content2 = VGroup(
            hist, defn_header, defn_eq, intuition, intuition2,
            max_header, max_eq, note,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="This is where the Wolff axioms come in. "
            "They were introduced by Tom Wolff in 1995 "
            "and later refined by Katz and Tao. "
            "The idea is simple but powerful. "
            "For any convex set K, we measure the density of tubes inside it. "
            "This is the total volume of all tubes contained in K, "
            "divided by the volume of K itself. "
            "Think of it as the fraction of K that is covered by tubes. "
            "For the unit ball, this density is naturally of order one, "
            "since we have about delta to the minus two tubes "
            "each of volume delta squared. "
            "The Wolff axiom says that this density is bounded "
            "not just for the unit ball, but for every convex set K. "
            "No convex region can contain disproportionately many tubes. "
            "This rules out the trivial counterexample "
            "where all tubes bunch up inside a thin slab."
        ):
            self.play(Write(title2))
            self.play(FadeIn(hist))
            self.play(FadeIn(defn_header))
            self.play(Write(defn_eq))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(max_header))
            self.play(Write(max_eq))
            self.play(Circumscribe(max_eq, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(note))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

        # --- Part C: The Main Theorem ---
        title3 = Tex(r"\text{The Main Theorem}", font_size=38, color=BLUE)
        title3.to_edge(UP, buff=0.5)

        thm_header = Tex(
            r"\textbf{Theorem (Wang-Zahl, 2025).}",
            font_size=30,
            color=GREEN,
        )

        thm_card, thm_rect, thm_content = make_theorem_card(
            Tex(
                r"If $\Delta_{\max}(\mathbb{T}) \lessapprox 1$, then $\mu(\mathbb{T}) \lessapprox 1$",
                font_size=32,
            ),
            color=GREEN,
            buff=0.3,
            stroke_width=3,
        )

        equiv = Tex(
            r"\textbf{Equivalently:}",
            font_size=28,
        )
        equiv_eq = MathTex(
            r"\Big| \bigcup_{T \in \mathbb{T}} T \Big| \gtrapprox |\mathbb{T}| \cdot |T| \approx 1",
            font_size=32,
            color=GREEN,
        )

        why_useful = Tex(
            r"\textbf{Why is this useful?}",
            font_size=28,
            color=TEAL,
        )
        why1 = Tex(
            r"$\bullet$ Implies Kakeya sets have dimension 3",
            font_size=26,
        )
        why2 = Tex(
            r"$\bullet$ Resolves the Tube Doubling Conjecture in $\mathbb{R}^3$",
            font_size=26,
        )
        why3 = Tex(
            r"$\bullet$ Stronger than previous bounds (dimension $5/2 + c$)",
            font_size=26,
            color=GREY_B,
        )

        all_content3 = VGroup(
            thm_header, thm_card, equiv, equiv_eq,
            why_useful, why1, why2, why3,
        )
        all_content3.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content3.next_to(title3, DOWN, buff=0.5)
        all_content3.set_x(0)
        thm_card.set_x(0)
        center_mathtex(all_content3)

        with self.voiceover(
            text="Now we can state the main theorem of Wang and Zahl. "
            "If a collection of tubes satisfies the convex Wolff axiom, "
            "meaning no convex set contains too many tubes, "
            "then the multiplicity is essentially bounded by one. "
            "Equivalently, the union of tubes has nearly maximal volume, "
            "close to the sum of all individual tube volumes. "
            "Why is this useful? "
            "First, it implies that every Kakeya set in R cubed "
            "has full Hausdorff and Minkowski dimension three. "
            "Second, it resolves the Tube Doubling Conjecture in R cubed, "
            "which asks how much the union grows when you dilate each tube. "
            "And third, it is a dramatic improvement over previous bounds. "
            "Before this work, the best known dimension bound was "
            "five halves plus a small constant, due to Katz, Laba, and Tao."
        ):
            self.play(Write(title3))
            self.play(FadeIn(thm_header))
            self.play(FadeIn(thm_content), Create(thm_rect))
            self.play(Circumscribe(thm_card, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(equiv))
            self.play(Write(equiv_eq))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(why_useful))
            self.play(FadeIn(why1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(why2))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(why3))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Step 1: Sticky vs Non-Sticky
    # ──────────────────────────────────────────────
    def _step1_sticky(self):
        # --- Part A: Multi-scale structure ---
        title = Tex(r"\text{Step 1: Sticky vs.\ Non-Sticky}", font_size=38, color=TEAL)
        title.to_edge(UP, buff=0.5)

        idea_header = Tex(
            r"\textbf{Key idea:} Look at tubes at \textbf{multiple scales}.",
            font_size=28,
        )
        idea_body = Tex(
            r"Pick an intermediate scale $\delta \ll \rho \ll 1$ and thicken everything.",
            font_size=26,
            color=TEAL,
        )

        bullet1 = Tex(
            r"$\bullet$ $\mathbb{T}_\rho$ = set of $\rho$-tubes covering $\mathbb{T}$",
            font_size=26,
        )
        bullet2 = Tex(
            r"$\bullet$ $\mathbb{T}[T_\rho]$ = $\delta$-tubes inside a given $\rho$-tube $T_\rho$",
            font_size=26,
        )
        bullet3 = Tex(
            r"$\bullet$ $\mathbb{T} = \bigsqcup_{T_\rho \in \mathbb{T}_\rho} \mathbb{T}[T_\rho]$",
            font_size=26,
        )

        why_header = Tex(
            r"\textbf{Why this helps:} Two simpler problems instead of one hard one.",
            font_size=26,
            color=GREEN,
        )
        why1 = Tex(
            r"$\bullet$ \textit{Fine scale:} How $\delta$-tubes overlap inside one $\rho$-tube",
            font_size=24,
        )
        why2 = Tex(
            r"$\bullet$ \textit{Coarse scale:} How $\rho$-tubes overlap globally",
            font_size=24,
        )

        all_content = VGroup(
            idea_header, idea_body, bullet1, bullet2, bullet3,
            why_header, why1, why2,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(-1.5)
        center_mathtex(all_content)

        # Visual: thin tubes → thickened rho-tube
        # Left: many thin δ-tubes
        delta_tubes = VGroup()
        for i, angle in enumerate([0, PI/8, PI/4, 3*PI/8, PI/2, 5*PI/8]):
            t = Rectangle(
                width=2.0, height=0.06,
                color=SEMINAR_BLUE, fill_opacity=0.25, stroke_width=1,
            )
            t.rotate(angle)
            delta_tubes.add(t)
        delta_label = Tex(r"$\delta$-tubes", font_size=22, color=SEMINAR_BLUE)
        delta_label.next_to(delta_tubes, DOWN, buff=0.15)
        delta_group = VGroup(delta_tubes, delta_label)

        # Arrow
        arrow = Tex(r"$\xrightarrow{\text{thicken to }\rho}$", font_size=24, color=GOLD)

        # Right: one thick ρ-tube containing the thin ones
        rho_tube = Rectangle(
            width=2.0, height=0.35,
            color=GOLD, fill_opacity=0.1, stroke_width=2, stroke_color=GOLD,
        )
        rho_label = Tex(r"$\rho$-tube $T_\rho$", font_size=22, color=GOLD)
        rho_label.next_to(rho_tube, DOWN, buff=0.15)
        # The δ-tubes inside (same angles but smaller)
        delta_inside = VGroup()
        for i, angle in enumerate([0, PI/8, PI/4, 3*PI/8, PI/2, 5*PI/8]):
            t = Rectangle(
                width=1.8, height=0.04,
                color=SEMINAR_BLUE, fill_opacity=0.3, stroke_width=1,
            )
            t.rotate(angle)
            delta_inside.add(t)
        rho_group = VGroup(rho_tube, delta_inside, rho_label)

        thick_demo = VGroup(delta_group, arrow, rho_group)
        thick_demo.arrange(RIGHT, buff=0.5)
        thick_demo.set_x(3.0)
        thick_demo.to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text="Step one: sticky versus non-sticky. "
            "The proof looks at tubes at multiple scales. "
            "This is a powerful technique in analysis: "
            "instead of trying to understand the whole structure at once, "
            "we zoom in and zoom out. "
            "Pick an intermediate scale rho between delta and one, "
            "and thicken all the delta tubes to get rho tubes. "
            "Each rho tube contains some number of delta tubes inside it. "
            "The full collection of delta tubes is the disjoint union "
            "of the delta tubes inside each rho tube. "
            "Why does this help? "
            "It breaks one hard problem into two simpler ones. "
            "At the fine scale, we ask how delta tubes overlap "
            "inside a single rho tube. "
            "At the coarse scale, we ask how the rho tubes overlap globally."
        ):
            self.play(Write(title))
            self.play(FadeIn(idea_header))
            self.play(FadeIn(idea_body))
            self.wait(PAUSE_ELEMENT)
            # Show thin tubes
            self.play(
                *[Create(t) for t in delta_tubes],
                lag_ratio=0.1,
            )
            self.play(FadeIn(delta_label))
            self.wait(PAUSE_BRIEF)
            # Show thickening animation
            self.play(FadeIn(arrow))
            self.play(Create(rho_tube))
            self.play(
                *[FadeIn(t) for t in delta_inside],
                lag_ratio=0.1,
            )
            self.play(FadeIn(rho_label))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(why_header))
            self.play(FadeIn(why1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(why2))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: The sticky case ---
        title2 = Tex(r"\text{The Sticky Case}", font_size=38, color=GREEN)
        title2.to_edge(UP, buff=0.5)

        sticky_def = Tex(
            r"\textbf{Sticky} means: at every scale $\rho$, each $\rho$-tube is \textit{packed full}.",
            font_size=28,
        )

        sticky_eq = MathTex(
            r"|\mathbb{T}[T_\rho]| \approx (\rho/\delta)^2 \quad \text{(maximum possible)}",
            font_size=32,
            color=GREEN,
        )

        intuition = Tex(
            r"\textbf{Intuition:} Tubes cluster tightly — they are \textit{sticky}.",
            font_size=26,
        )
        intuition2 = Tex(
            r"$\bullet$ After rescaling, $\mathbb{T}[T_\rho]$ looks like the original problem",
            font_size=26,
        )
        intuition3 = Tex(
            r"$\bullet$ This self-similarity is both powerful and restrictive",
            font_size=26,
            color=TEAL,
        )

        hist = Tex(
            r"\textbf{Sticky Kakeya Theorem:} Wang-Zahl (2022) proved $\mu \lessapprox 1$ in this case.",
            font_size=26,
            color=GREY_B,
        )
        hist2 = Tex(
            r"Uses sum-product theory (Bourgain) + projection theorems.",
            font_size=24,
            color=GREY_B,
        )

        all_content2 = VGroup(
            sticky_def, sticky_eq, intuition, intuition2, intuition3, hist, hist2,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="The sticky case is when each rho tube is packed as full as possible "
            "with delta tubes. "
            "The maximum number of essentially distinct delta tubes "
            "that can fit inside a rho tube is about rho over delta squared. "
            "When this bound is achieved at every scale, "
            "we say the tubes are sticky. "
            "The intuition is that the tubes cluster tightly together, "
            "like they are glued to each other. "
            "After rescaling a rho tube to the unit ball, "
            "the delta tubes inside look like a smaller copy of the original problem. "
            "This self-similarity is both powerful and restrictive. "
            "Wang and Zahl proved the sticky Kakeya theorem in 2022, "
            "showing that sticky sets must have bounded multiplicity. "
            "Their proof uses Bourgain's discretized sum-product theorem "
            "and recent projection theorems. "
            "The sticky case is now solved."
        ):
            self.play(Write(title2))
            self.play(FadeIn(sticky_def))
            self.play(Write(sticky_eq))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(hist))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(hist2))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part C: The non-sticky case ---
        title3 = Tex(r"\text{The Non-Sticky Case}", font_size=38, color=YELLOW)
        title3.to_edge(UP, buff=0.5)

        nonsticky_def = Tex(
            r"\textbf{Non-sticky} means: at some scale $\rho$, tubes are \textit{sparse}.",
            font_size=28,
        )

        nonsticky_eq = MathTex(
            r"|\mathbb{T}[T_\rho]| \ll (\rho/\delta)^2 \quad \text{for some } \rho",
            font_size=32,
            color=YELLOW,
        )

        challenge_header = Tex(
            r"\textbf{Why is this harder?}",
            font_size=28,
            color=RED,
        )
        challenge1 = Tex(
            r"$\bullet$ $\rho$-tubes intersect with \textbf{high multiplicity}",
            font_size=26,
        )
        challenge2 = Tex(
            r"$\bullet$ But $\delta$-tubes inside each $\rho$-tube are \textbf{sparse}",
            font_size=26,
        )
        challenge3 = Tex(
            r"$\bullet$ No self-similarity — cannot rescale and iterate",
            font_size=26,
        )
        challenge4 = Tex(
            r"$\bullet$ $|\mathbb{T}_\rho| \gg \rho^{-2}$: too many $\rho$-tubes!",
            font_size=26,
            color=RED,
        )

        analogy = Tex(
            r"\textbf{Analogy:} A sparse forest — trees are far apart, but many patches overlap.",
            font_size=24,
            color=TEAL,
        )

        all_content3 = VGroup(
            nonsticky_def, nonsticky_eq, challenge_header,
            challenge1, challenge2, challenge3, challenge4, analogy,
        )
        all_content3.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content3.next_to(title3, DOWN, buff=0.5)
        all_content3.set_x(0)
        center_mathtex(all_content3)

        with self.voiceover(
            text="The non-sticky case is where the real difficulty lies. "
            "At some scale rho, the delta tubes are sparse inside the rho tubes. "
            "This creates a paradoxical situation. "
            "The rho tubes intersect with very high multiplicity, "
            "meaning many rho tubes pass through a typical point. "
            "But the delta tubes inside each rho tube are sparse, "
            "so they only fill out a small fraction of the rho tube. "
            "There is no self-similarity to exploit. "
            "We cannot simply rescale and iterate. "
            "And there are far too many rho tubes — "
            "many more than rho to the minus two. "
            "Think of it like a sparse forest: "
            "the trees are far apart within each patch, "
            "but many patches overlap in complicated ways. "
            "This is the arrangement that previous methods could not handle."
        ):
            self.play(Write(title3))
            self.play(FadeIn(nonsticky_def))
            self.play(Write(nonsticky_eq))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(challenge_header))
            self.play(FadeIn(challenge1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(challenge2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(challenge3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(challenge4))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(analogy))

        self.wait(PAUSE_BREATHE)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Step 2: Multi-Scale Analysis
    # ──────────────────────────────────────────────
    def _step2_multiscale(self):
        # --- Part A: Factorization of multiplicity ---
        title = Tex(r"\text{Step 2: Multi-Scale Factorization}", font_size=38, color=GOLD)
        title.to_edge(UP, buff=0.5)

        idea_header = Tex(
            r"\textbf{Key idea.} Factor multiplicity across scales:",
            font_size=28,
        )

        mult_eq = MathTex(
            r"\mu(\mathbb{T}) \approx \mu(\mathbb{T}[T_\rho]) \cdot \mu_{\text{coarse}}",
            font_size=34,
            color=TEAL,
        )

        fine_header = Tex(r"\textbf{Fine scale:} Inside each $\rho$-tube,", font_size=28)
        fine_eq = MathTex(
            r"\mu(\mathbb{T}[T_\rho]) \lessapprox (\delta/\rho)^{2\beta} \ll \rho^{-2\beta}",
            font_size=30,
        )

        coarse_header = Tex(
            r"\textbf{Coarse scale:} How $\rho$-tubes overlap globally",
            font_size=28,
        )

        challenge = Tex(
            r"$\bullet$ $\mathbb{T}_\rho$ may have $\Delta_{\max} \gg 1$ (high density!)",
            font_size=26,
            color=YELLOW,
        )
        challenge2 = Tex(
            r"$\bullet$ Cannot apply induction directly",
            font_size=26,
            color=YELLOW,
        )

        all_content = VGroup(
            idea_header, mult_eq, fine_header, fine_eq,
            coarse_header, challenge, challenge2,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(-1.5)
        center_mathtex(all_content)

        # Visual: factorization diagram
        # Top: total multiplicity
        total_box = Rectangle(
            width=2.0, height=0.6,
            color=TEAL, fill_opacity=0.2, stroke_width=2,
        )
        total_label = MathTex(r"\mu(\mathbb{T})", font_size=24, color=TEAL)
        total_group = VGroup(total_box, total_label)
        total_label.move_to(total_box)

        # Split arrows
        split_arrow1 = Arrow(
            total_box.get_bottom(), LEFT * 1.5 + DOWN * 1.2,
            buff=0.1, color=SEMINAR_BLUE, stroke_width=2,
        )
        split_arrow2 = Arrow(
            total_box.get_bottom(), RIGHT * 1.5 + DOWN * 1.2,
            buff=0.1, color=GOLD, stroke_width=2,
        )

        # Fine scale box
        fine_box = Rectangle(
            width=1.8, height=0.8,
            color=SEMINAR_BLUE, fill_opacity=0.15, stroke_width=2,
        )
        fine_box.shift(LEFT * 1.5 + DOWN * 1.2)
        fine_inside = VGroup()
        for i in range(4):
            t = Rectangle(
                width=1.2, height=0.05,
                color=SEMINAR_BLUE, fill_opacity=0.3, stroke_width=1,
            )
            t.rotate(i * PI / 6)
            fine_inside.add(t)
        fine_inside.move_to(fine_box)
        fine_label = MathTex(r"\mu(\mathbb{T}[T_\rho])", font_size=20, color=SEMINAR_BLUE)
        fine_label.next_to(fine_box, DOWN, buff=0.1)
        fine_group = VGroup(fine_box, fine_inside, fine_label)

        # Coarse scale box
        coarse_box = Rectangle(
            width=1.8, height=0.8,
            color=GOLD, fill_opacity=0.15, stroke_width=2,
        )
        coarse_box.shift(RIGHT * 1.5 + DOWN * 1.2)
        coarse_inside = VGroup()
        for i in range(4):
            t = Rectangle(
                width=1.4, height=0.12,
                color=GOLD, fill_opacity=0.2, stroke_width=1,
            )
            t.rotate(i * PI / 5)
            coarse_inside.add(t)
        coarse_inside.move_to(coarse_box)
        coarse_label = MathTex(r"\mu_{\text{coarse}}", font_size=20, color=GOLD)
        coarse_label.next_to(coarse_box, DOWN, buff=0.1)
        coarse_group = VGroup(coarse_box, coarse_inside, coarse_label)

        times_label = MathTex(r"\times", font_size=28, color=WHITE)
        times_label.move_to(midpoint(fine_group.get_right(), coarse_group.get_left()))

        factor_demo = VGroup(
            total_group, split_arrow1, split_arrow2,
            fine_group, coarse_group, times_label,
        )
        factor_demo.set_x(3.2)
        factor_demo.to_edge(DOWN, buff=0.3)

        with self.voiceover(
            text="Step two: multi-scale factorization. "
            "The key idea is to factor the multiplicity across scales. "
            "The total multiplicity splits into a fine-scale part, "
            "which measures how delta tubes overlap inside each rho tube, "
            "and a coarse-scale part, which measures how the rho tubes overlap globally. "
            "In the non-sticky case, the fine-scale multiplicity is small. "
            "But the coarse-scale part is challenging, "
            "because the set of rho tubes may have very high density, "
            "and the Wolff axioms no longer apply directly. "
            "We need new tools to handle this."
        ):
            self.play(Write(title))
            self.play(FadeIn(idea_header))
            self.play(Write(mult_eq))
            # Show factorization diagram
            self.play(Create(total_box), FadeIn(total_label))
            self.wait(PAUSE_BRIEF)
            self.play(GrowArrow(split_arrow1), GrowArrow(split_arrow2))
            self.play(Create(fine_box))
            self.play(*[Create(t) for t in fine_inside], lag_ratio=0.15)
            self.play(FadeIn(fine_label))
            self.play(Create(coarse_box))
            self.play(*[Create(t) for t in coarse_inside], lag_ratio=0.15)
            self.play(FadeIn(coarse_label), FadeIn(times_label))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(fine_header))
            self.play(Write(fine_eq))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(coarse_header))
            self.play(FadeIn(challenge))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(challenge2))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: The high-density problem ---
        title2 = Tex(r"\text{The High-Density Problem}", font_size=38, color=GOLD)
        title2.to_edge(UP, buff=0.5)

        problem_header = Tex(
            r"\textbf{The problem:} $\mathbb{T}_\rho$ has \textbf{too many} tubes.",
            font_size=28,
        )

        prob_eq = MathTex(
            r"|\mathbb{T}_\rho| \gg \rho^{-2} \quad \text{(not Katz-Tao!)}",
            font_size=32,
            color=RED,
        )

        analogy_header = Tex(
            r"\textbf{Analogy:} Think of $\mathbb{T}_\rho$ as a \textit{Frostman measure}.",
            font_size=28,
            color=TEAL,
        )
        analogy_body = Tex(
            r"Density in any sub-region $\lesssim$ global density",
            font_size=26,
        )
        analogy_body2 = Tex(
            r"$\bullet$ This is like Frostman's lemma in geometric measure theory",
            font_size=26,
            color=GREY_B,
        )

        strategy_header = Tex(
            r"\textbf{Strategy:} Relate $\mathbb{T}_\rho$ back to Katz-Tao sets.",
            font_size=28,
            color=GREEN,
        )
        strategy1 = Tex(
            r"$\bullet$ Look inside small balls $B \subset B_1$",
            font_size=26,
        )
        strategy2 = Tex(
            r"$\bullet$ Use the \textbf{factoring lemma} to organize the tubes",
            font_size=26,
        )
        strategy3 = Tex(
            r"$\bullet$ Apply the \textbf{high density lemma} for Frostman sets",
            font_size=26,
        )

        all_content2 = VGroup(
            problem_header, prob_eq, analogy_header, analogy_body, analogy_body2,
            strategy_header, strategy1, strategy2, strategy3,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="Let us understand why the coarse scale is so difficult. "
            "In the non-sticky case, the set of rho tubes has far more than "
            "rho to the minus two tubes. "
            "This means it does not satisfy the Katz-Tao Wolff axiom. "
            "We cannot apply our induction hypothesis directly. "
            "However, the set of rho tubes does satisfy a weaker condition. "
            "The density inside any sub-region is controlled by the global density. "
            "This is called a Frostman condition, "
            "named after Frostman's lemma in geometric measure theory. "
            "The strategy is to relate these Frostman sets of tubes "
            "back to Katz-Tao sets that we can control. "
            "We do this by looking inside small balls, "
            "using the factoring lemma to organize the tubes, "
            "and applying the high density lemma for Frostman sets."
        ):
            self.play(Write(title2))
            self.play(FadeIn(problem_header))
            self.play(Write(prob_eq))
            self.play(Circumscribe(prob_eq, color=RED, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(analogy_header))
            self.play(FadeIn(analogy_body))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(analogy_body2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(strategy_header))
            self.play(FadeIn(strategy1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(strategy2))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(strategy3))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Step 3: The Factoring Lemma
    # ──────────────────────────────────────────────
    def _step3_factoring(self):
        # --- Part A: The idea ---
        title = Tex(r"\text{Step 3: The Factoring Lemma}", font_size=38, color=ORANGE)
        title.to_edge(UP, buff=0.5)

        problem = Tex(
            r"\textbf{Recall:} $\mathbb{T}_\rho$ has high density and no structure.",
            font_size=28,
        )
        question = Tex(
            r"\textbf{Question:} How do we find structure in chaos?",
            font_size=28,
            color=TEAL,
        )

        idea_header = Tex(
            r"\textbf{Answer:} Find the convex sets where tubes cluster most.",
            font_size=28,
            color=GREEN,
        )

        greedy = Tex(
            r"\textbf{Greedy algorithm:}",
            font_size=28,
        )
        greedy1 = Tex(
            r"$\bullet$ Find $W_1$ maximizing $\Delta(\mathbb{T}, W_1)$",
            font_size=26,
        )
        greedy2 = Tex(
            r"$\bullet$ Remove tubes in $W_1$, find $W_2$ maximizing the rest",
            font_size=26,
        )
        greedy3 = Tex(
            r"$\bullet$ Repeat until all tubes are assigned",
            font_size=26,
        )

        all_content = VGroup(
            problem, question, idea_header, greedy, greedy1, greedy2, greedy3,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(-1.5)
        center_mathtex(all_content)

        # Visual: chaotic tubes → convex clustering
        # Chaotic tubes (messy arrangement)
        chaotic_tubes = VGroup()
        tube_positions = [
            (0, 0, 0), (0.3, 0.2, PI/6), (-0.2, -0.1, -PI/8),
            (0.5, -0.3, PI/4), (-0.4, 0.1, PI/3), (0.1, 0.4, -PI/5),
            (-0.1, -0.4, PI/7), (0.6, 0.1, -PI/10), (-0.5, -0.2, PI/9),
            (0.2, 0.3, -PI/12), (-0.3, 0.35, PI/11), (0.4, -0.15, -PI/7),
        ]
        for x, y, angle in tube_positions:
            t = Rectangle(
                width=0.8, height=0.06,
                color=RED, fill_opacity=0.3, stroke_width=1,
            )
            t.rotate(angle)
            t.shift(UP * y + RIGHT * x)
            chaotic_tubes.add(t)
        chaotic_label = Tex(r"Chaotic tubes", font_size=20, color=RED)
        chaotic_label.next_to(chaotic_tubes, DOWN, buff=0.15)
        chaotic_group = VGroup(chaotic_tubes, chaotic_label)

        # Arrow
        factor_arrow = Tex(r"$\xrightarrow{\text{factor}}$", font_size=24, color=GREEN)

        # Clustered tubes (organized into convex sets)
        cluster1 = VGroup()
        for i in range(5):
            t = Rectangle(
                width=0.7, height=0.05,
                color=SEMINAR_BLUE, fill_opacity=0.3, stroke_width=1,
            )
            t.rotate(i * PI / 8)
            cluster1.add(t)
        cluster1_box = SurroundingRectangle(
            cluster1, color=TEAL, buff=0.1, corner_radius=0.15, stroke_width=2,
        )
        cluster1_label = Tex(r"$W_1$", font_size=18, color=TEAL)
        cluster1_label.next_to(cluster1_box, DOWN, buff=0.05)
        cluster1_group = VGroup(cluster1_box, cluster1, cluster1_label)
        cluster1_group.shift(UP * 0.5 + LEFT * 0.5)

        cluster2 = VGroup()
        for i in range(4):
            t = Rectangle(
                width=0.6, height=0.05,
                color=GOLD, fill_opacity=0.3, stroke_width=1,
            )
            t.rotate(i * PI / 6 + PI / 4)
            cluster2.add(t)
        cluster2_box = SurroundingRectangle(
            cluster2, color=ORANGE, buff=0.1, corner_radius=0.15, stroke_width=2,
        )
        cluster2_label = Tex(r"$W_2$", font_size=18, color=ORANGE)
        cluster2_label.next_to(cluster2_box, DOWN, buff=0.05)
        cluster2_group = VGroup(cluster2_box, cluster2, cluster2_label)
        cluster2_group.shift(DOWN * 0.5 + RIGHT * 0.5)

        clustered_label = Tex(r"Organized clusters", font_size=20, color=GREEN)
        clustered_group = VGroup(cluster1_group, cluster2_group, clustered_label)
        clustered_label.next_to(cluster2_group, DOWN, buff=0.2)

        cluster_demo = VGroup(chaotic_group, factor_arrow, clustered_group)
        cluster_demo.arrange(RIGHT, buff=0.4)
        cluster_demo.set_x(3.2)
        cluster_demo.to_edge(DOWN, buff=0.3)

        with self.voiceover(
            text="Step three: the factoring lemma. "
            "Recall that the set of rho tubes has high density "
            "and no obvious structure. "
            "The question is: how do we find structure in chaos? "
            "The answer is surprisingly elegant. "
            "Find the convex sets where tubes cluster the most. "
            "We use a greedy algorithm. "
            "First, find the convex set W one that maximizes the tube density. "
            "Then remove all tubes inside W one, "
            "and find the next convex set W two that maximizes the density of what remains. "
            "Repeat until all tubes are assigned to some convex set."
        ):
            self.play(Write(title))
            self.play(FadeIn(problem))
            self.play(FadeIn(question))
            # Show chaotic tubes
            self.play(
                *[Create(t) for t in chaotic_tubes],
                lag_ratio=0.08,
            )
            self.play(FadeIn(chaotic_label))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(idea_header))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(greedy))
            self.play(FadeIn(greedy1))
            # Show clustering animation
            self.play(FadeIn(factor_arrow))
            self.play(Create(cluster1_box))
            self.play(*[Create(t) for t in cluster1], lag_ratio=0.15)
            self.play(FadeIn(cluster1_label))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(greedy2))
            self.play(Create(cluster2_box))
            self.play(*[Create(t) for t in cluster2], lag_ratio=0.15)
            self.play(FadeIn(cluster2_label))
            self.play(FadeIn(clustered_label))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(greedy3))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: What we get ---
        title2 = Tex(r"\text{What the Factoring Lemma Gives Us}", font_size=38, color=ORANGE)
        title2.to_edge(UP, buff=0.5)

        header = Tex(
            r"\textbf{Result:} $\mathbb{T} = \bigsqcup_{W \in \mathcal{W}} \mathbb{T}_W$",
            font_size=30,
        )

        bullet1 = Tex(
            r"$\bullet$ $\mathcal{W}$ is \textbf{Katz-Tao}: $\Delta_{\max}(\mathcal{W}) \sim 1$",
            font_size=26,
            color=GREEN,
        )
        bullet1b = Tex(
            r"$\phantom{\bullet}$\;The container sets themselves are well-distributed",
            font_size=24,
            color=GREY_B,
        )
        bullet2 = Tex(
            r"$\bullet$ Each $\mathbb{T}_W$ is \textbf{Frostman} in $W$",
            font_size=26,
            color=GREEN,
        )
        bullet2b = Tex(
            r"$\phantom{\bullet}$\;Tubes inside $W$ are evenly spread (no sub-clustering)",
            font_size=24,
            color=GREY_B,
        )

        card, rect, card_content = make_theorem_card(
            MathTex(
                r"\mu(\mathbb{T}) \lessapprox \mu(\mathcal{W}) \cdot \mu(\mathbb{T}_W)",
                font_size=34,
                color=GREEN,
            ),
            color=GREEN,
            buff=0.3,
        )

        why_powerful = Tex(
            r"\textbf{Why this is powerful:}",
            font_size=28,
            color=TEAL,
        )
        why1 = Tex(
            r"$\bullet$ $\mathcal{W}$ is Katz-Tao $\Rightarrow$ we can apply induction!",
            font_size=26,
        )
        why2 = Tex(
            r"$\bullet$ $\mathbb{T}_W$ is Frostman $\Rightarrow$ we can use the high density lemma",
            font_size=26,
        )
        why3 = Tex(
            r"$\bullet$ One messy problem $\to$ two clean problems",
            font_size=26,
            color=GREEN,
        )

        all_content2 = VGroup(
            header, bullet1, bullet1b, bullet2, bullet2b, card,
            why_powerful, why1, why2, why3,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        card.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="What does this factoring lemma give us? "
            "Two remarkable structural properties. "
            "First, the collection of container sets W is itself Katz-Tao. "
            "The containers are well-distributed and do not cluster. "
            "This means we can apply our induction hypothesis to W. "
            "Second, the tubes inside each container W are Frostman. "
            "They are evenly spread inside W with no sub-clustering. "
            "This means we can use the high density lemma to control them. "
            "The multiplicity of the whole system factors into "
            "the multiplicity of the containers times the multiplicity inside each one. "
            "One messy, unstructured problem has been reduced to "
            "two clean, well-behaved problems. "
            "This is the key structural insight of the proof."
        ):
            self.play(Write(title2))
            self.play(FadeIn(header))
            self.play(FadeIn(bullet1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet1b))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet2b))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(card_content), Create(rect))
            self.play(Circumscribe(card, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(why_powerful))
            self.play(FadeIn(why1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(why2))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(why3))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Step 4: High Density Lemma
    # ──────────────────────────────────────────────
    def _step4_high_density(self):
        # --- Part A: What is a Frostman set? ---
        title = Tex(r"\text{Step 4: High Density Lemma}", font_size=38, color=PURPLE)
        title.to_edge(UP, buff=0.5)

        frostman_header = Tex(
            r"\textbf{Frostman condition.} A set of tubes $\mathbb{T}$ in $K$ is Frostman if:",
            font_size=28,
        )

        frostman_def = MathTex(
            r"C_F(\mathbb{T}, K) = \frac{\sup_{K' \subset K} \Delta(\mathbb{T}, K')}{\Delta(\mathbb{T}, K)} \lessapprox 1",
            font_size=30,
            color=TEAL,
        )

        intuition = Tex(
            r"\textbf{Meaning:} No sub-region of $K$ has much higher density than $K$ itself.",
            font_size=26,
        )
        analogy = Tex(
            r"\textbf{Analogy:} Like a uniform distribution — density is roughly constant everywhere.",
            font_size=24,
            color=GREY_B,
        )

        contrast = Tex(
            r"\textbf{Contrast with Katz-Tao:}",
            font_size=28,
        )
        contrast1 = Tex(
            r"$\bullet$ Katz-Tao: $\Delta_{\max} \lessapprox 1$ — tubes are sparse everywhere",
            font_size=26,
        )
        contrast2 = Tex(
            r"$\bullet$ Frostman: density is uniform, but can be \textit{large}",
            font_size=26,
        )
        contrast3 = Tex(
            r"$\bullet$ Frostman allows $|\mathbb{T}| \gg \delta^{-2}$ (many more tubes!)",
            font_size=26,
            color=YELLOW,
        )

        all_content = VGroup(
            frostman_header, frostman_def, intuition, analogy,
            contrast, contrast1, contrast2, contrast3,
        )
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(-1.5)
        center_mathtex(all_content)

        # Visual: Frostman vs non-Frostman density
        # Left: Frostman (uniform density)
        frostman_box = Rectangle(
            width=1.5, height=1.5,
            color=TEAL, fill_opacity=0.05, stroke_width=2,
        )
        frostman_tubes = VGroup()
        for i in range(8):
            angle = i * PI / 8
            t = Rectangle(
                width=1.2, height=0.04,
                color=SEMINAR_BLUE, fill_opacity=0.25, stroke_width=1,
            )
            t.rotate(angle)
            frostman_tubes.add(t)
        frostman_tubes.move_to(frostman_box)
        # Sub-region
        sub_box = Rectangle(
            width=0.6, height=0.6,
            color=YELLOW, fill_opacity=0.1, stroke_width=2, stroke_color=YELLOW,
        )
        sub_box.shift(RIGHT * 0.3 + UP * 0.2)
        frostman_label = Tex(r"Frostman: $C_F \lessapprox 1$", font_size=18, color=GREEN)
        frostman_label.next_to(frostman_box, DOWN, buff=0.15)
        frostman_group = VGroup(frostman_box, frostman_tubes, sub_box, frostman_label)

        # Right: non-Frostman (clustering)
        nonfrostman_box = Rectangle(
            width=1.5, height=1.5,
            color=RED, fill_opacity=0.05, stroke_width=2, stroke_color=RED,
        )
        nonfrostman_tubes = VGroup()
        # Clustered in one corner
        for i in range(8):
            angle = i * PI / 8
            t = Rectangle(
                width=1.0, height=0.04,
                color=RED, fill_opacity=0.3, stroke_width=1,
            )
            t.rotate(angle)
            t.shift(LEFT * 0.3 + DOWN * 0.3)
            nonfrostman_tubes.add(t)
        nonfrostman_sub = Rectangle(
            width=0.6, height=0.6,
            color=YELLOW, fill_opacity=0.15, stroke_width=2, stroke_color=YELLOW,
        )
        nonfrostman_sub.shift(LEFT * 0.3 + DOWN * 0.3)
        nonfrostman_label = Tex(r"Non-Frostman: $C_F \gg 1$", font_size=18, color=RED)
        nonfrostman_label.next_to(nonfrostman_box, DOWN, buff=0.15)
        nonfrostman_group = VGroup(
            nonfrostman_box, nonfrostman_tubes, nonfrostman_sub, nonfrostman_label,
        )

        density_demo = VGroup(frostman_group, nonfrostman_group)
        density_demo.arrange(RIGHT, buff=1.0)
        density_demo.set_x(3.2)
        density_demo.to_edge(DOWN, buff=0.5)

        vs_label = Tex(r"vs", font_size=24, color=GREY_B)
        vs_label.move_to(midpoint(frostman_group.get_right(), nonfrostman_group.get_left()))

        with self.voiceover(
            text="Step four: the high density lemma. "
            "First, let us understand what a Frostman set of tubes is. "
            "A set of tubes inside a convex set K is Frostman "
            "if no sub-region of K has much higher tube density than K itself. "
            "Think of it as a uniform distribution: "
            "the density is roughly constant everywhere. "
            "This is different from the Katz-Tao condition. "
            "Katz-Tao says tubes are sparse everywhere. "
            "Frostman says the density is uniform, "
            "but that uniform density can be very large. "
            "A Frostman set can have many more than delta to the minus two tubes, "
            "which is exactly what happens in the non-sticky case."
        ):
            self.play(Write(title))
            self.play(FadeIn(frostman_header))
            self.play(Write(frostman_def))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(intuition))
            # Show Frostman visualization
            self.play(Create(frostman_box))
            self.play(*[Create(t) for t in frostman_tubes], lag_ratio=0.1)
            self.play(Create(sub_box))
            self.play(FadeIn(frostman_label))
            self.wait(PAUSE_ELEMENT)
            # Show non-Frostman
            self.play(Create(nonfrostman_box))
            self.play(*[Create(t) for t in nonfrostman_tubes], lag_ratio=0.1)
            self.play(Create(nonfrostman_sub))
            self.play(FadeIn(nonfrostman_label), FadeIn(vs_label))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(analogy))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(contrast))
            self.play(FadeIn(contrast1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(contrast2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(contrast3))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: The lemma ---
        title2 = Tex(r"\text{The High Density Lemma}", font_size=38, color=PURPLE)
        title2.to_edge(UP, buff=0.5)

        lemma_header = Tex(
            r"\textbf{High Density Lemma.} If $\mathbb{T}$ is Frostman in $B_1$, then:",
            font_size=28,
        )

        lemma_eq = MathTex(
            r"\mu(\mathbb{T}) \lessapprox (\delta^{-2})^\beta \cdot (\delta^2 |\mathbb{T}|)^{1 - \beta}",
            font_size=32,
            color=PURPLE,
        )

        parse_header = Tex(
            r"\textbf{Parsing the bound:}",
            font_size=28,
        )
        parse1 = Tex(
            r"$\bullet$ If $|\mathbb{T}| \approx \delta^{-2}$: recovers $\mu \lessapprox \delta^{-2\beta}$",
            font_size=26,
        )
        parse2 = Tex(
            r"$\bullet$ If $|\mathbb{T}| \gg \delta^{-2}$: \textbf{better} bound (larger union!)",
            font_size=26,
            color=GREEN,
        )
        parse3 = Tex(
            r"$\bullet$ More tubes $\Rightarrow$ proportionally more union volume",
            font_size=26,
            color=TEAL,
        )

        how_header = Tex(
            r"\textbf{How is it proved?}",
            font_size=28,
        )
        how1 = Tex(
            r"$\bullet$ Uses the sticky Kakeya theorem as a black box",
            font_size=26,
        )
        how2 = Tex(
            r"$\bullet$ Multiscale analysis: look at $\mathbb{T}$ at scales $\rho = \delta^{k/M}$",
            font_size=26,
        )
        how3 = Tex(
            r"$\bullet$ Relate Frostman sets to Katz-Tao sets via random rotations",
            font_size=26,
        )

        all_content2 = VGroup(
            lemma_header, lemma_eq, parse_header, parse1, parse2, parse3,
            how_header, how1, how2, how3,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="Now the high density lemma. "
            "If a set of tubes is Frostman in the unit ball, "
            "then its multiplicity is bounded by this expression. "
            "Let us parse this bound. "
            "If the number of tubes is about delta to the minus two, "
            "we recover the standard bound mu lesssim delta to the minus two beta. "
            "But if there are many more tubes, "
            "the bound actually gets better. "
            "More tubes means proportionally more union volume. "
            "This is the key insight: "
            "if you pack more tubes into the unit ball "
            "while maintaining the Frostman condition, "
            "you cannot keep the union volume small. "
            "How is this proved? "
            "The proof uses the sticky Kakeya theorem as a black box, "
            "together with a subtle multiscale analysis. "
            "It also uses a clever trick: "
            "randomly rotate copies of the tube collection "
            "to turn a Frostman set into a Katz-Tao set."
        ):
            self.play(Write(title2))
            self.play(FadeIn(lemma_header))
            self.play(Write(lemma_eq))
            self.play(Circumscribe(lemma_eq, color=PURPLE, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(parse_header))
            self.play(FadeIn(parse1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(parse2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(parse3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(how_header))
            self.play(FadeIn(how1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(how2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(how3))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Step 5: Self-Improving Iteration
    # ──────────────────────────────────────────────
    def _step5_iteration(self):
        # --- Part A: The two statements ---
        title = Tex(r"\text{Step 5: Self-Improving Iteration}", font_size=38, color=GREEN)
        title.to_edge(UP, buff=0.5)

        setup = Tex(
            r"\textbf{Define $\beta$ as the critical exponent:}",
            font_size=28,
        )
        setup_eq = MathTex(
            r"\mu(\mathbb{T}) \lessapprox |\mathbb{T}|^\beta \quad \text{when } \Delta_{\max}(\mathbb{T}) \lessapprox 1",
            font_size=30,
            color=TEAL,
        )

        goal = Tex(
            r"\textbf{Goal:} Prove $\beta = 0$.",
            font_size=28,
            color=GREEN,
        )

        trivial = Tex(
            r"\textbf{Trivial:} $K_{KT}(1)$ is true (just union bound).",
            font_size=26,
            color=GREY_B,
        )

        all_content = VGroup(setup, setup_eq, goal, trivial)
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(-1.5)
        center_mathtex(all_content)

        # Visual: exponent decreasing
        beta_start = MathTex(r"\beta = 1", font_size=36, color=RED)
        beta_arrow = Tex(r"$\longrightarrow$", font_size=30, color=TEAL)
        beta_mid = MathTex(r"\beta = 1-\nu_1", font_size=30, color=YELLOW)
        beta_arrow2 = Tex(r"$\longrightarrow$", font_size=30, color=TEAL)
        beta_mid2 = MathTex(r"\beta = 1-\nu_1-\nu_2", font_size=28, color=ORANGE)
        beta_arrow3 = Tex(r"$\cdots \longrightarrow$", font_size=30, color=GREEN)
        beta_end = MathTex(r"\beta = 0", font_size=36, color=GREEN)

        beta_flow = VGroup(
            beta_start, beta_arrow, beta_mid,
            beta_arrow2, beta_mid2, beta_arrow3, beta_end,
        )
        beta_flow.arrange(RIGHT, buff=0.2)
        beta_flow.set_x(3.2)
        beta_flow.to_edge(DOWN, buff=1.0)

        with self.voiceover(
            text="Step five: the self-improving iteration. "
            "This is where all the pieces come together. "
            "Let beta be the critical exponent such that "
            "whenever tubes satisfy the Wolff axiom, "
            "their multiplicity is bounded by the number of tubes to the power beta. "
            "Our goal is to prove that beta equals zero. "
            "If beta is zero, the multiplicity is essentially bounded by one, "
            "which is exactly what we want. "
            "The trivial bound is beta equals one, "
            "which just says the multiplicity cannot exceed the number of tubes. "
            "We need to improve this all the way down to zero."
        ):
            self.play(Write(title))
            self.play(FadeIn(setup))
            self.play(Write(setup_eq))
            # Show beta flow
            self.play(Write(beta_start))
            self.play(FadeIn(beta_arrow))
            self.play(Write(beta_mid))
            self.play(FadeIn(beta_arrow2))
            self.play(Write(beta_mid2))
            self.play(FadeIn(beta_arrow3))
            self.play(Write(beta_end))
            self.play(Circumscribe(beta_end, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(goal))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(trivial))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part B: The bootstrap ---
        title2 = Tex(r"\text{The Bootstrap Mechanism}", font_size=38, color=GREEN)
        title2.to_edge(UP, buff=0.5)

        bullet1 = Tex(
            r"$\bullet$ $K_{KT}(\beta)$: multiplicity bound for \textbf{Katz-Tao} tubes",
            font_size=26,
        )
        bullet1b = Tex(
            r"$\phantom{\bullet}$\;$\Delta_{\max} \lessapprox 1 \implies \mu \lessapprox |\mathbb{T}|^\beta$",
            font_size=24,
            color=GREY_B,
        )
        bullet2 = Tex(
            r"$\bullet$ $K_F(\beta)$: multiplicity bound for \textbf{Frostman} tubes",
            font_size=26,
        )
        bullet2b = Tex(
            r"$\phantom{\bullet}$\;$C_F \lessapprox 1 \implies \mu \lessapprox (\delta^{-2})^\beta (\delta^2|\mathbb{T}|)^{1-\beta/2}$",
            font_size=24,
            color=GREY_B,
        )

        arrow1 = Tex(r"$\Downarrow$", font_size=30, color=TEAL)

        card1, rect1, c1_content = make_theorem_card(
            MathTex(r"K_{KT}(\beta) \implies K_F(\beta)", font_size=32, color=TEAL),
            color=TEAL,
            buff=0.25,
        )

        card1_note = Tex(
            r"Katz-Tao bound $\Rightarrow$ Frostman bound (via high density lemma)",
            font_size=22,
            color=GREY_B,
        )

        arrow2 = Tex(r"$\Downarrow$", font_size=30, color=GOLD)

        card2, rect2, c2_content = make_theorem_card(
            MathTex(
                r"K_{KT}(\beta) + K_F(\beta) \implies K_{KT}(\beta - \nu)",
                font_size=30,
                color=GOLD,
            ),
            color=GOLD,
            buff=0.25,
        )

        card2_note = Tex(
            r"Both bounds $\Rightarrow$ strictly better exponent $\beta - \nu(\beta)$",
            font_size=22,
            color=GREY_B,
        )

        all_content2 = VGroup(
            bullet1, bullet1b, bullet2, bullet2b,
            arrow1, card1, card1_note,
            arrow2, card2, card2_note,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        card1.set_x(0)
        card2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="The proof works with two statements. "
            "K K T of beta is the multiplicity bound for Katz-Tao tubes, "
            "those that satisfy the Wolff axiom. "
            "K F of beta is the multiplicity bound for Frostman tubes, "
            "those with uniform density but possibly many more tubes. "
            "The first implication says that if we know K K T at exponent beta, "
            "then we automatically get K F at the same exponent. "
            "This uses the high density lemma. "
            "The second, and crucial, implication says that "
            "if we know both K K T and K F at exponent beta, "
            "then we can prove K K T at a strictly better exponent beta minus nu. "
            "This is the self-improving step. "
            "The improvement nu depends on beta and is positive whenever beta is positive."
        ):
            self.play(Write(title2))
            self.play(FadeIn(bullet1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet1b))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(bullet2b))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(arrow1))
            self.play(FadeIn(c1_content), Create(rect1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(card1_note))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(arrow2))
            self.play(FadeIn(c2_content), Create(rect2))
            self.play(Circumscribe(card2, color=GOLD, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(card2_note))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

        # --- Part C: Why the iteration works ---
        title3 = Tex(r"\text{Closing the Argument}", font_size=38, color=GREEN)
        title3.to_edge(UP, buff=0.5)

        iter_header = Tex(
            r"\textbf{The iteration:}",
            font_size=28,
        )

        step1 = Tex(
            r"$\bullet$ Start with $K_{KT}(1)$ (trivially true)",
            font_size=26,
        )
        step2 = Tex(
            r"$\bullet$ $K_{KT}(1) \implies K_F(1)$",
            font_size=26,
        )
        step3 = Tex(
            r"$\bullet$ $K_{KT}(1) + K_F(1) \implies K_{KT}(1 - \nu_1)$",
            font_size=26,
        )
        step4 = Tex(
            r"$\bullet$ Repeat: $K_{KT}(1-\nu_1) \implies K_F(1-\nu_1) \implies K_{KT}(1-\nu_1-\nu_2)$",
            font_size=26,
        )

        converge = MathTex(
            r"\beta_0 = 1 \to \beta_1 \to \beta_2 \to \cdots \to 0",
            font_size=32,
            color=GREEN,
        )

        punchline = Tex(
            r"\textbf{Conclusion:} $K_{KT}(\beta)$ holds for all $\beta > 0$.",
            font_size=28,
            color=GREEN,
        )
        punchline2 = Tex(
            r"Let $\beta \to 0$: $\mu(\mathbb{T}) \lessapprox 1$ \quad \checkmark",
            font_size=30,
            color=GREEN,
        )

        why_works = Tex(
            r"\textbf{Why does $\beta \to 0$?} The improvement $\nu(\beta)$ stays positive.",
            font_size=24,
            color=GREY_B,
        )

        all_content3 = VGroup(
            iter_header, step1, step2, step3, step4, converge,
            punchline, punchline2, why_works,
        )
        all_content3.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content3.next_to(title3, DOWN, buff=0.5)
        all_content3.set_x(0)
        center_mathtex(all_content3)

        with self.voiceover(
            text="Here is how the iteration closes the argument. "
            "We start with K K T of one, which is trivially true. "
            "This gives us K F of one via the first implication. "
            "Together, they give us K K T of one minus nu one, "
            "via the self-improving step. "
            "Then we repeat: the new exponent gives us a new Frostman bound, "
            "which gives us an even better Katz-Tao bound. "
            "The sequence of exponents decreases: "
            "one, one minus nu one, one minus nu one minus nu two, and so on. "
            "The improvement nu of beta stays positive as long as beta is positive, "
            "so the sequence converges to zero. "
            "This means K K T of beta holds for every positive beta. "
            "Taking beta to zero, we get that the multiplicity is essentially bounded by one. "
            "The Kakeya conjecture is proved."
        ):
            self.play(Write(title3))
            self.play(FadeIn(iter_header))
            self.play(FadeIn(step1))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(step2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(step3))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(step4))
            self.wait(PAUSE_ELEMENT)
            self.play(Write(converge))
            self.play(Circumscribe(converge, color=GREEN, time_width=2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(punchline))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(punchline2))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(why_works))

        self.wait(PAUSE_KEY_RESULT)
        clear_screen(self)

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    def _summary(self):
        # --- Part A: The theorem ---
        title = Tex(r"\text{Summary}", font_size=40, color=BLUE)
        title.to_edge(UP, buff=0.5)

        thm_header = Tex(
            r"\textbf{Theorem (Wang-Zahl, 2025).}",
            font_size=32,
            color=GREEN,
        )

        thm_card, thm_rect, thm_content = make_theorem_card(
            MathTex(
                r"\text{Every Kakeya set in } \mathbb{R}^3 \text{ has dimension } 3",
                font_size=36,
                color=GREEN,
            ),
            color=GREEN,
            buff=0.3,
            stroke_width=3,
        )

        all_content = VGroup(thm_header, thm_card)
        all_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        all_content.next_to(title, DOWN, buff=0.5)
        all_content.set_x(0)
        thm_card.set_x(0)
        center_mathtex(all_content)

        with self.voiceover(
            text="And that completes the proof. "
            "Wang and Zahl proved that every Kakeya set in R cubed "
            "has full Hausdorff and Minkowski dimension three. "
            "Let us recap the key ideas."
        ):
            self.play(Write(title))
            self.play(FadeIn(thm_header))
            self.play(FadeIn(thm_content), Create(thm_rect))
            self.play(Circumscribe(thm_card, color=GREEN, time_width=2))

        self.wait(PAUSE_ELEMENT)
        clear_screen(self)

        # --- Part B: Key ideas recap ---
        title2 = Tex(r"\text{Key Ideas}", font_size=40, color=BLUE)
        title2.to_edge(UP, buff=0.5)

        recap1_header = Tex(
            r"\textbf{1. Multi-scale analysis}",
            font_size=28,
            color=TEAL,
        )
        recap1 = Tex(
            r"Look at tubes at scales $\delta \ll \rho \ll 1$. Factor multiplicity into fine and coarse parts.",
            font_size=24,
        )

        recap2_header = Tex(
            r"\textbf{2. Factoring lemma}",
            font_size=28,
            color=ORANGE,
        )
        recap2 = Tex(
            r"Organize arbitrary tubes into convex clusters. Reduce one messy problem to two clean ones.",
            font_size=24,
        )

        recap3_header = Tex(
            r"\textbf{3. High density lemma}",
            font_size=28,
            color=PURPLE,
        )
        recap3 = Tex(
            r"Control Frostman sets of tubes. More tubes $\Rightarrow$ proportionally larger union.",
            font_size=24,
        )

        recap4_header = Tex(
            r"\textbf{4. Self-improving iteration}",
            font_size=28,
            color=GOLD,
        )
        recap4 = Tex(
            r"Bootstrap: $K_{KT}(\beta) + K_F(\beta) \implies K_{KT}(\beta - \nu)$. Drive $\beta \to 0$.",
            font_size=24,
        )

        recap5_header = Tex(
            r"\textbf{5. Sticky Kakeya theorem}",
            font_size=28,
            color=GREEN,
        )
        recap5 = Tex(
            r"The base case. Sticky sets were solved earlier using sum-product theory.",
            font_size=24,
        )

        all_content2 = VGroup(
            recap1_header, recap1,
            recap2_header, recap2,
            recap3_header, recap3,
            recap4_header, recap4,
            recap5_header, recap5,
        )
        all_content2.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        all_content2.next_to(title2, DOWN, buff=0.5)
        all_content2.set_x(0)
        center_mathtex(all_content2)

        with self.voiceover(
            text="The key ideas are: "
            "First, multi-scale analysis. "
            "Look at tubes at intermediate scales and factor the multiplicity "
            "into fine-scale and coarse-scale contributions. "
            "Second, the factoring lemma. "
            "Organize arbitrary tubes into convex clusters, "
            "reducing one messy problem into two clean ones. "
            "Third, the high density lemma. "
            "Control Frostman sets of tubes, showing that more tubes "
            "force proportionally larger union volume. "
            "Fourth, the self-improving iteration. "
            "Use the bootstrap mechanism to drive the critical exponent to zero. "
            "And fifth, the sticky Kakeya theorem, "
            "proved earlier by Wang and Zahl using sum-product theory, "
            "which serves as the foundation for the entire argument."
        ):
            self.play(Write(title2))
            self.play(FadeIn(recap1_header))
            self.play(FadeIn(recap1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(recap2_header))
            self.play(FadeIn(recap2))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(recap3_header))
            self.play(FadeIn(recap3))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(recap4_header))
            self.play(FadeIn(recap4))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(recap5_header))
            self.play(FadeIn(recap5))

        self.wait(PAUSE_READ)
        clear_screen(self)

        # --- Part C: Historical context and significance ---
        title3 = Tex(r"\text{Historical Context}", font_size=40, color=BLUE)
        title3.to_edge(UP, buff=0.5)

        timeline_header = Tex(
            r"\textbf{A 100+ year journey:}",
            font_size=28,
        )

        t1 = Tex(
            r"1917 \quad Kakeya poses the needle rotation problem",
            font_size=24,
            color=GREY_B,
        )
        t2 = Tex(
            r"1919 \quad Besicovitch constructs sets of measure zero",
            font_size=24,
            color=GREY_B,
        )
        t3 = Tex(
            r"1971 \quad Davies proves the conjecture in $\mathbb{R}^2$",
            font_size=24,
            color=GREY_B,
        )
        t4 = Tex(
            r"1995 \quad Wolff introduces the Wolff axioms",
            font_size=24,
            color=GREY_B,
        )
        t5 = Tex(
            r"2000 \quad Katz-Laba-Tao: dimension $\geq 5/2 + c$",
            font_size=24,
            color=GREY_B,
        )
        t6 = Tex(
            r"2022 \quad Wang-Zahl: Sticky Kakeya Theorem",
            font_size=24,
            color=TEAL,
        )
        t7 = Tex(
            r"2025 \quad \textbf{Wang-Zahl: Full proof in $\mathbb{R}^3$}",
            font_size=24,
            color=GREEN,
        )

        impact_header = Tex(
            r"\textbf{Impact:}",
            font_size=28,
            color=TEAL,
        )
        impact1 = Tex(
            r"$\bullet$ Resolves the Tube Doubling Conjecture in $\mathbb{R}^3$",
            font_size=24,
        )
        impact2 = Tex(
            r"$\bullet$ New tools for harmonic analysis and PDE",
            font_size=24,
        )
        impact3 = Tex(
            r"$\bullet$ Opens the door to higher dimensions ($n \geq 4$)",
            font_size=24,
        )

        all_content3 = VGroup(
            timeline_header, t1, t2, t3, t4, t5, t6, t7,
            impact_header, impact1, impact2, impact3,
        )
        all_content3.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        all_content3.next_to(title3, DOWN, buff=0.5)
        all_content3.set_x(0)
        center_mathtex(all_content3)

        with self.voiceover(
            text="This result is the culmination of over a century of work. "
            "Kakeya posed the original needle rotation problem in 1917. "
            "Besicovitch shocked the mathematical community in 1919 "
            "by constructing sets of measure zero. "
            "Davies proved the conjecture in two dimensions in 1971. "
            "Wolff introduced the Wolff axioms in 1995, "
            "which became the language of the field. "
            "Katz, Laba, and Tao pushed the dimension bound "
            "to five halves plus a small constant in 2000. "
            "Wang and Zahl solved the sticky case in 2022, "
            "and now, in 2025, they have completed the full proof in R cubed. "
            "The impact extends beyond the Kakeya problem itself. "
            "The result resolves the Tube Doubling Conjecture in R cubed, "
            "provides new tools for harmonic analysis and partial differential equations, "
            "and opens the door to attacking the conjecture in higher dimensions. "
            "Thank you for watching."
        ):
            self.play(Write(title3))
            self.play(FadeIn(timeline_header))
            self.play(FadeIn(t1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(t2))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(t3))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(t4))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(t5))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(t6))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(t7))
            self.wait(PAUSE_ELEMENT)
            self.play(FadeIn(impact_header))
            self.play(FadeIn(impact1))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(impact2))
            self.wait(PAUSE_BRIEF)
            self.play(FadeIn(impact3))

        self.wait(PAUSE_FINALE)
