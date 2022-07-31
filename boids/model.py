import numpy as np

from boids.utils import random_states
from copy import deepcopy


class DynamicsModel:
    """Class for modelling the boids movements."""

    def __init__(self, params):

        boids_positions, boids_velocities = random_states(
            params['num_boids'], params['ranges_boids'])

        self.num_boids = params['num_boids']
        self.boids_positions = boids_positions
        self.boids_velocities = boids_velocities
        self.separation_factor = params['separation_factor']
        self.alignment_factor = params['alignment_factor']
        self.cohesion_factor = params['cohesion_factor']
        self.separation_distance = params['separation_ratio'] * params['x_bound']
        self.alignment_distance = params['alignment_ratio'] * params['x_bound']
        self.cohesion_distance = params['cohesion_ratio'] * params['x_bound']
        self.x_bound = params['x_bound']
        self.y_bound = params['y_bound']
        self.margin = params['margin']
        self.avoid_factor = params['avoid_factor']
        self.min_speed = params['min_speed']
        self.max_speed = params['max_speed']

    def update(self):

        diff = self._avoid_boundary()

        for i in range(self.num_boids):
            position = self.boids_positions[i]
            velocity = self.boids_velocities[i]
            pos_rest = np.delete(deepcopy(self.boids_positions), i, axis=0)
            vel_rest = np.delete(deepcopy(self.boids_velocities), i, axis=0)

            cohes_inds = np.where(np.linalg.norm(pos_rest -position, axis=1)
                < self.cohesion_distance)[0]
            separ_inds = np.where(np.linalg.norm(pos_rest -position, axis=1)
                < self.separation_distance)[0]
            align_inds = np.where(np.linalg.norm(pos_rest -position, axis=1)
                < self.alignment_distance)[0]

            if cohes_inds != []:
                diff[i,:] += self._cohesion(position, pos_rest[cohes_inds])
            if separ_inds != []:
                diff[i,:] += self._separation(position, pos_rest[separ_inds])
            if align_inds != []:
                diff[i,:] += self._alignment(velocity, vel_rest[align_inds])

        # print(diff[i,:])
        velocities = deepcopy(self.boids_velocities) + diff
        velocities = self._cut_off(velocities)
        self.boids_positions += velocities
        self.boids_velocities = velocities

    def _cohesion(self, position, pos_others):

        mean = np.mean(pos_others, axis=0)

        return self.cohesion_factor * (mean -position)

    def _separation(self, position, pos_others):

        mean = np.mean(pos_others, axis=0)

        return self.separation_factor * (position -mean)

    def _alignment(self, velocity, vel_others):

        mean = np.mean(vel_others, axis=0)

        return self.alignment_factor * (mean -velocity)

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
            ys_low < self.margin * self.x_bound).astype(float)
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
