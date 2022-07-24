import numpy as np

from boids.utils import random_states


class Model:
    """Class for modelling the boids movements."""

    def __init__(self, params):

        boids_positions, boids_velocities = random_states(
            params['num_boids'], params['ranges_boids'])

        self.num_boids = params['num_boids']
        self.boids_positions = boids_positions
        self.boids_velocities = boids_velocities
        # self.separation_scale = params['separation_scale']
        # self.alignment_scale = params['alignment_scale']
        # self.cohesion_scale = params['cohesion_scale']
        # self.separation_distance = params['separation_distance']
        # self.alignment_distance = params['alignment_distance']
        # self.cohesion_distance = params['cohesion_distance']
        # self.x_bound = params['x_bound']
        # self.y_bound = params['y_bound']
        # self.max_speed = params['max_speed']

        self._new_b_positions = np.zeros((self.num_boids, 2), dtype=float)
        self._new_b_velocities = np.zeros((self.num_boids, 2), dtype=float)

    def update(self):

        # Dummy version
        self._dummy_update()

    def _dummy_update(self): # TEMPORARY, REMOVE WHEN THE ACTUAL UPDATE EXISTS.
        self.boids_positions += self.boids_velocities
