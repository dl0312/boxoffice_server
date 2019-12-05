import requests
import json
from datetime import *


class ApiUnavailableException(Exception):
    def __init__(self, msg="Api Key Unavailable!!"):
        self.msg = msg

    def __str__(self):
        return self.msg


class KobisCrawler:
    urls = {
        'boxOffice': 'https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json',
        'movieDetail': 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json',
        'peopleList': 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json',
        'peopleDetail': 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json',
        'companyDetail': 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.json'
    }

    def __init__(self, **kwargs):
        if 'api_keys' in kwargs.keys():
            self.api_keys = kwargs['api_keys']
        else:
            with open('api_keys.json', 'r') as fp:
                self.api_keys = json.load(fp)['kobis']

    def refresh_api_key(self):
        self.api_keys.pop()

    def request_with_api_keys(self, request_endpoint, request_params):
        value = None
        while len(self.api_keys) > 0:
            try:
                request_params['key'] = self.api_keys[-1]
                value = requests.get(
                    self.urls[request_endpoint], params=request_params).json()
                break
            except Exception:
                print('refresh api key')
                self.refresh_api_key()
                continue
        return value

    def get_movie_detail(self, movieCd):
        value = self.request_with_api_keys('movieDetail', {'movieCd': movieCd})

        return value['movieInfoResult']['movieInfo']

    def get_company_detail(self, companyCd):
        value = self.request_with_api_keys(
            'companyDetail', {'companyCd': companyCd})
        return value['companyInfoResult']['companyInfo']

    def search_people_in_movie(self, movieNm, peopleNm):
        value1 = self.request_with_api_keys(
            'peopleList', {'peopleNm': peopleNm, 'filmoNames': movieNm})
        return self.get_people_detail(value1['peopleListResult']['peopleList'][0]['peopleCd'])

    def get_people_detail(self, peopleCd):
        value = self.request_with_api_keys(
            'peopleDetail', {'peopleCd': peopleCd})
        return value['peopleInfoResult']['peopleInfo']

    def get_boxoffice_daily_list(self, day, multi, nation):
        value = self.request_with_api_keys('boxOffice', {'targetDt': day.strftime(
            '%Y%m%d'), 'multiMovieYn': multi, 'repNationCd': nation})
        value = value['boxOfficeResult']['dailyBoxOfficeList']

        for i, e in enumerate(value):
            value[i] = {
                'audiAcc': e['audiAcc'],
                'audiChange': e['audiChange'],
                'audiCnt': e['audiCnt'],
                'currentDate': day.strftime('%Y-%m-%d'),
                'movieCd': e['movieCd'],
                'multi': multi,
                'nation': nation,
                'rank': e['rank'],
                'rankInten': e['rankInten'],
                'rankOldAndNew': 1 if e['rankOldAndNew'] == 'NEW' else 0,
                'salesAcc': e['salesAcc'],
                'salesAmt': e['salesAmt'],
                'salesChange': e['salesChange'],
                'salesShare': e['salesShare'],
                'scrnCnt': e['scrnCnt'],
                'showCnt': e['showCnt']
            }

        return value

    def get_boxoffice_40ranks(self, day):
        result = []

        for multi, rep in zip(['Y', 'Y', 'N', 'N'], ['K', 'F', 'K', 'F']):
            tmp = self.get_boxoffice_daily_list(day, multi, rep)
            result.extend(tmp)

        result.sort(key=lambda x: -int(x['audiCnt']))
        for i in range(len(result)):
            try:
                result[i]['totalRank'] = i+1
            except IndexError:
                print('index error : ', i, 'length : ',
                      len(result), 'day : ', str(day))
                exit(1)

        return result
