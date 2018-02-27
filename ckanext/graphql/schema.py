from sqlalchemy.ext.declarative import declarative_base

import graphene
from graphene import relay
from graphql_relay import from_global_id

from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from ckan.model.package import Package as CKANPackage
from ckan.model.package_extra import PackageExtra as CKANPackageExtra
from ckan.model.resource import Resource as CKANResource
from ckan.model.group import Group as CKANGroup
from ckan.model.group_extra import GroupExtra as CKANGroupExtra
from ckan.model.group import Member as CKANMember
from ckan.model.tag import Tag as CKANTag
from ckan.model.vocabulary import Vocabulary as CKANVocabulary

# graphene-sqlalchemy expects models that are based on declarative_base
Base = declarative_base()

class PackageModel(CKANPackage, Base):
    pass


class PackageExtraModel(CKANPackageExtra, Base):
    pass


class ResourceModel(CKANResource, Base):
    pass


class GroupModel(CKANGroup, Base):
    pass


class GroupExtraModel(CKANGroupExtra, Base):
    pass


class MemberModel(CKANMember, Base):
    pass


class TagModel(CKANTag, Base):
    pass


class VocabularyModel(CKANVocabulary, Base):
    pass


# GraphQL types


class PackageExtra(SQLAlchemyObjectType):

    class Meta:
        model = PackageExtraModel
        interfaces = (relay.Node, )


class Resource(SQLAlchemyObjectType):

    class Meta:
        model = ResourceModel
        interfaces = (relay.Node, )


class Group(SQLAlchemyObjectType):

    class Meta:
        model = GroupModel
        interfaces = (relay.Node, )


class GroupConnection(relay.Connection):

    class Meta:
        node = Group


class Package(SQLAlchemyObjectType):

    class Meta:
        model = PackageModel
        interfaces = (relay.Node, )
        exclude_fields = ['owner_org', 'private']

    ckan_id = graphene.String()
    groups = relay.ConnectionField(GroupConnection, description='The groups of this package')
    organization = graphene.Field(Group)

    def resolve_ckan_id(self, info):
        return self.id

    def resolve_groups(self, info):
        query = Group.get_query(info)
        query = query.join(MemberModel,
                           MemberModel.group_id == GroupModel.id and \
                           MemberModel.table_name == 'package' ).\
                join(PackageModel, PackageModel.id == MemberModel.table_id).\
                filter(MemberModel.state == 'active').\
                filter(GroupModel.type == 'group')
        query = query.filter(MemberModel.table_id == self.id)
        return query.all()

    def resolve_organization(self, info):
        query = Group.get_query(info)
        query = query.filter(GroupModel.id == self.owner_org)
        return query.first()


class GroupExtra(SQLAlchemyObjectType):

    class Meta:
        model = GroupExtraModel
        interfaces = (relay.Node, )


class Tag(SQLAlchemyObjectType):

    class Meta:
        model = TagModel
        interfaces = (relay.Node, )


class Vocabulary(SQLAlchemyObjectType):

    class Meta:
        model = VocabularyModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    hello = graphene.String(description='A typical hello world')

    node = relay.Node.Field()

    packages = graphene.List(Package)
    all_packages = SQLAlchemyConnectionField(Package)
    extras = graphene.List(PackageExtra)
    resources = graphene.List(Resource)
    organizations = graphene.List(Group)
    groups = graphene.List(Group)
    group_extras = graphene.List(GroupExtra)
    tags = graphene.List(Tag)
    vocabularies = graphene.List(Vocabulary)

    def resolve_packages(self, info):
        query = Package.get_query(info)
        query = query.join(PackageExtraModel)
        return query.filter(PackageModel.private == False).all()  # noqa 

    def resolve_resources(self, info):
        query = Resource.get_query(info)
        return query.all()

    def resolve_extras(self, info):
        query = PackageExtra.get_query(info)
        return query.all()

    def resolve_organizations(self, info):
        query = Group.get_query(info)
        return query.filter(GroupModel.is_organization == True).all()

    def resolve_groups(self, info):
        query = Group.get_query(info)
        return query.filter(GroupModel.is_organization == False).all()

    def resolve_group_extras(self, info):
        query = GroupExtra.get_query(info)
        return query.all()

    def resolve_member(self, info):
        query = Member.get_query(info)
        return query.all()

    def resolve_tagss(self, info):
        query = Tag.get_query(info)
        return query.all()

    def resolve_vocabularies(self, info):
        query = Vocabulary.get_query(info)
        return query.all()

    def resolve_hello(self, info):
        return 'World'


schema = graphene.Schema(query=Query, types=[Package, Resource, PackageExtra, Group, Tag, Vocabulary])
