import random


weights = [20, 30, 60, 90, 50, 70, 30]
priorities = [6, 5, 8, 7, 6, 9, 4]
items = 7
pop_size = 100


def weight(c):
    sum_weight = 0
    for i in range(items):
        if c[i]:
            sum_weight += weights[i]
    return sum_weight


# fitness function is the sum of priorities
# if the chromosome is overweight, we give it a fitness score of 0,
# so later it will be sorted at the bottom of the population
def fitness(c):
    fitness = 0
    for i in range(items):
        if weight(c) > 120:
            fitness = 0
        else:
            if c[i]:
                fitness += priorities[i]
    return fitness


def first_pop():
    # randomly generate many different individuals in population with size of 100
    population = []
    for i in range(pop_size):
        individual = []
        for index in range(items):
            rand_num = random.randint(0, 99)
            if rand_num > 50:
                rand_num = 0
            else:
                rand_num = 1
            individual.append(rand_num)
        fit = fitness(individual)
        # [0]:fitness [1]:individual chromosome
        # later we will sort it by the first element (fitness), and then cull 50% of them
        population.append([fit, individual])
    return population


def crossover(mate1, mate2):
    lucky = random.randint(0, len(mate1) - 1)
    return mate1[0:lucky] + mate2[lucky:]


def mutate(c):
    # Probability of mutation = 50% (it's an arbitrary number)
    if random.randint(0, 10) == 0:
        for i in range(1, items):
            if c[i] == 1:
                c[i] = 0
            else:
                c[i] = 1
    return c


# select chromosome from population
def select(p):
    ch = random.randint(1, len(p) - 1)
    # [1] is the chromosome of the (ch)th element in p
    return p[ch][1]


def cull(p):
    # sort by fitness (p[0])
    p = sorted(p, reverse=True)
    # Cull your population by 50 % at every generation
    p = p[:50]
    return p


def genetic_alg():
    cur_pop = first_pop()
    best_fitness = 0
    best_chromosome = []
    for iteration in range(0, 100):
        new_pop = []
        for i in range(0, pop_size):
            mate1 = select(cur_pop)
            mate2 = select(cur_pop)
            new_ch = crossover(mate1, mate2)
            new_ch = mutate(new_ch)
            new_fit = fitness(new_ch)
            new_pop.append([new_fit, new_ch])
        cull(new_pop)
        for individual in new_pop:
            if individual[0] > best_fitness:
                best_fitness = individual[0]
                best_chromosome = individual[1]
        cur_pop = new_pop
        
    print('The best chromosome is: ' + str(best_chromosome))
    print('The optimal allocation of the bag is :')
    for i in range(len(best_chromosome)):
        if best_chromosome[i]:
            print('Item ' + str(i + 1) + ' --' + ' weight:' + str(weights[i]) + '  priority:' + str(priorities[i]))
    print('The priority total is : ' + str(best_fitness))


genetic_alg()
