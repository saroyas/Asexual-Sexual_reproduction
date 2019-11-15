import noise
import numpy as np
from PIL import Image


shape = (500, 500)
scale = 100.0
octaves = 1
persistence = 0.5
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i / scale,
                                    j / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=1024,
                                    repeaty=1024,
                                    base=0)

from matplotlib import pyplot as plt
plt.imshow(world, interpolation='nearest')
plt.show()
world = np.asarray(world)
world = (world * 100) + 100
print(np.min(world))
print(np.max(world))
landscape = world


def generate_landscape(size = 600):
    #Right now we also assume that pop fitness never goes beyond 600 - this might eb a bad assumption
    #Right now this has to be disgned for each loci number, currently for two
    #this is because of the lambda function
    loci = 2
    if size ==0:
        size = int(input('What is the size of landscape'))
    landscape_ground = tuple([size]*loci)
    #we add the one to avoid 0 fitness
    landscape = np.fromfunction(lambda a, b: (a+b)**4, landscape_ground)

np.save('landscape.npy',landscape)
