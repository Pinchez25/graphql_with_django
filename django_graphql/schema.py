import graphene
import graphql_jwt

import links.schema
from accounts import schema


class Query(schema.Query, links.schema.Query, graphene.ObjectType):
    pass


class Mutation(schema.Mutation, links.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()  # for login
    verify_token = graphql_jwt.Verify.Field()  # for token refresh
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
