import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from boids.utils import init_animation


class Simulation:
    """Class for creating the animation for the boids movements."""

    def __init__(self, model, params):

        self.model = model
        boids_positions = model.boids_positions
        fig, boids_scatter = init_animation(params, boids_positions)
        fig.canvas.set_window_title('BlockBoids')
        self.fig = fig
        self.boids_scatter = boids_scatter

    def update(self, frame_number):

        self.model.update()
        updated_boids_pos = self.model.boids_positions
        self.boids_scatter.set_offsets(updated_boids_pos)

        return (self.boids_scatter,)

    def run(self):

        _ = FuncAnimation(self.fig, self.update, interval=0, blit=True)
        plt.show()
