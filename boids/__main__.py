import argparse

from boids.animation import Animation
from boids.model import Model


def main(params):

    dynamics_model = Model(params['model'])
    simulation = Animation(dynamics_model, params['animation'])
    simulation.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # common args
    parser.add_argument('-mx', '--max_x_value', type=float, default=1.0)
    parser.add_argument('-my', '--max_y_value', type=float, default=1.0)

    # fig args
    parser.add_argument('-fx', '--fig_size_x', type=float, default=7.0)
    parser.add_argument('-fy', '--fig_size_y', type=float, default=7.0)
    parser.add_argument('-sb', '--size_boids', type=int, default=10)

    # model args
    parser.add_argument('-nb', '--num_boids', type=int, default=1000)
    parser.add_argument('-sr', '--speed_ratio', type=float, default=0.5)
    parser.add_argument('-ms', '--max_speed', type=float, default=1e-3)
    parser.add_argument('-m', '--margin', type=float, default=0.01)
    parser.add_argument('-avf', '--avoid_factor', type=float, default=1e-2)

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
            'num_boids': args.num_boids,
            'x_bound': args.max_x_value,
            'y_bound': args.max_y_value,
            'margin': args.margin,
            'avoid_factor': args.avoid_factor,
            'min_speed': args.max_speed * args.speed_ratio,
            'max_speed': args.max_speed,
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
