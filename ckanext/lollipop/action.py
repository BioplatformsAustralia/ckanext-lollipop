from __future__ import annotations

import ckan.plugins.toolkit as tk
import ckan.plugins as p
import ckanext.lollipop.interface as interface
from ckan import model
from ckan.logic import validate
from ckanext.toolbelt.decorators import Collector
from . import schema

action, get_actions = Collector().split()


def _get_user_name(context, data_dict):
    if data_dict.get("user_id"):
        return data_dict["user_id"]

    user = context.get("user", None)
    return model.User.get(user).name



@action
@validate(schema.lollipop_process)
def lollipop_process(context, data_dict):
    tk.check_access("lollipop_process", context, data_dict)

    # FIXME ensure not logged in here

    valid = False
    for impl in p.PluginImplementations(interface.ILollipop):
        update = impl.lollipop_process(context, data_dict)
        if valid:
            return valid

    return valid


@action
@validate(schema.lollipop_process)
def lollipop_process(context, data_dict):
    tk.check_access("lollipop_process", context, data_dict)

    processed = False
    for impl in p.PluginImplementations(interface.IAcceptableUse):
        processed = impl.lollipop_process(context, data_dict)
        if processed:
            return processed

    return processed
