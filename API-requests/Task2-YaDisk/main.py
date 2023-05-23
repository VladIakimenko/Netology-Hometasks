import requests


class YandexDisk:
    host = 'https://cloud-api.yandex.net:443'

    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def get_link_upload_file(self, path, overwrite=True):
        uri = '/v1/disk/resources/upload'
        params = {'path': path, 'overwrite': overwrite}
        response = requests.get(self.host + uri, headers=self.headers, params=params)
        if response.status_code == 200:
            print('Ссылка для загрузки файла успешно получена...')
            return response.json()['href']
        else:
            print(f'Ошибка {response.status_code}')

    def upload_file(self, path, url, f):
        params = {'path': path}
        files = {'file': f}
        response = requests.put(url, headers=self.headers, params=params, files=files)
        if response.status_code == 201:
            return 'Файл успешно загружен'
        else:
            print(f'Ошибка {response.status_code}')

    def check_existance(self, path):
        uri = '/v1/disk/resources'
        params = {'path': path}
        response = requests.get(self.host + uri, headers=self.headers, params=params)
        return response.status_code

    def create_folder(self, path):
        uri = '/v1/disk/resources'
        params = {'path': path}
        response = requests.put(self.host + uri, headers=self.headers, params=params)
        if response.status_code == 201:
            return f'папка {path} успешно создана'
        else:
            return response.status_code


if __name__ == '__main__':
    ya_uploader = YandexDisk(input('введите TOKEN\n'))

    print('\nВведите путь и название файла на Яндекс Диске:')
    ya_disk_path = input().strip()
    file_name = "".join(ya_disk_path.split("/")[-1])
    print(f'    path = ./{"/".join(ya_disk_path.split("/")[:-1])}')
    print(f'    file name = {"".join(ya_disk_path.split("/")[-1])}')
    temp_path = ''
    for folder in ya_disk_path.split('/')[:-1]:
        temp_path += '/' + folder
        if ya_uploader.check_existance(temp_path) == 404:
            print(f'папка {temp_path} не найдена...')
            print(f'    ...идёт создание папки...')
            print(ya_uploader.create_folder(temp_path))

    if ya_uploader.check_existance(ya_disk_path) != 404:
        print('Файл с таким названием уже существует. Перезаписать? ("y" или "n")')
        reply = ''
        while reply not in ('y', 'n'):
            reply = input().strip().lower()
            if reply == 'n':
                ya_disk_path += '[duplicate]'

    print('\nВведите путь и название файла, который Вы хотите загрузить:')
    target_file_path = input().strip()
    upload_link = ya_uploader.get_link_upload_file(ya_disk_path)
    with open(target_file_path, 'rb') as f:
        print(ya_uploader.upload_file(target_file_path, upload_link, f)) \
            if upload_link \
            else print('Загрука файла не произведена')

    input()
