import math

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
        self.separation_distance = params['separation_distance']
        self.alignment_distance = params['alignment_distance']
        self.cohesion_distance = params['cohesion_distance']
        self.boundary_behaviour = params['boundary_behaviour']
        self.x_bound = params['x_bound']
        self.y_bound = params['y_bound']
        self.margin = params['margin']
        self.avoid_factor = params['avoid_factor']
        self.min_speed = params['min_speed']
        self.max_speed = params['max_speed']

        self._block_size = max(
            self.separation_distance,
            self.alignment_distance,
            self.cohesion_distance,
            )
        self._num_x_gird = math.ceil(self.x_bound/self._block_size)
        self._num_y_gird = math.ceil(self.y_bound/self._block_size)
        self._num_blocks = self._num_x_gird * self._num_y_gird

        # indeces of the boids in each block (empty set intialization)
        self._blocks = [set() for i in range(self._num_blocks)]

        # block indeces of each boid
        self._block_indeces = [self._block_index(self.boids_positions[i,:])
                               for i in range(self.num_boids)]

        # fill the correct indeces to the blocks
        for i in range(self.num_boids):
            ind = self._block_indeces[i]
            self._blocks[ind].add(i)

        # neighbour block indeces
        self._neighbour_inds = self._create_neighbours()

    def update(self):

        if self.boundary_behaviour == 'avoid':
            diff = self._avoid_boundary()
        elif self.boundary_behaviour == 'wrap':
            diff = np.zeros((self.num_boids, 2), dtype=float)
        else:
            raise ValueError('`boundary_behaviour` value should be either'
                ' `avoid` or `wrap`.')

        for i in range(self.num_boids):
            position = self.boids_positions[i]
            velocity = self.boids_velocities[i]
            pos_rest = np.delete(deepcopy(self.boids_positions), i, axis=0)
            vel_rest = np.delete(deepcopy(self.boids_velocities), i, axis=0)

            cohes_inds = np.where(
                (self.separation_distance <=
                 np.linalg.norm(pos_rest -position, axis=1)) &
                (np.linalg.norm(pos_rest -position, axis=1)
                 < self.cohesion_distance))[0]
            separ_inds = np.where(np.linalg.norm(pos_rest -position, axis=1)
                < self.separation_distance)[0]
            align_inds = np.where(
                (self.separation_distance <=
                 np.linalg.norm(pos_rest -position, axis=1)) &
                (np.linalg.norm(pos_rest -position, axis=1)
                 < self.alignment_distance))[0]

            if cohes_inds != []:
                diff[i,:] += self._cohesion(position, pos_rest[cohes_inds])
            if separ_inds != []:
                diff[i,:] += self._separation(position, pos_rest[separ_inds])
            if align_inds != []:
                diff[i,:] += self._alignment(velocity, vel_rest[align_inds])

        velocities = deepcopy(self.boids_velocities) + diff
        velocities = self._cut_off(velocities)

        if self.boundary_behaviour == 'avoid':
            self.boids_positions += velocities
        elif self.boundary_behaviour == 'wrap':
            self.boids_positions = self._wrap_around(
                self.boids_positions + velocities)
        self.boids_velocities = velocities

    def _cohesion(self, position, pos_others):

        mean = np.mean(pos_others, axis=0)

        return self.cohesion_factor * (mean -position)

    def _separation(self, position, pos_others):

        vec_sum = np.sum(position -pos_others, axis=0)

        return self.separation_factor * vec_sum

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

        diff_x_low = turn_speed * (xs_low < self.margin).astype(float)
        diff_y_low = turn_speed * (ys_low < self.margin).astype(float)
        diff_x_high = -1 * turn_speed * (xs_high < self.margin).astype(float)
        diff_y_high = -1 * turn_speed * (ys_high < self.margin).astype(float)

        avoid_diff_x = diff_x_low + diff_x_high
        avoid_diff_y = diff_y_low + diff_y_high
        avoid_diff = np.stack((avoid_diff_x, avoid_diff_y), axis=1)

        return avoid_diff

    def _wrap_around(self, positions):

        max_arr = np.array(
            [[self.x_bound, self.y_bound] for i in range(self.num_boids)])

        return np.remainder(positions, max_arr)

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

    def _block_index(self, vector):

        x_index = math.ceil(vector[0]/self._block_size)
        y_index = math.ceil(vector[1]/self._block_size)

        return (x_index * y_index) - 1

    def _create_neighbours(self):

        inds = []
        pairs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1), (0, 1), (1, 0),
            (1, 1)]
        for j in range(self._num_y_gird):
            for i in range(self._num_x_gird):
                neighbours = []
                for pair in pairs:
                    neigh_ind = self._get_neigh_ind((i, j), pair)
                    if neigh_ind is not None:
                        neighbours.append(neigh_ind)
                inds.append(neighbours)

        return inds

    def _get_neigh_ind(self, vector, pair):

        mx = self._num_x_gird - 1
        my = self._num_y_gird - 1

        if self.boundary_behaviour == 'avoid':
            if ((vector[0] + pair[0]) < 0) or ((vector[1] + pair[1]) < 0):
                return None
            elif ((vector[0] + pair[0]) > mx) or ((vector[1] + pair[1]) > my):
                return None
            else:
                grid_vec = (vector[0] + pair[0], vector[1] + pair[1])

        if self.boundary_behaviour == 'wrap':
            modulated = (
                (vector[0] + pair[0]) % (mx+1), (vector[1] + pair[1]) % (my+1))
            grid_vec = (modulated[0], modulated[1])

        return grid_vec[0] + self._num_x_gird * grid_vec[1]

    def _get_relevant_inds(self, boid_index):

        block_index = self._block_indeces[boid_index]
        neighbours = self._neighbour_inds[block_index]
        own_block_others = self._blocks[boid_index] - {boid_index}
        relevant_inds = own_block_others.union(*self._blocks[neighbours])

        return np.array(list(relevant_inds))
