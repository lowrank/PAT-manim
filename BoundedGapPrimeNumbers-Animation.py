from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
from BoundedGapPrimeNumbers_Phoetics import get_phonetic_text
from latent_utils import (
    center_mathtex,
    make_content_group,
    make_theorem_card,
    LatentPrelude,
    clear_screen,
    SEMINAR_BLUE,
)


class ZhangBoundedGaps(LatentPrelude, VoiceoverScene):
    """
    Visualizes Yitang Zhang's 2014 proof on bounded gaps between primes.
    Uses Kokoro TTS for synchronized narration.
    """

    def construct(self):
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))
        self.play_prelude()

        # === Intro / Title Card ===
        self.intro()

        # === Prime Gaps Context ===
        self.prime_gaps_context_part1()
        self.prime_gaps_context_part2()

        # === Twin Prime Conjecture ===
        self.twin_prime_conjecture()

        # === Sieve Theory Intuition ===
        self.sieve_intuition_part1()
        self.sieve_intuition_part2()

        # === Admissible Tuples ===
        self.admissible_tuples_part1()
        self.admissible_tuples_part2()

        # === GPY Sieve Method ===
        self.gpy_sieve_method_part1()
        self.gpy_sieve_method_part2()

        # === Level of Distribution ===
        self.level_of_distribution_part1()
        self.level_of_distribution_part2()

        # === GPY Sieve Barrier ===
        self.gpy_barrier_part1()
        self.gpy_barrier_part2()

        # === Zhang's Proof Roadmap ===
        self.zhang_roadmap()

        # === Smooth Moduli Restriction ===
        self.zhang_breakthrough_part1()
        self.zhang_breakthrough_part2()

        # === Type I and Type II Sums ===
        self.type_sums_part1()
        self.type_sums_part2()

        # === Deligne's Bound ===
        self.deligne_bound_part1()
        self.deligne_bound_part2()

        # === Putting It All Together ===
        self.putting_it_together_part1()
        self.putting_it_together_part2()
        self.putting_it_together_part3()

        # === Main Theorem ===
        self.main_theorem()

        # === Conclusion ===
        self.conclusion_part1()
        self.conclusion_part2()

    # ------------------------------------------------------------------
    # Scene 1: Intro
    # ------------------------------------------------------------------
    def intro(self):
        with self.voiceover(
            text=get_phonetic_text("Welcome to Latent Seminar. "
                 "In 2014, Yitang Zhang published a landmark paper, "
                 "proving for the first time that the gaps between prime numbers are bounded."),
            subcaption="Welcome to Latent Seminar. "
                 "In 2014, Yitang Zhang published a landmark paper, "
                 "proving for the first time that the gaps between prime numbers are bounded."
        ):
            title = Tex(
                r"\textbf{Bounded Gaps Between Primes}",
                font_size=44,
                color=SEMINAR_BLUE,
            ).to_edge(UP, buff=0.5)
            author = Tex(
                r"Y. Zhang, Ann. Math. 179(3) (2014)",
                font_size=30,
                color=GRAY,
            )
            author.next_to(title, DOWN, buff=0.5)

            self.play(Write(title), run_time=1.5)
            self.play(FadeIn(author))

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 2a: Prime Gaps Context — PNT and average gap
    # ------------------------------------------------------------------
    def prime_gaps_context_part1(self):
        header = Tex(
            r"\textbf{Prime Gaps}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        pnt_label = MathTex(
            r"p_n \sim n \log n",
            font_size=32,
            color=BLUE,
        )
        pnt_label.next_to(header, DOWN, buff=0.5).set_x(0)

        avg_gap = MathTex(
            r"\text{Average gap: } p_{n+1} - p_n \sim \log p_n",
            font_size=28,
        )
        avg_gap.next_to(pnt_label, DOWN, buff=0.4).set_x(0)

        with self.voiceover(text=get_phonetic_text("Let us start with the basics."),
            subcaption="Let us start with the basics."):
            self.play(Write(header), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The prime number theorem tells us "
                 "that the n-th prime is approximately n log n."),
            subcaption="The prime number theorem tells us "
                 "that the n-th prime is approximately n log n."
        ):
            self.play(Write(pnt_label), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("This means the average gap between consecutive primes "
                 "grows like the logarithm of n. "
                 "So on average, primes get farther apart as we go further out."),
            subcaption="This means the average gap between consecutive primes "
                 "grows like the logarithm of n. "
                 "So on average, primes get farther apart as we go further out."
        ):
            self.play(FadeIn(avg_gap), run_time=1.5)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 2b: Prime Gaps Context — Number line visualization
    # ------------------------------------------------------------------
    def prime_gaps_context_part2(self):
        header = Tex(
            r"\textbf{Prime Gaps}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        number_line = NumberLine(
            x_range=[0, 32, 1],
            length=10,
            include_numbers=False,
            include_ticks=True,
        ).shift(DOWN * 0.5)

        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        dots = VGroup()
        prime_labels = VGroup()
        gap_labels = VGroup()

        for p in primes:
            pos = number_line.n2p(p)
            dot = Dot(pos, radius=0.09, color=YELLOW)
            dots.add(dot)

            lbl = MathTex(str(p), font_size=22)
            lbl.next_to(pos, UP, buff=0.15)
            prime_labels.add(lbl)

        for i in range(len(primes) - 1):
            gap = primes[i + 1] - primes[i]
            mid = (number_line.n2p(primes[i]) + number_line.n2p(primes[i + 1])) / 2
            gap_lbl = MathTex(str(gap), font_size=18, color=TEAL)
            gap_lbl.next_to(mid, UP, buff=0.45)
            gap_labels.add(gap_lbl)

        with self.voiceover(
            text=get_phonetic_text("But the average does not tell the whole story. "
                 "Some gaps are small, and some are very large."),
            subcaption="But the average does not tell the whole story. "
                 "Some gaps are small, and some are very large."
        ):
            self.play(Write(header), run_time=1.5)
            self.play(Create(number_line), run_time=1.5)
            self.play(FadeIn(dots), Write(prime_labels), run_time=2.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The question is whether the small gaps keep appearing forever."),
            subcaption="The question is whether the small gaps keep appearing forever."
        ):
            self.play(FadeIn(gap_labels), run_time=2.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 3: Twin Prime Conjecture
    # ------------------------------------------------------------------
    def twin_prime_conjecture(self):
        header = Tex(
            r"\textbf{The Twin Prime Conjecture}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        conj = MathTex(
            r"\liminf_{n \to \infty} (p_{n+1} - p_n) = 2",
            font_size=36,
        )
        card, rect, content = make_theorem_card(conj, color=YELLOW, buff=0.3)
        card.next_to(header, DOWN, buff=0.5)
        card.set_x(0)

        examples = Tex(
            r"Examples: $(3,5),\, (5,7),\, (11,13),\, (17,19),\, \dots$",
            font_size=26,
            color=TEAL,
        )
        examples.next_to(card, DOWN, buff=0.4)

        zhang_note = Tex(
            r"Zhang proved: $\liminf (p_{n+1} - p_n) < \infty$",
            font_size=28,
            color=GREEN,
        )
        zhang_note.next_to(examples, DOWN, buff=0.4)

        with self.voiceover(
            text=get_phonetic_text("The most famous question about small gaps "
                 "is the Twin Prime Conjecture."),
            subcaption="The most famous question about small gaps "
                 "is the Twin Prime Conjecture."
        ):
            self.play(Write(header), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("It says that there are infinitely many pairs of primes "
                 "that differ by exactly two."),
            subcaption="It says that there are infinitely many pairs of primes "
                 "that differ by exactly two."
        ):
            self.play(FadeIn(content), Create(rect), run_time=2.0)

        self.wait(1.0)

        with self.voiceover(
            text=get_phonetic_text("For example, three and five, five and seven, "
                 "eleven and thirteen. "
                 "These pairs appear to persist no matter how far you go, "
                 "but nobody has been able to prove this for over a century."),
            subcaption="For example, three and five, five and seven, "
                 "eleven and thirteen. "
                 "These pairs appear to persist no matter how far you go, "
                 "but nobody has been able to prove this for over a century."
        ):
            self.play(FadeIn(examples), run_time=2.0)

        self.wait(1.0)

        with self.voiceover(
            text=get_phonetic_text("Zhang's breakthrough was to prove a weaker version: "
                 "that the gaps are bounded by some finite number, "
                 "even if we do not know which one."),
            subcaption="Zhang's breakthrough was to prove a weaker version: "
                 "that the gaps are bounded by some finite number, "
                 "even if we do not know which one."
        ):
            self.play(FadeIn(zhang_note), run_time=2.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 4a: Sieve Theory Intuition — Eratosthenes
    # ------------------------------------------------------------------
    def sieve_intuition_part1(self):
        header = Tex(
            r"\textbf{Sieve Theory Intuition}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        erat_label = Tex(
            r"\textbf{Sieve of Eratosthenes:}",
            font_size=28,
        )
        step1 = Tex(
            r"$\bullet$ Cross out multiples of 2",
            font_size=26,
        )
        step2 = Tex(
            r"$\bullet$ Cross out multiples of 3",
            font_size=26,
        )
        step3 = Tex(
            r"$\bullet$ Cross out multiples of 5, \dots",
            font_size=26,
        )

        erat_content = VGroup(erat_label, step1, step2, step3)
        erat_content.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        erat_content.next_to(header, DOWN, buff=0.5)
        erat_content.set_x(0)
        center_mathtex(erat_content)

        # Sieve visualization: numbers 1-30 in a grid
        numbers_grid = VGroup()
        for i in range(1, 31):
            sq = Square(side_length=0.35, fill_opacity=0.9, fill_color=WHITE, stroke_width=1, stroke_color=GRAY)
            num = MathTex(str(i), font_size=16)
            num.move_to(sq.get_center())
            cell = VGroup(sq, num)
            numbers_grid.add(cell)

        numbers_grid.arrange_in_grid(rows=3, cols=10, buff=0.08)
        numbers_grid.scale(0.8)
        numbers_grid.to_corner(DL, buff=0.5)

        composites_2 = {4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30}
        composites_3 = {9, 15, 21, 27}
        composites_5 = {25}

        with self.voiceover(
            text=get_phonetic_text("Before we get to Zhang's proof, "
                 "let us understand the main tool: sieve theory."),
            subcaption="Before we get to Zhang's proof, "
                 "let us understand the main tool: sieve theory."
        ):
            self.play(Write(header), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The idea goes back to the sieve of Eratosthenes. "
                 "To find primes, you cross out multiples of two, "
                 "then multiples of three, then five, and so on. "
                 "What remains are the primes."),
            subcaption="The idea goes back to the sieve of Eratosthenes. "
                 "To find primes, you cross out multiples of two, "
                 "then multiples of three, then five, and so on. "
                 "What remains are the primes."
        ):
            self.play(FadeIn(erat_label), run_time=0.8)
            self.play(FadeIn(step1, shift=RIGHT * 0.3), run_time=0.8)

            self.play(FadeIn(numbers_grid), run_time=1.0)
            for idx in range(30):
                n = idx + 1
                if n in composites_2:
                    cell = numbers_grid[idx]
                    sq = cell[0]
                    self.play(
                        sq.animate.set_fill(RED, opacity=0.4),
                        run_time=0.08,
                    )

            self.wait(0.3)
            self.play(FadeIn(step2, shift=RIGHT * 0.3), run_time=0.8)

            for idx in range(30):
                n = idx + 1
                if n in composites_3:
                    cell = numbers_grid[idx]
                    sq = cell[0]
                    self.play(
                        sq.animate.set_fill(RED, opacity=0.4),
                        run_time=0.08,
                    )

            self.wait(0.3)
            self.play(FadeIn(step3, shift=RIGHT * 0.3), run_time=0.8)

            for idx in range(30):
                n = idx + 1
                if n in composites_5:
                    cell = numbers_grid[idx]
                    sq = cell[0]
                    self.play(
                        sq.animate.set_fill(RED, opacity=0.4),
                        run_time=0.08,
                    )

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 4b: Sieve Theory Intuition — Modern sieves
    # ------------------------------------------------------------------
    def sieve_intuition_part2(self):
        header = Tex(
            r"\textbf{Sieve Theory Intuition}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        modern = Tex(
            r"\textbf{Modern sieves:} use weights $w(n)$",
            font_size=28,
            color=TEAL,
        )
        weight_note = Tex(
            r"$\phantom{\bullet}$\; Large on primes, small on composites",
            font_size=24,
            color=GRAY,
        )

        modern_content = VGroup(modern, weight_note)
        modern_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        modern_content.next_to(header, DOWN, buff=0.5)
        modern_content.set_x(0)
        center_mathtex(modern_content)

        # Sieve visualization: numbers 1-30 in a grid
        numbers_grid = VGroup()
        for i in range(1, 31):
            sq = Square(side_length=0.35, fill_opacity=0.9, fill_color=WHITE, stroke_width=1, stroke_color=GRAY)
            num = MathTex(str(i), font_size=16)
            num.move_to(sq.get_center())
            cell = VGroup(sq, num)
            numbers_grid.add(cell)

        numbers_grid.arrange_in_grid(rows=3, cols=10, buff=0.08)
        numbers_grid.scale(0.8)
        numbers_grid.to_corner(DL, buff=0.5)

        with self.voiceover(
            text=get_phonetic_text("Modern sieve methods are more sophisticated. "
                 "Instead of crossing out numbers one by one, "
                 "we assign weights to integers that are designed "
                 "to be large on primes and small on composites."),
            subcaption="Modern sieve methods are more sophisticated. "
                 "Instead of crossing out numbers one by one, "
                 "we assign weights to integers that are designed "
                 "to be large on primes and small on composites."
        ):
            self.play(Write(header), run_time=1.5)
            self.play(FadeIn(modern), run_time=1.0)
            self.play(FadeIn(weight_note, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(numbers_grid), run_time=1.0)

            primes_set = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29}
            for idx in range(30):
                n = idx + 1
                if n in primes_set:
                    cell = numbers_grid[idx]
                    sq = cell[0]
                    self.play(
                        sq.animate.set_fill(GREEN, opacity=0.6),
                        run_time=0.08,
                    )

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The goal is to count how many primes survive the sieve, "
                 "or in our case, how many pairs of integers "
                 "are simultaneously prime."),
            subcaption="The goal is to count how many primes survive the sieve, "
                 "or in our case, how many pairs of integers "
                 "are simultaneously prime."
        ):
            pass

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 5a: Admissible Tuples — Motivation and definition
    # ------------------------------------------------------------------
    def admissible_tuples_part1(self):
        header = Tex(
            r"\textbf{Admissible Tuples}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        motivation = Tex(
            r"\textbf{Why?} Avoid local obstructions to primality",
            font_size=26,
            color=TEAL,
        )
        bad_example = Tex(
            r"Bad: $\{0, 1\}$ --- one is always even",
            font_size=24,
            color=RED,
        )
        def_text = MathTex(
            r"\mathcal{H} = \{h_1, \dots, h_k\} \text{ admissible}",
            font_size=28,
        )
        cond_text = MathTex(
            r"\forall p, \quad |\mathcal{H} \bmod p| < p",
            font_size=28,
        )

        content = VGroup(motivation, bad_example, def_text, cond_text)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        # Bad tuple {0,1} mod 2: hits all classes
        bad_mod2_label = Tex(r"$\{0,1\} \bmod 2$:", font_size=22)

        def make_residue_classes(p, hits, size=0.3):
            group = VGroup()
            for i in range(p):
                circle = Circle(radius=size, fill_opacity=0.3, stroke_width=2)
                if i in hits:
                    circle.set_fill(GREEN, opacity=0.7)
                    circle.set_stroke(GREEN, width=3)
                else:
                    circle.set_fill(GRAY, opacity=0.2)
                    circle.set_stroke(GRAY, width=1)
                label = MathTex(str(i), font_size=16)
                label.move_to(circle.get_center())
                group.add(VGroup(circle, label))
            group.arrange(RIGHT, buff=0.15)
            return group

        bad_mod2_circles = make_residue_classes(2, {0, 1}, size=0.25)
        bad_mod2_circles.next_to(bad_mod2_label, RIGHT, buff=0.3)
        bad_mod2_group = VGroup(bad_mod2_label, bad_mod2_circles)
        bad_mod2_group.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("Now we come to a central concept: admissible tuples. "
                 "Why do we need this notion? "
                 "If you want to find two primes at a fixed distance, "
                 "say distance two, "
                 "you need to make sure there is no obvious obstruction."),
            subcaption="Now we come to a central concept: admissible tuples. "
                 "Why do we need this notion? "
                 "If you want to find two primes at a fixed distance, "
                 "say distance two, "
                 "you need to make sure there is no obvious obstruction."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(motivation), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("For example, if you look at n and n plus one, "
                 "one of them is always even, "
                 "so they cannot both be prime except for the pair two and three."),
            subcaption="For example, if you look at n and n plus one, "
                 "one of them is always even, "
                 "so they cannot both be prime except for the pair two and three."
        ):
            self.play(FadeIn(bad_example), run_time=1.5)
            self.play(FadeIn(bad_mod2_group), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("An admissible tuple is a set of shifts "
                 "that avoids this kind of obstruction for every prime. "
                 "Formally, a set H is admissible if for every prime p, "
                 "the elements of H do not cover all residue classes modulo p."),
            subcaption="An admissible tuple is a set of shifts "
                 "that avoids this kind of obstruction for every prime. "
                 "Formally, a set H is admissible if for every prime p, "
                 "the elements of H do not cover all residue classes modulo p."
        ):
            self.play(FadeOut(bad_mod2_group), run_time=0.5)
            self.play(FadeIn(def_text), run_time=1.5)
            self.play(FadeIn(cond_text), run_time=1.5)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 5b: Admissible Tuples — Example with residue classes
    # ------------------------------------------------------------------
    def admissible_tuples_part2(self):
        header = Tex(
            r"\textbf{Admissible Tuples}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        example = Tex(
            r"Good: $\mathcal{H} = \{0, 2, 6\}$",
            font_size=28,
            color=GREEN,
        )
        mod2 = Tex(
            r"$\bmod\, 2$: $\{0, 0, 0\}$ --- 1 of 2 classes",
            font_size=24,
            color=TEAL,
        )
        mod3 = Tex(
            r"$\bmod\, 3$: $\{0, 2, 0\}$ --- 2 of 3 classes",
            font_size=24,
            color=TEAL,
        )
        mod5 = Tex(
            r"$\bmod\, 5$: $\{0, 2, 1\}$ --- 3 of 5 classes",
            font_size=24,
            color=TEAL,
        )

        content = VGroup(example, mod2, mod3, mod5)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        def make_residue_classes(p, hits, size=0.3):
            group = VGroup()
            for i in range(p):
                circle = Circle(radius=size, fill_opacity=0.3, stroke_width=2)
                if i in hits:
                    circle.set_fill(GREEN, opacity=0.7)
                    circle.set_stroke(GREEN, width=3)
                else:
                    circle.set_fill(GRAY, opacity=0.2)
                    circle.set_stroke(GRAY, width=1)
                label = MathTex(str(i), font_size=16)
                label.move_to(circle.get_center())
                group.add(VGroup(circle, label))
            group.arrange(RIGHT, buff=0.15)
            return group

        with self.voiceover(
            text=get_phonetic_text("For example, the tuple zero, two, six is admissible. "
                 "Modulo two, all three elements are zero, "
                 "so they only hit one residue class. "
                 "Modulo three, they hit zero and two, missing the class one. "
                 "So there is no local obstruction to all three "
                 "being prime simultaneously."),
            subcaption="For example, the tuple zero, two, six is admissible. "
                 "Modulo two, all three elements are zero, "
                 "so they only hit one residue class. "
                 "Modulo three, they hit zero and two, missing the class one. "
                 "So there is no local obstruction to all three "
                 "being prime simultaneously."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(example), run_time=0.8)

            good_mod2_label = Tex(r"$\{0,2,6\} \bmod 2$:", font_size=22)
            good_mod2_circles = make_residue_classes(2, {0}, size=0.25)
            good_mod2_circles.next_to(good_mod2_label, RIGHT, buff=0.3)
            good_mod2_group = VGroup(good_mod2_label, good_mod2_circles)
            good_mod2_group.set_x(0)

            good_mod3_label = Tex(r"$\{0,2,6\} \bmod 3$:", font_size=22)
            good_mod3_circles = make_residue_classes(3, {0, 2}, size=0.25)
            good_mod3_circles.next_to(good_mod3_label, RIGHT, buff=0.3)
            good_mod3_group = VGroup(good_mod3_label, good_mod3_circles)
            good_mod3_group.set_x(0)

            good_mod5_label = Tex(r"$\{0,2,6\} \bmod 5$:", font_size=22)
            good_mod5_circles = make_residue_classes(5, {0, 1, 2}, size=0.2)
            good_mod5_circles.next_to(good_mod5_label, RIGHT, buff=0.3)
            good_mod5_group = VGroup(good_mod5_label, good_mod5_circles)
            good_mod5_group.set_x(0)

            self.play(FadeIn(good_mod2_group), run_time=0.8)
            self.play(FadeIn(mod2), run_time=0.6)
            self.wait(0.3)
            self.play(FadeIn(good_mod3_group), run_time=0.8)
            self.play(FadeIn(mod3), run_time=0.6)
            self.wait(0.3)
            self.play(FadeIn(good_mod5_group), run_time=0.8)
            self.play(FadeIn(mod5), run_time=0.6)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 6a: GPY Sieve Method — Idea and weighted sum
    # ------------------------------------------------------------------
    def gpy_sieve_method_part1(self):
        header = Tex(
            r"\textbf{The GPY Sieve Method}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        idea = Tex(
            r"\textbf{Key idea:} Weight integers by how ``prime-rich'' they are",
            font_size=26,
            color=TEAL,
        )
        sum_label = Tex(
            r"\textbf{Weighted sum:}",
            font_size=28,
        )
        sum_eq = MathTex(
            r"S = \sum_{n \leq x} "
            r"\left( \sum_{i=1}^{k} \Lambda(n + h_i) - \rho \right) "
            r"w(n)^2",
            font_size=26,
        )

        content = VGroup(idea, sum_label, sum_eq)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("The G P Y method, named after Goldston, Pintz, and Yildirim, "
                 "is the starting point for Zhang's work. "
                 "Here is the key idea."),
            subcaption="The G P Y method, named after Goldston, Pintz, and Yildirim, "
                 "is the starting point for Zhang's work. "
                 "Here is the key idea."
        ):
            self.play(Write(header), run_time=1.5)
            self.play(FadeIn(idea), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Instead of looking at individual primes, "
                 "we look at a weighted sum over integers n, "
                 "where the weight is designed to be large "
                 "when many of the shifted values n plus h sub i "
                 "are simultaneously prime."),
            subcaption="Instead of looking at individual primes, "
                 "we look at a weighted sum over integers n, "
                 "where the weight is designed to be large "
                 "when many of the shifted values n plus h sub i "
                 "are simultaneously prime."
        ):
            self.play(FadeIn(sum_label), run_time=0.8)
            self.play(FadeIn(sum_eq), run_time=2.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 6b: GPY Sieve Method — Lambda, weights, conclusion
    # ------------------------------------------------------------------
    def gpy_sieve_method_part2(self):
        header = Tex(
            r"\textbf{The GPY Sieve Method}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        lambda_def = MathTex(
            r"\Lambda(n) = \begin{cases} \log p & \text{if } n = p^m \\ 0 & \text{otherwise} \end{cases}",
            font_size=24,
        )
        weight_def = MathTex(
            r"w(n) = \sum_{d \mid P(n)} \lambda_d, \quad P(n) = \prod_{i=1}^k (n + h_i)",
            font_size=24,
        )
        conclusion = Tex(
            r"If $S > 0$, then $\exists\, n$ with $> \rho$ primes among $\{n+h_i\}$",
            font_size=26,
            color=GREEN,
        )

        content = VGroup(lambda_def, weight_def, conclusion)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("The inner sum counts primes among the shifts "
                 "using the von Mangoldt function. "
                 "Recall that the von Mangoldt function of n "
                 "is log p if n is a power of a prime p, "
                 "and zero otherwise. "
                 "So it essentially detects prime powers."),
            subcaption="The inner sum counts primes among the shifts "
                 "using the von Mangoldt function. "
                 "Recall that the von Mangoldt function of n "
                 "is log p if n is a power of a prime p, "
                 "and zero otherwise. "
                 "So it essentially detects prime powers."
        ):
            self.play(Write(header), run_time=1.5)
            self.play(FadeIn(lambda_def), run_time=2.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The weight w of n is a sieve weight, "
                 "a sum over divisors d of the product of all shifts. "
                 "The coefficients lambda sub d are chosen to optimize the sum. "
                 "The parameter rho is a threshold. "
                 "If the weighted sum is positive, "
                 "it means that for some n, more than rho of the shifts are prime. "
                 "By choosing rho carefully and making the sum positive, "
                 "one can guarantee that at least two shifts are prime simultaneously."),
            subcaption="The weight w of n is a sieve weight, "
                 "a sum over divisors d of the product of all shifts. "
                 "The coefficients lambda sub d are chosen to optimize the sum. "
                 "The parameter rho is a threshold. "
                 "If the weighted sum is positive, "
                 "it means that for some n, more than rho of the shifts are prime. "
                 "By choosing rho carefully and making the sum positive, "
                 "one can guarantee that at least two shifts are prime simultaneously."
        ):
            self.play(FadeIn(weight_def), run_time=2.0)
            self.wait(0.5)
            self.play(FadeIn(conclusion), run_time=1.5)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 7a: Level of Distribution — Arithmetic progressions
    # ------------------------------------------------------------------
    def level_of_distribution_part1(self):
        header = Tex(
            r"\textbf{Level of Distribution}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        ap_label = Tex(
            r"\textbf{Arithmetic progressions:} $a, a+q, a+2q, \dots$",
            font_size=26,
        )
        dirichlet = MathTex(
            r"\pi(x;q,a) \approx \frac{\pi(x)}{\phi(q)}",
            font_size=28,
        )

        content = VGroup(ap_label, dirichlet)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        # Visual: arithmetic progression highlight on number line
        number_line = NumberLine(
            x_range=[0, 30, 1],
            length=10,
            include_numbers=False,
            include_ticks=True,
        ).shift(DOWN * 1.5)

        # Highlight progression 1 mod 4: 1, 5, 9, 13, 17, 21, 25, 29
        ap_dots = VGroup()
        for n in range(1, 30, 4):
            pos = number_line.n2p(n)
            dot = Dot(pos, radius=0.12, color=TEAL)
            ap_dots.add(dot)
            lbl = MathTex(str(n), font_size=16, color=TEAL)
            lbl.next_to(pos, UP, buff=0.15)
            ap_dots.add(lbl)

        with self.voiceover(
            text=get_phonetic_text("To make the G P Y sum positive, "
                 "we need to understand how primes are distributed "
                 "in arithmetic progressions. "
                 "An arithmetic progression is a sequence like "
                 "a, a plus q, a plus two q, and so on, "
                 "where a and q are coprime."),
            subcaption="To make the G P Y sum positive, "
                 "we need to understand how primes are distributed "
                 "in arithmetic progressions. "
                 "An arithmetic progression is a sequence like "
                 "a, a plus q, a plus two q, and so on, "
                 "where a and q are coprime."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(ap_label), run_time=1.0)
            self.play(Create(number_line), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Dirichlet's theorem tells us that each such progression "
                 "contains infinitely many primes. "
                 "But we need a quantitative version: "
                 "how many primes are there up to x "
                 "in the progression a mod q? "
                 "The prime number theorem for arithmetic progressions says "
                 "this is approximately pi of x divided by phi of q, "
                 "where phi is Euler's totient function."),
            subcaption="Dirichlet's theorem tells us that each such progression "
                 "contains infinitely many primes. "
                 "But we need a quantitative version: "
                 "how many primes are there up to x "
                 "in the progression a mod q? "
                 "The prime number theorem for arithmetic progressions says "
                 "this is approximately pi of x divided by phi of q, "
                 "where phi is Euler's totient function."
        ):
            self.play(FadeIn(ap_dots), run_time=1.5)
            self.play(FadeIn(dirichlet), run_time=2.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 7b: Level of Distribution — Theta definition
    # ------------------------------------------------------------------
    def level_of_distribution_part2(self):
        header = Tex(
            r"\textbf{Level of Distribution}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        level_def = MathTex(
            r"\theta = \sup \left\{ \vartheta : \text{error is small for } q \leq x^\vartheta \right\}",
            font_size=26,
        )
        importance = Tex(
            r"$\bullet$ Larger $\theta$ $\Rightarrow$ more powerful sieve",
            font_size=26,
            color=TEAL,
        )
        importance2 = Tex(
            r"$\bullet$ $\theta > 1/2$ $\Rightarrow$ bounded prime gaps",
            font_size=26,
            color=GREEN,
        )

        content = VGroup(level_def, importance, importance2)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("The level of distribution theta measures "
                 "how large q can be "
                 "while this approximation still holds on average "
                 "over all a coprime to q."),
            subcaption="The level of distribution theta measures "
                 "how large q can be "
                 "while this approximation still holds on average "
                 "over all a coprime to q."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(level_def), run_time=2.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("If theta is larger, we can handle larger moduli, "
                 "and the sieve becomes more powerful."),
            subcaption="If theta is larger, we can handle larger moduli, "
                 "and the sieve becomes more powerful."
        ):
            self.play(FadeIn(importance), run_time=1.0)
            self.play(FadeIn(importance2), run_time=1.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 8a: GPY Sieve Barrier — The problem and BV theorem
    # ------------------------------------------------------------------
    def gpy_barrier_part1(self):
        header = Tex(
            r"\textbf{The GPY Barrier}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        req_text = MathTex(
            r"\text{GPY needs } \theta > 1/2",
            font_size=30,
            color=RED,
        )
        bv_text = MathTex(
            r"\text{Bombieri--Vinogradov: } \theta = 1/2",
            font_size=28,
        )
        bv_formula = MathTex(
            r"\sum_{q \leq x^{1/2} / (\log x)^B} \max_{(a,q)=1} "
            r"\left| \pi(x;q,a) - \frac{\pi(x)}{\phi(q)} \right| "
            r"\ll_A \frac{x}{(\log x)^A}",
            font_size=22,
        )
        barrier = Tex(
            r"\textbf{Gap:} need $\theta = 1/2 + \delta$ for some $\delta > 0$",
            font_size=26,
            color=RED,
        )

        info_group = VGroup(req_text, bv_text, bv_formula, barrier)
        info_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        info_group.next_to(header, DOWN, buff=0.5)
        info_group.set_x(0)
        center_mathtex(info_group)

        with self.voiceover(
            text=get_phonetic_text("Here is the problem. "
                 "The G P Y method needs a level of distribution "
                 "strictly greater than one-half to prove bounded gaps."),
            subcaption="Here is the problem. "
                 "The G P Y method needs a level of distribution "
                 "strictly greater than one-half to prove bounded gaps."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(req_text), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("But the best known result is the Bombieri Vinogradov theorem, "
                 "which gives exactly one-half. "
                 "Let us understand what this theorem says. "
                 "It bounds the average error in the prime number theorem "
                 "for arithmetic progressions, "
                 "summed over all moduli q up to x to the theta."),
            subcaption="But the best known result is the Bombieri Vinogradov theorem, "
                 "which gives exactly one-half. "
                 "Let us understand what this theorem says. "
                 "It bounds the average error in the prime number theorem "
                 "for arithmetic progressions, "
                 "summed over all moduli q up to x to the theta."
        ):
            self.play(FadeIn(bv_text), run_time=1.0)
            self.play(FadeIn(bv_formula), run_time=2.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The error term is small compared to x divided by any power of log x, "
                 "but only when theta is at most one-half."),
            subcaption="The error term is small compared to x divided by any power of log x, "
                 "but only when theta is at most one-half."
        ):
            self.play(FadeIn(barrier), run_time=1.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 8b: GPY Sieve Barrier — Theta scale visualization
    # ------------------------------------------------------------------
    def gpy_barrier_part2(self):
        header = Tex(
            r"\textbf{The GPY Barrier}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        note = Tex(
            r"This was the fundamental barrier that blocked progress for years.",
            font_size=26,
            color=RED,
        )
        note.next_to(header, DOWN, buff=0.5).set_x(0)

        # Visual: theta scale with barrier line
        theta_line = NumberLine(
            x_range=[0, 1, 0.1],
            length=6,
            include_numbers=True,
        ).shift(DOWN * 1)

        half_mark = Line(
            start=theta_line.n2p(0.5) + UP * 0.5,
            end=theta_line.n2p(0.5) + DOWN * 0.5,
            color=RED,
            stroke_width=4,
        )
        half_label = Tex(r"$\theta = 1/2$", font_size=20, color=RED)
        half_label.next_to(half_mark, UP, buff=0.1)

        bv_region = Line(
            start=theta_line.n2p(0) + DOWN * 0.3,
            end=theta_line.n2p(0.5) + DOWN * 0.3,
            color=BLUE,
            stroke_width=6,
        )
        bv_label = Tex(r"Bombieri--Vinogradov", font_size=18, color=BLUE)
        bv_label.next_to(bv_region, DOWN, buff=0.1)

        gpy_region = Line(
            start=theta_line.n2p(0.5) + UP * 0.7,
            end=theta_line.n2p(1.0) + UP * 0.7,
            color=GREEN,
            stroke_width=6,
        )
        gpy_label = Tex(r"GPY needs this", font_size=18, color=GREEN)
        gpy_label.next_to(gpy_region, UP, buff=0.1)

        gap_arrow = DoubleArrow(
            start=theta_line.n2p(0.5) + UP * 0.15,
            end=theta_line.n2p(0.52) + UP * 0.15,
            color=YELLOW,
            stroke_width=3,
        )
        gap_label = Tex(r"$\delta$", font_size=20, color=YELLOW)
        gap_label.next_to(gap_arrow, UP, buff=0.1)

        with self.voiceover(
            text=get_phonetic_text("The G P Y method was powerful enough to reduce bounded gaps "
                 "to this distribution problem, "
                 "but it could not break past the one-half threshold on its own."),
            subcaption="The G P Y method was powerful enough to reduce bounded gaps "
                 "to this distribution problem, "
                 "but it could not break past the one-half threshold on its own."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(note), run_time=1.0)
            self.play(Create(theta_line), run_time=1.0)
            self.play(Create(half_mark), Write(half_label), run_time=1.0)
            self.play(Create(bv_region), FadeIn(bv_label), run_time=1.0)
            self.play(Create(gpy_region), FadeIn(gpy_label), run_time=1.0)
            self.play(Create(gap_arrow), FadeIn(gap_label), run_time=0.8)

        self.wait(1.5)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 9: Zhang's Proof Roadmap
    # ------------------------------------------------------------------
    def zhang_roadmap(self):
        header = Tex(
            r"\textbf{Zhang's Proof Roadmap}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        step1 = Tex(
            r"$\bullet$ \textbf{Step 1:} Restrict to smooth moduli",
            font_size=26,
        )
        step1_note = Tex(
            r"$\phantom{\bullet}$\; Only $q$ with all prime factors $\leq x^\delta$",
            font_size=24,
            color=GRAY,
        )
        step2 = Tex(
            r"$\bullet$ \textbf{Step 2:} Type I / Type II decomposition",
            font_size=26,
        )
        step2_note = Tex(
            r"$\phantom{\bullet}$\; Split error terms by convolution structure",
            font_size=24,
            color=GRAY,
        )
        step3 = Tex(
            r"$\bullet$ \textbf{Step 3:} Deligne's bound on Kloosterman sums",
            font_size=26,
        )
        step3_note = Tex(
            r"$\phantom{\bullet}$\; Deep result from algebraic geometry",
            font_size=24,
            color=GRAY,
        )
        step4 = Tex(
            r"$\bullet$ \textbf{Step 4:} Distribution level $\theta = 1/2 + \delta$",
            font_size=26,
            color=GREEN,
        )
        step4_note = Tex(
            r"$\phantom{\bullet}$\; $\delta \approx 1/584$",
            font_size=24,
            color=GRAY,
        )

        steps = VGroup(step1, step1_note, step2, step2_note, step3, step3_note, step4, step4_note)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        steps.next_to(header, DOWN, buff=0.5)
        steps.set_x(0)
        center_mathtex(steps)

        with self.voiceover(
            text=get_phonetic_text("Zhang's proof follows a clear four-step roadmap. "
                 "Step one: instead of summing over all moduli q, "
                 "he restricts to smooth moduli, "
                 "meaning q whose prime factors are all small. "
                 "This restriction is mild but crucial."),
            subcaption="Zhang's proof follows a clear four-step roadmap. "
                 "Step one: instead of summing over all moduli q, "
                 "he restricts to smooth moduli, "
                 "meaning q whose prime factors are all small. "
                 "This restriction is mild but crucial."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(step1, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(step1_note, shift=RIGHT * 0.3), run_time=0.8)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Step two: he decomposes the error terms "
                 "into Type one and Type two sums. "
                 "Type one sums have a simple convolution structure, "
                 "while Type two sums are bilinear forms."),
            subcaption="Step two: he decomposes the error terms "
                 "into Type one and Type two sums. "
                 "Type one sums have a simple convolution structure, "
                 "while Type two sums are bilinear forms."
        ):
            self.play(FadeIn(step2, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(step2_note, shift=RIGHT * 0.3), run_time=0.8)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Step three: for the Type two sums, "
                 "he applies Deligne's bound on Kloosterman sums, "
                 "a deep result from algebraic geometry "
                 "proved as part of the Weil conjectures."),
            subcaption="Step three: for the Type two sums, "
                 "he applies Deligne's bound on Kloosterman sums, "
                 "a deep result from algebraic geometry "
                 "proved as part of the Weil conjectures."
        ):
            self.play(FadeIn(step3, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(step3_note, shift=RIGHT * 0.3), run_time=0.8)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Step four: combining all estimates, "
                 "he shows the distribution level exceeds one-half "
                 "by a tiny amount, "
                 "approximately one over five hundred eighty-four."),
            subcaption="Step four: combining all estimates, "
                 "he shows the distribution level exceeds one-half "
                 "by a tiny amount, "
                 "approximately one over five hundred eighty-four."
        ):
            self.play(FadeIn(step4, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(step4_note, shift=RIGHT * 0.3), run_time=0.8)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 10a: Smooth Moduli — Definition and example
    # ------------------------------------------------------------------
    def zhang_breakthrough_part1(self):
        header = Tex(
            r"\textbf{Step 1: Smooth Moduli}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        smooth_def = MathTex(
            r"q \text{ is } y\text{-smooth if } p \mid q \implies p \leq y",
            font_size=26,
        )
        example = Tex(
            r"Example: $12 = 2^2 \cdot 3$ is 3-smooth",
            font_size=26,
            color=TEAL,
        )
        zhang_choice = MathTex(
            r"y = x^\delta, \quad \delta \approx \frac{1}{584}",
            font_size=28,
        )

        content = VGroup(smooth_def, example, zhang_choice)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("Let us look at each step in more detail, "
                 "starting with smooth moduli. "
                 "A number q is called y-smooth "
                 "if all of its prime factors are at most y. "
                 "For example, twelve is three-smooth "
                 "because twelve equals two squared times three."),
            subcaption="Let us look at each step in more detail, "
                 "starting with smooth moduli. "
                 "A number q is called y-smooth "
                 "if all of its prime factors are at most y. "
                 "For example, twelve is three-smooth "
                 "because twelve equals two squared times three."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(smooth_def), run_time=1.5)
            self.play(FadeIn(example), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Zhang restricts his sieve sum "
                 "to only include smooth moduli q. "
                 "He chooses y to be x to the power delta, "
                 "where delta is about one over five hundred eighty-four. "
                 "This is a very small exponent, but it is enough."),
            subcaption="Zhang restricts his sieve sum "
                 "to only include smooth moduli q. "
                 "He chooses y to be x to the power delta, "
                 "where delta is about one over five hundred eighty-four. "
                 "This is a very small exponent, but it is enough."
        ):
            self.play(FadeIn(zhang_choice), run_time=1.5)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 10b: Smooth Moduli — Why this helps
    # ------------------------------------------------------------------
    def zhang_breakthrough_part2(self):
        header = Tex(
            r"\textbf{Step 1: Smooth Moduli}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        why_label = Tex(
            r"\textbf{Why this helps:}",
            font_size=28,
            color=TEAL,
        )
        benefit1 = Tex(
            r"$\bullet$ CRT factorization: $\mathbb{Z}/q\mathbb{Z} \cong \prod \mathbb{Z}/p_i^{e_i}\mathbb{Z}$",
            font_size=24,
        )
        benefit2 = Tex(
            r"$\bullet$ Kloosterman structure becomes visible",
            font_size=24,
        )
        benefit3 = Tex(
            r"$\bullet$ Error terms become tractable",
            font_size=24,
        )

        content = VGroup(why_label, benefit1, benefit2, benefit3)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("Why does this help? "
                 "When q has only small prime factors, "
                 "the arithmetic structure of q is very special. "
                 "The Chinese Remainder Theorem lets us factor "
                 "problems modulo q "
                 "into problems modulo each prime power dividing q. "
                 "This factorization is the key "
                 "that unlocks the deeper analysis."),
            subcaption="Why does this help? "
                 "When q has only small prime factors, "
                 "the arithmetic structure of q is very special. "
                 "The Chinese Remainder Theorem lets us factor "
                 "problems modulo q "
                 "into problems modulo each prime power dividing q. "
                 "This factorization is the key "
                 "that unlocks the deeper analysis."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(why_label), run_time=0.8)

            crt_demo = MathTex(
                r"\mathbb{Z}/12\mathbb{Z} \cong \mathbb{Z}/4\mathbb{Z} \times \mathbb{Z}/3\mathbb{Z}",
                font_size=24,
                color=TEAL,
            )
            crt_demo.next_to(why_label, DOWN, buff=0.4)
            crt_demo.set_x(0)

            self.play(FadeIn(crt_demo), run_time=1.5)
            self.play(FadeIn(benefit1, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(benefit2, shift=RIGHT * 0.3), run_time=1.0)
            self.play(FadeIn(benefit3, shift=RIGHT * 0.3), run_time=1.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 11a: Type I Sums
    # ------------------------------------------------------------------
    def type_sums_part1(self):
        header = Tex(
            r"\textbf{Step 2: Type I and Type II Sums}",
            font_size=30,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        type1_label = Tex(
            r"\textbf{Type I:} one long variable",
            font_size=28,
            color=TEAL,
        )
        type1_eq = MathTex(
            r"\sum_{m \sim M} \alpha_m \sum_{n \sim N} \psi(mn)",
            font_size=26,
        )
        type1_cond = MathTex(
            r"M \leq x^{1/2 + \delta}, \quad N = x / M \text{ is long}",
            font_size=24,
            color=GRAY,
        )
        type1_note = Tex(
            r"$\phantom{\bullet}$\; Easier: long range gives cancellation",
            font_size=24,
            color=GRAY,
        )

        content = VGroup(type1_label, type1_eq, type1_cond, type1_note)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("After restricting to smooth moduli, "
                 "Zhang needs to estimate the error terms. "
                 "The error terms come from the difference "
                 "between the actual count of primes "
                 "in arithmetic progressions and the expected count. "
                 "Zhang decomposes these error terms into two types."),
            subcaption="After restricting to smooth moduli, "
                 "Zhang needs to estimate the error terms. "
                 "The error terms come from the difference "
                 "between the actual count of primes "
                 "in arithmetic progressions and the expected count. "
                 "Zhang decomposes these error terms into two types."
        ):
            self.play(Write(header), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Type one sums have the form of a single sum over m, "
                 "where the coefficients alpha sub m are arbitrary "
                 "but the other variable n is long. "
                 "Think of it as a weighted average "
                 "of a sequence psi over a long range. "
                 "These are easier to handle "
                 "because the long variable gives cancellation."),
            subcaption="Type one sums have the form of a single sum over m, "
                 "where the coefficients alpha sub m are arbitrary "
                 "but the other variable n is long. "
                 "Think of it as a weighted average "
                 "of a sequence psi over a long range. "
                 "These are easier to handle "
                 "because the long variable gives cancellation."
        ):
            self.play(FadeIn(type1_label), run_time=0.8)
            self.play(FadeIn(type1_eq), run_time=1.5)
            self.play(FadeIn(type1_cond), run_time=1.0)

            short_bar = Rectangle(height=0.3, width=1.5, fill_color=TEAL, fill_opacity=0.6, stroke_width=1)
            long_bar = Rectangle(height=0.3, width=5, fill_color=TEAL, fill_opacity=0.3, stroke_width=1)
            short_label = Tex(r"short $M$", font_size=18)
            long_label = Tex(r"long $N = x/M$", font_size=18)
            short_label.move_to(short_bar)
            long_label.move_to(long_bar)
            type1_vis = VGroup(
                VGroup(short_bar, short_label),
                VGroup(long_bar, long_label),
            )
            type1_vis.arrange(RIGHT, buff=0.3)
            type1_vis.next_to(type1_eq, DOWN, buff=0.3)
            type1_vis.set_x(0)

            self.play(FadeIn(type1_vis), run_time=1.0)
            self.play(FadeIn(type1_note, shift=RIGHT * 0.3), run_time=0.8)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 11b: Type II Sums
    # ------------------------------------------------------------------
    def type_sums_part2(self):
        header = Tex(
            r"\textbf{Step 2: Type I and Type II Sums}",
            font_size=30,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        type2_label = Tex(
            r"\textbf{Type II:} bilinear form",
            font_size=28,
            color=GOLD,
        )
        type2_eq = MathTex(
            r"\sum_{m \sim M} \sum_{n \sim N} \alpha_m \beta_n \, \psi(mn)",
            font_size=26,
        )
        type2_cond = MathTex(
            r"x^\delta \leq M, N \leq x^{1/2 + \delta}",
            font_size=24,
            color=GRAY,
        )
        type2_note = Tex(
            r"$\phantom{\bullet}$\; Harder: needs Cauchy-Schwarz + Kloosterman",
            font_size=24,
            color=GRAY,
        )

        content = VGroup(type2_label, type2_eq, type2_cond, type2_note)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        content.next_to(header, DOWN, buff=0.5)
        content.set_x(0)
        center_mathtex(content)

        with self.voiceover(
            text=get_phonetic_text("Type two sums are bilinear. "
                 "Both variables m and n are of moderate size, "
                 "and both have arbitrary coefficients alpha and beta. "
                 "These are harder because neither variable "
                 "is long enough to give easy cancellation. "
                 "But the bilinear structure is precisely what allows us "
                 "to use Cauchy-Schwarz "
                 "and reduce to estimating Kloosterman sums."),
            subcaption="Type two sums are bilinear. "
                 "Both variables m and n are of moderate size, "
                 "and both have arbitrary coefficients alpha and beta. "
                 "These are harder because neither variable "
                 "is long enough to give easy cancellation. "
                 "But the bilinear structure is precisely what allows us "
                 "to use Cauchy-Schwarz "
                 "and reduce to estimating Kloosterman sums."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(type2_label), run_time=0.8)
            self.play(FadeIn(type2_eq), run_time=1.5)
            self.play(FadeIn(type2_cond), run_time=1.0)

            mod_bar1 = Rectangle(height=0.3, width=2.5, fill_color=GOLD, fill_opacity=0.5, stroke_width=1)
            mod_bar2 = Rectangle(height=0.3, width=2.5, fill_color=GOLD, fill_opacity=0.5, stroke_width=1)
            mod_label1 = Tex(r"moderate $M$", font_size=18)
            mod_label2 = Tex(r"moderate $N$", font_size=18)
            mod_label1.move_to(mod_bar1)
            mod_label2.move_to(mod_bar2)
            type2_vis = VGroup(
                VGroup(mod_bar1, mod_label1),
                VGroup(mod_bar2, mod_label2),
            )
            type2_vis.arrange(RIGHT, buff=0.3)
            type2_vis.next_to(type2_eq, DOWN, buff=0.3)
            type2_vis.set_x(0)

            self.play(FadeIn(type2_vis), run_time=1.0)
            self.play(FadeIn(type2_note, shift=RIGHT * 0.3), run_time=0.8)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 12a: Deligne's Bound — Kloosterman definition
    # ------------------------------------------------------------------
    def deligne_bound_part1(self):
        header = Tex(
            r"\textbf{Step 3: Deligne's Bound on Kloosterman Sums}",
            font_size=28,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        kl_label = Tex(
            r"\textbf{Kloosterman sum:}",
            font_size=28,
        )
        kl_def = MathTex(
            r"K(a, b; p) = \sum_{x \in \mathbb{F}_p^\times} "
            r"e\!\left(\frac{ax + b\overline{x}}{p}\right)",
            font_size=26,
        )
        trivial = MathTex(
            r"\text{Trivial bound: } |K| \leq p - 1",
            font_size=24,
            color=GRAY,
        )

        kl_group = VGroup(kl_label, kl_def, trivial)
        kl_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        kl_group.next_to(header, DOWN, buff=0.6)
        kl_group.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("Now we reach the deepest ingredient of Zhang's proof. "
                 "When estimating Type two sums, after applying Cauchy-Schwarz, "
                 "one encounters exponential sums called Kloosterman sums. "
                 "A Kloosterman sum is a sum over the multiplicative group "
                 "of a finite field. "
                 "It involves the exponential of a linear term plus its inverse, "
                 "divided by the prime p."),
            subcaption="Now we reach the deepest ingredient of Zhang's proof. "
                 "When estimating Type two sums, after applying Cauchy-Schwarz, "
                 "one encounters exponential sums called Kloosterman sums. "
                 "A Kloosterman sum is a sum over the multiplicative group "
                 "of a finite field. "
                 "It involves the exponential of a linear term plus its inverse, "
                 "divided by the prime p."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(kl_label), run_time=0.8)
            self.play(FadeIn(kl_def), run_time=2.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The trivial bound would give p minus one, "
                 "since there are p minus one terms each of size one."),
            subcaption="The trivial bound would give p minus one, "
                 "since there are p minus one terms each of size one."
        ):
            self.play(FadeIn(trivial), run_time=1.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 12b: Deligne's Bound — The square-root cancellation
    # ------------------------------------------------------------------
    def deligne_bound_part2(self):
        header = Tex(
            r"\textbf{Step 3: Deligne's Bound on Kloosterman Sums}",
            font_size=28,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        deligne = MathTex(
            r"|K(a, b; p)| \leq 2\sqrt{p}",
            font_size=36,
            color=GREEN,
        )
        card, rect, content = make_theorem_card(deligne, color=GREEN, buff=0.3)
        card.next_to(header, DOWN, buff=0.5)
        card.set_x(0)

        remark = Tex(
            r"Deligne (1974) --- Weil conjectures, algebraic geometry",
            font_size=24,
            color=GRAY,
        )
        remark.next_to(card, DOWN, buff=0.4)

        connection = Tex(
            r"Algebraic geometry $\rightarrow$ analytic number theory $\rightarrow$ prime gaps",
            font_size=24,
            color=TEAL,
        )
        connection.next_to(remark, DOWN, buff=0.3)

        with self.voiceover(
            text=get_phonetic_text("But Deligne proved, as part of his Fields Medal work "
                 "on the Weil conjectures, "
                 "that these sums exhibit square-root cancellation. "
                 "The absolute value is at most two times the square root of p. "
                 "This is dramatically smaller than p."),
            subcaption="But Deligne proved, as part of his Fields Medal work "
                 "on the Weil conjectures, "
                 "that these sums exhibit square-root cancellation. "
                 "The absolute value is at most two times the square root of p. "
                 "This is dramatically smaller than p."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(content), Create(rect), run_time=2.0)

            # Visual: bar chart comparison
            p_val = 101
            trivial_height = 3.0
            deligne_height = 3.0 / (p_val ** 0.5) * 2

            trivial_bar = Rectangle(
                height=trivial_height, width=0.8,
                fill_color=RED, fill_opacity=0.5, stroke_width=1,
            )
            trivial_bar_label = Tex(r"$p$", font_size=18)
            trivial_bar_label.next_to(trivial_bar, UP, buff=0.1)

            deligne_bar = Rectangle(
                height=deligne_height, width=0.8,
                fill_color=GREEN, fill_opacity=0.5, stroke_width=1,
            )
            deligne_bar_label = Tex(r"$2\sqrt{p}$", font_size=18)
            deligne_bar_label.next_to(deligne_bar, UP, buff=0.1)

            bound_vis = VGroup(trivial_bar, trivial_bar_label, deligne_bar, deligne_bar_label)
            bound_vis.arrange(RIGHT, buff=0.5)
            bound_vis.next_to(card, DOWN, buff=0.5)
            bound_vis.set_x(0)

            self.play(FadeIn(bound_vis), run_time=1.0)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Without this bound, the error terms in Zhang's estimates "
                 "would be too large, and the proof would fail. "
                 "It is remarkable that a result from algebraic geometry, "
                 "proved using etale cohomology and schemes, "
                 "is the key to a problem about prime numbers."),
            subcaption="Without this bound, the error terms in Zhang's estimates "
                 "would be too large, and the proof would fail. "
                 "It is remarkable that a result from algebraic geometry, "
                 "proved using etale cohomology and schemes, "
                 "is the key to a problem about prime numbers."
        ):
            self.play(FadeIn(remark), run_time=1.0)
            self.play(FadeIn(connection), run_time=1.0)

        self.wait(1.5)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 13a: Putting It All Together — Steps 1-2
    # ------------------------------------------------------------------
    def putting_it_together_part1(self):
        header = Tex(
            r"\textbf{Putting It All Together}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        step_labels = VGroup(
            Tex(r"\textbf{(1) Start with the GPY weighted sum}", font_size=26),
            MathTex(r"S = \sum_{n \leq x} \left(\sum_{i=1}^k \Lambda(n+h_i) - \rho\right) w(n)^2", font_size=24),
            Tex(r"$\bullet$ Goal: show $S > 0$ for some admissible $\mathcal{H}$", font_size=24, color=TEAL),
        )
        step_labels.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step_labels.next_to(header, DOWN, buff=0.5)
        step_labels.set_x(0)

        step_analysis = VGroup(
            Tex(r"\textbf{(2) Decompose the error}", font_size=26),
            Tex(r"$\bullet$ Restrict to smooth moduli $q$", font_size=24),
            Tex(r"$\bullet$ Split into Type I sums (one long variable)", font_size=24),
            Tex(r"$\bullet$ Split into Type II sums (bilinear form)", font_size=24),
        )
        step_analysis.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step_analysis.next_to(step_labels, DOWN, buff=0.4)
        step_analysis.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("Now let us see how all the pieces fit together. "
                 "We start with the G P Y weighted sum. "
                 "The goal is to show this sum is positive "
                 "for some admissible tuple H. "
                 "If it is positive, then for some integer n, "
                 "at least two of the shifted values n plus h sub i are prime."),
            subcaption="Now let us see how all the pieces fit together. "
                 "We start with the G P Y weighted sum. "
                 "The goal is to show this sum is positive "
                 "for some admissible tuple H. "
                 "If it is positive, then for some integer n, "
                 "at least two of the shifted values n plus h sub i are prime."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(step_labels), run_time=2.5)

            arrow1 = Arrow(
                start=step_labels.get_bottom(),
                end=step_analysis.get_top(),
                color=TEAL,
                buff=0.1,
            )
            self.play(GrowArrow(arrow1), run_time=0.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Step two: decompose the error. "
                 "First, we restrict the sum to smooth moduli only. "
                 "This means we only consider q whose prime factors are small. "
                 "Then we split the remaining error terms "
                 "into Type one sums, where one variable is long, "
                 "and Type two sums, which have a bilinear structure."),
            subcaption="Step two: decompose the error. "
                 "First, we restrict the sum to smooth moduli only. "
                 "This means we only consider q whose prime factors are small. "
                 "Then we split the remaining error terms "
                 "into Type one sums, where one variable is long, "
                 "and Type two sums, which have a bilinear structure."
        ):
            self.play(FadeIn(step_analysis), run_time=3.0)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 13b: Putting It All Together — Step 3
    # ------------------------------------------------------------------
    def putting_it_together_part2(self):
        header = Tex(
            r"\textbf{Putting It All Together}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        step_estimate = VGroup(
            Tex(r"\textbf{(3) Estimate each type}", font_size=26),
            Tex(r"$\bullet$ Type I: use smooth modulus factorization", font_size=24),
            Tex(r"$\bullet$ Type II: Cauchy-Schwarz $\rightarrow$ Kloosterman sums", font_size=24),
            Tex(r"$\bullet$ Apply Deligne: $|K| \leq 2\sqrt{p}$", font_size=24, color=GREEN),
        )
        step_estimate.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step_estimate.next_to(header, DOWN, buff=0.5)
        step_estimate.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("Step three: estimate each type. "
                 "For Type one sums, the smooth modulus structure "
                 "lets us factor the problem using the Chinese Remainder Theorem, "
                 "and the long variable gives us cancellation. "
                 "For Type two sums, we apply Cauchy-Schwarz, "
                 "which reduces the problem to bounding Kloosterman sums. "
                 "And here we use Deligne's bound: "
                 "the absolute value is at most two times the square root of p."),
            subcaption="Step three: estimate each type. "
                 "For Type one sums, the smooth modulus structure "
                 "lets us factor the problem using the Chinese Remainder Theorem, "
                 "and the long variable gives us cancellation. "
                 "For Type two sums, we apply Cauchy-Schwarz, "
                 "which reduces the problem to bounding Kloosterman sums. "
                 "And here we use Deligne's bound: "
                 "the absolute value is at most two times the square root of p."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(step_estimate), run_time=3.5)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 13c: Putting It All Together — Step 4 conclusion
    # ------------------------------------------------------------------
    def putting_it_together_part3(self):
        header = Tex(
            r"\textbf{Putting It All Together}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        step_conclude = VGroup(
            Tex(r"\textbf{(4) Conclusion}", font_size=26),
            MathTex(r"\theta = 1/2 + \delta \quad (\delta \approx 1/584)", font_size=28, color=GREEN),
            Tex(r"$\Rightarrow S > 0$ for large enough $k$", font_size=26, color=GREEN),
            Tex(r"$\Rightarrow \exists$ infinitely many $n$ with 2+ primes in $\{n+h_i\}$", font_size=24, color=GREEN),
        )
        step_conclude.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        step_conclude.next_to(header, DOWN, buff=0.5)
        step_conclude.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("Step four: putting the estimates together, "
                 "we find that the distribution level exceeds one-half "
                 "by a tiny amount delta, about one over five hundred eighty-four. "
                 "This is just enough to make the G P Y sum positive, "
                 "which guarantees that there are infinitely many integers n "
                 "such that at least two of the shifts n plus h sub i are prime. "
                 "Since the tuple is finite, the gap between these two primes "
                 "is bounded by the diameter of the tuple."),
            subcaption="Step four: putting the estimates together, "
                 "we find that the distribution level exceeds one-half "
                 "by a tiny amount delta, about one over five hundred eighty-four. "
                 "This is just enough to make the G P Y sum positive, "
                 "which guarantees that there are infinitely many integers n "
                 "such that at least two of the shifts n plus h sub i are prime. "
                 "Since the tuple is finite, the gap between these two primes "
                 "is bounded by the diameter of the tuple."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(step_conclude), run_time=4.0)

        self.wait(2.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 14: Main Theorem
    # ------------------------------------------------------------------
    def main_theorem(self):
        theorem_title = Tex(
            r"\textbf{Theorem (Zhang, 2014)}",
            font_size=36,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        result = MathTex(
            r"\liminf_{n \to \infty} (p_{n+1} - p_n) \leq 70,\!000,\!000",
            font_size=36,
            color=GREEN,
        )
        card, rect, content = make_theorem_card(result, color=GREEN, buff=0.3)
        card.next_to(theorem_title, DOWN, buff=0.5)
        card.set_x(0)

        pieces = Tex(
            r"Smooth moduli + Type I/II + Deligne $\Rightarrow \theta > 1/2$",
            font_size=24,
            color=TEAL,
        )
        pieces.next_to(card, DOWN, buff=0.5)

        sub_note = Tex(
            r"First finite bound on prime gaps in history",
            font_size=26,
            color=GRAY,
        )
        sub_note.next_to(pieces, DOWN, buff=0.4)

        with self.voiceover(
            text=get_phonetic_text("Putting all the pieces together, "
                 "Zhang proved his main theorem."),
            subcaption="Putting all the pieces together, "
                 "Zhang proved his main theorem."
        ):
            self.play(Write(theorem_title), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The smooth moduli restriction makes the error terms manageable. "
                 "The Type one and Type two decomposition organizes the analysis. "
                 "Deligne's bound provides the crucial square-root cancellation "
                 "for the hardest terms."),
            subcaption="The smooth moduli restriction makes the error terms manageable. "
                 "The Type one and Type two decomposition organizes the analysis. "
                 "Deligne's bound provides the crucial square-root cancellation "
                 "for the hardest terms."
        ):
            self.play(FadeIn(content), Create(rect), run_time=2.0)

        self.wait(1.0)

        with self.voiceover(
            text=get_phonetic_text("And the result is that the distribution level exceeds one-half "
                 "by a tiny but positive amount. "
                 "This is enough to make the G P Y sum positive, "
                 "which guarantees that some pair of shifts "
                 "is prime infinitely often."),
            subcaption="And the result is that the distribution level exceeds one-half "
                 "by a tiny but positive amount. "
                 "This is enough to make the G P Y sum positive, "
                 "which guarantees that some pair of shifts "
                 "is prime infinitely often."
        ):
            self.play(FadeIn(pieces), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("The bound he obtained was seventy million. "
                 "This was the first time anyone proved "
                 "that prime gaps are bounded by any finite number."),
            subcaption="The bound he obtained was seventy million. "
                 "This was the first time anyone proved "
                 "that prime gaps are bounded by any finite number."
        ):
            self.play(
                rect.animate.set_stroke(YELLOW, width=6),
                run_time=0.5,
            )
            self.play(
                rect.animate.set_stroke(GREEN, width=4),
                run_time=0.5,
            )
            self.play(FadeIn(sub_note), run_time=1.0)

        self.wait(1.5)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 15a: Conclusion — Polymath and Maynard
    # ------------------------------------------------------------------
    def conclusion_part1(self):
        header = Tex(
            r"\textbf{Aftermath}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        poly = MathTex(
            r"\text{Polymath8} \rightarrow \text{Bound } 4,\!680",
            font_size=28,
        )
        may = MathTex(
            r"\text{Maynard (2013)} \rightarrow \text{Bound } 246",
            font_size=28,
        )

        items = VGroup(poly, may)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        items.next_to(header, DOWN, buff=0.5)
        items.set_x(0)

        # Timeline visualization
        timeline_header = Tex(r"\textbf{Bound over time:}", font_size=24, color=TEAL)
        timeline_header.to_edge(DOWN, buff=1.5)

        bounds = [
            (r"Zhang 2014", 70000000),
            (r"Polymath8", 4680),
            (r"Maynard", 246),
        ]
        timeline_bars = VGroup()
        for i, (label, bound) in enumerate(bounds):
            height = 0.3 + 2.0 * (1 - (bound ** (1/8)) / (70000000 ** (1/8)))
            bar = Rectangle(
                height=max(0.3, height), width=0.6,
                fill_color=BLUE, fill_opacity=0.6, stroke_width=1,
            )
            lbl = Tex(label, font_size=14)
            lbl.next_to(bar, DOWN, buff=0.1)
            val = Tex(str(bound), font_size=12)
            val.next_to(bar, UP, buff=0.1)
            timeline_bars.add(VGroup(bar, lbl, val))

        timeline_bars.arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        timeline_bars.next_to(timeline_header, UP, buff=0.2)
        timeline_bars.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("Zhang's result sparked an explosion of activity. "
                 "The Polymath project, a collaborative online effort, "
                 "quickly improved the bound from seventy million "
                 "down to four thousand six hundred eighty."),
            subcaption="Zhang's result sparked an explosion of activity. "
                 "The Polymath project, a collaborative online effort, "
                 "quickly improved the bound from seventy million "
                 "down to four thousand six hundred eighty."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(poly, shift=RIGHT * 0.3), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("Then James Maynard, working independently, "
                 "introduced a new sieve method "
                 "that brought the bound down to six hundred, "
                 "and later to two hundred forty-six "
                 "when combined with Zhang's ideas."),
            subcaption="Then James Maynard, working independently, "
                 "introduced a new sieve method "
                 "that brought the bound down to six hundred, "
                 "and later to two hundred forty-six "
                 "when combined with Zhang's ideas."
        ):
            self.play(FadeIn(may, shift=RIGHT * 0.3), run_time=2.0)
            self.play(FadeIn(timeline_header), run_time=0.8)
            for bar_group in timeline_bars:
                self.play(FadeIn(bar_group), run_time=0.5)

        self.wait(1.0)
        clear_screen(self)

    # ------------------------------------------------------------------
    # Scene 15b: Conclusion — GEH and open problem
    # ------------------------------------------------------------------
    def conclusion_part2(self):
        header = Tex(
            r"\textbf{Aftermath}",
            font_size=32,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        eh = MathTex(
            r"\text{Under GEH: Bound } 6",
            font_size=26,
            color=TEAL,
        )
        twin = MathTex(
            r"\text{Open: } \liminf (p_{n+1} - p_n) = 2",
            font_size=30,
            color=YELLOW,
        )

        items = VGroup(eh, twin)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.next_to(header, DOWN, buff=0.5)
        items.set_x(0)

        with self.voiceover(
            text=get_phonetic_text("The current record is two hundred forty-six. "
                 "Assuming the generalized Elliott Halberstam conjecture, "
                 "it can be reduced to six."),
            subcaption="The current record is two hundred forty-six. "
                 "Assuming the generalized Elliott Halberstam conjecture, "
                 "it can be reduced to six."
        ):
            self.play(Write(header), run_time=1.0)
            self.play(FadeIn(eh, shift=RIGHT * 0.3), run_time=1.5)

        self.wait(0.5)

        with self.voiceover(
            text=get_phonetic_text("But the original Twin Prime Conjecture, "
                 "which claims the bound is exactly two, "
                 "remains wide open."),
            subcaption="But the original Twin Prime Conjecture, "
                 "which claims the bound is exactly two, "
                 "remains wide open."
        ):
            self.play(FadeIn(twin, shift=RIGHT * 0.3), run_time=1.5)

        self.wait(1.5)
        clear_screen(self)
