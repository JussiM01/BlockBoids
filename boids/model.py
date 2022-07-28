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
        self.x_bound = params['x_bound']
        self.y_bound = params['y_bound']
        self.margin = params['margin']
        self.avoid_factor = params['avoid_factor']
        self.min_speed = params['min_speed']
        self.max_speed = params['max_speed']

    def update(self):

        # Dummy version
        dummy_diff = self._dummy_update()
        diff = dummy_diff

        diff += self._avoid_boundary()

        velocities = deepcopy(self.boids_velocities) + diff
        velocities = self._cut_off(velocities)
        self.boids_positions += velocities
        self.boids_velocities = velocities

    def _dummy_update(self): # TEMPORARY, REMOVE WHEN THE ACTUAL UPDATE EXISTS.
        return np.zeros((self.num_boids, 2), dtype=float)

    def _avoid_boundary(self):

        turn_speed = self.avoid_factor * self.max_speed
        xs = self.boids_positions[:,0]
        ys = self.boids_positions[:,1]
        xs_low = abs(self.boids_positions[:,0])
        ys_low = abs(self.boids_positions[:,1])
        xs_high = abs(self.x_bound - xs)
        ys_high = abs(self.y_bound - ys)

        diff_x_low = turn_speed * (
            xs_low < self.margin * self.x_bound).astype(float)
        diff_y_low = turn_speed * (
            ys_low < self.margin * self.y_bound).astype(float)
        diff_x_high = -1 * turn_speed * (
            xs_high < self.margin * self.x_bound).astype(float)
        diff_y_high = -1 * turn_speed * (
            ys_high < self.margin * self.x_bound).astype(float)

        avoid_diff_x = diff_x_low + diff_x_high
        avoid_diff_y = diff_y_low + diff_y_high
        avoid_diff = np.stack((avoid_diff_x, avoid_diff_y), axis=1)

        return avoid_diff

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
