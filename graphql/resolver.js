import { getAllMovies, people } from "./db";

const resolvers = {
  Query: {
    people: () => people,
    getAllMovies: () => getAllMovies()
  }
};

export default resolvers;
