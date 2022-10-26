import numpy.random as npr
import os
import pandas       as pd
import random

from Chromosome import Chromosome
from Home       import Home

MAX_GENERATIONS = 1000
CROSSOVER = 0
MUTATION = 1

DATA_DIR = os.path.join("..", "data")
LOG_FILE = os.path.join(DATA_DIR, "data.csv")


class Genetic_Path_Planner:

    def __init__(self, 
                num_chromosomes=10, 
                num_homes=45, 
                warehouse_indices_list=[[10,5],[25,30]], 
                p=0.1):
        self.num_chromosomes = num_chromosomes
        self.generation = 0
        self.crossover_probability = p
        self.mutation_probability = 1-p
        self.chromosomes = self.generate_intial_random_chromosomes(num_homes, warehouse_indices_list)
        self.data_df = pd.DataFrame()


    
    def run_genetic_algorithm(self):
        while (not self.termination_condition_reached()):
            new_chromosomes = self.generate_crossover_mutation_chromosomes()
            self.chromosomes = self.selection(new_chromosomes)
            self.record_data()
            self.generation += 1


    
    def generate_crossover_mutation_chromosomes(self):
        new_chromosomes = []
        while len(new_chromosomes) < self.num_chromosomes:
            # randomly select a genetic operator (crossover or mutation)
            selection_probabilities = [self.crossover_probability, self.mutation_probability]
            genetic_operator = npr.choice(len(selection_probabilities), p=selection_probabilities)
            
            # randomly select 2 existing chromosomes. Better fitness means better chance of selection
            sum_fitnesses = sum([chromosome.fitness() for chromosome in self.chromosomes])
            selection_probabilities = [chromosome.fitness()/sum_fitnesses for chromosome in self.chromosomes]
            first_chrom = self.chromosomes[npr.choice(len(self.chromosomes), p=selection_probabilities)]
            second_chrom = self.chromosomes[npr.choice(len(self.chromosomes), p=selection_probabilities)]

            if genetic_operator == CROSSOVER:
                generated_chromosomes = first_chrom.crossover(second_chrom)
            else:
                generated_chromosomes = [first_chrom.mutate(), second_chrom.mutate()]
            new_chromosomes.extend(generated_chromosomes)

        return new_chromosomes


    
    def selection(self, chromosomes_list):
        # define the weights in which we will select (higher fitness is more likely)
        sum_fitnesses = sum([chromosome.fitness() for chromosome in chromosomes_list])
        selection_probabilities = [chromosome.fitness()/sum_fitnesses for chromosome in chromosomes_list]
        # select the chromosomes
        new_chromosome_list = []
        for _ in range(self.num_chromosomes):
            selected_chromosome = chromosomes_list[npr.choice(len(chromosomes_list), p=selection_probabilities)]
            new_chromosome_list.append(selected_chromosome)
        return new_chromosome_list

        

    def generate_intial_random_chromosomes(self, num_homes, warehouse_indices_list):
        occupied_indices = warehouse_indices_list.copy()

        # create num_homes unique random pairs of indices
        random_index = [random.randint(0,35), random.randint(0,35)]
        for _ in range(num_homes):
            while (random_index in occupied_indices):
                random_index = [random.randint(0,35), random.randint(0,35)]
            occupied_indices.append(random_index)

        # assign indices to home objects
        home_indices = occupied_indices[:num_homes]
        home_list = [Home(home_indices[i], i) for i in range(num_homes)]

        return [Chromosome(random.sample(home_list, len(home_list)), warehouse_indices_list)\
                     for i in range(self.num_chromosomes)]



    def termination_condition_reached(self):
        #TODO add condition for no appreciable improvement in fitness
        return (self.generation >= MAX_GENERATIONS)



    def record_data(self):
        new_row = {'Chromosome '+str(i):chrom.fitness() for i,chrom in enumerate(self.chromosomes)}
        self.data_df = self.data_df.append(new_row, ignore_index=True)
        self.data_df.to_csv(LOG_FILE)



    def __str__(self):
        return self.chromosomes.__str__()



if __name__=="__main__":

    NUM_CHROMOSOMES = 8
    NUM_HOMES = 100
    NUM_TRUCKS = 2
    CROSSOVER_PROBABILITY = 0.90

    genetic = Genetic_Path_Planner(num_chromosomes=NUM_CHROMOSOMES, p=CROSSOVER_PROBABILITY)
    genetic.run_genetic_algorithm()