import graphene

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from ckan.model.package import Package as PackageModel
from ckan.model.resource import Resource as ResourceModel


class Package(SQLAlchemyObjectType):

    class Meta:
        model = PackageModel

class Resource(SQLAlchemyObjectType):

    class Meta:
        model = ResourceModel

class Query(graphene.ObjectType):
    hello = graphene.String(description='A typical hello world')

    packages =  graphene.List(Package)
    resources = graphene.List(Resource)

    def resolve_packages(self, info):
        query = Package.get_query(info)
        return query.filter(PackageModel.private == False).all()

    def resolve_resources(self, info):
        query = Resource.get_query(info)
        return query.all()

    def resolve_hello(self, info):
        return 'World'

schema = graphene.Schema(query=Query, types=[Package, Resource])
