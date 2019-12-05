import json
import requests


class TmdbCrawler:

    urls = {
        'movieList': 'https://api.themoviedb.org/3/search/movie',
        'movieDetail': 'https://api.themoviedb.org/3/movie/%s',
        'peopleList': 'https://api.themoviedb.org/3/search/person',
        'peopleDetail': ''
    }

    def __init__(self, **kwargs):
        if 'api_keys' in kwargs.keys():
            self.api_keys = kwargs['api_keys']
        else:
            with open('api_keys.json', 'r') as fp:
                self.api_keys = json.load(fp)['tmdb']

    def refresh_api_key(self):
        self.api_keys.pop()

    def request_with_api_keys(self, request_endpoint, request_params, path_var=None):
        value = None
        while len(self.api_keys) > 0:
            try:
                request_params['api_key'] = self.api_keys[-1]
                if path_var is None:
                    value = requests.get(
                        self.urls[request_endpoint], params=request_params).json()
                else:
                    value = requests.get(
                        self.urls[request_endpoint] % path_var, params=request_params).json()
                break
            except Exception as e:
                print(e)
                print('refresh api key')
                self.refresh_api_key()
                continue
        return value

    def get_movie_id(self, movieNm, movieNmEn):
        value = self.request_with_api_keys('movieList', {
                                           'language': 'ko-KR', 'query': movieNm, 'region': 'KR', 'include_adult': 'true'})
        if len(value['results']) == 0 and movieNmEn != '':
            value = self.request_with_api_keys('movieList', {
                                               'language': 'en-US', 'query': movieNmEn, 'region': 'KR', 'include_adult': 'true'})
        if len(value['results']) == 0:
            return -1

        return value['results'][0]['id']

    def get_movie_detail(self, movieNm):
        movie_id = self.get_movie_id(movieNm, '')

        if movie_id == -1:
            return None

        detailed_data = self.request_with_api_keys('movieDetail', {
                                                   'language': 'ko-KR', 'append_to_response': 'images,videos'}, movie_id)

        return detailed_data

    def get_people_list(self, peopleNm):
        value = self.request_with_api_keys(
            'peopleList', {'language': 'ko-KR', 'query': peopleNm})
        return value['results']
