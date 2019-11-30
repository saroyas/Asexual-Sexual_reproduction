# %%

from population import *
from gen_landscape import *
import numpy as np
import datetime


# %%

def create_world_and_run_till_end(land, num_iterations=10000):
    gia = Population(population_size=10000, loci=2, gene_mean=0, gene_sd=10,
                     proportion_asexual=0.5, survival_rate=0.7, mutation_std=1, landscape=land)

    for i in range(num_iterations):
        gia.mutation_stage()
        gia.replication_stage()
        if True in np.isnan(gia.get_fitness(gia.total_pop_mat)):
            break
        else:
            gia.survival_stage()

    return gia.fitness_stats()


def run_assesment_of_landscape(points_chosen, assigned_fitness, num_times=1):
    sex_wins, asex_wins, draws, errors = 0, 0, 0, 0
    sex_minus_asex_fitness = 0
    land = Landscape2D(points_chosen=points_chosen, points_fitness_values=assigned_fitness)
    for n in range(num_times):
        try:
            ((asex_avg, asex_var), (sex_avg, sex_var)) = create_world_and_run_till_end(land)
            if asex_avg > sex_avg:
                asex_wins += 1
            elif sex_avg > asex_avg:
                sex_wins += 1
            else:
                draws += 1
            sex_minus_asex_fitness = sex_minus_asex_fitness + (sex_avg - asex_avg)
        except:
            errors += 1
    return (sex_minus_asex_fitness, sex_wins, asex_wins, draws, errors)


def test_arrangements(points_to_set, list_of_assigned_fitness, num_times_each):
    data_dict = {}
    for i in range(len(list_of_assigned_fitness)):
        print('Testing:', list_of_assigned_fitness[i])
        # results  - (sex_wins, asex_wins, draws, errors)
        results = run_assesment_of_landscape(points_chosen=points_to_set, assigned_fitness=list_of_assigned_fitness[i],
                                             num_times=num_times_each)
        data_dict[i] = (list_of_assigned_fitness[i], results)
        print('Total State:')
        print(data_dict)

    return data_dict


# %%
mn = 500
points_to_set_diamond = np.array([[mn, 0], [0, mn], [-mn, 0], [0, -mn], [0, 0]])
points_to_set_sqr = np.array([[mn, mn], [-mn, mn], [-mn, -mn], [mn, -mn], [0, 0]])
# pure concave
sz = 1000
pure_concave = [-sz, -sz, -sz, -sz, 0]
concave_almost_1 = [-sz, -sz, -sz, 0, 0]
concave_almost_2 = [-sz, -sz, 0, 0, 0]
concave_almost_3 = [-sz, 0, -sz, 0, 0]
concave_almost_4 = [-sz, 0, 0, 0, 0]

flat = [0, 0, 0, 0, 0]

hill_slope = [-sz, -sz, sz, sz, 0]
saddle_almost_1 = [-sz, -sz, -sz, sz, 0]
saddle_almost_2 = [-sz, sz, sz, sz, 0]
assigned_saddle = [-sz, sz, -sz, sz, 0]

convex_almost_4 = [sz, 0, 0, 0, 0]
convex_almost_3 = [sz, 0, sz, 0, 0]
convex_almost_2 = [sz, sz, 0, 0, 0]
convex_almost_1 = [sz, sz, sz, 0, 0]
pure_convex = [sz, sz, sz, sz, 0]

list_of_assigned_fitness = [pure_concave, concave_almost_1, concave_almost_2, concave_almost_3, concave_almost_4,
                            flat, hill_slope, saddle_almost_1, saddle_almost_2, assigned_saddle,
                            convex_almost_4, concave_almost_3, concave_almost_2, concave_almost_1, pure_convex]

# %%
which_orientation = int(input('Diamond: 0, Square: 1 ::'))
if which_orientation == 0:
    points_to_set = points_to_set_diamond
elif which_orientation == 1:
    points_to_set = points_to_set_sqr
data_dict = test_arrangements(points_to_set=points_to_set,
                              list_of_assigned_fitness=list_of_assigned_fitness, num_times_each=100)

# %%

print('WE ARE FINISHED')
print('data dict for orientation:', which_orientation)
print(data_dict)
# %%
stamp = str(datetime.datetime.now())
filename = 'orientation_' + str(which_orientation) + '_' + stamp + '.json'
with open(filename, 'w') as fp:
    json.dump(data_dict, fp)