from __future__ import annotations

import ckan.plugins.toolkit as tk
import ckan.plugins as p
import ckanext.lollipop.interface as interface
from ckan import model
from ckan.logic import validate
from ckanext.toolbelt.decorators import Collector
from . import schema

action, get_actions = Collector().split()
