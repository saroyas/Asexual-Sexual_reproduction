# %%

import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

print('hello')

skew_counter = 0
# %%
control = int(input('Enter 1 if this is to be run as control (else 0): '))
def fitness_landscape(organism_column):
    if control == 1:
        fitness_value_for_organism = 1
    elif control == 0:
        fitness_value_for_organism = np.sum(organism_column)
    return fitness_value_for_organism


# %%

class world():
    def __init__(self, population_size, loci, gene_mean, gene_sd, proportion_asexual,
                 survival_rate, asex_repl_ratio, sex_repl_ratio, mutation_down_prob, mutation_up_prob, mutation_step=1):
        self.population_size = population_size
        self.loci = loci
        self.organism_capacity = round(survival_rate * population_size)
        self.asex_repl_ratio = asex_repl_ratio
        self.sex_repl_ratio = sex_repl_ratio
        self.total_pop_mat = (np.random.normal(gene_mean, gene_sd, (loci, self.population_size))).astype(int)
        self.separator = round(self.population_size * proportion_asexual)  # To indicate where the asex ends and sex begins
        self.mutation_down_prob = mutation_down_prob
        self.mutation_up_prob = mutation_up_prob
        self.mutation_step = mutation_step
        self.plot_iter_num = 0
        self.plot_data_sex = {}
        self.plot_data_asex = {}
        self.plot_data_total = {}
        self.add_to_plot_data()
        self.loci_var_data = []

    def asex_pop_matrix(self):
        asex_matrix = self.total_pop_mat[:, :self.separator]
        return asex_matrix

    def sex_pop_matrix(self):
        sex_matrix = self.total_pop_mat[:, self.separator:]
        return sex_matrix

    def add_to_plot_data(self):
        species = {}
        species['asex'] = self.asex_pop_matrix().tolist()
        species['sex'] = self.sex_pop_matrix().tolist()
        self.plot_data_total[self.plot_iter_num] = species
        self.plot_iter_num += 1

    def population_sizes(self, total=False, asex=False, sex=False):
        if total == True:
            return self.total_pop_mat.shape[1]
        if asex == True:
            return self.asex_pop_matrix().shape[1]
        if sex == True:
            return self.sex_pop_matrix().shape[1]

    def mutation_stage(self):
        shape = self.total_pop_mat.shape
        mutation_prob = [self.mutation_down_prob, 1 - self.mutation_down_prob - self.mutation_up_prob,
                         self.mutation_up_prob]
        mutation_matrix = np.random.choice([-self.mutation_step, 0, self.mutation_step], size=shape, p=mutation_prob)
        self.total_pop_mat = self.total_pop_mat + mutation_matrix

    def calc_fitness_array(self, population_subset):
        return np.apply_along_axis(fitness_landscape, 0, population_subset)

    def survival_probability(self):
        # For now we make survival probability simply proportionate to
        # the fitness value. This is fine, and moves all the subtlety to the fitness landscape.
        self.fitness_array = self.calc_fitness_array(population_subset=self.total_pop_mat)
        total_fitness = np.sum(self.fitness_array)
        prop_fitness = np.divide(self.fitness_array, total_fitness)
        return prop_fitness

    def survival_stage(self):
        curr_population_index = range(self.population_sizes(total=True))
        prop_fitness = self.survival_probability()
        # The following step may be a serious computational time issue
        survivor_list = np.random.choice(curr_population_index, self.organism_capacity, replace=False, p=prop_fitness)
        survivor_list = np.sort(survivor_list)
        self.total_pop_mat = (self.total_pop_mat)[:, survivor_list]
        self.separator = np.size(np.where(survivor_list < self.separator))


    def asex_replication_stage(self):
        asex_pop_mat = self.asex_pop_matrix()
        current_organism_index = np.arange(0, self.population_sizes(asex=True))
        next_gen_size = round(self.population_sizes(asex=True) * self.asex_repl_ratio)
        next_gen_chosen = np.random.choice(current_organism_index, size=next_gen_size, replace=True)
        chosen_orgs = asex_pop_mat[:, next_gen_chosen]
        return chosen_orgs

    def sexual_recombination(self):
        current_organism_index = np.arange(0, self.population_sizes(sex=True))
        next_gen_size = round(self.population_sizes(sex=True) * self.sex_repl_ratio)
        next_gen_chosen = np.random.choice(current_organism_index, size=next_gen_size, replace=True)
        sex_pop_mat = self.sex_pop_matrix()
        chosen_orgs = sex_pop_mat[:, next_gen_chosen]
        for i in range(self.loci):
            np.random.shuffle(chosen_orgs[i])
        return chosen_orgs

    def pop_size_preserving_repl_rates(self):
        current_pop_size = self.population_sizes(total=True)
        ratio = self.population_size / current_pop_size
        self.sex_repl_ratio, self.asex_repl_ratio = ratio, ratio

    def replication_stage(self, pop_size_preserving=True):
        if pop_size_preserving == True:
            self.pop_size_preserving_repl_rates()
        asex_pop_mat = self.asex_replication_stage()
        sex_pop_mat = self.sexual_recombination()
        self.total_pop_mat = np.concatenate([asex_pop_mat, sex_pop_mat], axis=1)
        self.separator = asex_pop_mat.shape[1]

    def loci_variance(self, sex=True):
        if sex == True:
            pop_mat = self.sex_pop_matrix()
        else:
            pop_mat = self.asex_pop_matrix()
        loci_var = []
        for x in range(self.loci):
            loci_var.append(np.var(pop_mat[x, :]))
        return loci_var

    def diff_in_loci_var_data(self):
        sex_loci_var = self.loci_variance(sex=True)
        asex_loci_var = self.loci_variance(sex=False)
        diff_loci_var = [(asex_loci_var[i] - sex_loci_var[i]) for i in range(self.loci)]
        self.loci_var_data.append(diff_loci_var)

    def summarize_loci_var(self):
        avg_diff = np.average(self.loci_var_data, 0).astype(int)
        return avg_diff

    def publish_plot_data(self):
        with open('data.json', 'w') as fp:
            json.dump(self.plot_data_total, fp)

# %%

def iteration_plotting(gia):
    gia.mutation_stage()
    gia.add_to_plot_data()
    gia.survival_stage()
    gia.add_to_plot_data()
    gia.replication_stage()
    gia.add_to_plot_data()

def iteration(gia):
    gia.mutation_stage()
    gia.survival_stage()
    gia.replication_stage()


sex_win = 0
asex_win = 0
num_iterations = int(input('How many iterations?: '))
for a in range(num_iterations):
    #WEIGHTED MUTATION PROBS
    gia = world(population_size=10000, loci=2, gene_mean=100, gene_sd=10, proportion_asexual=0.5, survival_rate=0.7,
                asex_repl_ratio=10 / 7, sex_repl_ratio=10 / 7, mutation_down_prob=0.05, mutation_up_prob=0.05,
                mutation_step=1)
    for i in range(100000):
        if gia.population_sizes(asex = True)<100:
            sex_win+=1
            break
        elif gia.population_sizes(sex = True) < 100:
            asex_win+=1
            break
        if i % 50 == 0:
            iteration_plotting(gia)
        else:
            iteration(gia=gia)
        if i%500 == 0:
            print('World:', a, 'Iteration:', i)
            print('Asex population percentage:', gia.population_sizes(asex=True)/gia.population_sizes(total=True))
            print('INTER-ITER: Sex:', sex_win, ' Asex:', asex_win)
    print('Sex:', sex_win, ' Asex:', asex_win)