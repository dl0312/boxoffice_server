import mysql from "mysql2/promise";
import { dbConfig } from "../config/db.config";

const connection = mysql.createPool({
  host: dbConfig.host,
  user: dbConfig.user,
  password: dbConfig.password,
  database: dbConfig.database,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

export const getMovies = async () => {
  const [rows] = await connection.query("select * from movie");
  return rows;
};

export const getMoviesByCurrentDate = async () => {
  const [rows] = await connection.query("select * from movie");
  return rows;
};

export const getBoxoffices = async () => {
  const [rows] = await connection.query("select * from boxoffice");
  return rows;
};

export const getBoxofficesByCurrentDate = async currentDate => {
  const [rows] = await connection.query(
    "SELECT * FROM `boxoffice` WHERE `currentDate` = ?",
    [currentDate],
    (err, results) => {
      console.log(err, results);
    }
  );
  console.log(rows.length);
  return rows;
};

export const getBoxofficesByFromDateAndToDate = async (fromDate, toDate) => {
  const [rows] = await connection.query(
    "SELECT * FROM `boxoffice` WHERE DATE(currentDate) BETWEEN ? AND ?",
    [fromDate, toDate],
    (err, results) => {
      console.log(err, results);
    }
  );
  console.log(rows.length);
  return rows;
};

export const getBoxofficesByMovieCd = async movieCd => {
  const [rows] = await connection.query(
    "SELECT * FROM `boxoffice` WHERE movieCd = ?",
    [movieCd],
    (err, results) => {
      console.log(err, results);
    }
  );
  console.log(rows.length);
  return rows;
};

export const getExtendedBoxofficesByFromDateAndToDate = async (
  fromDate,
  toDate
) => {
  const [rows] = await connection.query(
    "SELECT * FROM `boxoffice` INNER JOIN movie ON boxoffice.movieCd=movie.movieCd WHERE DATE(currentDate) BETWEEN ? AND ?",
    [fromDate, toDate],
    (err, results) => {
      console.log(err, results);
    }
  );
  const movies = [];
  const obj = [
    "currentDate",
    "showCnt",
    "scrnCnt",
    "rankOldAndNew",
    "audiAcc",
    "audiCnt",
    "salesShare",
    "salesAmt",
    "salesAcc",
    "rank",
    "totalRank",
    "audiChange",
    "salesChange",
    "rankInten"
  ];
  rows.forEach(row => {
    const movieIdx = movies.findIndex(movie => movie.movieCd === row.movieCd);
    if (movieIdx !== -1) {
      obj.forEach(key => movies[movieIdx][key].push(row[key]));
    } else {
      const movie = {
        movieCd: row.movieCd,
        movieNm: row.movieNm,
        movieNmEn: row.movieNmEn,
        movieNmOg: row.movieNmOg,
        tmdbId: row.tmdbId,
        multi: row.multi,
        nation: row.nation,
        currentDate: [],
        showCnt: [],
        scrnCnt: [],
        rankOldAndNew: [],
        audiAcc: [],
        audiCnt: [],
        salesShare: [],
        salesAmt: [],
        salesAcc: [],
        rank: [],
        totalRank: [],
        audiChange: [],
        salesChange: [],
        rankInten: []
      };
      obj.forEach(key => movie[key].push(row[key]));
      movies.push(movie);
    }
  });
  console.log(movies);
  return movies;
};
