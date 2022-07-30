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
    parser.add_argument('-mx', '--max_x_value', type=float, default=2000.0)
    parser.add_argument('-my', '--max_y_value', type=float, default=2000.0)

    # fig args
    parser.add_argument('-fx', '--fig_size_x', type=float, default=10.0)
    parser.add_argument('-fy', '--fig_size_y', type=float, default=5.0)
    parser.add_argument('-sb', '--size_boids', type=int, default=10)

    # model args
    parser.add_argument('-nb', '--num_boids', type=int, default=1000)
    parser.add_argument('-spr', '--speed_ratio', type=float, default=0.5)
    parser.add_argument('-ms', '--max_speed', type=float, default=3.0)
    parser.add_argument('-m', '--margin', type=float, default=0.05)
    parser.add_argument('-avf', '--avoid_factor', type=float, default=0.02)
    parser.add_argument('-cf', '--cohesion_factor', type=float, default=0.01)
    parser.add_argument('-sef', '--separation_factor', type=float, default=0.01)
    parser.add_argument('-af', '--alignment_factor', type=float, default=0.01)
    parser.add_argument('-cr', '--cohesion_ratio', type=float, default=0.1)
    parser.add_argument('-ser','--separation_ratio', type=float, default=0.05)
    parser.add_argument('-ar', '--alignment_ratio', type=float, default=0.025)

    # init args
    parser.add_argument('-it', '--init_type', type=str, default='fixed_speed')
    parser.add_argument('-ir', '--init_ratio', type=float, default=0.1)
    parser.add_argument('-is', '--init_speed', type=float, default=2.5)
    parser.add_argument('-idx', '--init_direct_x', type=float, default=1.0)
    parser.add_argument('-idy', '--init_direct_y', type=float, default=1.0)

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
            'cohesion_factor': args.cohesion_factor,
            'cohesion_ratio': args.cohesion_ratio,
            'separation_factor': args.separation_factor,
            'separation_ratio': args.separation_ratio,
            'alignment_factor': args.alignment_factor,
            'alignment_ratio': args.alignment_ratio,
            'min_speed': args.max_speed * args.speed_ratio,
            'max_speed': args.max_speed,
            'ranges_boids': { # TEMPORARY. FIX THESE WHEN READY TO BE SET.
                'init_type': args.init_type,
                'x_pos_min': args.init_ratio * args.max_x_value,
                'x_pos_max': (1 - args.init_ratio) * args.max_x_value,
                'y_pos_min': args.init_ratio * args.max_y_value,
                'y_pos_max': (1 - args.init_ratio) * args.max_y_value,
                'init_speed': args.init_speed,
                'init_direction': [args.init_direct_x, args.init_direct_y], # CHANGE LATER ? (only used with fixed_velocity)
            },

        },
    }

    main(params)
