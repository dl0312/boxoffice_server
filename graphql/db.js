import mysql from "mysql2/promise";
import { dbConfig } from "../config/db.config";

const pool = mysql.createPool({
  host: dbConfig.host,
  user: dbConfig.user,
  password: dbConfig.password,
  database: dbConfig.database,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

export const people = [
  {
    id: 1,
    name: "dave",
    age: 18,
    gender: "male"
  },
  {
    id: 2,
    name: "dave",
    age: 18,
    gender: "male"
  },
  {
    id: 3,
    name: "dave",
    age: 18,
    gender: "male"
  }
];

export const getAllMovies = async () => {
  const [rows] = await pool.query("select * from movie");
  return rows;
};
