import request


class SuperHeroesAPI:
    host = 'https://akabab.github.io/superhero-api/api'
    alter_host = 'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api'

    def get_all_json(self, alt=False):
        uri = '/all.json'
        url = self.alter_host + uri if alt else self.host + uri
        response = requests.get(url)
        return response.json()


def find_smartest(chars, names):
    intel_dict = {}
    for char in chars:
        if char['name'] in names:
            intel_dict[char['name']] = char['powerstats']['intelligence']
    smartest = max(intel_dict, key=intel_dict.get)
    return f'Самый умный из {", ".join(names[:-1])} и {names[-1]} - ' \
           f'{smartest}. Его "intelligence": {intel_dict[smartest]}'


if __name__ == '__main__':
    super_heroes = SuperHeroesAPI()
    all_chars = super_heroes.get_all_json()
    print(find_smartest(all_chars, ['Hulk', 'Captain America', 'Thanos']))
    input()

