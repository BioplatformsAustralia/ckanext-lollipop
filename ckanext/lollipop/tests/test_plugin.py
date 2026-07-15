"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest
import logging

import ckan.model as model
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as tk
import ckanext.lollipop.plugin as plugin

from ckan.plugins import plugin_loaded
from ckan.plugins import get_plugin

log = logging.getLogger(__name__)

@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert plugin_loaded("lollipop")

@pytest.mark.ckan_config("app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae")
@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
class TestLollipopPlugin(object):
    @pytest.mark.usefixtures("clean_db")
    def test_lollipop_set(self,app):
        url = tk.url_for('dataset.search')

        response = app.get(url)

        assert response.status_code == 200

        p = get_plugin("lollipop")

        assert p.lollipop_set(response)

        assert u'ckanext-lollipop-yum=a772cc4392939dda9ef66ec4c90a303f8ba42badf29279b4891077a0d6881e2b' in response.headers[u'Set-Cookie']

    def test_lollipop_update(self,app):
        url = tk.url_for('dataset.search')

        response = app.get(url)

        assert response.status_code == 200

        p = get_plugin("lollipop")

        assert p.lollipop_update(response)

        assert u'ckanext-lollipop-yum=a772cc4392939dda9ef66ec4c90a303f8ba42badf29279b4891077a0d6881e2b' in response.headers[u'Set-Cookie']

    def test_lollipop_clear(self,app):
        url = tk.url_for('dataset.search')

        response = app.get(url)

        assert response.status_code == 200

        p = get_plugin("lollipop")

        assert p.lollipop_clear(response)

        log.warn(response.headers[u'Set-Cookie'])
        assert u'ckanext-lollipop-yum=a772cc4392939dda9ef66ec4c90a303f8ba42badf29279b4891077a0d6881e2b' in response.headers[u'Set-Cookie']
        assert u'Expires=Thu, 01-Jan-1970 00:00:07 GMT' in response.headers[u'Set-Cookie']

    def test_lollipop_required(self):
        pass
        #return logic.lollipop_required()

    def test_lollipop_process(self):
        pass
        #return logic.lollipop_process(context, data_dict)
