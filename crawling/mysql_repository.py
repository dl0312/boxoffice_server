import json
import pymysql
import sql_builder


class MySqlRepository:

    sqls = {
        # 'insert_into_boxoffice': sql_builder.SQL(sql_type='insert', table='boxoffice', columns=[
        #     'audiAcc', 'audiChange', 'audiCnt', 'currentDate', 'movieCd', 'multi', 'nation',
        #     'rank', 'rankInten', 'rankOldAndNew', 'salesAcc', 'salesAmt', 'salesChange',
        #     'salesShare', 'scrnCnt', 'showCnt', 'totalRank'
        # ]),
        'insert_into_boxoffice': """INSERT INTO boxoffice
                                (`audiAcc`, `audiChange`, `audiCnt`, `currentDate`, `movieCd`, `multi`, `nation`,
                                            `rank`, `rankInten`, `rankOldAndNew`, `salesAcc`, `salesAmt`, `salesChange`,
                                            `salesShare`, `scrnCnt`,`showCnt`, `totalRank`)
                                VALUES
                                (%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,
                                %s,%s);
                                """,
        'select_movieCd_from_movie': sql_builder.SQL(sql_type='select',
                                                     table='movie',
                                                     columns=['movieCd'],
                                                     where='movieCd=%s'),
        'insert_into_movie': sql_builder.SQL(sql_type='insert', table='movie', columns=[
            'movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'tmdbId', 'multi', 'nation'
        ])
    }

    def __init__(self, config=None):
        if config is None:
            with open('mysql_connect_conf.json', 'r') as fp:
                config = json.load(fp)
        self.config = config

        if 'port' not in config.keys():
            config['port'] = 3306

        self.db = pymysql.connect(host=self.config['host'], port=self.config['port'], user=self.config['user'],
                                  passwd=self.config['passwd'], db=self.config['db'], charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def commit(self):
        self.db.commit()

    def connect(self):
        self.db = pymysql.connect(host=self.config['host'], port=self.config['port'], user=self.config['user'],
                                  passwd=self.config['passwd'], db=self.config['db'], charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def close(self):
        self.db.close()

    def add_to_boxoffice(self, records):
        for record in records:
            try:
                print('record : ', record)
                print('sql : ', self.sqls['insert_into_boxoffice'])
                self.cursor.execute(
                    str(self.sqls['insert_into_boxoffice']), sql_builder.SQL.sort_args(record))
            except TypeError:
                print('record : ', record)
                print('sql : ', self.sqls['insert_into_boxoffice'])
                print('error message : ', TypeError)
                exit(1)
        self.commit()

    def add_to_movie(self, records):
        for record in records:
            print('movie record : ', record)
            self.cursor.execute(
                str(self.sqls['insert_into_movie']), sql_builder.SQL.sort_args(record))
        self.commit()

    def get_unique_new_movie(self, movieCds):
        result = []
        for movieCd in movieCds:
            if self.cursor.execute(str(self.sqls['select_movieCd_from_movie']), movieCd) == 0:
                result.append(movieCd)
        return result
