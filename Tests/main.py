def filter_visits(geo_logs):
    """
    Задание 1
    Дан список с визитами по городам и странам.
    Напишите код, который возвращает отфильтрованный список geo_logs, содержащий только визиты из России.

    """
    return list(filter(lambda dct: 'россия' in [location.casefold()
                                                for location in list(dct.values())[0]],
                       geo_logs))


def unique_ids(ids):
    """
    Задание 2
    Выведите на экран все уникальные гео-ID из значений словаря ids.
    Т.е. список вида [213, 15, 54, 119, 98, 35]
    """
    return list(set([id_ for ids in ids.values() for id_ in ids]))


def words_spreadout(queries):
    """
    Задание 3
    Дан список поисковых запросов. Получить распределение количества слов в них.
    Т.е. поисковых запросов из одного - слова 5%, из двух - 7%, из трех - 3% и т.д.
    """
    return {len(query.split()):
            f'{round((len([q for q in queries if len(q.split()) == len(query.split())]) * 100) / len(queries))}%'
            for query in queries}


if __name__ == '__main__':

    geo_logs_data = [
        {'visit1': ['Москва', 'Россия']},
        {'visit2': ['Дели', 'Индия']},
        {'visit3': ['Владимир', 'Россия']},
        {'visit4': ['Лиссабон', 'Португалия']},
        {'visit5': ['Париж', 'Франция']},
        {'visit6': ['Лиссабон', 'Португалия']},
        {'visit7': ['Тула', 'Россия']},
        {'visit8': ['Тула', 'Россия']},
        {'visit9': ['Курск', 'Россия']},
        {'visit10': ['Архангельск', 'Россия']}
    ]

    ids_data = {'user1': [213, 213, 213, 15, 213],
                'user2': [54, 54, 119, 119, 119],
                'user3': [213, 98, 98, 35]}

    queries_data = [
        'смотреть сериалы онлайн',
        'новости спорта',
        'афиша кино',
        'курс доллара',
        'сериалы этим летом',
        'курс по питону',
        'сериалы про спорт'
        ]

    print(filter_visits(geo_logs_data))
    print(unique_ids(ids_data))
    print(words_spreadout(queries_data))
