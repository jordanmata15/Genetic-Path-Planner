import random

from Home import Home

class Chromosome:

    def __init__(self, houses_list, warehouse_locations_list):
        num_trucks = len(warehouse_locations_list)
        truck_route_size = len(houses_list)/num_trucks
        
        self.path_order = houses_list
        self.truck_warehouse_indices = warehouse_locations_list
        self.truck_routes = [[int(truck_route_size*x), int(truck_route_size*(x+1))] \
                                    for x in range(num_trucks)]
        # the last truck may have a shorter route, make sure it's last house to visit it's still in bounds
        self.truck_routes[-1][1] = len(houses_list)-1


    def mutate(self):
        i = random.randint(0, len(self.path_order)-1)
        j = random.randint(0, len(self.path_order)-1)

        # swap 2 homes randomly along all truck routes
        mutated_path = self.path_order.copy()
        mutated_path[i], mutated_path[j] = mutated_path[j], mutated_path[i]
        new_chromosome = Chromosome(mutated_path, self.truck_warehouse_indices)
        
        if self.is_valid_path(new_chromosome.path_order):
            return new_chromosome
        else:
            raise Exception("Mutated path is not valid! + \n" + str(new_chromosome))


    def crossover(self, other_chromosome):
        # let p be the split point of our chromosome
        # one side will have p elements, the other side has n-p
        crossover_index = random.randint(1, len(self.path_order)-1)
        
        # use the first p elements of the calling chromosome. Fill the rest using the missing elements
        # from 'other' (in order while avoiding duplicates) 
        new_path_1_left = self.path_order[:crossover_index]
        new_path_1_right = [x for x in other_chromosome.path_order if x not in new_path_1_left]
        new_path_1 = new_path_1_left + new_path_1_right

        # use the first p elements of the 'other' chromosome. Fill the rest using the missing elements
        # from calling chromosome (in order while avoiding duplicates) 
        new_path_2_right = self.path_order[crossover_index:]
        new_path_2_left = [x for x in other_chromosome.path_order if x not in new_path_2_right]
        new_path_2 = new_path_2_left + new_path_2_right

        # return the 2 new chromosomes (after verifying both are valid)
        new_child_chromosomes = [Chromosome(new_path_1, self.truck_warehouse_indices), \
                            Chromosome(new_path_2, self.truck_warehouse_indices)]
        for new_chrom in new_child_chromosomes:
            if not self.is_valid_path(new_chrom.path_order):
                raise Exception("Crossover path is not valid!: \n" + str(new_chrom))
        
        return new_child_chromosomes


    def is_valid_path(self, houses_list):
        for i in self.path_order:
            if i not in houses_list:
                return False
        return True


    def fitness(self):
        distance = 0
        for warehouse_idx, route in zip(self.truck_warehouse_indices, self.truck_routes):
            start, end = route
            # warehouse to first home
            distance += self.path_order[start].distance_to(warehouse_idx)
            # ith home to jth home (i>0 and j<# homes)
            for home_i, home_j in zip(self.path_order[start:end], self.path_order[start+1:end]):
                distance += home_i.distance_to(home_j.xy_index)
            # last home back to warehouse
            distance += self.path_order[end].distance_to(warehouse_idx)
        return distance
            


    def __str__(self):
        return self.path_order.__str__()



if __name__=="__main__":
    x_list = [Home([random.randint(0,100), random.randint(0,100)], x) for x in range(11)]
    y_list = x_list.copy()
    random.shuffle(y_list)

    warehouse_locations = [[random.randint(0,100), random.randint(0,100)] for x in range(1)]

    x = Chromosome(x_list, warehouse_locations)
    y = Chromosome(y_list, warehouse_locations)

    z = x.crossover(y)
    print(x.fitness())
    print(y.fitness())
    print(z[0].fitness())
    print(z[1].fitness())

    #print(x.mutate())