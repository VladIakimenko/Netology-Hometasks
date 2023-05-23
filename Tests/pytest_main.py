import pytest

from main import filter_visits, unique_ids, words_spreadout


class TestMain:
    @pytest.mark.parametrize("test_data, expected", [
        ([
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
         ])
    ])
    def test_filter_visits(self, test_data, expected):
        result = filter_visits(test_data)
        assert result == expected

    @pytest.mark.parametrize("test_data, expected", [
        ({'user1': [213, 213, 213, 213, 213],
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
         ['foo', 'bar', 'bas', '1', 1, 'one', '2', ' 2', None])
    ])
    def test_unique_ids(self, test_data, expected):
        result = unique_ids(test_data)
        assert all([el in expected for el in result]) \
               and not any([el not in expected for el in result])

    @pytest.mark.parametrize("test_data, expected", [
        (['смотреть сериалы онлайн',
          'курс доллара'],
         {2: '50%', 3: '50%'}),
        ([],
         {}),
        (['смотреть сериалы онлайн',
          'курс доллара',
          'новости'],
         {1: '33%', 2: '33%', 3: '33%'})
    ])
    def test_words_spreadout(self, test_data, expected):
        result = words_spreadout(test_data)
        assert all([el in expected.items() for el in result.items()]) \
               and not any([el not in expected.items() for el in result.items()])
