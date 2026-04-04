from manim import *
from manim_voiceover import VoiceoverScene
from kokoro_mv import KokoroService
import numpy as np
import random

class FullAnimationPAT(VoiceoverScene):
    def construct(self):
        # self.set_speech_service(GTTSService(lang="en", tld="us"))
        self.set_speech_service(KokoroService(voice="af_heart", lang="en-us"))

        #######################################################################################################
        # Scene 1
        #######################################################################################################

        self.next_section()
        
        # Title
        title = Text("Photoacoustic Tomography (PAT)", font_size=36)

        with self.voiceover(text="Photoacoustic Tomography is an emerging biomedical modality.") as tracker:
            self.play(Write(title))
            self.play(title.animate.to_edge(UP + RIGHT, buff=0.5))
            self.wait(1)
            self.play(FadeOut(title))

        # Tissue
        tissue = Circle(radius=2.5, color=BLUE).shift(LEFT*3.5 + UP*0.5)
        tissue_label = Text("Biological Tissue", font_size=40, color=BLUE).scale(0.5).next_to(tissue, DOWN, buff=0.4)

        # Multiple absorbers
        absorbers = VGroup(
            Dot(color=RED).move_to(tissue.get_center() + LEFT*0.5 + UP*0.5),
            Dot(color=ORANGE).move_to(tissue.get_center() + RIGHT*0.7 + DOWN*0.3),
            Dot(color=YELLOW).move_to(tissue.get_center() + UP*0.8),
            Dot(color=MAROON).move_to(tissue.get_center() + LEFT*0.3 + DOWN*0.8),
        )
        abs_label = Text("Optical Absorbers", font_size=36).scale(0.5).next_to(absorbers, UP, buff=0.5)
        
        with self.voiceover(text="First, we look at the biological tissue containing some targets to be identified.") as tracker:
            self.play(Create(tissue), Write(tissue_label))
            self.play(FadeIn(absorbers))

        # Spectrum setup
        spectrum = VGroup(
            Text("Visible", font_size=40).scale(0.45).shift(LEFT*1.8 + DOWN*0.3),
            Text("Infrared (Invisible)", font_size=40, color=RED_E).scale(0.45).shift(RIGHT*0.8 + DOWN*0.3)
        ).to_edge(RIGHT).shift(LEFT*1+ UP*1.5)

        gradient = Rectangle(width=2.6, height=0.2, fill_color=[RED, GREEN, BLUE], fill_opacity=1, stroke_width=0).next_to(spectrum[0], UP, buff=0.1)
        
        # Fixed: Use a normal rectangle with very low opacity to represent the 'invisible' bar clearly
        ir_rect = Rectangle(width=2.6, height=0.2, fill_opacity=0.1, stroke_width=1, stroke_color=WHITE, stroke_opacity=1).next_to(spectrum[1], UP, buff=0.1)

        with self.voiceover(text="These targets can absorb infrared light, which has a longer wavelength than visible light.") as tracker:
            self.play(Write(abs_label))
            self.play(FadeIn(spectrum), FadeIn(gradient), FadeIn(ir_rect))
            self.play(Indicate(ir_rect, color=YELLOW))
            self.wait(2)
            self.play(FadeOut(spectrum), FadeOut(gradient), FadeOut(ir_rect))

        # Laser pulse
        laser_start = RIGHT * 6 + UP * 0.5
        laser_end = tissue.get_right()
        laser = Arrow(start=laser_start, end=laser_end, color=YELLOW, buff=0)
        laser_text = Text("Infrared Laser Pulse", font_size=40, color=YELLOW).scale(0.5).next_to(laser, UP)
        
        with self.voiceover(text="A short laser pulse is fired into the region.") as tracker:
            self.play(GrowArrow(laser, run_time=tracker.duration/2), Write(laser_text))
            self.play(FadeOut(laser), FadeOut(laser_text))

        # Flash / Thermal Expansion
        with self.voiceover(text="The absorbed energy causes rapid thermoelastic expansion within the absorbers.") as tracker:
            flashes = [Flash(dot, color=YELLOW, flash_radius=0.4) for dot in absorbers]
            self.play(*flashes)
            self.play(*flashes)
            self.play(*flashes)
            self.play(*flashes)

        # Detectors
        detectors = VGroup()
        center = tissue.get_center()
        angles = np.linspace(-50, 70, 7)
        for angle in angles:
            theta = angle * DEGREES
            pos = center + 3.2 * np.array([np.cos(theta), np.sin(theta), 0])
            detector = Square(side_length=0.25, color=GREEN)
            detector.move_to(pos)
            detectors.add(detector)
        det_label = Text("Ultrasound Detectors", font_size=54, color=GREEN).scale(0.33).next_to(detectors, RIGHT, buff=0.3)


        # Acoustic waves and Concurrent Blinking
        all_wave_animations = []
        for absorber in absorbers:
            radii = np.arange(0.5, 4.5, 0.5)
            for r in radii:
                w = Circle(radius=r, color=WHITE, stroke_width=1.0, stroke_opacity=max(0.1, 1.0 - r/5)).move_to(absorber)
                all_wave_animations.append(Succession(GrowFromCenter(w, run_time=3.0), FadeOut(w, run_time=0.2)))

        blinking_anims = [
            Succession(
                Wait(random.uniform(0.5, 2.0)), 
                *[Succession(Indicate(d, color=WHITE, scale_factor=1.4, run_time=0.4), Wait(random.uniform(0.1, 0.8))) for _ in range(4)]
            ) for d in detectors
        ]
        
        with self.voiceover(text="This expansion creates ultrasound waves that travel through the tissue.") as tracker:
            self.play(
                LaggedStart(*all_wave_animations, lag_ratio=0.15), 
                FadeIn(detectors), 
                Write(det_label), 
                run_time=tracker.duration)



        with self.voiceover(text="Finally, the detectors capture these waves as they propagate, allowing for image reconstruction.") as tracker:
            self.play(
                LaggedStart(*all_wave_animations, lag_ratio=0.15),
                *blinking_anims,
                run_time=tracker.duration
            )
        self.wait(2)

        self.clear()

        #######################################################################################################
        # End of Scene 1
        #######################################################################################################


        #######################################################################################################
        # Scene 2
        #######################################################################################################

        self.next_section()

        # Title
        title = Text("Mathematical Model of PAT", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 1. Radiative Transport Equation (RTE)
        rte_group = VGroup(
            Text("Photon Transport: RTE", font_size=28, color=YELLOW),
            MathTex(
                "\\frac{1}{c} \\frac{\\partial \\phi }{\\partial t} + \\hat{\\Omega} \\cdot \\nabla \\phi  + (\\mu_a + \\mu_s) \\phi = \\mu_s \\int_{4\\pi} p(\\hat{\\Omega}', \\hat{\\Omega}) \\phi (\\mathbf{r}, \\hat{\\Omega}', t) d\\hat{\\Omega}'",
                font_size=34
            ),
            Text("Describes light scattering and absorption in tissue.", font_size=40).scale(0.5)
        ).arrange(DOWN, buff=0.4).shift(UP*0.5)

        with self.voiceover(text="The first part of the model is the Radiative Transport Equation. It describes how photons travel, scatter, and are absorbed within biological tissue.") as tracker:
            self.play(FadeIn(rte_group))
        self.wait(1)

        # 2. The Coupling Equation: Absorbed Energy Density
        coupling_eq = MathTex(
            "H(\\mathbf{r}, t) = \\mu_a(\\mathbf{r}) \\Phi(\\mathbf{r}, t)",
            color=RED,
            font_size=36
        ).shift(UP*0.2)
        
        coupling_label = Text("Heat Source Density", font_size=28, color=RED).next_to(coupling_eq, UP)

        coupling_group = VGroup(coupling_label, 
                                coupling_eq).arrange(DOWN, buff=0.4)

        flu_eq = MathTex(
            "\\Phi(\\mathbf{r}, t) = \\int_{4\\pi} \\phi(\\mathbf{r}, \\hat{\\Omega}, t) d\\hat{\\Omega}",
            color=ORANGE,
            font_size=36
        ).shift(LEFT * 0.2 + DOWN*0.2)
        
        with self.voiceover(text="When photons are absorbed by the tissue, the energy is transformed into heat. We denote it by H, which represents the heat source density. It is the product of the absorption coefficient and the optical fluence. The fluence is the angular integral of the solution to RTE. ") as tracker:
            self.play(
                rte_group.animate.scale(1).to_edge(UP + LEFT, buff=0.5),
                run_time=2
            )
            self.play(FadeIn(coupling_group))
            self.play(coupling_group.animate.scale(1).to_edge(RIGHT, buff=0.5),
                     run_time=2)
            
            heat_term_box = SurroundingRectangle(coupling_eq[0][0:6], color=YELLOW)
            self.play(Create(heat_term_box))
            self.play(FadeOut(heat_term_box)) 

            absorb_term_box = SurroundingRectangle(coupling_eq[0][7:11], color=YELLOW)
            self.wait(3.8)
            self.play(Create(absorb_term_box))
            self.play(FadeOut(absorb_term_box)) 

            flu_term_box = SurroundingRectangle(coupling_eq[0][12:], color=YELLOW)
            self.wait(0.2)
            self.play(Create(flu_term_box))
            self.play(FadeOut(flu_term_box)) 

            self.play(FadeIn(flu_eq))
            self.play(flu_eq.animate.scale(1).next_to(coupling_group, DOWN), run_time=2)


        # 2. Acoustic Wave Equation
        wave_title = Text("Ultrasound: Wave Equation", font_size=28, color=BLUE)
        wave_eq = MathTex(
            "\\left( \\nabla^2 - \\frac{1}{v_s^2} \\frac{\\partial^2}{\\partial t^2} \\right) p(\\mathbf{r}, t) = -\\frac{\\beta}{C_p} \\frac{\\partial H(\\mathbf{r}, t)}{\\partial t}",
            font_size=34
        )
        wave_desc = Text("Describes the propagation of pressure waves to the surface.", font_size=40).scale(0.5)

        wave_group = VGroup(wave_title, wave_eq, wave_desc).arrange(DOWN, buff=0.4).to_edge(LEFT+DOWN*1.2, buff=0.5)

        self.wait(1)
        
        with self.voiceover(text="The heat source acts as the source for the second part of the model: the wave equation. It describes how the resulting ultrasound pressure waves propagate through the body.") as tracker:
            self.wait(2)
            self.play(FadeIn(wave_group))
            self.wait(2)

        # Linking the two
        link_arrow1 = CurvedArrow(rte_group[1].get_right(), coupling_eq.get_top(), color=RED, angle=-TAU/4)
        link_arrow2 = CurvedArrow(coupling_eq.get_bottom(), wave_eq.get_right(), color=RED, angle=-TAU/4)
        source_term_box = SurroundingRectangle(wave_eq[0][-10:], color=RED)
        source_label = Text("Initial Pressure Source", font_size=36, color=RED).scale(0.5).next_to(source_term_box, RIGHT)

        self.wait(1)
        
        with self.voiceover(text="The absorbed energy from the RTE becomes the heat source. Then the heat source becomes the initial pressure for the wave equation, linking optics and acoustics into a single modality.") as tracker:
            self.play(Create(link_arrow1))
            self.wait(1.5)
            self.play(FadeOut(link_arrow1))
            self.play(Create(link_arrow2)) 
            self.wait(1.5)
            self.play(FadeOut(link_arrow2))
            self.play(Create(source_term_box), Write(source_label))

        self.wait(3)

        self.clear()

        #######################################################################################################
        # End of Scene 2
        #######################################################################################################

        #######################################################################################################
        # Scene 3
        #######################################################################################################
        self.next_section()

        # Title
        title = Text("Acoustic Inverse Problem", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Consistent Setup
        tissue = Circle(radius=2.5, color=BLUE).shift(LEFT*3.5 + UP*0.5)
        tissue_label = Text("Biological Tissue", font_size=40, color=BLUE).scale(0.5).next_to(tissue, DOWN, buff=0.4)

        ips = VGroup(
            Dot(radius=0.2, color=YELLOW).move_to(tissue.get_center() + LEFT*0.5 + UP*0.5),
            Dot(radius=0.2, color=YELLOW).move_to(tissue.get_center() + RIGHT*0.7 + DOWN*0.3),
            Dot(radius=0.2, color=ORANGE).move_to(tissue.get_center() + UP*0.8),
            Dot(radius=0.2, color=ORANGE).move_to(tissue.get_center() + LEFT*0.3 + DOWN*0.8),
        )
        ip_label = Text("Recovered Initial Pressure", font_size=54).scale(0.33).next_to(ips, UP, buff=0.5)

        detectors = VGroup()
        center = tissue.get_center()
        angles = np.linspace(-50, 70, 7)
        for angle in angles:
            theta = angle * DEGREES
            pos = center + 3.2 * np.array([np.cos(theta), np.sin(theta), 0])
            detector = Square(side_length=0.25, color=GREEN)
            detector.move_to(pos)
            detectors.add(detector)
        det_label = Text("Ultrasound Detectors", font_size=54, color=GREEN).scale(0.33).next_to(detectors, RIGHT, buff=0.3)

        self.add(tissue, tissue_label, detectors, det_label)

        blinking_anims = [
            Succession(
                Wait(random.uniform(0.1, 0.5)),
                *[Succession(Indicate(d, color=WHITE, scale_factor=1.4, run_time=0.4), Wait(random.uniform(0.1, 0.8))) for _ in range(3)]
            ) for d in detectors
        ]

        with self.voiceover(text="The reconstruction process begins with the recorded ultrasound data. These signals were captured by the detector array at the surface.") as tracker:
            self.play(*blinking_anims, run_time=tracker.duration)

        # Speed Comparison Visualization
        speed_comp = VGroup(
            Text("Light Speed", font_size=40, color=YELLOW).scale(0.5),
            Line(RIGHT*3, RIGHT*5, color=YELLOW),
            Text("Sound Speed", font_size=40, color=BLUE).scale(0.5),
            Line(RIGHT*3, RIGHT*5, color=BLUE)
        ).arrange_in_grid(rows=2, cols=2, buff=0.5).to_edge(RIGHT, buff=1).shift(DOWN*1)
        
        light_pulse = Dot(speed_comp[1].get_left(), color=YELLOW)
        sound_pulse = Dot(speed_comp[3].get_left(), color=BLUE)

        with self.voiceover(text="Because sound speed and light speed differ significantly, the acoustic and optical processes are essentially decoupled.") as tracker:
            self.play(FadeIn(speed_comp))
            # Sound moves to 1/5 of the line length
            target_sound_pos = speed_comp[3].point_from_proportion(0.02)
            self.play(
                light_pulse.animate.move_to(speed_comp[1].get_right()),
                sound_pulse.animate.move_to(target_sound_pos),
                run_time=tracker.duration,
                rate_func=linear
            )
            self.play(FadeOut(speed_comp), FadeOut(light_pulse), FadeOut(sound_pulse))

        step1_text = Text("Acoustic Inverse Problem", font_size=28, color=YELLOW).to_edge(UP + RIGHT, buff=0.5)

        with self.voiceover(text="Therefore, we first solve the acoustic inverse problem by propagating the recorded data back into the tissue. This is solving the wave equation backward in time.") as tracker:
            self.play(Write(step1_text))
            back_waves = VGroup()
            for d in detectors:
                vec = tissue.get_center() - d.get_center()
                angle = np.arctan2(vec[1], vec[0])
                bw = Arc(radius=0.1, start_angle=angle - PI/4, angle=PI/2, color=BLUE_B).move_to(d.get_center())
                back_waves.add(bw)

            self.play(
                *[w.animate.scale(25).move_to(tissue.get_center()).set_style(stroke_opacity=0) for w in back_waves],
                run_time=tracker.duration * 0.8
            )

        p0_label = MathTex("p_0(\\mathbf{r})", font_size=36, color=RED).next_to(ips, RIGHT)

        with self.voiceover(text="As these signals are all propagated, the initial pressure distribution, P-zero, can be recovered.") as tracker:
            self.play(FadeIn(ips, scale=1.5), Write(p0_label), Write(ip_label))
            self.play(Flash(ips, color=RED, flash_radius=1.5))
            self.wait(1.5)
            self.play(Indicate(p0_label))

        self.wait(3)
        
        self.clear()
        #######################################################################################################
        # End of Scene 3
        #######################################################################################################
        
        #######################################################################################################
        # Scene 4
        #######################################################################################################

        self.next_section()

        # Title
        title = Text("Optical Inverse Problem", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Consistent Setup
        tissue = Circle(radius=2.5, color=BLUE).shift(LEFT*3.5 + UP*0.5)
        tissue_label = Text("Biological Tissue", font_size=40, color=BLUE).scale(0.5).next_to(tissue, DOWN, buff=0.4)
        self.play(Create(tissue), Create(tissue_label))

        ips = VGroup(
            Dot(radius=0.2, color=YELLOW).move_to(tissue.get_center() + LEFT*0.5 + UP*0.5),
            Dot(radius=0.2, color=YELLOW).move_to(tissue.get_center() + RIGHT*0.7 + DOWN*0.3),
            Dot(radius=0.2, color=ORANGE).move_to(tissue.get_center() + UP*0.8),
            Dot(radius=0.2, color=ORANGE).move_to(tissue.get_center() + LEFT*0.3 + DOWN*0.8),
        )

        # Ambiguous Initial Pressure Distribution p0(r)
        # p0_area = tissue.copy().set_fill(RED, opacity=0.3).set_stroke(RED, opacity=0.5)
        p0_label = MathTex("p_0(\\mathbf{r})", font_size=36, color=RED).next_to(ips, RIGHT)

        with self.voiceover(text="However, the recovered initial pressure distribution, P-zero, only tells us the absorbed energy's distribution throughout the tissue volume.") as tracker:
            self.play(Write(p0_label))
            self.play(FadeIn(ips, scale=1.5))
            
        # The Equation - Positioned to the RIGHT of the tissue
        math_p0 = MathTex("p_0(\\mathbf{r}) = \\Gamma  \\mu_a(\\mathbf{r}) \\Phi(\\mathbf{r})", font_size=34)
        math_p0.shift(RIGHT * 3 + UP * 1.5)

        self.wait(1)
        
        with self.voiceover(text="This value is proportional to a product of the absorption coefficient and the local light fluence, making the individual components ambiguous.") as tracker:
            self.play(Write(math_p0))

            absorb_term_box = SurroundingRectangle(math_p0[0][7:11], color=YELLOW)
            self.wait(1)
            self.play(Create(absorb_term_box))
            self.play(FadeOut(absorb_term_box)) 

            flu_term_box = SurroundingRectangle(math_p0[0][12:], color=YELLOW)
            self.wait(0.2)
            self.play(Create(flu_term_box))
            self.play(FadeOut(flu_term_box)) 

            self.wait(1)
            self.play(Create(absorb_term_box.set_color(RED)), run_time=0.1)
            self.play(FadeOut(absorb_term_box)) 
            self.play(Create(flu_term_box.set_color(RED)), run_time=0.1)
            self.play(FadeOut(flu_term_box)) 

        # Targets inside the tissue
        healthy_vessel = ips[0]
        tumor_target = ips[1]

        h_text = Text("Healthy Cell", font_size= 64).scale(0.25).next_to(healthy_vessel, LEFT, buff=0.2)
        t_text = Text("Tumor Cell", font_size=64).scale(0.25).next_to(tumor_target, DOWN, buff=0.2)

        with self.voiceover(text="Within this pressure map, a healthy cell and a tumor cell might appear identical if they absorb the same amount of energy.") as tracker:
            self.play(FadeIn(healthy_vessel), FadeIn(tumor_target), Write(h_text), Write(t_text))

            for _ in range(4):
                self.play(Indicate(healthy_vessel), Indicate(tumor_target))

        # Optical Inversion Step
        step2_text = MathTex("\\text{Optical Inverse Problem: } p_0 \\rightarrow \\mu_a", font_size=34, color=YELLOW).next_to(math_p0, DOWN*1.5)

        self.wait(1)
        
        with self.voiceover(text=" By solving the optical inverse problem, we can reconstruct the absorption coefficient (μ-'A')  from the initial pressure field P-zero.") as tracker:
            self.play(Write(step2_text))
        
        self.wait(1)
        with self.voiceover(text="This distinguishes targets by their optical properties, allowing us to accurately identify the tumor cells based on its higher absorption properties.") as tracker:
            self.play(
                healthy_vessel.animate.set_color(RED_E),
                tumor_target.animate.set_color(PURPLE),
                run_time=2
            )
            for _ in range(4):
                self.play(Indicate(healthy_vessel, color=RED_E), Indicate(tumor_target, color=PURPLE))
         
            
            self.play(FadeOut(h_text), FadeOut(t_text))
            new_h_label = MathTex("\\text{Low } \\mu_a", font_size=28, color=WHITE).next_to(healthy_vessel, LEFT, buff=0.1)
            new_t_label = MathTex("\\text{High } \\mu_a", font_size=28, color=WHITE).next_to(tumor_target, DOWN, buff=0.1)
            self.play(Write(new_h_label), Write(new_t_label))

        self.wait(3)        

        self.clear()

        
        #######################################################################################################
        # End of Scene 4
        #######################################################################################################