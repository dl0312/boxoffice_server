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

export const getAllMovies = async () => {
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
