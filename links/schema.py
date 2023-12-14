import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    all_links = graphene.List(LinkType)
    link = graphene.Field(LinkType, id=graphene.String(required=True))

    def resolve_all_links(self, info, **kwargs):
        # print(info.context.user)
        return Link.objects.all()

    def resolve_link(self, info, id):
        return get_object_or_404(Link, id__iexact=id)


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description
        )


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
