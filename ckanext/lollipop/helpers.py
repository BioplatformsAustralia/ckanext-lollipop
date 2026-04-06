import ckan.plugins as p
import ckanext.lollipop.interface as interface
import ckan.plugins.toolkit as tk
import ckan.lib.dictization.model_dictize as model_dictize
from ckan.common import g


def _get_user_name(user_id):
    if not user_id:
        return g.userobj.name

    site_user = tk.get_action("get_site_user")({"ignore_auth": True}, {})["name"]
    admin_ctx = {"ignore_auth": True, "user": site_user}
    user_id = {"id": user_id, "include_plugin_extras": True}
    return tk.get_action("user_show")(admin_ctx, user_id).get("name", None)


def lollipop_required():
    """Return true if CAPTCHA is required for that page"""

    for impl in p.PluginImplementations(interface.ILollipop):
        required = impl.lollipop_required()
        if required is not None:
            return required

    return True


def get_helpers():
    return {
        "lollipop_required": lollipop_required,
    }
