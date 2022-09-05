import argparse

from boids.animation import Simulation
from boids.model import DynamicsModel


def main(params, mode):

    dynamics_model = DynamicsModel(params['model'])

    if mode == 'simulation':
        simulation = Simulation(dynamics_model, params['animation'])
        simulation.run()

    elif mode == 'profiling':
        for i in range(params['num_steps']):
            dynamics_model.update()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # common args
    parser.add_argument('-mx', '--max_x_value', type=float, default=1500.0)
    parser.add_argument('-my', '--max_y_value', type=float, default=750.0)

    # fig args
    parser.add_argument('-fx', '--fig_size_x', type=float, default=10.0)
    parser.add_argument('-fy', '--fig_size_y', type=float, default=5.0)
    parser.add_argument('-sb', '--size_boids', type=int, default=10)

    # model args
    parser.add_argument('-no', '--no_blocks', action='store_true')
    parser.add_argument('-nb', '--num_boids', type=int, default=300)
    parser.add_argument('-mis', '--min_speed', type=float, default=2.0)
    parser.add_argument('-mas', '--max_speed', type=float, default=3.0)
    parser.add_argument('-m', '--margin', type=float, default=40.0)
    parser.add_argument('-avf', '--avoid_factor', type=float, default=1.0)
    parser.add_argument('-cf', '--cohesion_factor', type=float, default=0.005)
    parser.add_argument('-sf', '--separation_factor', type=float, default=0.05)
    parser.add_argument('-af', '--alignment_factor', type=float, default=0.05)
    parser.add_argument('-cd', '--cohesion_distance', type=float, default=75.0)
    parser.add_argument('-sd','--separation_distance', type=float, default=20.0)
    parser.add_argument('-ad', '--alignment_distance', type=float, default=75.0)
    parser.add_argument('-bb', '--boundary_behaviour', type=str,
        default='avoid')

    # init args
    parser.add_argument('-dt', '--dtype', type=str, default='float16')
    parser.add_argument('-p', '--profiling', action='store_true')
    parser.add_argument('-ns',  '--num_steps', type=int, default=100)
    parser.add_argument('-it', '--init_type', type=str, default='fixed_speed')
    parser.add_argument('-ixm', '--init_x_margin', type=float, default=200)
    parser.add_argument('-iym', '--init_y_margin', type=float, default=200)
    parser.add_argument('-is', '--init_speed', type=float, default=2.5)
    parser.add_argument('-idx', '--init_direct_x', type=float, default=1.0)
    parser.add_argument('-idy', '--init_direct_y', type=float, default=1.0)
    parser.add_argument('-ia', '--init_angle', type=float, default=45.0)
    parser.add_argument('-aw', '--angle_width', type=float, default=15.0)

    args = parser.parse_args()

    if args.no_blocks:
        use_blocks = False
    else:
        use_blocks = True

    if args.dtype in ['float16', 'float32', 'float64']:
        dtype = args.dtype
    else:
        raise ValueError('The `dtype` value should be one of the following:'
            ' `float16`, `float32` or `float64`.')

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
            'dtype': dtype,
            'use_blocks': use_blocks,
            'num_boids': args.num_boids,
            'x_bound': args.max_x_value,
            'y_bound': args.max_y_value,
            'margin': args.margin,
            'avoid_factor': args.avoid_factor,
            'cohesion_factor': args.cohesion_factor,
            'cohesion_distance': args.cohesion_distance,
            'separation_factor': args.separation_factor,
            'separation_distance': args.separation_distance,
            'alignment_factor': args.alignment_factor,
            'alignment_distance': args.alignment_distance,
            'min_speed': args.min_speed,
            'max_speed': args.max_speed,
            'boundary_behaviour': args.boundary_behaviour,
            'ranges_boids': { # TEMPORARY. FIX THESE WHEN READY TO BE SET.
                'dtype': dtype,
                'init_type': args.init_type,
                'x_pos_min': args.init_x_margin,
                'x_pos_max': args.max_x_value - args.init_x_margin,
                'y_pos_min': args.init_y_margin,
                'y_pos_max': args.max_y_value - args.init_y_margin,
                'init_speed': args.init_speed,
                'init_direction': [args.init_direct_x, args.init_direct_y], # CHANGE LATER ? (only used with fixed_velocity)
                'init_angle': args.init_angle,
                'angle_width': args.angle_width,
            },
        },
        'num_steps': args.num_steps
    }

    if args.profiling:
        mode = 'profiling'
    else:
        mode = 'simulation'

    main(params, mode)
