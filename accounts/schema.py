from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

import graphene
from graphene_django import DjangoObjectType

import graphql_jwt
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, token=token, refresh_token=refresh_token)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    me = graphene.Field(UserType)

    @login_required
    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_user_by_username(self, info, username):
        return get_object_or_404(get_user_model(), username__iexact=username)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
