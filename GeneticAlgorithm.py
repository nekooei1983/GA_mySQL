from Individual import Individual
from random import random
import plotly.express as px
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        self.generation = 0
        self.best_solution = None
        self.list_of_solution = []

    def initialize_population(self, spaces, prices, space_limit):
        for i in range(self.population_size):
            self.population.append(Individual(spaces, prices, space_limit))

        self.best_solution = self.population[0]

    def order_population(self):
        self.population = sorted(self.population, key=lambda population: population.score_evaluation, reverse=True)

    def best_individual(self, individual):
        if individual.score_evaluation > self.best_solution.score_evaluation:
            self.best_solution = individual

    def sum_evaluations(self):
        sum_eval = 0
        for individual in self.population:
            sum_eval += individual.score_evaluation
        return sum_eval

    def select_parent(self, sum_evaluation):
        parent = -1
        random_value = random() * sum_evaluation
        tmp_sum = 0
        i = 0
        # print("*** Random value:", random_value)
        while i < len(self.population) and tmp_sum < random_value:
            # print("i: ", i, " - tmp_sum: ", tmp_sum)
            tmp_sum += self.population[i].score_evaluation
            parent += 1
            i += 1

        # print("Parent: ", parent, " - tmp_sum: ", tmp_sum)
        return parent

    def visualize_generation(self):
        best = self.population[0]
        print("Generation: ", self.population[0].generation,
              "Total price: ", best.score_evaluation, "Space: ", best.used_space,
              "Chromosome: ", best.chromosome)

    def visualize_solutionsv1(self, number_ge):
        figure = px.line(x=range(0, number_ge+1), y=self.list_of_solution, title="Genetic Algorithm results")
        figure.show()


    def visualize_solutionsv2(self):
        plt.plot(self.list_of_solution)
        plt.title("Genetic Algorithm results")
        plt.show()

    def solve(self, mutation_probability, number_of_generations, spaces, prices, limit):
        self.initialize_population(spaces, prices, limit)

        # Evaluate the population
        for individual in self.population:
            individual.fitness()
        # Order the population where the best is at top
        self.order_population()
        self.best_solution = self.population[0]
        self.list_of_solution.append(self.best_solution.score_evaluation)

        self.visualize_generation()

        for generation in range(number_of_generations):
            sum_roulette = self.sum_evaluations()
            new_population = []
            for new_individual in range(0, self.population_size, 2):
                parent1 = self.select_parent(sum_roulette)
                parent2 = self.select_parent(sum_roulette)
                children = self.population[parent1].crossover(self.population[parent2])
                new_population.append(children[0].mutation(mutation_probability))
                new_population.append(children[1].mutation(mutation_probability))
            # Create the new generation
            self.population = list(new_population)
            # Evaluate the population
            for individual in self.population:
                individual.fitness()
            # Order the population where the best is at top
            self.order_population()
            best = self.population[0]
            self.best_individual(best)
            self.list_of_solution.append(self.best_solution.score_evaluation)
            self.visualize_generation()

        print("*** Best solution in Generation ", self.best_solution.generation,
              "Total price: ", self.best_solution.score_evaluation, "Space: ", self.best_solution.used_space,
              "Chromosome: ", self.best_solution.chromosome)
        return self.best_solution.chromosome
