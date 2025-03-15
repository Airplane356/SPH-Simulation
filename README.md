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
​
![pressure gradient](https://github.com/user-attachments/assets/47d715c4-230b-4a5a-8940-952844a0ad9f)

4️⃣ SPH Kernel
SPH particles interact through a kernel function that defines their influence range.
We will use the Gaussian Kernel:
![Gaussian kernel](https://github.com/user-attachments/assets/ff48c081-e432-4601-a181-dc1d9fc80cae)

where: 
- d=x−y is the distance between two particles.
- h is the smoothing length, controlling how far the influence extends (similar to standard deviation on the normal distribution). 
The gradient (∇𝐺) of the kernel is:
![Gaussian gradient](https://github.com/user-attachments/assets/0bf03a2c-865d-47d7-8b14-91def75af7eb)

5️⃣ Density 

Each particle has a local density, which is computed as:
![density function](https://github.com/user-attachments/assets/ca20a2fe-1c17-4fcc-981a-c2b40ffdebd0)

where the sum runs over all neighboring particles. This means that each particle’s density is influenced by nearby particles.

6️⃣ Pressure 
The pressure at each particle is computed as:
![pressure](https://github.com/user-attachments/assets/744a7c60-b54c-498e-8d22-ef84867e805f)

where: 
- 𝑝 is the pressure
- 𝜌 is the density
- 𝜌rest is the initial rest density
- 𝑘 is the "stiffness" constant

Using the Symmetric Gradient Formula (since the gradient of the original pressure function is not a very good pressure force)
![pressure gradient](https://github.com/user-attachments/assets/94af0bd0-22ac-4bdd-92ab-eae7156b7cd8)

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


