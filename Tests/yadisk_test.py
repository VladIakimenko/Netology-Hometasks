from unittest import TestCase
import os

import requests

TOKEN_PATH = 'data/secret.token'
RQST_LINK = 'https://cloud-api.yandex.net/v1/disk/resources'


def send_request(method, headers, path):
    link = RQST_LINK
    params = {'path': path}
    response = getattr(requests, method)(link, headers=headers, params=params)
    return response


class TestYaDiskApi(TestCase):
    """
    Проверим правильность работы Яндекс.Диск REST API.
    Написать тесты, проверяющий создание папки на Диске.
    Используя библиотеку requests напишите unit-test на верный ответ
    и возможные отрицательные тесты на ответы с ошибкой

    Пример положительных тестов:

    Код ответа соответствует 200.
    Результат создания папки - папка появилась в списке файлов.
    """
    token = ''
    headers = ''
    folder_name = 'test_folder'

    @classmethod
    def setUpClass(cls):
        directory = TOKEN_PATH.replace('\\', '/').rpartition('/')[0]
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rt', encoding='UTF-8') as token_file:
                cls.token = token_file.read().rstrip()

        if not os.path.exists(TOKEN_PATH) or not cls.token:
            with open(TOKEN_PATH, 'wt', encoding='UTF-8') as token_file:
                cls.token = input(f'Enter token from https://yandex.ru/dev/disk/poligon/:\t')
                token_file.write(cls.token)

        cls.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {cls.token}',
            'Connection': 'keep-alive'
        }

    def test_folder_creation_201(self):
        result_put = send_request('put', self.headers, self.folder_name)
        result_get = send_request('get', self.headers, self.folder_name)
        self.assertEqual(201, result_put.status_code) \
            and self.assertEqual(self.folder_name, result_get.json().get('name'))

    def test_folder_creation_401(self):
        wrong_headers = self.headers.copy()
        del(wrong_headers['Authorization'])
        result = send_request('put', wrong_headers, self.folder_name)
        self.assertEqual(401, result.status_code)

    def test_folder_creation_409(self):
        send_request('put', self.headers, self.folder_name)
        result = send_request('put', self.headers, self.folder_name)
        self.assertEqual(409, result.status_code)

    def tearDown(self):
        send_request('delete', self.headers, self.folder_name)

