from datetime import datetime
from random import choice

from colorama import init, Fore

from application import *


if __name__ == '__main__':
    init()
    employees = get_employees()
    print(datetime.now().strftime("%d.%m.%Y %H:%M"))
    print()
    for employee in employees:
        color = choice([Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW])
        print(f'{color}{calculate_salary(employee)}')
        
