def load_cook_book(path):
    cook_book = {}
    with open(path, 'r', encoding='UTF-8') as filehandle:
        for dish in filehandle.read().split('\n\n'):
            dish_name = dish.split('\n')[0]
            cook_book[dish_name] = []
            num_lines = int(dish.split('\n')[1])
            for i in range(num_lines):
                line = dish.split('\n')[2 + i]
                cook_book[dish_name].append({
                    'ingredient_name': line.split('|')[0].strip(),
                    'quantity': int(line.split('|')[1].strip()),
                    'measure': line.split('|')[2].strip()
                                            })
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    result = {}
    for dish in cook_book:
        if dish in dishes:
            for ingredient in cook_book[dish]:
                if ingredient['ingredient_name'] in result:
                    result[ingredient['ingredient_name']]['quantity'] += \
                                person_count * ingredient['quantity']
                else:
                    result[ingredient['ingredient_name']] = {
                        'measure': ingredient['measure'],
                        'quantity': ingredient['quantity'] * person_count
                                                            }
    return result


def join_and_sort_files(dir_, amount_of_files):
    all_files = {}
    for i in range(1, amount_of_files + 1):
        name = f'{i}.txt'
        with open(f'{dir_}{name}', 'r', encoding='UTF-8') as f:
            all_files[name] = f.readlines()
    all_files_list = sorted(all_files.items(), key=lambda x: len(x[1]))

    with open(f'{dir_}result.txt', 'w', encoding='UTF-8') as f:
        for i, pair in enumerate(all_files_list):
            f.write(f'{pair[0]}\n')
            f.write(str(len(''.join(pair[1]).split("\n"))) + '\n')
            f.write("".join(pair[1]) + '\n') if i != len(all_files_list) - 1 \
                                             else f.write("".join(pair[1]))
    print(f'Файл {dir_}result.txt создан.')


def main():
    print('\t\tзадание 1')
    cook_book = load_cook_book('data/recipes.txt')
    for dish in cook_book:
        print(dish)
        for line in cook_book[dish]:
            print(*line.values())
        print()

    print('\t\tзадание 2')
    dish_list = []
    for i, dish in enumerate(cook_book):
        print(f'{i + 1}. {dish}')
    print('введите номера блюд в одну строку через пробел: \t')
    choice = list(map(int, input().strip().split(' ')))
    for i, dish in enumerate(cook_book):
        if i + 1 in choice:
            dish_list.append(dish)
    print(*dish_list, sep=', ')
    result = get_shop_list_by_dishes(dish_list,
                                     int(input('введите количество персон\t')),
                                     cook_book)
    for ingredient in result:
        print(ingredient, end='\t')
        print(*list(result[ingredient].values())[::-1])
    print()

    print('\t\tзадание 3')
    join_and_sort_files('files/', 3)


main()
