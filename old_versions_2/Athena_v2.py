#%%
from gen_landscape import *
from world_class_v2 import *
import datetime
import json
import numpy as np
#%%
def create_world_and_run_till_end(land):
    gia = world(population_size=10000, loci=2, gene_mean=200, gene_sd=10, proportion_asexual=0.5, survival_rate=0.7,
                asex_repl_ratio=10 / 7, sex_repl_ratio=10 / 7, mutation_down_prob=0.05, mutation_up_prob=0.05,
                mutation_step=1, control=4, landscape=land.fitness_grid)
    i = 0
    for i in range(11000):
        if gia.population_sizes(asex=True) < 100:
            who_won = 2
            print('SEX WINNER')
            break
        elif gia.population_sizes(sex=True) < 100:
            who_won = 1
            print('ASEX WINNER')
            break
        elif i>10000:
            who_won = 0
            print('DRAW')
            break
        gia.mutation_stage()
        gia.survival_stage()
        gia.replication_stage()
    return who_won

#%%
def isCircular(arr1, arr2):
    if len(arr1) != len(arr2):
        return False

    str1 = ' '.join(map(str, arr1))
    str2 = ' '.join(map(str, arr2))
    if len(str1) != len(str2):
        return False

    return str1 in str2 + ' ' + str2
#%%
range_possible = [10,50,90]
import itertools
all_possible = list(itertools.product(range_possible,range_possible, range_possible, range_possible))
final_arrangements = []
for arrangement in all_possible:
    no_cyclic_quivalent = True
    for arr in final_arrangements:
        if isCircular(arrangement, arr) == True:
            no_cyclic_quivalent = False
    if no_cyclic_quivalent == True:
        final_arrangements.append(arrangement)
final_arrangements = final_arrangements[1:]
#%%
def run_assesment_of_landscape(assigned_fitness, num_times=1):
    sex_wins, asex_wins, draws, errors = 0,0,0,0
    assigned_fitness = np.array(assigned_fitness)
    for n in range(num_times):
        try:
            land = Landscape(num_dimensions=2, dimension_size=300, num_grid_res=3, assigned_fitness = assigned_fitness)
            who_won = create_world_and_run_till_end(land)
            if who_won==0:
                draws+=1
            elif who_won==1:
                asex_wins+=1
            elif who_won==2:
                sex_wins+=1
            print('     Arrangement Stats: Sex, Asex, Draws')
            print('     ',arrangement, sex_wins, asex_wins, draws)
        except:
            errors += 1
    return (sex_wins, asex_wins, draws, errors)
#%%
data_dict = {}
counter = 0
for arrangement in final_arrangements:
    arrangement1 = list(arrangement)
    arrangement1 = arrangement1[:2]+[50]+arrangement1[2:]
    sex_wins, asex_wins, draws, errors = run_assesment_of_landscape(assigned_fitness=arrangement1, num_times=20)
    data_dict[counter] = (arrangement1, sex_wins, asex_wins, draws, errors)
    counter +=1
    print('Just finished the stuff for arrangement', arrangement1)
    print('SEX/ASEX/DRAWS/ERRORS:',sex_wins, asex_wins, draws, errors)
    print('===============')
    print('Current Summary')
    print(data_dict)

#%%

print('WE ARE FINISHED')
print('data dict')
print(data_dict)

stamp = str(datetime.datetime.now())
filename = 'Experiment_Data\\two_sim_7_deg_'+stamp+'.json'
with open(filename, 'w') as fp:
    json.dump(data_dict, fp)