#%%
from gen_landscape import *
from world_class_v2 import *
import datetime
import json
#%%
def create_world_and_run_till_end(land):
    gia = world(population_size=10000, loci=2, gene_mean=150, gene_sd=10, proportion_asexual=0.5, survival_rate=0.7,
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
        if i % 500 == 0:
            print('     Inside iteration:', i)
            print('     Asex population percentage:', gia.population_sizes(asex=True) / gia.population_sizes(total=True))
            print('     ===================================')
    return who_won

#%%
def calc_win_stats(data_dict):
    sex, asex, draws = 0, 0, 0
    for key in data_dict.keys():
        (land.chosen_points, who_won) = data_dict[key]
        if who_won==1:
            asex +=1
        elif who_won == 2:
            sex +=1
        elif who_won == 0:
            draws += 1
    print('Current Overall Statistics:')
    print('Sex wins:', sex, ' Asex wins:', asex, ' Draws:', draws)
#%%
range_tens = range(0,101, 10)
def gen_assigned_values(range = range_tens):
    fst_part = np.random.choice(range_tens, 4).tolist()
    centre_of_space = 50
    snd_part = np.random.choice(range_tens, 4).tolist()
    assigned_values = np.asarray(fst_part+[centre_of_space]+snd_part)
    return assigned_values
#%%
land_num = 0
data_dict = {}
grid_res = 3
for n in range(300):
    land = Landscape(num_dimensions=2, dimension_size=300, num_grid_res=grid_res, assigned_fitness = gen_assigned_values())
    print(land.assigned_fitness)
    who_won = create_world_and_run_till_end(land)
    assigned_fitness = land.assigned_fitness.tolist()
    data_dict[n] = (assigned_fitness, who_won)
    print('Just finished world number', n)
    calc_win_stats(data_dict)

print('WE ARE FINISHED')
print('data dict')
print(data_dict)

stamp = str(datetime.datetime.now())
filename = 'Experiment_Data\\two_sim_7_deg_'+stamp+'.json'
with open(filename, 'w') as fp:
    json.dump(data_dict, fp)