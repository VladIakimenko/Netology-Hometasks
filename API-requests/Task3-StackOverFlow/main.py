import requests
import time
import datetime
from pprint import pprint


class StackOverFlow:
    host = 'https://api.stackexchange.com/'

    def get_questions(self, from_date, tagged):
        uri = '/2.3/questions/'
        params = {
            'order': 'desc',
            'sort': 'activity',
            'site': 'stackoverflow',
            'fromdate': from_date,
            'tagged': tagged
                  }
        response = requests.get(self.host + uri, params=params)
        return response.json()


if __name__ == '__main__':
    downloader = StackOverFlow()
    date = datetime.date.today() - datetime.timedelta(days=2)
    unixdate = int(time.mktime(date.timetuple()))

    questions = downloader.get_questions(unixdate, 'python')
    # pprint(questions['items'])

    for i, question in enumerate(questions['items']):
        print(f"{i + 1}. {question['title']}\n{question['link']}\n")

    input()
