
from gen_landscape import *
from world_class_v2 import *

def create_world_and_run_till_end(sex_win, asex_win, land):
    gia = world(population_size=10000, loci=2, gene_mean=150, gene_sd=10, proportion_asexual=0.5, survival_rate=0.7,
                asex_repl_ratio=10 / 7, sex_repl_ratio=10 / 7, mutation_down_prob=0.05, mutation_up_prob=0.05,
                mutation_step=1, control=4, landscape=land.fitness_grid)

    print('max for each loci', np.max(gia.total_pop_mat, axis=1))
    print('min for each loci:', np.min(gia.total_pop_mat, axis=1))
    for i in range(100000):
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
            print('Asex population percentage:', gia.population_sizes(asex=True) / gia.population_sizes(total=True))
    return sex_win, asex_win


sex_win, asex_win = 0, 0
land_num = 0
land_dict = {}
for n in range(100):
    try:
        land = Landscape(2, 300, num_grid_res=2)
        sex_win, asex_win = create_world_and_run_till_end(sex_win, asex_win, land)
    except:
        print('WENT OUT OF RANGE')
    print('INTER-ITER: Sex:', sex_win, ' Asex:', asex_win)
