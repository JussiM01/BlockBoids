import argparse

from boids.animation import Animation
from boids.model import Model


def main(params):

    dynamics_model = Model(params['model'])
    simulation = Animation(dynamics_model, params['animation'])
    simulation.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-fx', '--fig_size_x', type=float, default=7.0)
    parser.add_argument('-fy', '--fig_size_y', type=float, default=7.0)
    parser.add_argument('-mx', '--max_x_value', type=float, default=1.0)
    parser.add_argument('-my', '--max_y_value', type=float, default=1.0)
    parser.add_argument('-sb', '--size_boids', type=int, default=10)

    args = parser.parse_args()

    params = {
        'animation': {
            'size_x': args.fig_size_x,
            'size_y': args.fig_size_y,
            'x_max': args.max_x_value,
            'y_max': args.max_y_value,
            'size_boids': args.size_boids,
            'color_boids': (0, 0, 0, 1),
        },
        'model': {
            'num_boids': 100,
            'ranges_boids': { # TEMPORARY. FIX THESE WHEN READY TO BE SET.
                'x_pos_min': 0.25,
                'x_pos_max': 0.5,
                'x_pos_min': 0.25,
                'x_pos_max': 0.5,
                'x_vel_min': -0.25,
                'x_vel_max': 0.25,
                'x_vel_min': -0.25,
                'x_vel_max': 0.25,
            },

        },
    }

    main(params)
