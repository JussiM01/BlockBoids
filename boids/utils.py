import matplotlib.pyplot as plt
import numpy as np


def random_states(num_points, scales):

    # Dummy version (ADD USE OF SCALES ETC. ...)
    positions = 0.25 * np.random.uniform(0, 1, (num_points, 2))
    velocities = 1e-3 * np.ones((num_points, 2), dtype=float)

    return positions, velocities


def init_animation(params, boids_positions):

    # Dummy version (ADD USE OF SCALES ETC. ...)
    fig = plt.figure(figsize=(params['size_x'], params['size_y']))
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_xlim(0, params['x_max']), ax.set_xticks([])
    ax.set_ylim(0, params['y_max']), ax.set_yticks([])

    boids_scatter = ax.scatter(boids_positions[:, 0], boids_positions[:, 1],
        s=params['size_boids'], lw=0.5, c=params['color_boids'])

    return fig, boids_scatter
