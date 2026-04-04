from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService

import numpy as np

class GCIDetailedProof(VoiceoverScene):
    def construct(self):
        # Initialize the text-to-speech service
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))

        # ---------------------------------------------------------
        # Helper System
        # ---------------------------------------------------------
        def clear_screen():
            """Safely clears all objects from the screen."""
            if self.mobjects:
                self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

        # ---------------------------------------------------------
        # 1. Title Sequence
        # ---------------------------------------------------------
        title = Tex(r"\textbf{Gaussian Correlation Inequality} (GCI)")
        subtitle = Tex(r"A Walkthrough of Royen's Proof")
        subtitle.next_to(title, DOWN)
        
        with self.voiceover(text="This video walks through Royen's proof for the Gaussian Correlation Inequality. This problem was famously open for decades until Thomas Royen solved it in 2014. We will step-by-step derive this famous result.") as tracker:
            self.play(Write(title))
            self.play(FadeIn(subtitle))
            
        clear_screen()
        self.wait(1.5)

         # ---------------------------------------------------------
        # 2. Statement of the Theorem & VISUALIZATION
        # ---------------------------------------------------------
        statement_text = Tex(r"For a centered Gaussian measure $\mu$ on $\mathbb{R}^d$ \\ and symmetric convex sets $K, L$:")
        gci_eq = MathTex(r"\mu(K \cap L) \geq \mu(K)\mu(L)")
        gci_eq.set_color(YELLOW).scale(1.2)
        
        text_group = VGroup(statement_text, gci_eq).arrange(DOWN, buff=0.7)
        
        with self.voiceover(text="The theorem states that for any centered Gaussian measure, knowing a point is inside a symmetric convex set K, will make it more likely to be in set L.") as tracker:
            self.play(Write(statement_text))
            self.play(FadeIn(gci_eq))

        # Animate the text moving to the left to make room
        self.play(text_group.animate.scale(0.85).to_edge(LEFT, buff=0.5))

        # --- Visual Animation ---
        # Position axes on the right
        ax = Axes(x_range=[-3, 3], y_range=[-3, 3], x_length=4.5, y_length=4.5)
        ax.to_edge(RIGHT, buff=0.5)
        
        # Generate Gaussian scatter points
        np.random.seed(42)
        dots = VGroup()
        for _ in range(400):
            x, y = np.random.normal(0, 0.9, 2)
            if -3 < x < 3 and -3 < y < 3:
                dots.add(Dot(ax.c2p(x, y), radius=0.03, color=GRAY, fill_opacity=0.6))
                
        k_strip = Rectangle(width=ax.x_length * (1.2/6), height=ax.y_length, color=BLUE, fill_opacity=0.3)
        l_strip = Rectangle(width=ax.x_length, height=ax.y_length * (1.2/6), color=RED, fill_opacity=0.3)
        intersect = Rectangle(width=k_strip.width, height=l_strip.height, color=PURPLE, fill_opacity=0.6)
        
        k_strip.move_to(ax.c2p(0,0))
        l_strip.move_to(ax.c2p(0,0))
        intersect.move_to(ax.c2p(0,0))

        k_label = MathTex("K").set_color(BLUE).next_to(k_strip, UP)
        l_label = MathTex("L").set_color(RED).next_to(l_strip, LEFT)
        
        with self.voiceover(text="Visually, imagine a two-dimensional Gaussian distribution centered at the origin, represented by these points.") as tracker:
            self.play(Create(ax))
            self.play(FadeIn(dots))
            
        with self.voiceover(text="Let Set K be a vertical symmetric strip, and Set L be a horizontal symmetric strip.") as tracker:
            self.play(FadeIn(k_strip), Write(k_label))
            self.play(FadeIn(l_strip), Write(l_label))
            
        with self.voiceover(text="Because the Gaussian density is heavily concentrated at the center, knowing a point is inside the blue strip forces it near the origin. This naturally increases the likelihood that it also falls inside the red strip.") as tracker:
            self.play(FadeIn(intersect))
            self.play(Circumscribe(intersect, color=YELLOW, time_width=2))

        clear_screen()
        self.wait(1.5)
        # ---------------------------------------------------------
        # 3. Step 1A: The Symmetric Strip Formulation
        # ---------------------------------------------------------
        step1a = Tex(r"\textbf{Step 1: The Symmetric Strip Formulation}").to_edge(UP)
        self.play(Write(step1a))

        strip_def_text = Tex(r"We define a \textbf{symmetric strip} as the region between \\ two parallel hyperplanes, centered at the origin:", font_size=36)
        strip_eq = MathTex(r"S_{i} = \{x \in \mathbb{R}^d : |\langle x, v_i \rangle| \le t_i\}").set_color(BLUE)
        VGroup(strip_def_text, strip_eq).arrange(DOWN, buff=0.4).next_to(step1a, DOWN, buff=0.6)

        with self.voiceover(text="We begin our proof by defining our fundamental building block: the symmetric strip. Geometrically, this is simply the space between two parallel hyperplanes that are symmetric around the origin.") as tracker:
            self.play(FadeIn(strip_def_text))
            self.play(Write(strip_eq))

        reduce_text = Tex(r"We reduce the problem by formulating test sets $K_n$ and $L_n$ \\ as finite intersections of these strips:", font_size=36)
        k_strip_eq = MathTex(r"K_n = \bigcap_{i=1}^{n_1} S_{i}")
        l_strip_eq = MathTex(r"L_n = \bigcap_{i=n_1+1}^{n_1+n_2} S_{i}")
        
        strip_group = VGroup(k_strip_eq, l_strip_eq).arrange(RIGHT, buff=1.5)
        formulation_group = VGroup(reduce_text, strip_group).arrange(DOWN, buff=0.5).next_to(strip_eq, DOWN, buff=0.8)

        with self.voiceover(text="We then formulate our test sets K and L as finite intersections of these strips. K is formed by the first batch of strips, and L is formed by the remaining strips.") as tracker:
            self.play(FadeIn(reduce_text))
            self.play(Write(k_strip_eq), Write(l_strip_eq))

        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 4. Step 1B: Justifying the Reduction
        # ---------------------------------------------------------
        step1b = Tex(r"\textbf{Step 1 (cont.): Why is this enough?}").to_edge(UP)
        self.play(Write(step1b))

        geom_text1 = Tex("1. Geometric Separation", font_size=36).set_color(BLUE)
        geom_text2 = Tex(r"Any closed symmetric convex set is exactly the intersection \\ of all symmetric strips containing it.", font_size=32)
        strip_inf = MathTex(r"K = \bigcap_{i=1}^{\infty} S_i").scale(0.8)
        geom_group = VGroup(geom_text1, geom_text2, strip_inf).arrange(DOWN, buff=0.3)

        meas_text1 = Tex("2. Continuity of Gaussian Measure", font_size=36).set_color(BLUE)
        meas_text2 = Tex(r"We can evaluate the infinite shape by taking the limit \\ of our finite polyhedra ($K_n \to K$).", font_size=32)
        limit_eq = MathTex(r"\mu(K \cap L) = \lim_{n \to \infty} \mu(K_n \cap L_n)").scale(0.8)
        meas_group = VGroup(meas_text1, meas_text2, limit_eq).arrange(DOWN, buff=0.3)

        content_group = VGroup(geom_group, meas_group).arrange(DOWN, buff=0.6)
        content_group.next_to(step1b, DOWN, buff=0.5)

        with self.voiceover(text="But why is this finite strip formulation enough? First, geometry. By the separation theorem, any closed symmetric convex set can be perfectly described as an infinite intersection of symmetric strips.") as tracker:
            self.play(FadeIn(geom_text1))
            self.play(Write(geom_text2))
            self.play(Write(strip_inf))
        
        self.wait(0.5)

        with self.voiceover(text="Second, measure theory. Gaussian probability measures are continuous. The probability of the true shape is exactly the limit of our finite approximations.") as tracker:
            self.play(FadeIn(meas_text1))
            self.play(Write(meas_text2))
            self.play(Write(limit_eq))

        with self.voiceover(text="Because limits preserve inequalities, if Royen can prove the correlation holds for our finite strips, the limit guarantees it for all symmetric convex sets.") as tracker:
            pass 

        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 5. Step 2A: Building the Covariance Matrix
        # ---------------------------------------------------------
        step2a = Tex(r"\textbf{Step 2A: Building the Covariance Matrix}").to_edge(UP)
        self.play(Write(step2a))

        y_def1 = Tex(r"To check if $X$ is in the strips, we evaluate its projections:", font_size=36)
        y_def2 = MathTex(r"Y_i = \langle X, v_i \rangle").set_color(BLUE)
        y_group = VGroup(y_def1, y_def2).arrange(DOWN, buff=0.3).next_to(step2a, DOWN, buff=0.5)

        with self.voiceover(text="To determine if our point X falls inside these strips, we must evaluate its projection against every normal vector. Let's call these projections Y_i.") as tracker:
            self.play(FadeIn(y_def1))
            self.play(Write(y_def2))

        y_vec1 = Tex(r"We stack these into a new Gaussian vector $Y = (Y^{(K)}, Y^{(L)})$ \\ and compute its covariance matrix $C$:", font_size=36)
        y_vec2 = MathTex(r"C_{ij} = \mathbb{E}[Y_i Y_j] = \langle v_i, v_j \rangle").set_color(YELLOW)
        vec_group = VGroup(y_vec1, y_vec2).arrange(DOWN, buff=0.3).next_to(y_group, DOWN, buff=0.6)

        with self.voiceover(text="By stacking all these projection variables together, we form a new Gaussian vector. Its covariance matrix, C, is simply the matrix of dot products between all the strip normal vectors.") as tracker:
            self.play(FadeIn(y_vec1))
            self.play(Write(y_vec2))

        c_block = MathTex(
            r"C = \begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} \begin{matrix} \leftarrow \text{Variables for } K \\ \leftarrow \text{Variables for } L \end{matrix}"
        ).scale(0.9).next_to(vec_group, DOWN, buff=0.6)

        with self.voiceover(text="Because the variables are grouped by set K and set L, the matrix naturally forms blocks. The off-diagonal blocks perfectly capture the geometric correlation between the two sets.") as tracker:
            self.play(Write(c_block))

        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 6. Step 2B: Covariance Interpolation
        # ---------------------------------------------------------
        step2b = Tex(r"\textbf{Step 2B: The Interpolation Parameter}").to_edge(UP)
        self.play(Write(step2b))

        cov_matrix = MathTex(
            r"C(\tau) = \begin{pmatrix} C_{11} & \tau C_{12} \\ \tau C_{21} & C_{22} \end{pmatrix}, \quad \tau \in [0,1]"
        ).set_color(ORANGE)

        # Case: tau = 1
        t1_title = Tex(r"\textbf{At } $\tau=1$ \textbf{(True Correlation):}", font_size=32).set_color(BLUE)
        t1_eq = MathTex(r"C(1) = C \implies \mathbb{P}_{\tau=1}(X \in K \cap L) = \mu(K \cap L)", font_size=32)
        tau1_group = VGroup(t1_title, t1_eq).arrange(DOWN, buff=0.15)

        # Case: tau = 0
        t0_title = Tex(r"\textbf{At } $\tau=0$ \textbf{(Independence):}", font_size=32).set_color(BLUE)
        t0_eq1 = MathTex(r"C(0) = \begin{pmatrix} C_{11} & 0 \\ 0 & C_{22} \end{pmatrix} \implies \textbf{Independent}", font_size=32)
        t0_eq2 = MathTex(r"\implies \mathbb{P}_{\tau=0}(X \in K \cap L) = \mu(K)\mu(L)", font_size=32)
        tau0_group = VGroup(t0_title, t0_eq1, t0_eq2).arrange(DOWN, buff=0.15)

        # The Goal
        cov_goal = MathTex(r"\textbf{Goal: } \frac{\partial}{\partial \tau} \mathbb{P}_\tau(X \in K \cap L) \ge 0").set_color(GREEN)

        # Master layout grouping to prevent spilling off-screen
        content_group = VGroup(cov_matrix, tau1_group, tau0_group, cov_goal).arrange(DOWN, buff=0.4)
        content_group.next_to(step2b, DOWN, buff=0.4)

        with self.voiceover(text="Royen now defines a virtual covariance matrix that scales only those cross-correlation blocks by a parameter, tau.") as tracker:
            self.play(Write(cov_matrix))

        with self.voiceover(text="When tau equals one, we have the original covariance matrix. Therefore, the probability represents the true, correlated joint measure, the left side of our inequality.") as tracker:
            self.play(FadeIn(t1_title))
            self.play(Write(t1_eq))

        with self.voiceover(text="When tau equals zero, the cross-covariance vanishes. For Gaussian variables, zero covariance means strict statistical independence. Thus, the probability splits into the product of the individual measures, the right side of our inequality.") as tracker:
            self.play(FadeIn(t0_title))
            self.play(Write(t0_eq1))
            self.play(Write(t0_eq2))
            self.wait(1)

        with self.voiceover(text="We have built a mathematical bridge. The entire proof now reduces to proving that the derivative of this probability with respect to tau is non-negative.") as tracker:
            self.play(Write(cov_goal))
            
        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 7. Step 3A: Squaring the Gaussian to Gamma
        # ---------------------------------------------------------
        step3a = Tex(r"\textbf{Step 3: Squaring the Gaussian}").to_edge(UP)
        self.play(Write(step3a))

        abs_eq = MathTex(r"|\langle X, v_i \rangle| \le t_i")
        equiv = MathTex(r"\iff").rotate(PI/2)
        sq_eq = MathTex(r"\frac{1}{2}\langle X, v_i \rangle^2 \le \frac{1}{2}t_i^2").set_color(BLUE)
        geom_group = VGroup(abs_eq, equiv, sq_eq).arrange(DOWN, buff=0.5)

        with self.voiceover(text="Step 3 is Royen's stroke of genius. Absolute values are geometrically rigid and mathematically difficult to integrate. He observed that bounding an absolute value is strictly equivalent to bounding its square.") as tracker:
            self.play(FadeIn(abs_eq))
            self.play(FadeIn(equiv))
            self.play(Write(sq_eq))

        explain_gamma1 = Tex(r"Let $Y = \langle X, v_i \rangle$. Since $X$ is Gaussian, $Y$ is a 1D Gaussian.", font_size=32)
        explain_gamma2 = Tex(r"The square of a Gaussian is a Chi-Squared variable.", font_size=32)
        explain_gamma3 = Tex(r"By scaling it by one-half, $Z_i = \frac{1}{2}Y^2$ maps perfectly to a \\ \textbf{Multivariate Gamma Distribution}.", font_size=32).set_color(YELLOW)
        
        text_group = VGroup(explain_gamma1, explain_gamma2, explain_gamma3).arrange(DOWN, buff=0.4).next_to(geom_group, RIGHT, buff=1.0)
        VGroup(geom_group, text_group).move_to(ORIGIN)

        with self.voiceover(text="Because the projection of a Gaussian vector is a one-dimensional Gaussian, squaring it transforms it into a Chi-Squared variable.") as tracker:
            self.play(Write(explain_gamma1))
            self.play(Write(explain_gamma2))

        with self.voiceover(text="By adding the one-half coefficient, Royen maps the entire problem space directly into a Multivariate Gamma Distribution. We have transformed geometry into pure probability analysis.") as tracker:
            self.play(FadeIn(explain_gamma3))

        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 8. Step 3B: The Laplace Transform Integrals
        # ---------------------------------------------------------
        step3b = Tex(r"\textbf{Step 3 (cont.): The Laplace Transform}").to_edge(UP)
        self.play(Write(step3b))

        with self.voiceover(text="Calculating the exact probability of this Gamma distribution is practically impossible. But, because we converted the problem into quadratic exponents, computing its Laplace transform is beautifully simple.") as tracker:
            pass 

        eq1 = MathTex(r"\mathcal{L}(\lambda, \tau) = \mathbb{E}[e^{-\sum \lambda_i Z_i}] = \mathbb{E}[e^{-\frac{1}{2} X^T V \Lambda V^T X}]").scale(0.8)
        eq2 = MathTex(r"= \int \frac{e^{-\frac{1}{2} x^T C^{-1} x}}{\sqrt{(2\pi)^d \det(C)}} \cdot e^{-\frac{1}{2} x^T V \Lambda V^T x} dx").scale(0.8)
        eq3 = MathTex(r"= \frac{1}{\sqrt{\det(C)}} \int \frac{e^{-\frac{1}{2} x^T (C^{-1} + V \Lambda V^T) x}}{\sqrt{(2\pi)^d}} dx").scale(0.8)
        eq4 = MathTex(r"= \frac{1}{\sqrt{\det(C)}} \cdot \frac{1}{\sqrt{\det(C^{-1} + V \Lambda V^T)}}").scale(0.8)
        eq5 = MathTex(r"= \det(I + \Lambda V^T C(\tau) V)^{-1/2}").set_color(BLUE)

        VGroup(eq1, eq2, eq3, eq4, eq5).arrange(DOWN, buff=0.3).next_to(step3b, DOWN, buff=0.5)

        with self.voiceover(text="We write out the Laplace expectation. Notice how the quadratic Gamma variables perfectly mirror the format of a Gaussian density exponent.") as tracker:
            self.play(Write(eq1))

        with self.voiceover(text="We substitute the standard Gaussian probability density function into the integral.") as tracker:
            self.play(Write(eq2))

        with self.voiceover(text="We can now factor out the variables and combine the two exponents into a single, unified quadratic form.") as tracker:
            self.play(Write(eq3))

        with self.voiceover(text="Applying the standard multidimensional Gaussian integral formula immediately evaluates this to the inverse square root of the matrix determinant.") as tracker:
            self.play(Write(eq4))

        with self.voiceover(text="By applying basic matrix properties, the original covariance determinants cancel out, leaving us with this elegant, tractable formula.") as tracker:
            self.play(Write(eq5))
            
        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 9. Step 4: Taylor Expansion and Non-Negative Derivative
        # ---------------------------------------------------------
        step4 = Tex(r"\textbf{Step 4: Why is the Derivative Non-Negative?}").to_edge(UP)
        self.play(Write(step4))

        t1 = MathTex(r"\ln \mathcal{L} = \frac{1}{2} \sum_{m=1}^\infty \frac{(-1)^{m-1}}{m} \text{Tr}\Big((\Lambda C(\tau))^m\Big)").set_color(YELLOW)
        
        with self.voiceover(text="To prove the derivative is positive, Royen expanded the logarithm of the Laplace transform into an infinite Taylor series of traces.") as tracker:
            self.play(Write(t1))
            self.wait(1)

        self.play(t1.animate.shift(UP * 1.5).scale(0.8))

        c_mat = MathTex(r"C(\tau) = \begin{pmatrix} C_{11} & \tau C_{12} \\ \tau C_{21} & C_{22} \end{pmatrix}").scale(0.9)
        t2 = Tex(r"Taking $\frac{\partial}{\partial \tau}$ isolates the off-diagonal blocks $\tau C_{12}$ and $\tau C_{21}$.", font_size=32)
        VGroup(c_mat, t2).arrange(DOWN, buff=0.3).next_to(t1, DOWN, buff=0.5)

        with self.voiceover(text="Taking the derivative with respect to tau zeroes out the constants and isolates the off-diagonal covariance blocks.") as tracker:
            self.play(FadeIn(c_mat))
            self.play(Write(t2))

        t3 = Tex(r"Because $C_{21} = C_{12}^T$, the cyclic property of the trace pairs them:", font_size=32)
        t4 = MathTex(r"\text{Tr}(\dots C_{12} C_{21} \dots) = \text{Tr}(\dots C_{12} C_{12}^T \dots) \implies \textbf{Positive Semi-Definite}", font_size=32).set_color(BLUE)
        t5 = Tex(r"Royen proved that across the entire alternating series, these PSD components \\ guarantee the final derivative is strictly non-negative.", font_size=32).set_color(GREEN)
        
        VGroup(t3, t4, t5).arrange(DOWN, buff=0.3).next_to(t2, DOWN, buff=0.5)

        with self.voiceover(text="Because the covariance matrix is symmetric, the cyclic nature of the trace always multiplies these off-diagonal blocks in pairs.") as tracker:
            self.play(Write(t3))

        with self.voiceover(text="Any matrix multiplied by its transpose forms a positive semi-definite matrix.") as tracker:
            self.play(Write(t4))

        with self.voiceover(text="Royen masterfully proved that across the entire alternating series, these positive semi-definite components overpower any negative terms, guaranteeing the derivative is strictly non-negative.") as tracker:
            self.play(Write(t5))
            
        clear_screen()
        self.wait(1.5)

        # ---------------------------------------------------------
        # 10. Conclusion
        # ---------------------------------------------------------
        conc_title = Tex(r"\textbf{Conclusion}").to_edge(UP)
        self.play(Write(conc_title))

        f_eq = MathTex(r"\mathbb{P}_{\tau=1}(X \in K \cap L) \ge \mathbb{P}_{\tau=0}(X \in K \cap L)")
        gci_final = MathTex(r"\mu(K \cap L) \ge \mu(K)\mu(L)").set_color(YELLOW).scale(1.5)
        
        VGroup(f_eq, gci_final).arrange(DOWN, buff=0.8)

        with self.voiceover(text="Because the probability grows from tau equals zero to tau equals one...") as tracker:
            self.play(Write(f_eq))

        with self.voiceover(text="We recover the original Gaussian Correlation Inequality. Knowing a Gaussian vector falls in one symmetric set implies it is more likely to fall in the other. Q. E. D.") as tracker:
            self.play(TransformFromCopy(f_eq, gci_final))
            
        self.wait(3)
        clear_screen()