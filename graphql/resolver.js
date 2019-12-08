import {
  getMovies,
  getBoxoffices,
  getBoxofficesByCurrentDate,
  getBoxofficesByFromDateAndToDate,
  getBoxofficesByMovieCd,
  getExtendedBoxofficesByFromDateAndToDate
} from "./db";

const resolvers = {
  Query: {
    getMovies: (obj, args, ctx, info) => getMovies(),
    getBoxoffices: (obj, args, ctx, info) => getBoxoffices(),
    getBoxofficesByCurrentDate: (obj, args, ctx, info) => {
      const { currentDate } = args;
      return getBoxofficesByCurrentDate(currentDate);
    },
    getBoxofficesByFromDateAndToDate: (obj, args, ctx, info) => {
      const { fromDate, toDate } = args;
      return getBoxofficesByFromDateAndToDate(fromDate, toDate);
    },
    getBoxofficesByMovieCd: (obj, args, ctx, info) => {
      const { movieCd } = args;
      return getBoxofficesByMovieCd(movieCd);
    },
    getExtendedBoxofficesByFromDateAndToDate: (obj, args, ctx, info) => {
      const { fromDate, toDate } = args;
      return getExtendedBoxofficesByFromDateAndToDate(fromDate, toDate);
    }
  }
};

export default resolvers;
