from random import random


class Individual:
    def __init__(self, spaces, prices, space_limit, generation=0):
        self.spaces = spaces
        self.prices = prices
        self.space_limit = space_limit
        self.score_evaluation = 0
        self.used_space = 0
        self.generation = generation
        self.chromosome = []
        for i in range(len(spaces)):
            if random() < 0.5:
                self.chromosome.append('0')
            else:
                self.chromosome.append('1')

    def fitness(self):
        score = 0
        sum_spaces = 0
        for i in range(len(self.chromosome)):
            if self.chromosome[i] == '1':
                score += self.prices[i]
                sum_spaces += self.spaces[i]
        if sum_spaces > self.space_limit:
            score = 1
        self.score_evaluation = score
        self.used_space = sum_spaces
        return score, sum_spaces

    def crossover(self, other_individual):
        cutoff = round(random() * len(self.chromosome))
        # print('cutoff: ', cutoff)
        child1 = other_individual.chromosome[0:cutoff] + self.chromosome[cutoff::]
        child2 = self.chromosome[0:cutoff] + other_individual.chromosome[cutoff::]
        # print('child1: ', child1)
        # print('child2: ', child2)
        children = [Individual(self.spaces, self.prices, self.space_limit, self.generation + 1),
                    Individual(self.spaces, self.prices, self.space_limit, self.generation + 1)]
        children[0].chromosome = child1
        children[1].chromosome = child2

        return children

    def mutation(self, mutation_rate):
        # print('Before: ', self.chromosome)
        for i in range(len(self.chromosome)):
            if random() < mutation_rate:
                if self.chromosome[i] == '1':
                    self.chromosome[i] = '0'
                else:
                    self.chromosome[i] = '1'

        # print('After:  ', self.chromosome)

        return self
