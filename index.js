import { GraphQLServer } from "graphql-yoga";
import {
  typeDefs as scalarsTypeDefs,
  resolvers as scalarsResolvers
} from "graphql-scalars";
import resolvers from "./graphql/resolver";

const server = new GraphQLServer({
  resolvers: [...scalarsResolvers, resolvers],
  typeDefs: ["graphql/schema.graphql"]
});

server.start(({ port }) =>
  console.log(`🚀 Graphql Server is Running at http://localhost:${port}`)
);
