import json
import requests


class NaverCrawler:

    urls = {
        'movieList': 'https://openapi.naver.com/v1/search/movie.json'
    }

    def __init__(self, **kwargs):
        if 'api_keys' in kwargs.keys():
            self.api_keys = kwargs['api_keys']
        else:
            with open('api_keys.json', 'r') as fp:
                self.api_keys = json.load(fp)['naver']

    def refresh_api_key(self):
        self.api_keys.pop()

    def request_with_api_keys(self, request_endpoint, request_params):
        value = None
        while len(self.api_keys) > 0:
            try:
                header = {
                    'X-Naver-Client-Id': self.api_keys[-1]['clientId'],
                    'X-Naver-Client-Secret': self.api_keys[-1]['clientSecret']
                }
                value = requests.get(
                    self.urls[request_endpoint], headers=header, params=request_params).json()
                break
            except Exception:
                print('refresh api key')
                self.refresh_api_key()
                continue
        return value

    def searchMovie(self, movieNm):
        return self.request_with_api_keys('movieList', {'query': movieNm})
