import kobis_crawler as kc
import naver_crawler as nc
import tmdb_crawler as tc
import mysql_repository
import datetime
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir + '/api_keys.json', 'r') as fp:
    keys = json.load(fp)

with open(current_dir + '/mysql_connect_conf.json') as fp:
    mysql_config = json.load(fp)

kobis = kc.KobisCrawler(api_keys=keys['kobis'])
naver = nc.NaverCrawler(api_keys=keys['naver'])
tmdb = tc.TmdbCrawler(api_keys=keys['tmdb'])
repository = mysql_repository.MySqlRepository(config=mysql_config)

start_date = datetime.date.today() - datetime.timedelta(days=10)
end_date = start_date

date_range = [datetime.date.fromordinal(i) for i in range(
    start_date.toordinal(), end_date.toordinal() + 1)]

movieCd_dict = dict()
boxoffice_records = []

for target_date in date_range:
    new_boxoffice_records = kobis.get_boxoffice_40ranks(target_date)
    boxoffice_records.extend(new_boxoffice_records)

for record in boxoffice_records:
    if record['movieCd'] not in movieCd_dict.keys():
        movieCd_dict[record['movieCd']] = (record['multi'], record['nation'])

unique_movie_records = []
for unique_movieCd in repository.get_unique_new_movie(movieCd_dict.keys()):
    try:
        movie_detail = kobis.get_movie_detail(unique_movieCd)
    except KeyError:
        print("error movieCd : " + unique_movieCd)
        exit(1)
    tmdbId = tmdb.get_movie_id(
        movie_detail['movieNm'], movie_detail['movieNmEn'])
    unique_movie_records.append({'movieCd': unique_movieCd,
                                 'movieNm': movie_detail['movieNm'],
                                 'movieNmEn': movie_detail['movieNmEn'],
                                 'movieNmOg': movie_detail['movieNmOg'],
                                 'tmdbId': tmdbId, 'multi': movieCd_dict[unique_movieCd][0], 'nation': movieCd_dict[unique_movieCd][1]})

repository.add_to_movie(unique_movie_records)
repository.add_to_boxoffice(boxoffice_records)

repository.close()
