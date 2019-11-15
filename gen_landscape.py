import numpy as np
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

generate_landscape()