# %%

import scipy as sp
import scipy.interpolate
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
import plotly.graph_objects as go


# %%

def grid_chosen_points_2D(range=100, resolution=3):
    k = complex(0, resolution)
    grid_x, grid_y = np.mgrid[-range:range:k, -range:range:k]
    points_chosen = np.vstack((grid_x.ravel(), grid_y.ravel())).T
    return points_chosen

def grid_chosen_points_3D(range=100, resolution=3):
    k = complex(0, resolution)
    grid_x, grid_y, grid_z = np.mgrid[-range:range:k, -range:range:k, -range:range:k]
    points_chosen = np.vstack((grid_x.ravel(), grid_y.ravel(), grid_z.ravel())).T
    return points_chosen

def gen_rand_uniform(num_rand_points, min=0, max=200):
    rand_fitness_array = np.random.random_integers(min, max, num_rand_points)
    return rand_fitness_array


class Landscape2D():
    def __init__(self, points_chosen=[], points_fitness_values=[], spline=True, rbf_func='multiquadric'):
        self.points_chosen = points_chosen
        self.points_fitness_values = points_fitness_values
        if spline == True:
            self.get_points = self.spline_landscape_getter()
        else:
            self.get_points = self.rbf_landscape_getter(rbf_func)

    def rbf_landscape_getter(self, rbf_func):
        '''
        Rbf method is more robust, in that it extrapolates outside the points!
        But we may not really want this tbh, since outside is only implicitily defined
        '''
        rbf_land = sp.interpolate.Rbf(self.points_chosen[:, 0], self.points_chosen[:, 1]
                                      , self.points_fitness_values, function=rbf_func)
        return rbf_land

    def spline_landscape_getter(self):
        spline_land = scipy.interpolate.CloughTocher2DInterpolator(self.points_chosen, self.points_fitness_values)
        return spline_land

    def draw(self, elevation_deg=80, rotation_deg=-90, flat=False, mesh=False, save = False):

        def get_grid_range():
            xrange_min, xrange_max = np.min(self.points_chosen[:, 0]), np.max(self.points_chosen[:, 0]).astype(int)
            yrange_min, yrange_max = np.min(self.points_chosen[:, 1]), np.max(self.points_chosen[:, 1]).astype(int)
            grid_x, grid_y = np.mgrid[xrange_min:xrange_max, yrange_min:yrange_max]
            grid_min = np.minimum(xrange_min, yrange_min)
            grid_max = np.maximum(xrange_max, yrange_max)
            return grid_x, grid_y, grid_min, grid_max

        grid_x, grid_y, grid_min, grid_max = get_grid_range()
        # generate the full landscape in that area, sometimes computationally intensive
        fitness_grid = self.get_points(grid_x, grid_y)

        if flat == False:
            fig = p.figure()
            ax = p3.Axes3D(fig)
            ax.auto_scale_xyz(1,1)
            if mesh == True:
                ax.plot_wireframe(grid_x, grid_y, fitness_grid, color='black')
            else:
                ax.contour3D(grid_x, grid_y, fitness_grid, 50, cmap=plt.cm.viridis)
            ax.set_xlabel('loci_0')
            ax.set_ylabel('loci_1')
            ax.set_zlabel('Fitness')
            ax.view_init(elevation_deg, rotation_deg)
            if save:
                filename = input('What should this be saved as?')
                p.savefig(filename)
            p.show()
        else:
            plt.plot(self.points_chosen[:, 0], self.points_chosen[:, 1], 'k.', ms=10)
            plt.imshow(fitness_grid.T, extent = (grid_min, grid_max, grid_min, grid_max))
            plt.xlabel('Loci 0')
            plt.ylabel('Loci 1')
            plt.gcf().set_size_inches(10, 10)
            if save:
                filename = input('What should this be saved as?')
                plt.savefig(filename)
            plt.show()


class Landscape3D():
    def __init__(self, points_chosen=[], points_fitness_values=[], rbf_func='multiquadric'):
        self.points_chosen = points_chosen
        self.points_fitness_values = points_fitness_values
        self.get_points = self.rbf_landscape_getter(rbf_func)

    def rbf_landscape_getter(self, rbf_func):
        rbf_land = sp.interpolate.Rbf(self.points_chosen[:, 0], self.points_chosen[:, 1],
                                      self.points_chosen[:, 2], self.points_fitness_values, function=rbf_func)
        return rbf_land

    def draw(self,resolution=50):
        k = complex(0, resolution)
        def get_grid_range():
            xrange_min, xrange_max = np.min(self.points_chosen[:, 0]), np.max(self.points_chosen[:, 0])
            yrange_min, yrange_max = np.min(self.points_chosen[:, 1]), np.max(self.points_chosen[:, 1])
            zrange_min, zrange_max = np.min(self.points_chosen[:, 2]), np.max(self.points_chosen[:, 2])
            grid_x, grid_y, grid_z = np.mgrid[xrange_min:xrange_max:k, yrange_min:yrange_max:k,zrange_min:zrange_max:k].astype(int)
            return grid_x, grid_y, grid_z

        grid_x, grid_y, grid_z = get_grid_range()

        # generate the full landscape in that area, sometimes computationally intensive
        fitness_grid = np.array(self.get_points(grid_x, grid_y, grid_z)).astype(int)
        fig = go.Figure(data=go.Volume(x=grid_x.flatten(),
                                       y=grid_y.flatuniformten(),
                                       z=grid_z.flatten(),
                                       value=fitness_grid.flatten(),
                                       isomin=np.min(fitness_grid),
                                       isomax=np.max(fitness_grid),
                                       opacity=0.1, # needs to be small to see through all surfaces
                                       surface_count=20, # needs to be a large number for good volume rendering
                                        ))
        fig.show()