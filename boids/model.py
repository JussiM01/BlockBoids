import numpy as np

from boids.utils import random_states
from copy import deepcopy


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
        self.min_speed = params['min_speed']
        self.max_speed = params['max_speed']

    def update(self):

        # Dummy version
        dummy_diff = self._dummy_update()
        diff = dummy_diff

        velocities = deepcopy(self.boids_velocities) + diff
        velocities = self._cut_off(velocities)
        self.boids_positions += velocities
        self.boids_velocities = velocities

    def _dummy_update(self): # TEMPORARY, REMOVE WHEN THE ACTUAL UPDATE EXISTS.
        return np.zeros((self.num_boids, 2), dtype=float)

    def _cut_off(self, velocities):

        def cut(velocity):
            norm = np.linalg.norm(velocity)
            if norm < self.min_speed:
                return self.min_speed * velocity/norm
            elif norm > self.max_speed:
                normalized = velocity/norm
                return self.max_speed * velocity/norm
            else:
                return velocity

        return np.apply_along_axis(lambda v: cut(v), 1, velocities)
