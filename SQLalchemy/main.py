from models import *
from config import *
from postgres import Postgres
from sys import exit
import json


def read_population():
    with open(POPULATION, 'rt') as filehandle:
        pop = json.load(filehandle)
    return pop


def check_population(connect, pop):
    return sum([len(val) for val in connect.get_records().values()]) == len(pop)


def populate(connect, pop):
    for record in pop:
        connect.add_record(record['model'], **record['fields'])
    if check_population(connect, pop):
        print(f'Successfully populated as per {POPULATION}.\n'
              f'{len(population)} records added.')


def check_sales_by_publisher(connect):
    publishers = connect.get_records()['publisher']
    for publisher in publishers:
        print(*publisher)
    print()
    print('Type "quit" to exit,\n'
          'Enter publisher (number or name):')

    while True:
        id_pub = 0
        while id_pub == 0:
            input_ = input().lower().strip()
            if input_ in ('q', 'quit', 'exit', 'e', 'esc'):
                exit()
            for pub in publishers:
                if input_.isdigit() and pub[0] == int(input_) or input_ == pub[1].lower():
                    id_pub = pub[0]
                    break

        selection = Book.title, Shop.name, Sale.price, Sale.date_sale
        relations = Sale.stock, Stock.book, Stock.shop, Book.publisher
        filter_ = Publisher.id == id_pub

        result = connect.select(selection, relations, filter_)
        for record in result:
            print(*record, sep=' | ')


def launch():
    connect = Postgres()
    pop = read_population()
    return connect, pop


if __name__ == '__main__':
    connector, population = launch()

    if not connector.check_tables():
        print('TASK 1: Create 5 tables as per .png')
        connector.create_tables()
        if connector.check_tables():
            print('Successfully created.\n')

    if not check_population(connector, population):
        print('TASK 3: Populate DB with "data/population.json"')
        populate(connector, population)


    print()
    print('TASK 2: Display info on each sale by Publisher name')
    check_sales_by_publisher(connector)












