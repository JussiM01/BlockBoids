import matplotlib.pyplot as plt
import numpy as np


def random_states(num_points, params):

    x_positions = np.random.uniform(
        params['x_pos_min'], params['x_pos_max'], num_points)
    y_positions = np.random.uniform(
        params['y_pos_min'], params['y_pos_max'], num_points)
    positions = np.stack((x_positions, y_positions), axis=1)

    if params['init_type'] == 'fixed_speed':
        thetas = np.random.uniform(0, 2*np.pi, num_points)
        velocities = params['init_speed'] * np.array(
            [[np.cos(thetas[i]), np.sin(thetas[i])]
             for i in range(num_points)], dtype=float)

    elif params['init_type'] == 'fixed_velocity':
        init_direction = np.array(params['init_direction'], float)
        norm = np.linalg.norm(init_direction)
        if norm == 0:
            raise ValueError('Args `init_direct_x` and `init_direct_y`'
                ' are not allowed to be simultaniously zeros.')
        normalized = init_direction / norm
        velocities = params['init_speed'] * np.array(
            [normalized for i in range(num_points)], dtype=float)

    elif params['init_type'] == 'angle_range':
        angle = params['init_angle'] * np.pi / 180
        limit = params['angle_width'] * np.pi / 90
        thetas = np.random.uniform(angle - limit, angle + limit, num_points)
        velocities = params['init_speed'] * np.array(
            [[np.cos(thetas[i]), np.sin(thetas[i])]
             for i in range(num_points)], dtype=float)

    else:
        raise ValueError('`init_type` value should be one of: `fixed_speed`,'
            ' `fixed_velocity`, `angle_range`.')

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
