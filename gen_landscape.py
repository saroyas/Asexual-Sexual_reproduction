# %%

import scipy as sp
import scipy.interpolate
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3


# %%

def grid_chosen_points_2D(range=100, resolution=3):
    k = complex(0, resolution)
    grid_x, grid_y = np.mgrid[-range:range:k, -range:range:k]
    points_chosen = np.vstack((grid_x.ravel(), grid_y.ravel())).T
    return points_chosen


def gen_rand_uniform(num_rand_points, min=0, max=200):
    rand_fitness_array = np.random.random_integers(min, max, num_rand_points)
    return rand_fitness_array


class Landscape2D():
    def __init__(self, points_chosen=[], points_fitness_values=[], spline=True):
        self.points_chosen = points_chosen
        self.points_fitness_values = points_fitness_values
        if spline == True:
            self.get_points = self.spline_landscape_getter()
        else:
            self.get_points = self.rbf_landscape_getter()

    def rbf_landscape_getter(self):
        '''
        Rbf method is more robust, in that it extrapolates outside the points!
        But we may not really want this tbh, since outside is only implicitily defined
        '''
        rbf_land = sp.interpolate.Rbf(self.points_chosen[:, 0], self.points_chosen[:, 1]
                                      , self.points_fitness_values, function='cubic')
        return rbf_land

    def spline_landscape_getter(self):
        spline_land = scipy.interpolate.CloughTocher2DInterpolator(self.points_chosen, self.points_fitness_values)
        return spline_land

    def draw(self, elevation_deg=80, rotation_deg=-90, mesh=False):
        def get_grid_range():
            xrange_min, xrange_max = np.min(self.points_chosen[:, 0]), np.max(self.points_chosen[:, 0])
            yrange_min, yrange_max = np.min(self.points_chosen[:, 1]), np.max(self.points_chosen[:, 1])
            grid_x, grid_y = np.mgrid[xrange_min:xrange_max, yrange_min:yrange_max]
            return grid_x, grid_y

        grid_x, grid_y = get_grid_range()
        # generate the full landscape in that area, sometimes computationally intensive
        fitness_grid = self.get_points(grid_x, grid_y)
        fig = p.figure()
        ax = p3.Axes3D(fig)
        if mesh == True:
            ax.plot_wireframe(grid_x, grid_y, fitness_grid, color='black')
        else:
            ax.contour3D(grid_x, grid_y, fitness_grid, 50, cmap=plt.cm.viridis)
        ax.set_xlabel('loci_0')
        ax.set_ylabel('loci_1')
        ax.set_zlabel('Fitness')
        ax.view_init(elevation_deg, rotation_deg)
        p.show()