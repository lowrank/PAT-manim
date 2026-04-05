"""
The Sensitivity Conjecture: A 30-Year Problem Solved in 2 Pages
Hao Huang's 2019 proof using spectral methods

Based on: "Induced subgraphs of hypercubes and a proof of the Sensitivity Conjecture"
Annals of Mathematics (2019)
"""

from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
from latent_utils import (
    LatentPrelude,
    make_content_group,
    make_theorem_card,
    center_mathtex,
    clear_screen,
    SEMINAR_BLUE,
)


# ═══════════════════════════════════════════════════════════════════════════
# Main Scene
# ═══════════════════════════════════════════════════════════════════════════

class SensitivityConjectureScene(LatentPrelude, VoiceoverScene):
    def construct(self):
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))
        self.play_prelude()

        # ═══════════════════════════════════════════════════════════════════
        # Scene 1: Title Card
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{The Sensitivity Conjecture}",
            font_size=44,
            color=BLUE,
        ).to_edge(UP, buff=0.5)

        # Load researcher photos
        import os
        _proj = os.path.dirname(os.path.abspath(__file__))

        nisan_photo = ImageMobject(os.path.join(_proj, "nisan.jpg"))
        nisan_photo.set(height=1.5)
        nisan_label = Tex(r"Noam Nisan", font_size=22, color=GREY_B)

        szegedy_photo = ImageMobject(os.path.join(_proj, "szegedy.jpg"))
        szegedy_photo.set(height=1.5)
        szegedy_label = Tex(r"Mario Szegedy", font_size=22, color=GREY_B)

        # Arrange photos side by side (use Group, not VGroup, for ImageMobject)
        nisan_group = Group(nisan_photo, nisan_label).arrange(DOWN, buff=0.12)
        szegedy_group = Group(szegedy_photo, szegedy_label).arrange(DOWN, buff=0.12)
        photo_pair = Group(nisan_group, szegedy_group).arrange(RIGHT, buff=0.8)

        contribution = Tex(
            r"Posed the Sensitivity Conjecture (1992)",
            font_size=22, color=YELLOW,
        )

        photo_block = Group(photo_pair, contribution).arrange(DOWN, buff=0.25)
        photo_block.next_to(title, DOWN, buff=0.5)

        with self.voiceover(
            text="The Sensitivity Conjecture, proposed in 1992 by Nisan and Szegedy, "
                 "stood as one of the most intriguing open problems in theoretical computer science "
                 "for nearly 30 years."
        ):
            self.play(Write(title))
            self.wait(1)
            self.play(FadeIn(nisan_group), FadeIn(szegedy_group))
            self.wait(1)
            self.play(FadeIn(contribution))
            self.wait(2)

        # Fade out photos before showing Huang's info
        self.play(FadeOut(photo_block))
        self.wait(0.5)

        subtitle = Tex(
            r"A 30-Year Problem Solved in 2 Pages",
            font_size=32,
            color=TEAL,
        )

        # Load Huang photo and place it next to his name
        huang_photo = ImageMobject(os.path.join(_proj, "huang.jpg"))
        huang_photo.set(height=1.5)

        author = Tex(
            r"Hao Huang, Emory University (now NUS)",
            font_size=28,
            color=GREY_B,
        )
        # Group photo with author name so they appear together
        huang_group = Group(huang_photo, author).arrange(RIGHT, buff=0.3)
        huang_group.set_x(0)

        journal = Tex(
            r"\textit{Annals of Mathematics}, 2019",
            font_size=28,
            color=GOLD,
        )

        subtitle.next_to(title, DOWN, buff=0.6)
        huang_group.next_to(subtitle, DOWN, buff=0.5)
        journal.next_to(huang_group, DOWN, buff=0.4)

        with self.voiceover(
            text="In 2019, Hao Huang, then at Emory University and now at the "
                 "National University of Singapore, published an elegant 2-page proof "
                 "in the Annals of Mathematics."
        ):
            self.play(FadeIn(subtitle), FadeIn(huang_photo))
            self.wait(1)
            self.play(FadeIn(author))
            self.wait(0.5)
            self.play(FadeIn(journal))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 1b: Historical Timeline
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Historical Timeline}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        timeline = [
            (r"\textbf{1988}", r"Chung--F\"uredi--Graham--Seymour: degree $\ge (1/2 - o(1))\log_2 n$"),
            (r"\textbf{1992}", r"Nisan--Szegedy: Sensitivity Conjecture posed"),
            (r"\textbf{1992}", r"Gotsman--Linial: equivalence to hypercube problem"),
            (r"\textbf{2013}", r"Tal: $bs(f) \le \deg(f)^2$"),
            (r"\textbf{2019}", r"Huang: $\Delta(H) \ge \sqrt{n}$ \quad $\longrightarrow$ \quad Conjecture solved!"),
        ]

        items = VGroup()
        for year_str, desc_str in timeline:
            item = Tex(
                year_str + r" \quad " + desc_str,
                font_size=28,
            )
            items.add(item)

        # Color the last item green
        items[-1].set_color(GREEN)

        content = make_content_group(
            *items,
            reference=title,
            buff_between=0.35,
            buff_below=0.6,
        )

        with self.voiceover(
            text="Here's a brief timeline. In 1988, Chung, Furedi, Graham, and Seymour "
                 "proved a logarithmic lower bound on induced subgraph degree. "
                 "In 1992, Nisan and Szegedy posed the Sensitivity Conjecture, "
                 "and Gotsman and Linial proved it equivalent to a hypercube problem."
        ):
            for item in items[:3]:
                self.play(FadeIn(item))
                self.wait(1)
            self.wait(1.5)

        with self.voiceover(
            text="In 2013, Tal improved the degree-block sensitivity bound. "
                 "And finally in 2019, Huang's breakthrough resolved everything."
        ):
            self.play(FadeIn(items[3]))
            self.wait(1)
            self.play(FadeIn(items[4]))
            self.wait(1.5)
            self.play(Indicate(items[4], color=GREEN))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 2: Preliminaries — Graph Terminology
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Preliminaries: Graph Terminology}",
            font_size=40,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        def1 = Tex(
            r"$\bullet$ \textbf{Graph} $G = (V, E)$: a set of vertices $V$ and edges $E$",
            font_size=28,
        )

        def2 = Tex(
            r"$\bullet$ \textbf{Degree} $\deg(v)$: number of edges touching vertex $v$",
            font_size=28,
        )

        def3 = Tex(
            r"$\bullet$ \textbf{Maximum degree} $\Delta(G) = \max_{v} \deg(v)$",
            font_size=28,
        )

        def4 = Tex(
            r"$\bullet$ \textbf{Adjacency matrix:} $W_{u,v} = 1$ if $\{u,v\} \in E$, else $0$",
            font_size=28,
        )

        content = make_content_group(
            def1, def2, def3, def4,
            reference=title,
            buff_between=0.4,
            buff_below=0.6,
        )

        with self.voiceover(
            text="Let's start with some graph theory basics. "
                 "A graph has vertices and edges. "
                 "The degree of a vertex counts its edges. "
                 "The maximum degree, delta of G, is the largest degree over all vertices."
        ):
            self.play(FadeIn(def1))
            self.wait(1)
            self.play(FadeIn(def2))
            self.wait(1)
            self.play(FadeIn(def3))
            self.wait(2.5)

        self.wait(2)

        with self.voiceover(
            text="We can encode a graph as an adjacency matrix. "
                 "The entry W u v is 1 if u and v are connected by an edge, "
                 "and 0 otherwise. This matrix is symmetric, with zeros on the diagonal."
        ):
            self.play(FadeIn(def4))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ─────────────────────────────────────────────────────────────────
        # Scene 2b: Induced Subgraph + Principal Submatrix
        # ─────────────────────────────────────────────────────────────────

        title = Tex(
            r"\textbf{Induced Subgraph \& Principal Submatrix}",
            font_size=40,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        induced_def = Tex(
            r"$\bullet$ \textbf{Induced subgraph} $H$ of $G$: pick a subset $S \subseteq V$, \\",
            r"  keep \textit{all} edges of $G$ between vertices in $S$",
            font_size=28,
            tex_environment="flushleft",
        )

        principal_def = Tex(
            r"$\bullet$ \textbf{Principal submatrix:} delete the \textit{same} rows and columns \\",
            r"  from a matrix $W$ (keeps the adjacency structure of the subgraph)",
            font_size=28,
            tex_environment="flushleft",
        )

        key_point = Tex(
            r"\textbf{Key link:} The adjacency matrix of an induced subgraph \\",
            r"is exactly a principal submatrix of $G$'s adjacency matrix!",
            font_size=28,
            color=TEAL,
            tex_environment="flushleft",
        )

        content = make_content_group(
            induced_def, principal_def, key_point,
            reference=title,
            buff_between=0.5,
            buff_below=0.6,
        )

        with self.voiceover(
            text="An induced subgraph is formed by picking a subset of vertices "
                 "and keeping all original edges between them. "
                 "On the matrix side, this corresponds to a principal submatrix: "
                 "deleting the same rows and columns."
        ):
            self.play(FadeIn(induced_def))
            self.wait(1.5)
            self.play(FadeIn(principal_def))
            self.wait(2)

        self.wait(2)

        with self.voiceover(
            text="The key link: the adjacency matrix of an induced subgraph "
                 "is exactly a principal submatrix of the full adjacency matrix. "
                 "This connection is at the heart of Huang's proof."
        ):
            self.play(FadeIn(key_point))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 3: The Hypercube Graph
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{The Hypercube Graph $Q^n$}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        definition_header = Tex(
            r"\textbf{Definition:}",
            font_size=32,
            color=TEAL,
        )

        definition_text = Tex(
            r"$\bullet$ Vertices: all binary strings in $\{0,1\}^n$ \quad ($2^n$ vertices) \\",
            r"$\bullet$ Edges: connect strings differing in exactly 1 bit \quad (degree $= n$)",
            font_size=30,
            tex_environment="flushleft",
        )

        content = make_content_group(
            definition_header,
            definition_text,
            reference=title,
            buff_between=0.4,
            buff_below=0.6,
        )

        with self.voiceover(
            text="The hypercube graph Q to the n has a beautiful structure. "
                 "Its vertices are all binary strings of length n, giving 2 to the n vertices. "
                 "Two vertices share an edge if they differ in exactly one bit, "
                 "so every vertex has degree n."
        ):
            self.play(FadeIn(definition_header))
            self.wait(1)
            self.play(FadeIn(definition_text))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ─────────────────────────────────────────────────────────────────
        # Scene 3b: Q^3 Example — Proper 3D Cube
        # ─────────────────────────────────────────────────────────────────

        title = Tex(
            r"\textbf{Example: $Q^3$ (The 3-Dimensional Cube)}",
            font_size=38,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 3D cube layout: front face + back face with perspective offset
        s = 1.3    # half-side of front face
        dx = 0.7   # back-face offset right
        dy = 0.5   # back-face offset up

        # Front face (z=0): 000, 010, 110, 100  (bottom-left CW)
        # Back face  (z=1): 001, 011, 111, 101
        vertex_data = {
            "000": np.array([-s, -s, 0]),
            "010": np.array([-s,  s, 0]),
            "110": np.array([ s,  s, 0]),
            "100": np.array([ s, -s, 0]),
            "001": np.array([-s + dx, -s + dy, 0]),
            "011": np.array([-s + dx,  s + dy, 0]),
            "111": np.array([ s + dx,  s + dy, 0]),
            "101": np.array([ s + dx, -s + dy, 0]),
        }

        # Label placement direction for each vertex
        label_dirs = {
            "000": DOWN + LEFT,
            "010": UP + LEFT,
            "110": UP + LEFT * 0.3,
            "100": DOWN + RIGHT * 0.3,
            "001": DOWN + LEFT * 0.3,
            "011": UP + LEFT * 0.3,
            "111": UP + RIGHT,
            "101": DOWN + RIGHT,
        }

        edge_pairs = [
            # Front face
            ("000", "010"), ("010", "110"), ("110", "100"), ("100", "000"),
            # Back face
            ("001", "011"), ("011", "111"), ("111", "101"), ("101", "001"),
            # Connecting edges (depth)
            ("000", "001"), ("010", "011"), ("110", "111"), ("100", "101"),
        ]

        # Build edges
        edges = VGroup()
        for v1, v2 in edge_pairs:
            edge = Line(
                vertex_data[v1], vertex_data[v2],
                stroke_width=2, color=GREY_B,
            )
            edges.add(edge)

        # Position the whole graph, THEN add dots and labels
        edges.scale(1.0).move_to(ORIGIN + DOWN * 0.3)

        # Create dots and labels AFTER positioning
        vertices = VGroup()
        vertex_labels = VGroup()
        for label_str, _ in vertex_data.items():
            pos = self._get_vertex_pos(edges, edge_pairs, list(vertex_data.keys()), label_str)
            dot = Dot(pos, color=BLUE, radius=0.09)
            lbl = Tex(
                r"\texttt{" + label_str + "}",
                font_size=22,
            ).next_to(dot, label_dirs[label_str], buff=0.12)
            vertices.add(dot)
            vertex_labels.add(lbl)

        properties = Tex(
            r"$|V| = 8$, \quad $|E| = 12$, \quad $\Delta = 3$",
            font_size=28,
            color=GREY_B,
        )
        properties.next_to(VGroup(edges, vertices), DOWN, buff=0.6)

        with self.voiceover(
            text="For example, Q 3 is the familiar 3-dimensional cube. "
                 "It has 8 vertices labeled by 3-bit binary strings, "
                 "12 edges, and every vertex has degree 3."
        ):
            self.play(Create(edges))
            self.wait(0.5)
            self.play(FadeIn(vertices), FadeIn(vertex_labels))
            self.wait(1.5)
            self.play(FadeIn(properties))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 4: The Induced Subgraph Problem
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{The Induced Subgraph Problem}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        question = Tex(
            r"\textbf{Question:} How large can an induced subgraph of $Q^n$ be \\",
            r"while keeping its maximum degree $\Delta(H)$ small?",
            font_size=30,
            color=YELLOW,
            tex_environment="flushleft",
        )

        background = Tex(
            r"Chung--F\"uredi--Graham--Seymour (1988): \\",
            r"If $|V(H)| > 2^{n-1}$, then $\Delta(H) \ge (1/2 - o(1)) \log_2 n$",
            font_size=28,
            color=GREY_B,
            tex_environment="flushleft",
        )

        content = make_content_group(
            question,
            background,
            reference=title,
            buff_between=0.6,
            buff_below=0.7,
        )

        with self.voiceover(
            text="Here is the central question. If you pick more than half the vertices of the hypercube "
                 "and keep all edges between them, how large must the maximum degree be? "
                 "In 1988, Chung and coauthors proved a logarithmic lower bound."
        ):
            self.play(FadeIn(question))
            self.wait(1.5)
            self.play(FadeIn(background))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ─────────────────────────────────────────────────────────────────
        # Scene 4b: Huang's Main Theorem
        # ─────────────────────────────────────────────────────────────────

        title = Tex(
            r"\textbf{Huang's Breakthrough (2019)}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        thm_line1 = Tex(
            r"For every $(2^{n-1}+1)$-vertex induced subgraph $H$ of $Q^n$:",
            font_size=30,
        )
        thm_eq = MathTex(
            r"\Delta(H) \ge \sqrt{n}",
            font_size=42,
            color=GREEN,
        )

        card, rect, _ = make_theorem_card(thm_line1, thm_eq, color=GREEN, buff=0.4)
        card.next_to(title, DOWN, buff=0.8)

        with self.voiceover(
            text="Huang proved a dramatically stronger result: "
                 "every induced subgraph with 2 to the n minus 1 plus 1 vertices "
                 "has maximum degree at least square root of n. This is tight!"
        ):
            self.play(FadeIn(thm_line1), Write(thm_eq), Create(rect))
            self.wait(1.5)
            self.play(Circumscribe(card, color=GREEN, time_width=2))
            self.wait(3)

        insight = Tex(
            r"\textbf{Key insight:} The $2^{n-1}$ even-parity vertices form an independent set. \\",
            r"Adding just 1 more vertex forces $\Delta \ge \sqrt{n}$!",
            font_size=28,
            color=YELLOW,
            tex_environment="flushleft",
        )
        insight.next_to(card, DOWN, buff=0.7)

        with self.voiceover(
            text="The 2 to the n minus 1 even-parity vertices have no edges between them. "
                 "But adding just one more vertex forces the maximum degree "
                 "to jump to at least square root n."
        ):
            self.play(FadeIn(insight))
            self.wait(3)

        # Tightness: Chung et al. construction
        tightness = Tex(
            r"\textbf{Tight!} Chung--F\"uredi--Graham--Seymour, \\",
            r"\textit{On induced subgraphs of the cube}, \\",
            r"J.\ Comb.\ Theory, Ser.\ A, \textbf{49}(1), 1988, 180--187: \\",
            r"constructed a $(2^{n-1}+1)$-vertex induced subgraph with $\Delta = \lceil\sqrt{n}\,\rceil$.",
            font_size=26,
            color=GREY_B,
            tex_environment="flushleft",
        )
        tightness.next_to(insight, DOWN, buff=0.5)

        with self.voiceover(
            text="And this bound is tight! Back in 1988, Chung, Furedi, Graham, and Seymour "
                 "already constructed an induced subgraph with 2 to the n minus 1 plus 1 vertices "
                 "whose maximum degree is exactly the ceiling of square root n."
        ):
            self.play(FadeIn(tightness))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 5: Proof Roadmap (2 x 2 Grid)
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Proof Roadmap}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        step_colors = [BLUE, TEAL, GOLD, GREEN]
        step_labels = [
            r"\textbf{Step 1: Construct $M_n$}",
            r"\textbf{Step 2: Compute Spectrum}",
            r"\textbf{Step 3: Cauchy Interlacing}",
            r"\textbf{Step 4: Degree Bound}",
        ]
        step_descs = [
            r"Recursive signed adjacency \\ matrix with entries in $\{-1,0,1\}$",
            r"$M_n^2 = nI$ \\ $\Rightarrow$ spectrum is $\pm\sqrt{n}$",
            r"Submatrix inherits \\ large spectral value $\ge \sqrt{n}$",
            r"$\Delta(H) \ge \lambda_1(M_H)$ \\ $\ge \sqrt{n}$ \quad Done!",
        ]

        cards = VGroup()
        for i, (color, label, desc) in enumerate(zip(step_colors, step_labels, step_descs)):
            box = RoundedRectangle(
                width=5.0,
                height=1.6,
                corner_radius=0.15,
                color=color,
                stroke_width=2.5,
                fill_color=color,
                fill_opacity=0.08,
            )
            label_tex = Tex(label, font_size=26, color=color)
            desc_tex = Tex(desc, font_size=24, color=GREY_B, tex_environment="flushleft")
            inner = VGroup(label_tex, desc_tex).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            inner.move_to(box.get_center())
            card_group = VGroup(box, inner)
            cards.add(card_group)

        # Arrange as 2x2 grid
        top_row = VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.5)
        bot_row = VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.5)
        grid = VGroup(top_row, bot_row).arrange(DOWN, buff=0.4)
        grid.next_to(title, DOWN, buff=0.6)
        grid.set_x(0)

        with self.voiceover(
            text="Before diving in, here's the roadmap. "
                 "Step one: construct a special recursive matrix M n. "
                 "Step two: show its spectrum is plus or minus square root n."
        ):
            self.play(FadeIn(cards[0], shift=RIGHT * 0.3))
            self.wait(1)
            self.play(FadeIn(cards[1], shift=RIGHT * 0.3))
            self.wait(2)

        with self.voiceover(
            text="Step three: apply Cauchy interlacing to any large submatrix. "
                 "Step four: connect spectral values to maximum degree. That's the whole proof!"
        ):
            self.play(FadeIn(cards[2], shift=RIGHT * 0.3))
            self.wait(1)
            self.play(FadeIn(cards[3], shift=RIGHT * 0.3))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 6: Boolean Function Sensitivity — Accessible Explanation
        # ═══════════════════════════════════════════════════════════════════

        # Transition: explain why we're discussing sensitivity now
        transition = Tex(
            r"But wait --- why is this hypercube problem called \\",
            r"the \textbf{Sensitivity} Conjecture?",
            font_size=34,
            color=TEAL,
            tex_environment="flushleft",
        )
        transition.move_to(ORIGIN)

        with self.voiceover(
            text="But wait. We've seen the proof roadmap for a hypercube problem. "
                 "Why is it called the Sensitivity Conjecture? "
                 "Let's step back and understand the connection to boolean functions."
        ):
            self.play(FadeIn(transition))
            self.wait(3)

        clear_screen(self)

        title = Tex(
            r"\textbf{Boolean Sensitivity: What Is It?}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        intro = Tex(
            r"A \textbf{boolean function} $f: \{0,1\}^n \to \{0,1\}$ takes a binary string and returns 0 or 1.",
            font_size=28,
        )

        example_label = Tex(
            r"\textbf{Example:} The OR function on 3 bits, $f = \mathrm{OR}_3$",
            font_size=28,
            color=YELLOW,
        )

        example_table = MathTex(
            r"f(0,0,0) = 0, \quad f(1,0,0) = 1, \quad f(0,1,0) = 1, \quad \ldots",
            font_size=28,
        )

        sens_def = Tex(
            r"\textbf{Definition.} Let $x^{(i)}$ denote $x$ with the $i$-th bit flipped. The \textbf{sensitivity} of $f$ at $x$ is",
            font_size=28,
            tex_environment="flushleft",
        )

        sens_formula = MathTex(
            r"s(f,\, x) \;=\; \bigl|\{\, i \in [n] : f(x) \neq f(x^{(i)}) \,\}\bigr|.",
            font_size=34,
            color=TEAL,
        )

        sens_explain = Tex(
            r"\textbf{Example at $x = (0,0,0)$:} flip each bit one at a time --- \\",
            r"$(1,0,0) \to f=1$, \; $(0,1,0) \to f=1$, \; $(0,0,1) \to f=1$. \\",
            r"All 3 flips change the output, so $s(f, x) = 3$.",
            font_size=28,
            tex_environment="flushleft",
        )

        content = make_content_group(
            intro, example_label, example_table, sens_def, sens_formula, sens_explain,
            reference=title,
            buff_between=0.35,
            buff_below=0.45,
        )

        with self.voiceover(
            text="A boolean function takes a binary string and outputs 0 or 1. "
                 "For example, the OR function on 3 bits returns 1 "
                 "if any input bit is 1, and 0 only when all bits are 0."
        ):
            self.play(FadeIn(intro))
            self.wait(1)
            self.play(FadeIn(example_label))
            self.wait(0.5)
            self.play(FadeIn(example_table))
            self.wait(2)

        self.wait(2)

        with self.voiceover(
            text="Now let's define sensitivity precisely. "
                 "Write x with a superscript in parentheses i, "
                 "for the string obtained from x by flipping bit i. "
                 "The sensitivity of f at input x counts how many coordinates "
                 "have the property that flipping that single bit changes the output of f."
        ):
            self.play(FadeIn(sens_def))
            self.wait(1)
            self.play(Write(sens_formula))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="Let's see this in action. "
                 "At x equals 0 0 0, the OR function outputs 0. "
                 "Flip the first bit: we get 1 0 0, and the output becomes 1. That's a change. "
                 "Flip the second bit: 0 1 0, output is 1. Another change. "
                 "Flip the third bit: 0 0 1, output is 1. Again a change. "
                 "All 3 flips change the output, so the sensitivity at this input is 3."
        ):
            self.play(FadeIn(sens_explain))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ─────────────────────────────────────────────────────────────────
        # Scene 6b: Sensitivity vs Block Sensitivity
        # ─────────────────────────────────────────────────────────────────

        title = Tex(
            r"\textbf{Sensitivity vs.\ Block Sensitivity}",
            font_size=40,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        sensitivity_formal = Tex(
            r"\textbf{Sensitivity} $s(f) = \max_x s(f, x)$: \\",
            r"max over all inputs of single-bit flips that change $f$",
            font_size=28,
            tex_environment="flushleft",
        )

        block_formal = Tex(
            r"\textbf{Block sensitivity} $bs(f) = \max_x bs(f, x)$: \\",
            r"same, but flip disjoint \textit{blocks} of bits at once. \\",
            r"Always $bs(f) \ge s(f)$ (single bits are blocks of size 1).",
            font_size=28,
            tex_environment="flushleft",
        )

        gap_note = Tex(
            r"\textbf{The gap can be huge:} there exist functions where \\",
            r"$bs(f) = \tfrac{2}{3} s(f)^2$, a quadratic separation!",
            font_size=28,
            color=YELLOW,
            tex_environment="flushleft",
        )

        deg_def = Tex(
            r"\textbf{Polynomial degree} $\deg(f)$: every $f:\{0,1\}^n\!\to\!\{0,1\}$ \\",
            r"can be written as a unique multilinear polynomial over $\mathbb{R}$; \\",
            r"$\deg(f)$ is the degree of that polynomial.",
            font_size=28,
            tex_environment="flushleft",
        )

        content = make_content_group(
            sensitivity_formal, block_formal, deg_def, gap_note,
            reference=title,
            buff_between=0.5,
            buff_below=0.6,
        )

        with self.voiceover(
            text="The sensitivity of the entire function f is the maximum of s of f x, "
                 "taken over all possible inputs x. "
                 "It captures the worst-case fragility of f to a single-bit change."
        ):
            self.play(FadeIn(sensitivity_formal))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="Block sensitivity generalizes this idea. "
                 "Instead of flipping one bit at a time, you can flip entire disjoint blocks of bits simultaneously. "
                 "Since a single bit is just a block of size 1, "
                 "block sensitivity is always at least as large as sensitivity."
        ):
            self.play(FadeIn(block_formal))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="One more measure: the polynomial degree of f. "
                 "Every boolean function can be uniquely written as a multilinear polynomial over the reals, "
                 "and degree of f is the degree of that polynomial."
        ):
            self.play(FadeIn(deg_def))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="The gap between sensitivity and block sensitivity can be surprisingly large. "
                 "Rubinstein constructed functions "
                 "where block sensitivity is quadratically larger than sensitivity. "
                 "The big question is: can the gap be even worse than quadratic?"
        ):
            self.play(FadeIn(gap_note))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 7: Gotsman-Linial Connection
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{The Sensitivity Conjecture}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        conjecture = Tex(
            r"\textbf{Conjecture (Nisan--Szegedy, 1992):} \\",
            r"$bs(f) \le s(f)^C$ for some absolute constant $C$.",
            font_size=30,
            color=YELLOW,
            tex_environment="flushleft",
        )

        connection = Tex(
            r"\textbf{Gotsman--Linial (1992):} This conjecture is \textit{equivalent} \\",
            r"to the hypercube induced subgraph problem! \\",
            r"Proving $\Delta(H) \ge h(n)$ implies $s(f) \ge h(\deg(f))$.",
            font_size=28,
            color=TEAL,
            tex_environment="flushleft",
        )

        therefore = Tex(
            r"$\Rightarrow$ Huang's $\Delta(H) \ge \sqrt{n}$ directly gives $s(f) \ge \sqrt{\deg(f)}$.",
            font_size=28,
            color=GREEN,
        )

        content = make_content_group(
            conjecture, connection, therefore,
            reference=title,
            buff_between=0.6,
            buff_below=0.6,
        )

        with self.voiceover(
            text="The Sensitivity Conjecture asks whether block sensitivity is polynomially bounded by sensitivity. "
                 "Gotsman and Linial proved a remarkable equivalence: "
                 "this is the same as the hypercube induced subgraph problem."
        ):
            self.play(FadeIn(conjecture))
            self.wait(1.5)
            self.play(FadeIn(connection))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="So Huang's degree bound immediately gives sensitivity at least square root of degree. "
                 "That's the key link to resolving the conjecture."
        ):
            self.play(FadeIn(therefore))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 8: The Proof — The Magic Matrix
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{The Proof: A Recursive Matrix $M_n$}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        intro = Tex(
            r"\textbf{Huang's key insight:} Construct a \textit{signed} adjacency matrix for $Q^n$.",
            font_size=30,
            color=TEAL,
        )

        signed_explain = Tex(
            r"A \textbf{signed adjacency matrix} is like an adjacency matrix, \\",
            r"but some $1$'s are replaced by $-1$'s. Entries lie in $\{-1,\, 0,\, 1\}$: \\",
            r"$W_{u,v} \neq 0$ only when $\{u,v\}$ is an edge, but the sign can vary.",
            font_size=28,
            tex_environment="flushleft",
        )

        a1_def = MathTex(
            r"M_1 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}",
            font_size=38,
        )

        recursive_def = MathTex(
            r"M_n = \begin{bmatrix} M_{n-1} & I \\ I & -M_{n-1} \end{bmatrix}",
            font_size=38,
        )

        content = make_content_group(
            intro,
            signed_explain,
            a1_def,
            recursive_def,
            reference=title,
            buff_between=0.45,
            buff_below=0.5,
        )

        with self.voiceover(
            text="Huang's proof starts with a brilliant construction: "
                 "a signed adjacency matrix for the hypercube."
        ):
            self.play(FadeIn(intro))
            self.wait(2)

        self.wait(2)

        with self.voiceover(
            text="What does signed mean? Recall that an adjacency matrix has a 1 wherever "
                 "two vertices share an edge. A signed adjacency matrix is the same, "
                 "except some of those 1's are replaced by minus 1's. "
                 "The key rule is: the entry is nonzero only when there is an edge, "
                 "but the sign can be positive or negative."
        ):
            self.play(FadeIn(signed_explain))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="Here is Huang's recursive construction. "
                 "M 1 is a simple 2 by 2 matrix with 0 on the diagonal and 1 off-diagonal. "
                 "M n is built recursively: upper left is M n minus 1, "
                 "upper right and lower left are identity, and lower right is negative M n minus 1."
        ):
            self.play(Write(a1_def))
            self.wait(1.5)
            self.play(Write(recursive_def))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ─────────────────────────────────────────────────────────────────
        # Scene 8b: M_2 Example
        # ─────────────────────────────────────────────────────────────────

        title = Tex(
            r"\textbf{Example: $M_2$}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        m2_construction = MathTex(
            r"M_2 = \begin{bmatrix} M_1 & I \\ I & -M_1 \end{bmatrix} "
            r"= \begin{bmatrix} 0 & 1 & 1 & 0 \\ 1 & 0 & 0 & 1 \\ 1 & 0 & 0 & -1 \\ 0 & 1 & -1 & 0 \end{bmatrix}",
            font_size=32,
        )
        m2_construction.next_to(title, DOWN, buff=0.8)

        note = Tex(
            r"Entries are in $\{-1, 0, 1\}$ --- replacing each $-1$ with $1$ gives the adjacency matrix of $Q^2$",
            font_size=26,
            color=GREY_B,
        )
        note.next_to(m2_construction, DOWN, buff=0.6)

        with self.voiceover(
            text="For example, M 2 is this 4 by 4 matrix with entries in minus 1, 0, and 1. "
                 "Notice that replacing every minus 1 with plus 1 gives exactly "
                 "the adjacency matrix of Q 2."
        ):
            self.play(Write(m2_construction))
            self.wait(1.5)
            self.play(FadeIn(note))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 9: The Magic Property
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{The Magic Property: $M_n^2 = nI$}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        magic_property = MathTex(
            r"M_n^2 = n I",
            font_size=48,
            color=GREEN,
        )

        card_magic, rect_magic, _ = make_theorem_card(magic_property, color=GREEN, buff=0.4)
        card_magic.next_to(title, DOWN, buff=0.8)

        with self.voiceover(
            text="Here is the magic property: M n squared equals n times the identity matrix!"
        ):
            self.play(FadeIn(magic_property), Create(rect_magic))
            self.wait(1.5)
            self.play(Circumscribe(card_magic, color=GREEN, time_width=2))
            self.wait(2)

        self.wait(2)

        proof_header = Tex(
            r"\textbf{Proof by induction:}",
            font_size=30,
            color=TEAL,
        )
        proof_header.next_to(card_magic, DOWN, buff=0.6)

        proof_calc = MathTex(
            r"M_n^2 &= \begin{bmatrix} M_{n-1}^2 + I & 0 \\ 0 & M_{n-1}^2 + I \end{bmatrix} \\",
            r"&= \begin{bmatrix} (n-1)I + I & 0 \\ 0 & (n-1)I + I \end{bmatrix} \\",
            r"&= n I \quad \checkmark",
            font_size=32,
        )
        proof_calc.next_to(proof_header, DOWN, buff=0.4)

        with self.voiceover(
            text="The proof is a clean induction. Squaring M n using the block structure, "
                 "you get M n minus 1 squared plus I in each diagonal block. "
                 "By induction that's n minus 1 times I plus I, which equals n I."
        ):
            self.play(FadeIn(proof_header))
            self.wait(1)
            self.play(Write(proof_calc))
            self.wait(3.5)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 10: Spectral Consequence
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Spectral Consequence}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        spectral_result = MathTex(
            r"\text{Since } M_n^2 = n I, \text{ the spectrum is } \pm\sqrt{n}",
            font_size=36,
            color=TEAL,
        )

        multiplicity = MathTex(
            r"\text{Since } \operatorname{Tr}(M_n) = 0\text{:} \\",
            r"\sqrt{n} \text{ has multiplicity } 2^{n-1} \\",
            r"-\sqrt{n} \text{ has multiplicity } 2^{n-1}",
            font_size=32,
        )

        content = make_content_group(
            spectral_result,
            multiplicity,
            reference=title,
            buff_between=0.6,
            buff_below=0.8,
        )

        with self.voiceover(
            text="Since M n squared is n I, every value in the spectrum satisfies "
                 "lambda squared equals n. So the spectrum is plus or minus square root n."
        ):
            self.play(Write(spectral_result))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="Since the trace of M n is zero, exactly half are positive and half are negative. "
                 "Each appears with multiplicity 2 to the n minus 1."
        ):
            self.play(FadeIn(multiplicity))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 11: Cauchy's Interlace Theorem
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Cauchy's Interlace Theorem}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        cauchy_statement = Tex(
            r"Let $B$ be an $m \times m$ principal submatrix of an $n \times n$ symmetric matrix $W$. \\",
            r"If $\lambda_1 \ge \cdots \ge \lambda_n$ and $\mu_1 \ge \cdots \ge \mu_m$ are their spectra, then:",
            font_size=28,
            tex_environment="flushleft",
        )

        cauchy_eq = MathTex(
            r"\lambda_i \ge \mu_i \ge \lambda_{i+n-m} \quad \text{for all } 1 \le i \le m",
            font_size=36,
            color=GREEN,
        )

        cauchy_card, cauchy_rect, _ = make_theorem_card(cauchy_statement, cauchy_eq, color=TEAL, buff=0.3)
        cauchy_card.next_to(title, DOWN, buff=0.7)

        with self.voiceover(
            text="The next key tool is Cauchy's Interlace Theorem. "
                 "It says that the spectrum of a principal submatrix interlaces "
                 "the spectrum of the full matrix."
        ):
            self.play(FadeIn(cauchy_statement), Write(cauchy_eq), Create(cauchy_rect))
            self.wait(3)

        self.wait(2)

        # Application to our case
        note = Tex(
            r"\textbf{Our case:} $W = M_n$ ($2^n \times 2^n$), \; $B = M_H$ ($m = 2^{n-1}+1$) \\",
            r"$\Rightarrow \; \mu_1 \ge \lambda_{2^{n-1}}(M_n) = \sqrt{n}$",
            font_size=28,
            color=YELLOW,
            tex_environment="flushleft",
        )
        note.next_to(cauchy_card, DOWN, buff=0.6)

        with self.voiceover(
            text="In our case, W is M n with size 2 to the n, "
                 "and B has 2 to the n minus 1 plus 1 rows. "
                 "So the largest spectral value of B is at least square root n."
        ):
            self.play(FadeIn(note))
            self.wait(3.5)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 12: Eigenvector Lemma
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Connecting Spectrum and Degree}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        lemma = Tex(
            r"\textbf{Lemma:} If $W$ is a signed adjacency matrix (entries in $\{-1,0,1\}$) \\",
            r"with $W_{u,v} = 0$ for non-adjacent $u, v$ in graph $G$, then:",
            font_size=28,
            tex_environment="flushleft",
        )

        lemma_result = MathTex(
            r"\Delta(G) \ge \lambda_1(W)",
            font_size=38,
            color=GREEN,
        )

        proof_idea = Tex(
            r"\textbf{Proof:} Pick eigenvector entry $v_k$ with largest $|v_k|$. Then: \\",
            r"$|\lambda_1 v_k| = |(W\vec{v})_k| = \left|\sum_{j \sim k} W_{k,j} v_j\right|"
            r" \le \sum_{j \sim k} |v_k| \le \Delta(G) \, |v_k|$",
            font_size=26,
            tex_environment="flushleft",
        )

        content = make_content_group(
            lemma, lemma_result, proof_idea,
            reference=title,
            buff_between=0.5,
            buff_below=0.6,
        )

        with self.voiceover(
            text="The final piece connects the spectrum to maximum degree. "
                 "If W is a signed adjacency matrix, then the maximum degree "
                 "is at least the largest spectral value."
        ):
            self.play(FadeIn(lemma))
            self.wait(1.5)
            self.play(Write(lemma_result))
            self.wait(3)

        self.wait(2)

        with self.voiceover(
            text="The proof is short: pick the characteristic vector entry with the largest absolute value. "
                 "The left side gives lambda times that entry, "
                 "and the right side is bounded by the degree times that entry."
        ):
            self.play(FadeIn(proof_idea))
            self.wait(3.5)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 13: Proof Assembly
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Putting It All Together}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        step1 = Tex(r"1. $H$ = induced subgraph of $Q^n$ with $2^{n-1}+1$ vertices", font_size=30)
        step2 = Tex(r"2. $M_H$ = principal submatrix of $M_n$ (same rows/columns as $H$)", font_size=30)
        step3 = Tex(r"3. Cauchy Interlacing: $\lambda_1(M_H) \ge \lambda_{2^{n-1}}(M_n) = \sqrt{n}$", font_size=30, color=TEAL)
        step4 = Tex(r"4. Eigenvector Lemma: $\Delta(H) \ge \lambda_1(M_H)$", font_size=30, color=TEAL)

        conclusion_eq = MathTex(
            r"\therefore \quad \Delta(H) \ge \sqrt{n} \quad \checkmark",
            font_size=42,
            color=GREEN,
        )

        card_final, rect_final, _ = make_theorem_card(conclusion_eq, color=GREEN, buff=0.3)

        content = make_content_group(
            step1, step2, step3, step4, card_final,
            reference=title,
            buff_between=0.4,
            buff_below=0.6,
        )

        with self.voiceover(
            text="Now we assemble the proof. "
                 "Take H, an induced subgraph with 2 to the n minus 1 plus 1 vertices. "
                 "Let M H be the corresponding principal submatrix of M n."
        ):
            self.play(FadeIn(step1))
            self.wait(1)
            self.play(FadeIn(step2))
            self.wait(1.5)

        self.wait(1.5)

        with self.voiceover(
            text="By Cauchy interlacing, lambda 1 of M H is at least square root n. "
                 "By the previous lemma, delta of H is at least lambda 1 of M H. "
                 "Therefore, delta of H is at least square root n. Done!"
        ):
            self.play(FadeIn(step3))
            self.wait(1.5)
            self.play(FadeIn(step4))
            self.wait(1.5)
            self.play(FadeIn(conclusion_eq), Create(rect_final))
            self.wait(1.5)
            self.play(Circumscribe(card_final, color=GREEN, time_width=2))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 14: Sensitivity Conjecture Resolution
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Resolving the Sensitivity Conjecture}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        gotsman = MathTex(
            r"\text{Gotsman--Linial (1992): } s(f) \ge \sqrt{\deg(f)}",
            font_size=34,
        )

        tal = MathTex(
            r"\text{Tal (2013): } bs(f) \le \deg(f)^2",
            font_size=34,
        )

        combination = MathTex(
            r"\text{Combining:} \quad bs(f) \le \deg(f)^2 \le (s(f)^2)^2 = s(f)^4",
            font_size=34,
            color=GREEN,
        )

        content = make_content_group(
            gotsman, tal, combination,
            reference=title,
            buff_between=0.6,
            buff_below=0.8,
        )

        with self.voiceover(
            text="Finally, we resolve the Sensitivity Conjecture. "
                 "Huang's theorem via Gotsman-Linial gives sensitivity at least square root of degree. "
                 "Tal proved block sensitivity is at most degree squared."
        ):
            self.play(Write(gotsman))
            self.wait(1.5)
            self.play(Write(tal))
            self.wait(2)

        self.wait(2)

        with self.voiceover(
            text="Combining: block sensitivity is at most s to the fourth. "
                 "The 30-year conjecture is solved!"
        ):
            self.play(Write(combination))
            self.wait(1.5)
            self.play(Circumscribe(combination, color=GREEN, time_width=2))
            self.wait(3)

        celebration = Tex(
            r"\textbf{30-Year Conjecture SOLVED!}",
            font_size=38,
            color=GOLD,
        )
        celebration.next_to(combination, DOWN, buff=0.8)

        with self.voiceover(text="A truly remarkable achievement!"):
            self.play(FadeIn(celebration, scale=1.3))
            self.play(Flash(celebration.get_center(), color=GOLD, flash_radius=0.5))
            self.wait(3)

        self.wait(1.5)
        clear_screen(self)

        # ═══════════════════════════════════════════════════════════════════
        # Scene 15: Summary
        # ═══════════════════════════════════════════════════════════════════

        title = Tex(
            r"\textbf{Summary}",
            font_size=42,
            color=BLUE,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title))

        summary_header = Tex(
            r"\textbf{Huang's elegant proof uses three key ingredients:}",
            font_size=30,
            color=TEAL,
        )

        ingredient1 = Tex(
            r"$\bullet$ Recursive signed matrix $M_n$ with spectrum $\pm\sqrt{n}$",
            font_size=28,
        )

        ingredient2 = Tex(
            r"$\bullet$ Cauchy's Interlace Theorem for principal submatrices",
            font_size=28,
        )

        ingredient3 = Tex(
            r"$\bullet$ Eigenvector argument: $\Delta(H) \ge \lambda_1(M_H)$",
            font_size=28,
        )

        impact = Tex(
            r"\textbf{Impact:} Connects combinatorics, complexity theory, and linear algebra. \\",
            r"A masterpiece of mathematical elegance!",
            font_size=28,
            color=GOLD,
            tex_environment="flushleft",
        )

        content = make_content_group(
            summary_header,
            ingredient1,
            ingredient2,
            ingredient3,
            impact,
            reference=title,
            buff_between=0.4,
            buff_below=0.7,
        )

        with self.voiceover(
            text="To summarize: Huang's proof uses three simple ingredients. "
                 "A recursive matrix construction, Cauchy's interlacing theorem, "
                 "and a basic characteristic vector argument."
        ):
            self.play(FadeIn(summary_header))
            self.wait(1)
            self.play(FadeIn(ingredient1))
            self.wait(1)
            self.play(FadeIn(ingredient2))
            self.wait(1)
            self.play(FadeIn(ingredient3))
            self.wait(3)

        with self.voiceover(
            text="Together, they resolve a 30-year-old problem connecting combinatorics, "
                 "complexity theory, and linear algebra. Truly beautiful mathematics!"
        ):
            self.play(FadeIn(impact))
            self.wait(4)

        self.wait(2.5)
        clear_screen(self)

    # ─────────────────────────────────────────────────────────────────────
    # Helper: get vertex position from transformed edges
    # ─────────────────────────────────────────────────────────────────────

    def _get_vertex_pos(self, edges, edge_pairs, keys, target_label):
        """Find the actual position of a vertex after edges have been scaled/moved."""
        for i, (v1, v2) in enumerate(edge_pairs):
            if v1 == target_label:
                return edges[i].get_start()
            if v2 == target_label:
                return edges[i].get_end()
        return ORIGIN
