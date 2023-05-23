import random


def get_employees():
    employees = []
    with open('application/db/names.txt', 'rt', encoding='UTF-8') as f:
        male_names, female_names, surnames = [line.rstrip().split(',') 
                                              for line in f.readlines()]
    
    for _ in range(random.randrange(1,1001)):
        employees.append(f'{random.choice(male_names + female_names).strip()} '
                         f'{random.choice(surnames).strip()}')
    return employees
