import { getBoxoffices, getBoxofficesByCurrentDate } from "./db";

const resolvers = {
  Query: {
    getAllMovies: (obj, args, context, info) => getAllMovies(),
    getBoxoffices: (obj, args, context, info) => getBoxoffices(),
    getBoxofficesByCurrentDate: (obj, args, context, info) => {
      const { currentDate } = args;
      return getBoxofficesByCurrentDate(currentDate);
    }
  }
};

export default resolvers;
