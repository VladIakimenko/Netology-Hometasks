from unittest import TestCase

from main import filter_visits, unique_ids, words_spreadout


class TestFilterVisits(TestCase):
    def test_parametrized(self):
        test_cases = (([
                           {'visit1': ['Москва', 'Россия']},
                           {'visit2': ['Дели', 'Индия']},
                           {'visit3': ['Владимир', 'Россия']}
                       ],
                       [
                           {'visit1': ['Москва', 'Россия']},
                           {'visit3': ['Владимир', 'Россия']}
                       ]),
                      ([
                           {'visit1': ['Москва', 'россия']},
                           {'visit2': ['Дели', 'Индия']},
                           {'visit3': ['Владимир', 'Россия']}
                       ],
                       [
                           {'visit1': ['Москва', 'россия']},
                           {'visit3': ['Владимир', 'Россия']}
                       ]),
                      ([
                           {'visit1': ['Россия', 'Москва']},
                           {'visit2': ['Дели', 'Индия']},
                           {'visit3': ['Владимир', 'Россия']}
                       ],
                       [
                           {'visit1': ['Россия', 'Москва']},
                           {'visit3': ['Владимир', 'Россия']}
                       ]))
        for i, (test_data, expected) in enumerate(test_cases):
            with self.subTest(i=i, test_data=test_data, expected=expected):
                result = filter_visits(test_data)
                self.assertEqual(result, expected)


class TestUniqueIds(TestCase):
    def test_parametrized(self):
        test_cases = (({'user1': [213, 213, 213, 213, 213],
                        'user2': [0, 0, 0, 0, 0],
                        'user3': [312, 312, 312, 312]},
                       [213, 0, 312]),
                      ({'user1': [],
                        'user2': [],
                        'user3': []},
                       []),
                      ({'user1': ['foo', 'bar', 'bas'],
                        'user2': ['1', 1, 'one'],
                        'user3': ['2', ' 2', None]},
                       ['foo', 'bar', 'bas', '1', 1, 'one', '2', ' 2', None]))
        for i, (test_data, expected) in enumerate(test_cases):
            with self.subTest(i=i, test_data=test_data, expected=expected):
                result = unique_ids(test_data)
                self.assertCountEqual(result, expected)


class TestWordsSpreadout(TestCase):
    def test_parametrized(self):
        test_cases = ((['смотреть сериалы онлайн',
                        'курс доллара'],
                       {2: '50%', 3: '50%'}),
                      ([],
                       {}),
                      (['смотреть сериалы онлайн',
                        'курс доллара',
                        'новости'],
                       {1: '33%', 2: '33%', 3: '33%'}))
        for i, (test_data, expected) in enumerate(test_cases):
            with self.subTest(i=i, test_data=test_data, expected=expected):
                result = words_spreadout(test_data)
                self.assertCountEqual(result.items(), expected.items())












