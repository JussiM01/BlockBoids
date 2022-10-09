# BlockBoids
NumPy array based Boids simulation optimized with spatial tiling.

<p align="middle">
  <img src="./pics/frame_1st.png" width="49%" />
  <img src="./pics/frame_2nd.png" width="49%" />
</p>

The images above show two frames from the simulation.

## Intro
The Boids model is used for simulating the flocking behavior of birds and the
name comes from the abbreviation of "bird-oid object" which refers to a
bird-like object. The model uses three simple movement rules: alignment,
cohesion and separation.

These rules compare boids positions and velocities with the other boids and
adjust the velocities based on the average differences. This is done inside a
sphere of given distance radius for each boid. I use separate variables for
the distances corresponding to each rule in the code. Many sources use only
two variables (one for the alignment and cohesion and another one for the
separation).

#### Optimizations
The implementation uses NumPy array based manipulations for computing each
boid's position and velocity updates. Also, instead of using all the other
boids in these computations, only the boids from the relevant rectangular areas
are used. This is done by dividing the position space into rectangular tiles
which I decided to call blocks. These blocks are squares whose side length is
defined by

<p align="center">
  <i>
  length = max(alignment distance, cohesion distance, separation distance)
  </i>
<p>

(boundary facing blocks might have reduced size). For each boid only the boids
from the same block and from the blocks next to it in each direction are needed
for the updates.

## Installation
Clone this repository and install the libraries with pip:
```
git clone https://github.com/JussiM01/BlockBoids
cd BlockBoids/
pip install -r requirements.txt
```
I used Python 3.8 but the code probably works also with slightly earlier or
later versions. It was tested only with a computer that has Ubuntu as the
operating system. The animation is done with matplotlib and may need some
tweaks on other operating systems.

## How to use

### Basic use
For running the program with the default values use the following command:
```
python3 -m boids
```

### Changing the default values
The program uses command line arguments for changing the default parameter
values. Here only the main parameters and the ones which have slightly
non-trivial behavior are described.

Full list of the options and their descriptions along with the default values
can be printed out by using the help flag:
```
python3 -m boids -h
```

#### Model's main parameters
Number of boids is changed with the ```-nb``` option. The distances can be
changed with ```-ad```, ```-cd``` and ```-sd``` which stand for
alignment distance, cohesion distance and separation distance. The related
strength factors are controlled with the options ```-af```, ```-cf```
and ```-sf```. For example the command:
```
python3 -m boids -nb 100 -sd 40.0 -af 0.1
```
will run the simulation with 100 boids, using 40.0 separation distance and 0.1
alignment factor.

For computation time comparison purposes the use of blocks can be turned off.
This is done by using the no_blocks flag as follows:
```
python3 -m boids -no
```

#### Boundary behavior
There are two types of boundary behaviors available. These are avoid and wrap.
The first one which is the default choice turns the boids away from the canvas
boundaries when they get close enough to them. The second choice causes the
boids to reappear from the opposite side when they exit the canvas. For the
later behavior use the boundary_behavior flag as follows:
```
python3 -m boids -bb wrap
```

#### Positions and velocities
The boids' positions and velocities are initialized randomly. There are three
types of ways to do this: fixed_speed, fixed_velocity and angle_range. The
default is the fixed_speed. All these methods use init_x_margin and
init_y_margin and init_speed for the boids' state initialization. The default
values for these are 200.0, 200.0 and 2,5. These can be changed as follows:
```
python3 -m boids -ixm 100.0 -iym 50.0 -is 3.0
```
where the example command above sets the x-margin to 100.0, y-margin to 50.0
and all boids speeds to 3.0. This means that the boids are initialized inside a
box which stops at 100.0 units away from left and right canvas boundaries
and similarly 50.0 units from the top and bottom. The directions of the boids'
initial velocities are uniformly random but they all have the init_speed length.

The fixed_velocity initialization sets all the boids' initial velocities to
same value. This can be used as follows:
```
python3 -m boids -it fixed_velocity -idx 1.0 -idy 0.0
```
where the above example command sets all the boids' initial velocities
x-components to 1.0 and y-components to 0.0. The directional vectors will be
scaled to have init_speed length. Error will be thrown if the both components
are simultaneously zeros.

The angle_range initialization uses initial_angle and angle_width parameters.
The boids' velocity direction angles are sampled from an uniform distribution
where the mean is the initial_angle and the interval width is the angle_width.
This can be set as follows:
```
python3 -m boids -it angle_range -ia 90.0 -aw 60.0
```
The above example samples the velocities direction angles between the angles
60.0 and 120.0 degrees with respect to the positive x-axis. Again the velocity
vectors will be scaled to have the init_speed length.

There are also minimum and maximum values for the boids velocities which will
also overwrite the init_speed if its value is not in between them (boundaries
included). Their default values are 2.0 and 3.0. These can be changed as
follows:
```
python3 -m boids -mis 1.0 -mas 4.0
```
In the example above the minimum speed is set to 1.0 and maximum speed is set
to 4.0.

#### Random seed
For reproducibility purposes it is possible to use the random_seed flag as
follows:
```
python3 -m boids -r <seed>
```
where ```<seed>``` stands for the integer value for the random seed.

#### Profiling
The profiling option runs the simulation without the animation for the duration
of given amount of update steps. It is meant to be used with the cProfiler. For
running it with the default amount of update steps use:
```
python3 -m cProfile -m boids -p
```
The number of update steps can be changed with the num_steps flag as follows:
```
python3 -m cProfile -m boids -p -ns <number of steps>
```
where ```<number of steps>``` is the integer value for the amount of steps.

This functionality has been added mainly for the purpose of testing the
effectiveness of the block structure. Namely, one can run the profiling with
some number of boids and a random seed, for example 100 boids and 123 as
the value of the random seed:
```
python3 -m cProfile -m boids -nb 100 -r 123 -p
```
and then run the same command with the no_blocks flag added to it:
```
python3 -m cProfile -m boids -nb 100 -r 123 -p -no
```

## Computation time comparison
I ran the profiling with a fixed random seed for a few different numbers of
boids with and without the blocks. Without the blocks the computation time
growth began to look quadratic whereas with them it was fairly linear. The
exact time values will of course depend on the used hardware.

<p align="middle">
  <img src="./pics/Figure_1.png" width="60%" />
</p>

## Closing thoughts
Without the blocks the model compares each boid with all the other boids which
explains the quadratic time growth. When the blocks are used the growth should
be roughly linear provided that the average count of the boids within each
boid's relevant blocks stays close to a constant. If the size of the space
dimensions are kept same this will be violated at some point when the total
number of boids grows large enough.

The algorithm performs faster if the block size is reduced by scaling all the
distance parameters smaller. This however weakens the flocking effect and makes
it more likely that the boids are split into several smaller groups.

One thing that I didn't optimize is the loop over all boids. I thought that
it would be interesting to do this with parallel processing on a GPU with
PyTorch tensors. This will be implemented in a separate project since the block
structure is not supported by the tensor based batch processing. Link to the
project will be added here when it's ready.

## Sources
General information about the Boids model is available in a
[Wikipedia article](https://en.wikipedia.org/wiki/Boids).
More details about the original model can be found from its inventor's
[Boids page](https://www.red3d.com/cwr/boids/). The idea for trying out the
block structure came to us from a research oriented
[blog post](https://adamprice.io/blog/boids.html). Before starting the project
I searched on the net for a good pseudocode presentation of the basic Boids
algorithm and found a very good one from this microcontroller
[lab exercise](https://people.ece.cornell.edu/land/courses/ece4760/labs/s2021/Boids/Boids.html) page.
