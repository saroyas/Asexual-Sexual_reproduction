
from gen_landscape import *
from world_class_v2 import *

def create_world_and_run_till_end(sex_win, asex_win, land):
    gia = world(population_size=10000, loci=2, gene_mean=150, gene_sd=10, proportion_asexual=0.5, survival_rate=0.7,
                asex_repl_ratio=10 / 7, sex_repl_ratio=10 / 7, mutation_down_prob=0.05, mutation_up_prob=0.05,
                mutation_step=1, control=4, landscape=land.fitness_grid)
    for i in range(15000):
        if gia.population_sizes(asex=True) < 100:
            sex_win += 1
            print('SEX WINNER')
            break
        elif gia.population_sizes(sex=True) < 100:
            asex_win += 1
            print('ASEX WINNER')
            break
        gia.mutation_stage()
        gia.survival_stage()
        gia.replication_stage()
        if i % 500 == 0:
            print('Iteration:', i)
            print('inter world status: asex wins:', asex_win, 'sex win', sex_win)
            print('Asex population percentage:', gia.population_sizes(asex=True) / gia.population_sizes(total=True))
    return sex_win, asex_win

def gen_fitness_dots(half_diff = 45):
    corner = 50 - half_diff
    middle = 50 + half_diff
    fitness_dots = [corner] * 4 + [middle] + [corner] * 4
    return fitness_dots

sex_win, asex_win = 0, 0
land_num = 0
land_dict = {}
grid_res = int(input('what is the grid resolution of landscape'))

diffs = [15, 30, 45]
for half_diff in diffs:
    sex_win, asex_win = 0, 0
    for n in range(100):
        try:
            fitness_dots = gen_fitness_dots(half_diff = half_diff)
            land = Landscape(num_dimensions=2, dimension_size=300, num_grid_res=3, assigned_fitness=fitness_dots)
            sex_win, asex_win = create_world_and_run_till_end(sex_win, asex_win, land)
        except:
            print('WENT OUT OF RANGE')
        print('half diff:', half_diff)
        print('INTER-ITER: Sex:', sex_win, ' Asex:', asex_win)
        print('land_dict',land_dict)
    land_dict[half_diff] = (sex_win, asex_win)

print('WE ARE FINISHED')
for half_diff in diffs:
    print('Half Diff', half_diff, '; Sex Win, Asex Win', land_dict[half_diff])