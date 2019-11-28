# %%
from population import *
from gen_landscape import *
import numpy as np
import datetime


# %%
def create_world_and_run_till_end(land, max_iterations=10000):
    gia = Population(population_size=10000, loci=2, gene_mean=0, gene_sd=1,
                     proportion_asexual=0.5, survival_rate=0.7, mutation_std=1, landscape=land)

    for i in range(max_iterations + 10):
        if gia.population_sizes(asex=True) < 100:
            result = 2
            break
        elif gia.population_sizes(sex=True) < 100:
            result = 1
            break
        elif i > max_iterations:
            result = 0
            break
        gia.mutation_stage()
        gia.survival_stage()
        gia.replication_stage()
    return result


def run_assesment_of_landscape(points_chosen, assigned_fitness, num_times=1):
    sex_wins, asex_wins, draws, errors = 0, 0, 0, 0
    assigned_fitness = np.array(assigned_fitness)
    land = Landscape2D(points_chosen=points_chosen, points_fitness_values=assigned_fitness)
    for n in range(num_times):
        try:
            result = create_world_and_run_till_end(land)
            if result == 0:
                draws += 1
            elif result == 1:
                asex_wins += 1
            elif result == 2:
                sex_wins += 1
            print('     Arrangement Stats: Sex, Asex, Draws')
            print('     ', assigned_fitness, sex_wins, asex_wins, draws)
        except:
            errors += 1
    return (sex_wins, asex_wins, draws, errors)


def test_arrangements(points_to_set, list_of_assigned_fitness, num_times_each):
    data_dict = {}
    for i in range(len(list_of_assigned_fitness)):
        # results  - (sex_wins, asex_wins, draws, errors)
        results = run_assesment_of_landscape(points_chosen=points_to_set, assigned_fitness=list_of_assigned_fitness[i],
                                             num_times=num_times_each)
        data_dict[i] = (list_of_assigned_fitness[i], results)
        print('Total State:')
        print(data_dict)

    return data_dict


# %%
points_to_set = np.array([[100, 0], [0, 100], [-100, 0], [0, -100], [0, 0]])
# pure concave
assigned_concave_1 = [-100, -100, -100, -100, 0]
# saddle
assigned_half_saddle = [-100, 100, -100, -100, 0]
assigned_saddle = [-100, 100, -100, 100, 0]

list_of_assigned_fitness = [assigned_concave_1, assigned_half_saddle, assigned_saddle]
# %%

data_dict = test_arrangements(points_to_set=points_to_set,
                              list_of_assigned_fitness=list_of_assigned_fitness, num_times_each=100)

# %%
print('WE ARE FINISHED')
print('data dict')
print(data_dict)

stamp = str(datetime.datetime.now())
filename = 'Experiment_Data\\two_sim_7_deg_' + stamp + '.json'
with open(filename, 'w') as fp:
    json.dump(data_dict, fp)