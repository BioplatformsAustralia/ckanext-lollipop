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
@pytest.mark.ckan_config("app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae")
@pytest.mark.ckan_config("ckanext.lollipop.cookie_name", "custard_creams")
@pytest.mark.ckan_config("ckan.recaptcha.privatekey", "secretSweet")
@pytest.mark.usefixtures("with_plugins")
def test_lollipop_process_bad_captcha(app, reset_db):
    data = {
        "return_to": tk.h.url_for("dataset.search"),
        "g-recaptcha-response": "notAValidResponse",
    }

    resp = app.post(
        tk.h.url_for("lollipop.lollipop_process"),
        data=data,
    )
    assert resp.status_code == 200

    assert resp.body.find("CAPTCHA Required") >= 0

@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.ckan_config("app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae")
@pytest.mark.ckan_config("ckanext.lollipop.cookie_name", "custard_creams")
@pytest.mark.ckan_config("ckan.recaptcha.privatekey", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")
@pytest.mark.usefixtures("with_plugins")
def test_lollipop_process_good_captcha(app, reset_db):
    data = {
        "return_to": tk.h.url_for("dataset.search"),
        "g-recaptcha-response": "thisWillAlwaysWork",
    }

    resp = app.post(
        tk.h.url_for("lollipop.lollipop_process"),
        data=data,
    )
    assert resp.status_code == 200

    assert not resp.body.find("CAPTCHA Required") >= 0

@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
def test_lollipop_captcha_failed(app, reset_db):
    resp = app.get(tk.h.url_for("lollipop.lollipop_captcha_failed"))
    assert resp.status_code == 200
    log.warn(resp.body)
    # look for phrase from rejection template
    assert resp.body.find("CAPTCHA Failed") >= 0


@pytest.mark.usefixtures("with_request_context")
@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.usefixtures("with_plugins")
class TestLollipopViewsUpdates(object):
    pass
