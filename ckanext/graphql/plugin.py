import ckan.plugins as p
import ckan.plugins.toolkit as tk

from flask_graphql import GraphQLView
from ckanext.graphql.schema import schema


class GraphqlPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        tk.add_public_directory(config_, 'public')
        tk.add_resource('fanstatic', 'graphql')

    def get_blueprint(self):
        blueprint = Blueprint('graphql', self.__module__)
        blueprint.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

        return blueprint 
