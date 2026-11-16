# kirkwood-resonance-dynamics
Visualizing 3:1 Kirkwood resonance and dynamical chaos in the asteroid belt using Manim
# Kirkwood Gaps & Orbital Resonance Dynamics

An animated physical visualization of **mean-motion resonances and dynamical chaos** in the asteroid belt, produced using Python (Manim).

## 🧭 Scientific Motivation

The asteroid belt is not uniformly filled; it contains prominent gaps—known as **Kirkwood gaps**—at specific orbital distances from the Sun. The most famous of these is the **3:1 mean-motion resonance with Jupiter**, where an asteroid orbits the Sun three times for every single orbit of Jupiter.

Rather than being empty due to an absence of material at formation, these gaps are carved out by **gravitational chaos**:
- **Resonant Forcing:** Periodic gravitational kicks from Jupiter pump up an asteroid’s orbital eccentricity.
- **Mars-Crossing Chaos:** As eccentricity grows beyond a threshold ($e \approx 0.39$), the asteroid's orbit crosses that of Mars.
- **Ejection / Collisional Removal:** Close gravitational encounters with Mars scatter the asteroid out of the resonance zone, leaving a depleted "gap" in the spatial distribution of the asteroid belt.

This project translates celestial mechanics into a dynamic visual model, illustrating how long-term gravitational perturbations drive orbital instability.

## 🔭 Physical Interpretation

- **Why resonances matter:** They demonstrate that the solar system is not a collection of static Keplerian ellipses, but a deeply coupled, interacting dynamical system.
- **Resonance vs. Stability:** While non-resonant asteroids (e.g., at $2.20\text{ AU}$) maintain stable, low-eccentricity orbits indefinitely, resonant bodies experience secular chaos.
- **From Math to Motion:** The animation contrasts a stable background asteroid with a resonant chaotic asteroid, tracking both its spatial trajectory and its growing eccentricity on a phase space graph until it crosses the Mars barrier.

## ⚙️ Pipeline & Implementation (Concise)

The visualization is built using programmatic mathematical animation:
- **Orbital Mechanics:** Computes instantaneous conic-section orbital paths and heliocentric coordinates under forced eccentricity evolution.
- **Synchronized Dynamics:** Simulates Jupiter's orbital period alongside test-particle asteroid motion.
- **Phase Space Evolution:** Simultaneously plots eccentricity vs. time, marking the critical Mars-crossing threshold.

## 🚀 Usage

To render the Manim animation locally:
```bash
manim -pqh kirkwood_chaos_scene.py KirkwoodResonanceChaos
