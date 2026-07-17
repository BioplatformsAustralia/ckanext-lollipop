from ckan.common import config

import hashlib

from logging import getLogger

logger = getLogger(__name__)


def cookie_filling():
    cookie_name = config.get("ckanext.lollipop.cookie_name", "ckanext-lollipop-yum")
    app_instance_uuid = config.get("app_instance_uuid", None)

    if app_instance_uuid is None:
        raise ValueError

    raw_filling = (cookie_name + app_instance_uuid).encode("utf-8")

    return hashlib.sha256(raw_filling).hexdigest()
