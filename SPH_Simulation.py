import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# ParticleList Class
class ParticleList:
    def __init__(self, masses, positions, velocities, h, k, num_fluid_particles):
        self.masses = masses
        self.positions = positions
        self.velocities = velocities
        self.h = h
        self.k = k
        self.num_particles = positions.shape[0]
        self.num_fluid_particles = num_fluid_particles
        self.rest_densities = reconstruct_density(self)

# Function Definitions
def timestep(particles, g, dt):
    densities = reconstruct_density(particles)
    pressure_grads = eval_pressure_grad(particles, densities)
    velocities1 = apply_gravity_force(particles, g, dt)
    new_velocities = apply_pressure_force(particles, velocities1, densities, pressure_grads, dt)
    new_positions = update_positions(particles, new_velocities, dt)
    particles.positions = new_positions
    particles.velocities = new_velocities

def update_positions(particles, velocities, dt):
    """Update positions of particles"""
    positions_new = particles.positions.copy()
    positions_new[:particles.num_fluid_particles] += dt * velocities[:particles.num_fluid_particles]
    return positions_new

def apply_gravity_force(particles, g, dt):
    """Update velocities by gravity"""
    velocities_new = particles.velocities.copy()
    velocities_new[:particles.num_fluid_particles] += dt * g
    return velocities_new

def gaussian(d, h):
    """Gaussian Kernel"""
    return 1 / (h * np.sqrt(2 * np.pi)) * np.exp(-((np.linalg.norm(d, axis=-1)) ** 2) / (2 * (h**2)))

def reconstruct_density(particles):
    """Calculate density function"""
    densities = np.zeros(particles.num_particles)
    positions_diff = particles.positions[:, np.newaxis, :] - particles.positions[np.newaxis, :, :]
    densities = np.sum(particles.masses[np.newaxis, :] * gaussian(positions_diff, particles.h), axis=1)
    return densities

def eval_pressure(particles, densities):
    """Calculate pressure function"""
    pressures = particles.k * np.maximum((densities / particles.rest_densities) - 1, 0)
    return pressures

def gaussian_grad(d, h):
    """Gaussian Gradient"""
    dnorm = np.linalg.norm(d, axis=-1)[:, :, np.newaxis]
    return -1 / ((h**3) * np.sqrt(2 * np.pi)) * np.exp(-(dnorm**2) / (2 * (h**2))) * d

def eval_pressure_grad(particles, densities):
    """Pressure gradient function"""
    pressures = eval_pressure(particles, densities)
    positions_diff = particles.positions[:, np.newaxis, :] - particles.positions[np.newaxis, :, :]
    gaussian = gaussian_grad(positions_diff, particles.h)
    fraction_sum = (pressures[:, np.newaxis] / (densities[:, np.newaxis]**2) + pressures[:, np.newaxis] / (densities[:, np.newaxis]**2))
    pressure_grads = np.sum(densities[:, np.newaxis] * particles.masses[:, np.newaxis] * fraction_sum * gaussian, axis=1)
    return pressure_grads

def apply_pressure_force(particles, velocities, densities, pressure_grads, dt):
    """Calculate force function"""
    force = -1 / densities[:, np.newaxis] * pressure_grads
    return velocities + dt * force / particles.masses[:, np.newaxis]

# Initialize Particles
grid_dim = 20
num_fluid_particles = grid_dim * grid_dim
x = np.linspace(-0.2, 0.2, grid_dim)
y = np.linspace(0.2, 0.4, grid_dim)
xgrid, ygrid = np.meshgrid(x, y)
fluid_positions = np.stack((xgrid.flatten(), ygrid.flatten()), axis=1)

# Boundaries 
num_wall_particles = 50
num_boundary_particles = 4 * num_wall_particles

wall0_x = np.linspace(-0.5, 0.5, num_wall_particles + 1)[:-1]  # Bottom Boundary
wall0_y = np.zeros_like(wall0_x)

wall1_x = 0.5 * np.ones_like(wall0_x)  # Right Boundary
wall1_y = np.linspace(0, 1, num_wall_particles + 1)[:-1]

wall2_x = np.linspace(0.5, -0.5, num_wall_particles + 1)[:-1]  # Top Boundary
wall2_y = np.ones_like(wall2_x)

wall3_x = -0.5 * np.ones_like(wall0_x)  # Left Boundary
wall3_y = np.linspace(1, 0, num_wall_particles + 1)[:-1]

boundary_x = np.concatenate((wall0_x, wall1_x, wall2_x, wall3_x), axis=0)
boundary_y = np.concatenate((wall0_y, wall1_y, wall2_y, wall3_y), axis=0)
boundary_positions = np.stack((boundary_x, boundary_y), axis=1)

# Assemble the ParticleList instance and simulation constants 
positions = np.concatenate((fluid_positions, boundary_positions), axis=0)
velocities = np.zeros_like(positions)
masses = 0.1 * np.ones(positions.shape[0])
h = 0.02
k = 2.3
g = np.array([0, -1])
dt = 0.02
particles = ParticleList(masses, positions.copy(), velocities.copy(), h, k, num_fluid_particles)

# Precompute all frames
num_frames = 500
frame_data = []

for _ in range(num_frames):
    timestep(particles, g, dt)
    frame_data.append(particles.positions.copy())

# Create Plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.set_aspect('equal')
fluid_particles = frame_data[0][:num_fluid_particles]
boundary_particles = frame_data[0][num_fluid_particles:]
fp_scatter = ax.scatter(fluid_particles[:, 0], fluid_particles[:, 1], color='#7570b3', s=15)
bp_scatter = ax.scatter(boundary_particles[:, 0], boundary_particles[:, 1], color='#d95f02', s=15)

# Frame Slider
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Frame', 0, num_frames - 1, valinit=0, valfmt='%d')

# Play/Pause Buttons
ax_play = plt.axes([0.8, 0.02, 0.1, 0.04])
play_button = Button(ax_play, "Play")
ax_pause = plt.axes([0.68, 0.02, 0.1, 0.04])
pause_button = Button(ax_pause, "Pause")

# Speed Control Slider
ax_speed = plt.axes([0.2, 0.02, 0.4, 0.03])
speed_slider = Slider(ax_speed, 'Speed', 0.1, 5, valinit=1, valfmt='%.1fx')

running = False
speed = 1.0

def update(frame):
    """Update function to set new particle positions."""
    fluid_particles = frame_data[frame][:num_fluid_particles]
    boundary_particles = frame_data[frame][num_fluid_particles:]
    fp_scatter.set_offsets(fluid_particles)
    bp_scatter.set_offsets(boundary_particles)
    return fp_scatter, bp_scatter

def on_slider_update(val):
    """Update scatter plot"""
    if not running:
        frame = int(slider.val)
        update(frame)

slider.on_changed(on_slider_update)

def play_animation(event):
    """Play the animation."""
    global running
    running = True
    animate()

def pause_animation(event):
    """Pause the animation."""
    global running
    running = False

def animate():
    """Loop through frames."""
    global running
    frame = int(slider.val)
    while running and frame < num_frames:
        update(frame)
        plt.pause(0.02 / speed)  
        frame += 1
        slider.set_val(frame)

play_button.on_clicked(play_animation)
pause_button.on_clicked(pause_animation)

def update_speed(val):
    """Update animation speed."""
    global speed
    speed = speed_slider.val

speed_slider.on_changed(update_speed)

plt.show()
