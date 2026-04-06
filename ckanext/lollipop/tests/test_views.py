"""Tests for views.py."""

import pytest
import logging

import ckan.model as model
import ckan.logic as logic
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as tk
import ckanext.lollipop.plugin as plugin

log = logging.getLogger(__name__)


@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
def test_lollipop_processed(app, reset_db):
    resp = app.get(tk.h.url_for("lollipop.lollipop_process"))
    assert resp.status_code == 200
    # look for phrase from rejection template
    assert resp.body.find("has been rejected by the user") >= 0


@pytest.mark.usefixtures("with_request_context")
@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
class TestLollipopViewsUpdates(object):
    pass
