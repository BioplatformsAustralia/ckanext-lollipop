import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.lollipop.logic as logic
import ckanext.lollipop.action as action
import ckanext.lollipop.views as views
import ckanext.lollipop.interface as interface
import ckanext.lollipop.helpers as helpers
import ckanext.lollipop.auth as auth

from logging import getLogger

logger = getLogger(__name__)


class LollipopPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(interface.ILollipop, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "lollipop")

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()

    # ILollipop

    def lollipop_set(self, response):
        return logic.lollipop_set(response)

    def lollipop_update(self, response):
        return logic.lollipop_update(response)

    def lollipop_clear(self, response):
        return logic.lollipop_clear(response)

    def lollipop_required(self):
        return logic.lollipop_required()

    def lollipop_process(self, context, data_dict):
        return logic.lollipop_process(context, data_dict)

    # IActions

    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions

    def get_auth_functions(self):
        return auth.get_auth_functions()

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()
