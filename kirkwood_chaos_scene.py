from manim import *
import numpy as np

# Physical constants (AU, Years)
A_MARS = 1.524
A_JUP = 5.204
T_JUP = 11.86  # Jupiter period in years

class KirkwoodResonanceChaos(Scene):
    def construct(self):
        # 1. Header
        title = Title("Astrophysical Chaos: 3:1 Kirkwood Resonance Gap", font_size=28)
        subtitle = Text(
            "Periodic resonant kicks pump eccentricity (e) until the orbit crosses Mars (e >= 0.39)",
            font_size=15, color=GRAY
        ).next_to(title, DOWN, buff=0.1)
        self.add(title, subtitle)

        # 2. Left Panel: Heliocentric Orbit Map
        left_center = LEFT * 3.4 + DOWN * 0.4
        scale = 0.48  # AU to scene units

        sun = Dot(left_center, radius=0.14, color=YELLOW)
        sun_glow = Dot(left_center, radius=0.28, color=YELLOW, fill_opacity=0.25)
        sun_lbl = Text("Sun", font_size=12, color=YELLOW).next_to(sun, DOWN, buff=0.08)

        # Mars Orbit Circle (r = 1.524 AU)
        mars_orbit = Circle(radius=A_MARS * scale, color=RED, stroke_width=2.0, stroke_opacity=0.8).move_to(left_center)
        mars_lbl = Text("Mars Orbit (1.52 AU)", font_size=11, color=RED_A).next_to(mars_orbit, UP, buff=0.05)

        # Jupiter Orbit Circle (r = 5.2 AU)
        jup_orbit = Circle(radius=A_JUP * scale, color=ORANGE, stroke_width=1.2, stroke_opacity=0.35).move_to(left_center)
        jup_lbl = Text("Jupiter Orbit (5.20 AU)", font_size=11, color=ORANGE).next_to(jup_orbit, RIGHT, buff=0.1)

        # Stable Asteroid (a = 2.20 AU, e = 0.05 regular)
        stable_orbit = Ellipse(
            width=2 * 2.20 * scale,
            height=2 * 2.20 * np.sqrt(1 - 0.05**2) * scale,
            color=GREEN_B, stroke_width=1.8, stroke_opacity=0.7
        ).move_to(left_center)

        # Resonant Chaotic Asteroid: starts at a = 2.50 AU, e = 0.08
        # We will dynamically update this curve so it visibly stretches and intersects Mars
        chaos_orbit_curve = VMobject(color=PURPLE_B, stroke_width=2.5)

        # Moving bodies
        jupiter_dot = Dot(radius=0.14, color=ORANGE)
        ast_stable_dot = Dot(radius=0.08, color=GREEN_B)
        ast_chaos_dot = Dot(radius=0.09, color=PURPLE_B)

        # 3. Right Panel: Eccentricity Time Evolution Graph
        axes = Axes(
            x_range=[0, 80, 20],
            y_range=[0, 0.6, 0.1],
            x_length=4.8,
            y_length=3.4,
            axis_config={"include_numbers": False, "stroke_width": 2},
        ).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)

        x_ticks = VGroup(*[
            Text(str(xv), font_size=11).next_to(axes.c2p(xv, 0), DOWN, buff=0.15)
            for xv in [0, 20, 40, 60, 80]
        ])
        y_ticks = VGroup(*[
            Text(f"{yv:.1f}", font_size=11).next_to(axes.c2p(0, yv), LEFT, buff=0.15)
            for yv in [0.0, 0.2, 0.4, 0.6]
        ])

        x_label = Text("Time (Years)", font_size=13).next_to(axes.x_axis, DOWN, buff=0.45)
        y_label = Text("Eccentricity (e)", font_size=13).next_to(axes.y_axis, UP, buff=0.25).shift(RIGHT * 0.4)

        # Mars-crossing limit line (e = 0.39 for a = 2.5 AU, where perihelion q = a(1-e) <= 1.524 AU)
        mars_threshold = DashedLine(
            axes.c2p(0, 0.39), axes.c2p(80, 0.39),
            color=RED, stroke_width=2
        )
        danger_text = Text("Mars-Crossing Threshold (e = 0.39)", font_size=11, color=RED).next_to(mars_threshold, UP, buff=0.06)

        # Plot tracker dots and continuous traces
        p_stable_dot = Dot(axes.c2p(0, 0.05), radius=0.07, color=GREEN_B)
        p_chaos_dot = Dot(axes.c2p(0, 0.08), radius=0.08, color=PURPLE_B)

        p_stable_trace = TracedPath(p_stable_dot.get_center, stroke_color=GREEN_B, stroke_width=1.8)
        p_chaos_trace = TracedPath(p_chaos_dot.get_center, stroke_color=PURPLE_B, stroke_width=2.5)

        # Legend
        sq_green = Square(side_length=0.12, color=GREEN_B, fill_opacity=1.0).to_corner(UL).shift(DOWN * 0.85 + RIGHT * 0.2)
        txt_stable = Text("a = 2.2 AU (Regular non-resonant)", font_size=12, color=GREEN_B).next_to(sq_green, RIGHT, buff=0.15)
        
        sq_purple = Square(side_length=0.12, color=PURPLE_B, fill_opacity=1.0).next_to(sq_green, DOWN, buff=0.15)
        txt_chaos = Text("a = 2.5 AU (3:1 Resonant Chaotic)", font_size=12, color=PURPLE_B).next_to(sq_purple, RIGHT, buff=0.15)

        # Add initial static and dynamic objects
        self.add(
            sun, sun_glow, sun_lbl, mars_orbit, jup_orbit, mars_lbl, jup_lbl,
            stable_orbit, chaos_orbit_curve, jupiter_dot, ast_stable_dot, ast_chaos_dot,
            axes, x_ticks, y_ticks, x_label, y_label, mars_threshold, danger_text,
            p_stable_dot, p_chaos_dot, p_stable_trace, p_chaos_trace,
            sq_green, txt_stable, sq_purple, txt_chaos
        )

        # 4. Resonant Eccentricity Function (Wisdom 1982 map approximation)
        def get_ecc_chaos(t):
            # Sigmoidal resonant jump crossing e=0.39 around t=50 yrs with fast high-order modulations
            base = 0.08 + 0.38 / (1.0 + np.exp(-0.10 * (t - 48.0)))
            perturb = 0.035 * np.sin(0.45 * t) + 0.015 * np.cos(1.2 * t)
            return np.clip(base + perturb, 0.05, 0.52)

        def get_ecc_stable(t):
            return 0.05 + 0.02 * np.sin(0.3 * t)

        # 5. Updaters for orbital positions & dynamic trajectory elongation
        sim_time = ValueTracker(0.0)

        # Helper to construct the dynamic ellipse around the Sun at left_center
        def update_chaos_orbit(mob):
            t = sim_time.get_value()
            e_val = get_ecc_chaos(t)
            a_val = 2.50
            # Perihelion angle precesses slowly
            omega_p = 0.08 * t
            
            thetas = np.linspace(0, 2 * np.pi, 120)
            r_vals = a_val * (1.0 - e_val**2) / (1.0 + e_val * np.cos(thetas - omega_p))
            
            points = [
                left_center + np.array([r * np.cos(th), r * np.sin(th), 0.0]) * scale
                for th, r in zip(thetas, r_vals)
            ]
            mob.set_points_as_corners(points)

        chaos_orbit_curve.add_updater(update_chaos_orbit)

        # Jupiter position updater (4 full orbits in 80 sim-years)
        jupiter_dot.add_updater(
            lambda mob: mob.move_to(
                left_center + np.array([
                    A_JUP * scale * np.cos(2 * np.pi * sim_time.get_value() / T_JUP),
                    A_JUP * scale * np.sin(2 * np.pi * sim_time.get_value() / T_JUP),
                    0.0
                ])
            )
        )

        # Stable asteroid dot updater
        ast_stable_dot.add_updater(
            lambda mob: mob.move_to(
                left_center + np.array([
                    2.20 * scale * np.cos(2 * np.pi * sim_time.get_value() / 3.26),
                    2.20 * scale * np.sin(2 * np.pi * sim_time.get_value() / 3.26),
                    0.0
                ])
            )
        )

        # Chaotic asteroid dot updater (follows the osculating eccentric path)
        def update_ast_chaos(mob):
            t = sim_time.get_value()
            e_val = get_ecc_chaos(t)
            omega_p = 0.08 * t
            theta_orb = 2 * np.pi * t / 3.95
            r = 2.50 * (1.0 - e_val**2) / (1.0 + e_val * np.cos(theta_orb - omega_p))
            mob.move_to(left_center + np.array([r * np.cos(theta_orb), r * np.sin(theta_orb), 0.0]) * scale)

        ast_chaos_dot.add_updater(update_ast_chaos)

        # Graph tracker updaters
        p_stable_dot.add_updater(
            lambda mob: mob.move_to(axes.c2p(sim_time.get_value(), get_ecc_stable(sim_time.get_value())))
        )
        p_chaos_dot.add_updater(
            lambda mob: mob.move_to(axes.c2p(sim_time.get_value(), get_ecc_chaos(sim_time.get_value())))
        )

        # 6. Play the full 24-second continuous simulation
        self.play(
            sim_time.animate.set_value(80.0),
            run_time=24.0,
            rate_func=linear
        )
        self.wait(2.0)
