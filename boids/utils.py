import matplotlib.pyplot as plt
import numpy as np


def random_states(num_points, params):

    if params['init_type'] == 'fixed_speed':
        x_positions = np.random.uniform(
            params['x_pos_min'], params['x_pos_max'], num_points)
        y_positions = np.random.uniform(
            params['y_pos_min'], params['y_pos_max'], num_points)
        positions = np.stack((x_positions, y_positions), axis=1)

        thetas = np.random.uniform(0, 2*np.pi, num_points)
        velocities = np.array([[np.cos(thetas[i]), np.sin(thetas[i])]
            for i in range(num_points)], dtype=float)

    elif params['init_type'] == 'fixed_velocity':
        x_positions = np.random.uniform(
            params['x_pos_min'], params['x_pos_max'], num_points)
        y_positions = np.random.uniform(
            params['y_pos_min'], params['y_pos_max'], num_points)
        positions = np.stack((x_positions, y_positions), axis=1)

        velocities = 1e-3 * np.ones((num_points, 2), dtype=float)

    return positions, velocities


def init_animation(params, boids_positions):

    # Dummy version (ADD USE OF params ETC. ...)
    fig = plt.figure(figsize=(params['size_x'], params['size_y']))
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_xlim(0, params['x_max']), ax.set_xticks([])
    ax.set_ylim(0, params['y_max']), ax.set_yticks([])

    boids_scatter = ax.scatter(boids_positions[:, 0], boids_positions[:, 1],
        s=params['size_boids'], lw=0.5, c=np.array([params['color_boids']]))

    return fig, boids_scatter
