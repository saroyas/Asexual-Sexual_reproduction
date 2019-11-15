# %%
from world_class_v2 import *


gia = world(population_size=2000, loci=2, gene_mean=100, gene_sd=10, proportion_asexual=0.5, survival_rate=0.7,
            asex_repl_ratio=10 / 7, sex_repl_ratio=10 / 7, mutation_down_prob=0.05, mutation_up_prob=0.05,
            mutation_step=1, control=4)
print('max for each loci', np.max(gia.total_pop_mat, axis = 1))
print('min for each loci:', np.min(gia.total_pop_mat, axis = 1))
sex_win, asex_win = 0, 0
for i in range(100000):
    if gia.population_sizes(asex=True) < 100:
        sex_win += 1
        break
    elif gia.population_sizes(sex=True) < 100:
        asex_win += 1
        break
    gia.survival_stage()
    gia.replication_stage()
    gia.add_to_plot_data()
    if i % 500 == 0:
        print('Iteration:', i)
        print('Asex population percentage:', gia.population_sizes(asex=True) / gia.population_sizes(total=True))
gia.publish_plot_data()
print('INTER-ITER: Sex:', sex_win, ' Asex:', asex_win)
print('iterations', i)
print('max for each loci', np.max(gia.total_pop_mat, axis = 1))
print('min for each loci:', np.min(gia.total_pop_mat, axis = 1))