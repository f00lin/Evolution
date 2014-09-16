#Hardy-Weinberg equilibrium -- calculates expected genotype frequencies from allele
#frequencies

#frequency of genotypes reaches Hardy-Weinberg equilibrium after one generation of
#random mating and fertilization

##REQUIRES

#diploidy
#sexual reproduction


##ASSUMES:

#random mating
#equal reproductive success
#no mutations
#no effect of selection
#no effect of migration


# p2 + 2pq + q2 = 1

#using #1 produces a population where 0 and 1 alleles are 50% each and the mix of
#11, 10 and 00 genotypes are as expected.  using #2 produces a population where 1 and
#0 alleles are still 50% each, but 11 and 00 genotypes are unexpectedly common and
#10 genotypes are unexpectedly rare given the frequency of the alleles



import random
from copy import deepcopy

alleles = [1, 0]



#migration variables

#outsider_pop = [[[0], [0]], [[1], [1]]]
outsider_pop = [[[1], [0]], [[0], [1]]]

migration_rate = 0



def agent():
    agent = [[], []]
    agent[0].append(random.choice(alleles))
    agent[1].append(random.choice(alleles))    #1 produces a population in H-W equ.
    #agent[1].append(agent[0][0])                #2 produces pop out of H-W equ.
    return agent

#print(agent())



def population(size):
    pop = []
    for i in range(size):
        pop.append(agent())
    return pop

#print(population(100))




def select_parent(pop):
    return random.choice(pop)



def mating_pair(pop):
    pair = []
    first = select_parent(pop)
    pair.append(first)
    temp = deepcopy(pop)
    temp.remove(first)
    second = select_parent(temp)
    pair.append(second)
    del temp
    return pair




"""
#makes it impossible for heterozygotes to breed with homozygotes
#actually no use in current model

def mating_pair_2(pop):
    pair = []
    first = select_parent(pop)
    pair.append(first)
    if first[0][0] != first[1][0]:
        while len(pair) < 2:
            temp = deepcopy(pop)
            second = select_parent(temp)
            if second[0][0] != second[1][0]:
                pair.append(second)
    if first[0][0] == first[1][0]:
        while len(pair) < 2:
            temp = deepcopy(pop)
            second = select_parent(temp)
            if second[0][0] == second[1][0]:
                pair.append(second)
    return pair

#print(mating_pair_2(population(100)))
            
"""            

    
    

def cross_over(pop):
    parents = mating_pair(pop)
    #parents = mating_pair_2(pop)
    offspring = []
    for index, object in enumerate(parents[0]):
        rand = random.random()
        if rand < 0.5:
            offspring.append(parents[0][index])
        if rand > 0.5:
            offspring.append(parents[1][index])
    return offspring

#print(cross_over(population(100)))




def new_gen(pop, size):
    next_gen = []
    for i in range(size):
        rand = random.random()
        if rand > migration_rate:
            offspring = cross_over(pop)
            next_gen.append(offspring)
        if rand < migration_rate:
            offspring = random.choice(outsider_pop)
            next_gen.append(offspring)
    return next_gen

#print(new_gen(population(100), 100))
    


#returns a list of the observed genome frequencies

def observed_gen_freqs(pop):
    one_one = 0
    hetero = 0
    zero_zero = 0
    for i in pop:
        if i[0][0] == 1:
            if i[1][0] == 1:
                 one_one += 1
        if i[0][0] == 0:
            if i[1][0] == 0:
                zero_zero += 1
        if i[0][0] != i[1][0]:
            hetero += 1
    return [one_one, hetero, zero_zero]

#print(observed_gen_freqs(new_gen(population(100), 100)))




#returns list of observed genome frequencies and expected genome frequencies if
#population was in Hardy-Weinberg equilibrium

def observed_expected(pop):
    obs_exp = []
    observed = observed_gen_freqs(pop)
    obs_exp.append(observed)
    one = float((observed[1] + 2*observed[0])) / (2*len(pop))
    zero = float(1-one)
    homo_one = (one**2) * (len(pop))                #p2
    hetero = (2*one*zero) * (len(pop))               #2pq
    homo_zero = (zero**2) * (len(pop))              #q2
    obs_exp.append([homo_one, hetero, homo_zero])
    return obs_exp

#print(observed_expected(new_gen(population(100), 100)))





#compares the expected genome frequencies with the observed to see if the difference
#is significant, to see, that is, if the population is NOT in Hardy-Weinberg equilibrium
#and so possibly IS subject to something such as selection, assortative mating or
#migration    
    
def chi_squared(comp):
    print(comp)
    comp1 = comp[0]
    comp2 = comp[1]
    likely = []
    for index, object in enumerate(comp1):
        temp = float(((comp1[index] - comp2[index])**2) / (comp1[index]))
        likely.append(temp)
    return likely

#print(chi_squared(observed_expected(new_gen(population(100), 100))))
        
    


def simulation(pop, gens, size):
    for i in range(gens):
        pop = new_gen(pop, size)
    return chi_squared(observed_expected(pop))
            
print(simulation(population(100), 1, 100))







    
                     



    
    
    
    
    
