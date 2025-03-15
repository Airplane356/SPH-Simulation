# 🌀 Smoothed-Particle Hydrodynamics (SPH) Simulation

A simple **Smoothed-Particle Hydrodynamics (SPH) simulation** developed with guidance from **Computer Science PhD students at the University of Toronto**. This project explores computational fluid dynamics using the Lagrangian Approach of particle-based simulation methods.

---

## 🚀 Features
✔️ Real-time SPH fluid simulation  
✔️ Time slider and speed controls  
✔️ Fully implemented boundary conditions

---

## 📸 Demo
![SPH Demo](https://github.com/user-attachments/assets/d8fa4798-7e74-4b9e-ab02-a748993b381a)

---

## 🛠️ The Theory 
1️⃣ Discretization 
Fluids are continuous in reality, but for simulation, we break them down into discrete particles.
Each SPH particle represents a small volume of fluid and influences its surroundings through a smoothing kernel.

2️⃣ Motion 
Each particle moves accordingly to Newton's second law, F=ma. We updated the positions by integrating with dt. 

3️⃣ Forces
The simulation uses two key forces: gravity and pressure forces. 
Gravity applies a downward force F=mg which results in an acceleration. 
Fluids resist compression, so pressure forces push particles apart if they are too close, maintaining near-constant density. 

The pressure force is computed by using the gradient of the pressure: 

<img width="123" alt="Screenshot 2025-03-14 at 21 03 32" src="https://github.com/user-attachments/assets/9838569a-81a2-46b6-bb98-7650724abfaa" />

The pressure gradient (∇𝑝) tells us how quickly and in what direction pressure changes. Since fluids naturally move from high-pressure to low-pressure areas, we negate the pressure force to ensure that particles are pushed outward from regions of high pressure. 


​<img width="420" alt="Screenshot 2025-03-14 at 21 04 23" src="https://github.com/user-attachments/assets/97dab5e0-f3ad-4d4e-a509-7a62b7068cf2" />

4️⃣ SPH Kernel
SPH particles interact through a kernel function that defines their influence range.
We will use the Gaussian Kernel:

<img width="260" alt="Screenshot 2025-03-14 at 21 05 02" src="https://github.com/user-attachments/assets/9dcbfd7f-64de-4059-b6d0-be2b1a6f8555" />

where: 
- d=x−y is the distance between two particles.
- h is the smoothing length, controlling how far the influence extends (similar to standard deviation on the normal distribution). 
The gradient (∇𝐺) of the kernel is:

<img width="316" alt="Screenshot 2025-03-14 at 21 05 31" src="https://github.com/user-attachments/assets/c7b37406-865a-4ef4-9661-81bb094468d5" />

5️⃣ Density 

Each particle has a local density, which is computed as:

<img width="219" alt="Screenshot 2025-03-14 at 21 05 47" src="https://github.com/user-attachments/assets/3668edac-4001-41e6-9e69-924e5e7a974d" />

where the sum runs over all neighboring particles. This means that each particle’s density is influenced by nearby particles.

6️⃣ Pressure 
The pressure at each particle is computed as:

<img width="209" alt="Screenshot 2025-03-14 at 21 06 08" src="https://github.com/user-attachments/assets/d5e56cec-bb36-4ab3-bc35-0222372a9a82" />

where: 
- 𝑝 is the pressure
- 𝜌 is the density
- 𝜌rest is the initial rest density
- 𝑘 is the "stiffness" constant

Using the Symmetric Gradient Formula (since the gradient of the original pressure function is not a very good pressure force)

<img width="425" alt="Screenshot 2025-03-14 at 21 06 26" src="https://github.com/user-attachments/assets/e8f8076f-e81c-4ee2-96d5-dff9cc9fe3bb" />

7️⃣ Apply
After computing the density, and pressure gradient, the force acting on each particle is calculated, resulting in acceleration from the pressure. 

8️⃣ Boundaries
We used fixed boundary particles define the simulation area.
Fluid particles collide with boundaries and experience repelling forces.
Boundary particles exert pressure forces on fluid particles, preventing most particles from passing through.

9️⃣ Optimizations: Vectorization & Performance
To make the simulation faster, we used NumPy vectorization. This allowed us to avoid high rendering times. 

## 👥 Acknowledgments
This project was developed with guidance from Computer Science PhD students at the University of Toronto.
Special thanks to:

- Abhishek Madan
- Mengfei Liu

## 📚 Resources

This simulation is based on the concepts from this SPH tutorial: https://sph-tutorial.physics-simulation.org/.


