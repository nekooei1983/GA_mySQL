# import matplotlib.pyplot as plt
import pymysql

from GeneticAlgorithm import GeneticAlgorithm


class Product:
    def __init__(self, name, space, price):
        self.name = name
        self.space = space
        self.price = price


if __name__ == '__main__':
    products_list = []
    connection = pymysql.connect(host='localhost', user='root', passwd='8245438', db='products')
    cursor = connection.cursor()
    cursor.execute('select product_name, space, price, quantity from products')
    #for product in cursor:
    #    print(product)

    for product in cursor:
        # print(product[0], product[1], product[2])
        for i in range(product[3]):
            products_list.append(Product(product[0], product[1], product[2]))

    cursor.close()
    connection.close()

    spaces = []
    prices = []
    names = []
    for product in products_list:
        print(product.name, '-', product.space, '-', product.price)
        spaces.append(product.space)
        names.append(product.name)
        prices.append(product.price)

    limit = 10  # Maximum capacity of the Truck
    population_size = 20
    mutation_probability = 0.01
    number_of_generation = 100
    ga = GeneticAlgorithm(population_size)
    result = ga.solve(mutation_probability, number_of_generation, spaces, prices, limit)
    ga.visualize_solutionsv1(number_of_generation)
    ga.visualize_solutionsv2()
    print(result)
    for i in range(len(products_list)):
        if result[i] == '1':
            print("Name: ", products_list[i].name, " - Price: ", products_list[i].price)
