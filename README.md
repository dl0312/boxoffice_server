# BOXOFFICE SERVER

GraphQL Server for Boxoffice

## CONFIG
you should add config or key files

* ./crawling/api_keys.json
```json
{
  "kobis": [${KOBIS_API_KEY}, ...],
  "tmdb": [${TMDB_API_KEY}, ...],
  "naver": [
    { 
        "clientId": ${NAVER_CLIENT_ID}"clientSecret": ${NAVER_CLIENT_SECRET} 
    }
  ]
}
```
* ./crawling/mysql_connect_conf.json
```json
{
  "host": ${DB_SERVER_IP},
  "port": ${DB_SERVER_PORT},
  "user": ${DB_USERNAME},
  "passwd": ${DB_PASSWORD},
  "db": ${DB_NAME}
}
```

## DB QUERY

```sql
CREATE DATABASE ${DB_NAME}
```

### DB SCHEMAS
* movie
```sql
CREATE TABLE `movie` (
  `movieCd` varchar(100) NOT NULL,
  `movieNm` varchar(1024) DEFAULT NULL,
  `movieNmEn` varchar(1024) DEFAULT NULL,
  `movieNmOg` varchar(1024) DEFAULT NULL,
  `tmdbId` varchar(255) DEFAULT NULL,
  `multi` enum('Y','N') DEFAULT NULL,
  `nation` enum('K','F') DEFAULT NULL,
  PRIMARY KEY (`movieCd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```
* boxoffice
```sql
CREATE TABLE `boxoffice` (
  `showCnt` bigint DEFAULT NULL,
  `scrnCnt` bigint DEFAULT NULL,
  `rankOldAndNew` tinyint DEFAULT NULL,
  `movieCd` varchar(100) DEFAULT NULL,
  `audiAcc` bigint DEFAULT NULL,
  `audiCnt` bigint DEFAULT NULL,
  `salesShare` double DEFAULT NULL,
  `rank` int DEFAULT NULL,
  `salesAmt` bigint DEFAULT NULL,
  `salesAcc` bigint DEFAULT NULL,
  `currentDate` date DEFAULT NULL,
  `totalRank` int DEFAULT NULL,
  `audiChange` double DEFAULT NULL,
  `salesChange` double DEFAULT NULL,
  `rankInten` int DEFAULT NULL,
  `multi` enum('Y','N') DEFAULT NULL,
  `nation` enum('K','F') DEFAULT NULL,
  KEY `movieCd` (`movieCd`),
  CONSTRAINT `boxoffice_ibfk_1` FOREIGN KEY (`movieCd`) REFERENCES `movie` (`movieCd`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```
