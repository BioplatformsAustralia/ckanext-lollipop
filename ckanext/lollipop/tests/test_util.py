"""Tests for util.py."""

import pytest
import logging
import ckan.tests.factories as factories
import ckan.plugins
import ckan.plugins.toolkit as tk
import ckanext.lollipop.util as lollipop_util
import ckan.model as model
from ckan.common import g

log = logging.getLogger(__name__)


@pytest.mark.ckan_config("ckanext.lollipop.cookie_name", "custard_creams")
@pytest.mark.ckan_config("ckan.plugins", "lollipop")
class TestLollipopUtil(object):
    @pytest.mark.ckan_config(
        "app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae"
    )
    def test_cookie_filling(self):
        filling = lollipop_util.cookie_filling()
        prepared_beforehand = (
            "0b49850b093cfe6da565e20b3084e9371d27d5e26f4f08334541127fb8765f35"
        )

        assert filling == prepared_beforehand

    def test_cookie_filling_no_app_instance_uuid(self):
        with pytest.raises(ValueError):
            filling = lollipop_util.cookie_filling()
