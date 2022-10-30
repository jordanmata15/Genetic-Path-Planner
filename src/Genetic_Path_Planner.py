from enum import Enum
from typing import List
import numpy.random as npr
import os
import pandas       as pd
import random

from Chromosome import Chromosome
from Home       import Home

class Genetic_Operator(Enum):
    CROSSOVER = 0
    MUTATION = 1

    def __eq__(self, other: int):
        """Compares this enum to an int

        Args:
            other (int): int to compare to this enum

        Returns:
            _type_: True if equal. False otherwise.
        """
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, Genetic_Operator):
            return self is other
        return False


class Genetic_Path_Planner:

    PACKAGE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    DATA_DIR = os.path.join(PACKAGE_DIR, "data")

    def __init__(self,
                num_chromosomes=10,
                num_homes=45, 
                warehouse_indices_list=[[10,5],[25,30]], 
                crossover_probability=0.1,
                max_generations=400):
        self.num_chromosomes = num_chromosomes
        self.max_generations = max_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = 1-crossover_probability
        self.chromosomes = self.generate_intial_random_chromosomes(num_homes, warehouse_indices_list)
        self.data_df = pd.DataFrame()


    
    def run_genetic_algorithm(self):
        """Runs the genetic algorithm and writes our data to our dataframe
        """
        for _ in range(self.max_generations):
            new_chromosomes = self.generate_crossover_mutation_chromosomes()
            self.chromosomes = self.selection(new_chromosomes)
            self.record_data()
        file_pct = str(int(self.crossover_probability*100))
        log_filename = os.path.join(self.DATA_DIR, "data_"+file_pct+"_pct.csv")
        self.data_df.to_csv(log_filename)


    
    def generate_crossover_mutation_chromosomes(self) -> List[Chromosome]:
        """Generates N more chromosomes from an existing set of chromosomes using
        crossover and mutation genetic operators. Returns the set of existing and created
        chromosomes.

        Returns:
            List[Chromosome]: List of 2N chromosomes. N from the existing chromosomes,
                                the remaining N created through genetic operators. 
        """
        new_chromosomes = []
        while len(new_chromosomes) < self.num_chromosomes:
            # randomly select a genetic operator (crossover or mutation)
            selection_probabilities = [self.crossover_probability, self.mutation_probability]
            genetic_operator = npr.choice(len(selection_probabilities), p=selection_probabilities)
            
            # randomly select an existing chromosome. Better fitness means better chance of selection
            sum_fitnesses = sum([chromosome.total_distance() for chromosome in self.chromosomes])
            selection_probabilities = [chromosome.total_distance()/sum_fitnesses for chromosome in self.chromosomes]
            chrom = self.chromosomes[npr.choice(len(self.chromosomes), p=selection_probabilities)]
            
            if genetic_operator == Genetic_Operator.CROSSOVER:
                # randomly select a second chromosome
                second_chrom = self.chromosomes[npr.choice(len(self.chromosomes), p=selection_probabilities)]
                generated_chromosomes = chrom.crossover(second_chrom)
            else:
                generated_chromosomes = [chrom.mutate()]
            new_chromosomes.extend(generated_chromosomes)

        # we may have created one extra chromosome
        new_chromosomes = new_chromosomes[:self.num_chromosomes]
        # add existing chromosomes for a total of 2N chromosomes
        new_chromosomes.extend(self.chromosomes)
        return new_chromosomes


    
    def selection(self, chromosomes_list: List[Chromosome]) -> List[Chromosome]:
        """Performs the selection process by selecting N chromosomes from a list of 2N
        chromosomes. Selection is done based on roulette wheel selection. Lower distance
        means higher probability of being selected.

        Args:
            chromosomes_list (List[Chromosome]): List of 2N number of chromosomes

        Returns:
            List[Chromosome]: List of N chromosomes after roulette wheel selection.
        """
        # define the weights in which we will select (higher fitness is more likely)
        selection_probabilities = self.roulette_wheel_probabilities(chromosomes_list)
        #  select the chromosomes
        new_chromosome_list = []
        for _ in range(self.num_chromosomes):
            selected_chromosome = chromosomes_list[npr.choice(len(chromosomes_list), p=selection_probabilities)]
            new_chromosome_list.append(selected_chromosome)
        return new_chromosome_list

        

    def generate_intial_random_chromosomes(self,
                                            num_homes: int, 
                                            warehouse_indices_list: List[List[int]]) -> List[Chromosome]:
        """Generates the initial set of chromosomes to a random ordering of the homes
        with the predefined indexes of warehouses.

        Args:
            num_homes (int): Number of houses to generate in the chromosomes
            warehouse_indices_list (List[List[int]]): List of indices of our warehouses. 
                                                        For 2 warehouses at (1,1) and (3,2), pass in:
                                                        [[1,1],[3,2]]

        Returns:
            List[Chromosome]: List of generated chromosomes. Each with the same number of randomly 
                                ordered homes and the same warehouse indices.
        """
        occupied_indices = warehouse_indices_list.copy()
        home_indices = []

        # create num_homes unique random pairs of indices
        random_index = [random.randint(0,35), random.randint(0,35)]
        for _ in range(num_homes):
            while (random_index in occupied_indices):
                random_index = [random.randint(0,35), random.randint(0,35)]
            occupied_indices.append(random_index)
            home_indices.append(random_index)

        # assign indices to home objects
        home_list = [Home(home_indices[i], i) for i in range(num_homes)]

        # create a new list where each chromosome has shuffled houses list
        return [Chromosome(random.sample(home_list, len(home_list)), warehouse_indices_list)\
                     for _ in range(self.num_chromosomes)]



    def record_data(self) -> None:
        """Record the distances of each of the current viable chromosomes in a dataframe
        """
        new_row = {'Chromosome_'+str(i):chrom.total_distance() for i,chrom in enumerate(self.chromosomes)}
        self.data_df = self.data_df.append(new_row, ignore_index=True)



    def roulette_wheel_probabilities(self, chromosomes_list: List[Chromosome]) -> List[float]:
        """From a list of chromosomes, generate a list of probabilities simulating 
        roulette wheel selection. Every chromosome will have a probability corresponding
        to how likely this chromosome should be selected. Smaller distance gets higher
        probability.

        Args:
            chromosomes_list (List[Chromosome]): List of chromosomes, each with their own 
                                                    total_distance() function.

        Returns:
            List[float]: List of probabilities. Sum of all probabilities equal to 1.
        """
        distance_list = [chromosome.total_distance() for chromosome in chromosomes_list]
        max_distance = max(distance_list)
        fitness_list = [(1.1*max_distance)-c_distance for c_distance in distance_list]
        sum_fitnesses = sum(fitness_list)
        selection_probabilities = [c_fitness/sum_fitnesses for c_fitness in fitness_list]
        return selection_probabilities



if __name__=="__main__":

    genetic_planner = Genetic_Path_Planner(num_chromosomes=10,
                                            crossover_probability=0.95,
                                            max_generations=1000,
                                            #num_homes=45,
                                            #warehouse_indices_list=[[10,5],[25,30]]
                                            )
    genetic_planner.run_genetic_algorithm()