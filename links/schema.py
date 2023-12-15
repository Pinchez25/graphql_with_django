import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from .models import Link
from graphql_jwt.decorators import login_required
from accounts.schema import UserType
from votes.models import Vote


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    all_links = graphene.List(LinkType)
    link = graphene.Field(LinkType, id=graphene.String(required=True))

    all_votes = graphene.List(VoteType)
    vote = graphene.Field(VoteType, id=graphene.String(required=True))
    my_votes = graphene.List(VoteType)

    @login_required
    def resolve_all_links(self, info, **kwargs):
        # print(info.context.user)
        return Link.objects.all()

    @login_required
    def resolve_link(self, info, id):
        return get_object_or_404(Link, id__iexact=id)

    @login_required
    def resolve_all_votes(self, info, **kwargs):
        return Vote.objects.all()

    @login_required
    def resolve_vote(self, info, id):
        return get_object_or_404(Vote, id__iexact=id)

    @login_required
    def resolve_my_votes(self, info, **kwargs):
        user = info.context.user
        return Vote.objects.filter(user=user)


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    @login_required
    def mutate(self, info, url, description):
        user = info.context.user or None
        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    @login_required
    def mutate(self, info, link_id):
        user = info.context.user

        link = get_object_or_404(Link, id__exact=link_id)
        if not link:
            raise Exception('Invalid Link')

        Vote.objects.create(
            user=user,
            link=link
        )
        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
