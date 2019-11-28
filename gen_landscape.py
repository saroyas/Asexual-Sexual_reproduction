import scipy as sp
import scipy.interpolate
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3


class Landscape2D():
    def __init__(self, points_chosen=[], points_fitness_values=[]):
        self.points_chosen = points_chosen
        self.points_fitness_values = points_fitness_values
        self.get_points = self.gen_landscape()

    def gen_landscape(self):
        '''
        Rbf method is more robust, in that it extrapolates outside the points!
        But we may not really want this tbh, since outside is only implicitily defined
        and if the population goes there, our model doesnt really think about this.
        one solution might be to expand the borders, and increase the fitness range to conpensate
        the flattening of gradients
        '''
        spline = sp.interpolate.Rbf(self.points_chosen[:, 0], self.points_chosen[:, 1]
                                    , self.points_fitness_values, function='cubic')
        return spline

    def draw(self, elevation_deg=80, rotation_deg=-90, mesh=False):
        xrange_min, xrange_max = np.min(self.points_chosen[:, 0]), np.max(self.points_chosen[:, 0])
        yrange_min, yrange_max = np.min(self.points_chosen[:, 1]), np.max(self.points_chosen[:, 1])
        grid_x, grid_y = np.mgrid[xrange_min:xrange_max, yrange_min:yrange_max]
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