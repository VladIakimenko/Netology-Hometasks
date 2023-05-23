import requests


class VKLoader:
    host = 'https://api.vk.com'

    def __init__(self, token):
        self.params = {'access_token': token, 'v': '5.131'}

    def create_album(self, title, description):
        url = self.host + '/method/photos.createAlbum'
        params = {**{'title': title, 'description': description}, **self.params}
        request = requests.post(url, params=params)
        return request.json()['response']['id']

    def photos_get_server(self, album):
        url = self.host + '/method/photos.getUploadServer'
        params = {**{'album_id': album}, **self.params}
        request = requests.get(url, params=params)
        return request.json()['response']['upload_url']

    def send_picture(self, upload_url, file_list):
        url = upload_url
        files_dict = {}
        for i, path in enumerate(file_list):
            files_dict[f'file{i + 1}'] = (path, open(path, 'rb'), "multipart/form-data")
        request = requests.post(url,
                                params=self.params,
                                files=files_dict)

        return request.json()

    def save_picture(self, album_id, s_server, s_photos_list, s_hash, caption=''):
        url = self.host + '/method/photos.save'
        params = {**{'album_id': album_id,
                     'server': s_server,
                     'photos_list': s_photos_list,
                     'hash': s_hash,
                     'caption': caption},
                  **self.params}
        request = requests.post(url, params=params)

        return 'success' if request.status_code == 200 else 'error'


def convert(server_data):
    server = server_data['server']
    photos_list = server_data['photos_list']
    hash_ = server_data['hash']
    return server, photos_list, hash_


if __name__ == '__main__':
    loader = VKLoader(input('Введите TOKEN:\n'))

    title = input('Введите название альбома\t')
    description = input('Введите описание альбома\n')

    print("""
    Введите путь и название файлов.'
    Вводите по одному файлу за раз (5 файлов максимум), "enter" чтобы сохранить.
    Введите команду "end", чтобы закончить ввод файлов\n
          """)
    file_list = []
    path = ''
    while len(file_list) < 5:
        path = input()
        if path.lower().strip() != 'end':
            file_list.append(path)
            print(*file_list, sep=', ')
        else:
            break

    album = loader.create_album(title, description)
    link = loader.photos_get_server(album)

    print(loader.save_picture(album, *convert(loader.send_picture(link, file_list))))

    input()
