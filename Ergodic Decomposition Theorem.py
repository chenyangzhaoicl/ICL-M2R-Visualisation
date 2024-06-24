import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Ellipse

# Parameters
alpha = np.sqrt(2)  # irrational number
v = np.array([alpha, 1, 0])  # direction of the flow

# Time steps
T = 1000
t = np.linspace(0, 10, T)

# Define the sphere parameters
sphere_center = np.array([0.5, 0.5, 0.5])
sphere_radius = 0.25

# Initial points in the torus with z-values within the range of the sphere
num_points = 5
initial_points = np.random.rand(num_points, 3)
initial_points[:, 2] = sphere_center[2] - sphere_radius + 2 * sphere_radius * np.random.rand(num_points)  # z-values within the sphere range

# Flow on T^3
def flow(point, t):
    return (point + v * t) % 1

# Flow on the subtorus T_x
def subtorus_flow(x, point, t):
    sub_v = np.array([0, 1, 0])
    return (point + sub_v * t) % 1

# Function to plot trajectories with teleportation handling
def plot_trajectories(ax, points, colors, flow_func, t):
    for point, color in zip(points, colors):
        trajectory = np.array([flow_func(point, t_i) for t_i in t])
        ax.scatter(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], c=color, s=1)

# Distinct colors for better contrast
distinct_colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']

# Plotting
fig = plt.figure(figsize=(18, 8))

# Plot on T^3
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title("Visualization of Ergodic Decomposition in the Flow on $\mathbb{T}^3$")
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_zlim(0, 1)
ax1.set_xlabel("$x$")
ax1.set_ylabel("$y$")
ax1.set_zlabel("$z$")
ax1.grid(True)

# Non-ergodic flow on T^3
plot_trajectories(ax1, initial_points, distinct_colors, flow, t)

# Add a semi-transparent sphere in the middle to represent the subtorus
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = sphere_center[0] + sphere_radius * np.cos(u) * np.sin(v)
y = sphere_center[1] + sphere_radius * np.sin(u) * np.sin(v)
z = sphere_center[2] + sphere_radius * np.cos(v)
ax1.plot_surface(x, y, z, color='blue', alpha=0.1)

# Add smoother and less visible sphere border
ax1.plot_wireframe(x, y, z, color='blue', alpha=0.2, linewidth=0.5)

# Plot on the subtorus T_x
ax2 = fig.add_subplot(122)
ax2.set_title("Flow on $T_x \subset \mathbb{T}^3$")
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_xlabel("$y$")
ax2.set_ylabel("$z$")
ax2.grid(True)

# Ergodic flow on T_x
x_fixed = 0.5  # fixed x coordinate
for point, color in zip(initial_points, distinct_colors):
    trajectory = np.array([subtorus_flow(x_fixed, point, t_i) for t_i in t])
    ax2.scatter(trajectory[:, 1], trajectory[:, 2], c=color, s=1)

# Add the projection of the sphere on the subtorus
ellipse = Ellipse((sphere_center[1], sphere_center[2]), 2*sphere_radius, 2*sphere_radius, linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.1)
ax2.add_patch(ellipse)

# Plot the origin axes on T^3
ax1.plot([0, 1], [0, 0], [0, 0], color='k', linewidth=1)
ax1.plot([0, 0], [0, 1], [0, 0], color='k', linewidth=1)
ax1.plot([0, 0], [0, 0], [0, 1], color='k', linewidth=1)

plt.tight_layout()
plt.show()
