import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import imageio
import os

# Function to create and save frames for the GIF
def create_2d_torus_flow(a, b, num_frames=20000, output_dir='2d_torus_flow_frames', small_square_side=0.25):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize trajectory and small square
    x, y = 0.0, 0.0
    small_square_x, small_square_y = 0.25, 0.25
    times_in_square = []
    trajectory = []
    proportions = []

    for i in range(num_frames):
        # Compute new position with wrap-around (mod 1)
        x = (x + a) % 1  # Applying modulo 1 arithmetic to x
        y = (y + b) % 1  # Applying modulo 1 arithmetic to y
        trajectory.append((x, y))

        # Check if the point is inside the small square
        if small_square_x <= x < small_square_x + small_square_side and small_square_y <= y < small_square_y + small_square_side:
            times_in_square.append(i)

        # Calculate the proportion of time spent inside the small square
        proportion_in_square = len(times_in_square) / (i + 1)
        proportions.append(proportion_in_square)

        # Save every frame
        if i % 100 == 0:  # Adjust the frame saving frequency for performance
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.set_title(f"2D Torus Flow in a 2-Torus (Frame {i})")
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            # Plot the trajectory points
            ax.scatter([p[0] for p in trajectory], [p[1] for p in trajectory], c='r', s=1)  # Small red dots for points

            # Add the small square with darker shading
            rect = Rectangle((small_square_x, small_square_y), small_square_side, small_square_side, linewidth=1, edgecolor='b', facecolor='blue', alpha=0.3)
            ax.add_patch(rect)

            # Add start and end points
            ax.scatter([trajectory[0][0]], [trajectory[0][1]], c='g', s=50, label='Start')
            ax.scatter([trajectory[-1][0]], [trajectory[-1][1]], c='b', s=50, label='End')

            frame_path = os.path.join(output_dir, f'frame_{i:05d}.png')
            plt.savefig(frame_path)
            plt.close(fig)

    return output_dir, trajectory, proportions

# Function to create the GIF from frames
def create_gif_from_frames(output_dir='2d_torus_flow_frames', gif_name='2d_torus_flow_animation.gif'):
    frames = []
    for frame in sorted(os.listdir(output_dir)):
        if frame.endswith('.png'):
            frame_path = os.path.join(output_dir, frame)
            frames.append(imageio.imread(frame_path))
    gif_path = os.path.join(output_dir, gif_name)
    imageio.mimsave(gif_path, frames, duration=0.1)
    return gif_path

# Function to plot the proportion of time spent inside the small square over time
def plot_proportion_over_time(proportions, file_name='proportion_over_time.png'):
    fig, ax = plt.subplots()
    ax.plot(proportions, label='Proportion in Small Square')
    ax.axhline(y=0.0625, color='r', linestyle='--', label='Expected Proportion (0.0625)')
    ax.set_xlabel('Time Frame')
    ax.set_ylabel('Proportion Inside the Small Square')
    ax.set_title('Proportion of Time Spent Inside the Small Square Over Time in a 2-Torus')
    ax.legend()
    plt.savefig(file_name)
    plt.close(fig)

# Generate and plot the 2D torus flow visualization
phi = (1 + np.sqrt(5)) / 2  # Golden ratio
a_irrational, b_irrational = 1/1000, phi/1000  # Irrational direction scaled for smaller steps

# Create flows for irrational direction
output_dir_irrational, trajectory_irrational, proportions_irrational = create_2d_torus_flow(a_irrational, b_irrational, num_frames=20000, output_dir='2d_torus_flow_irrational_frames', small_square_side=0.25)

# Create GIFs
gif_path_irrational = create_gif_from_frames(output_dir=output_dir_irrational, gif_name='2d_torus_flow_irrational.gif')

print(f"Irrational direction flow visualization saved as {gif_path_irrational}")

# Plot proportions over time
plot_proportion_over_time(proportions_irrational, file_name='proportion_over_time_irrational.png')

# Create combined static image showing the entire route
def create_combined_image(trajectory, title, file_name):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.scatter([p[0] for p in trajectory], [p[1] for p in trajectory], c='r', s=1)  # Small red dots for points

    # Add the small square with darker shading
    rect = Rectangle((0.25, 0.25), 0.25, 0.25, linewidth=1, edgecolor='b', facecolor='blue', alpha=0.3)
    ax.add_patch(rect)

    # Add start and end points
    ax.scatter([trajectory[0][0]], [trajectory[0][1]], c='g', s=50, label='Start')
    ax.scatter([trajectory[-1][0]], [trajectory[-1][1]], c='b', s=50, label='End')

    plt.savefig(file_name)
    plt.close(fig)

# Save combined image
create_combined_image(trajectory_irrational, "Irrational Direction Flow in a 2-Torus", "2d_torus_flow_irrational.png")
