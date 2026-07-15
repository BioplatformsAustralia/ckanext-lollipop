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

import ckan.model as model
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.plugins.toolkit as tk

import ckanext.lollipop.logic as logic

from ckanext.lollipop.util import cookie_filling
from werkzeug.http import dump_cookie

@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
class TestLollipopLogic(object):
    @pytest.mark.ckan_config("ckan.recaptcha.privatekey", "secretSweet")
    def test_lollipop_process_bad_captcha(self,app):
        with app.flask_app.test_request_context(
            tk.url_for("lollipop.lollipop_process"),
            method="GET",
            data={"g-recaptcha-response": "notAValidResponse"},
            ):
                assert logic.lollipop_process({},{}) == "bad"

    # Google test key for reCaptcha
    @pytest.mark.ckan_config("ckan.recaptcha.privatekey", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")
    def test_lollipop_process_good_captcha(self,app):
        with app.flask_app.test_request_context(
            tk.url_for("lollipop.lollipop_process"),
            method="GET",
            data={"g-recaptcha-response": "willAlwaysPassWithTestKey"},
            ):
                assert logic.lollipop_process({},{}) == "good"

    @pytest.mark.ckan_config("app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae")
    def test__cookie_valid(self,app):
        cookie_name = 'ckanext-lollipop-yum'
        cookie_header = dump_cookie(cookie_name,cookie_filling())

        with app.flask_app.test_request_context(
            tk.url_for("dataset.search"),
            method="GET",
            environ_base={'HTTP_COOKIE': cookie_header}
            ):
                assert logic._cookie_valid()

    def test_lollipop_required(self,app):
        urls = [
            (tk.url_for("lollipop.lollipop_captcha_failed"),False),
            (tk.url_for("lollipop.lollipop_process"),False),
            (tk.url_for("dataset.search"),True),
        ]

        for url,required in urls:
            with app.flask_app.test_request_context(
                url,
                method="GET",
            ):
                assert logic.lollipop_required() == required

    @pytest.mark.ckan_config("app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae")
    def test_lollipop_required_with_valid_cookie(self,app):
        cookie_name = 'ckanext-lollipop-yum'
        cookie_header = dump_cookie(cookie_name,cookie_filling())

        urls = [
            (tk.url_for("lollipop.lollipop_captcha_failed"),False),
            (tk.url_for("lollipop.lollipop_process"),False),
            (tk.url_for("dataset.search"),False),
        ]

        for url,required in urls:
            with app.flask_app.test_request_context(
                url,
                method="GET",
                environ_base={'HTTP_COOKIE': cookie_header}
            ):
                assert logic.lollipop_required() == required
