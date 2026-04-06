"""Tests for helpers.py."""

import pytest
import logging
import ckan.tests.factories as factories
import ckan.plugins
import ckan.plugins.toolkit as tk
import ckanext.lollipop.helpers as lollipop_helpers
import ckan.model as model
from ckan.common import g

log = logging.getLogger(__name__)


@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins", "with_request_context")
class TestLollipopHelpers(object):
    def test_lollipop_required(self, app):
        required = [
            tk.url_for("home.index"),
            tk.url_for("home.about"),
            tk.url_for("dataset.search"),
        ]

        not_required = [
            tk.url_for("lollipop.lollipop_process"),
        ]

        for path in required:
            with app.flask_app.test_request_context(path):
                assert lollipop_helpers.lollipop_required() == True

        for path in not_required:
            with app.flask_app.test_request_context(path):
                assert lollipop_helpers.lollipop_required() == False

    def test_lollipop_required_unloaded(self, app):
        ckan.plugins.unload("lollipop")

        path = tk.url_for("home.index")

        with app.flask_app.test_request_context(path):
            assert lollipop_helpers.lollipop_required() == True

    def test_get_helpers(self):
        assert "lollipop_required" in lollipop_helpers.get_helpers()
