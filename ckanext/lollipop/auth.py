# coding: utf8
import ckan.plugins.toolkit as tk
import ckan.authz as authz
import ckan.model as model
from ckan.common import g, _
from ckanext.toolbelt.decorators import Collector

from logging import getLogger

log = getLogger(__name__)

action, get_auth_functions = Collector().split()
