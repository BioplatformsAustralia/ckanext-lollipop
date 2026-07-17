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

    response = app.post(
        tk.h.url_for("lollipop.lollipop_process"),
        data=data,
        follow_redirects=False,
    )
    assert response.status_code == 302

    # Cookie to be cleared
    assert [
        cookie
        for cookie in [
            header[1] for header in response.headers if header[0] == "Set-Cookie"
        ]
        if "custard_creams=0b49850b093cfe6da565e20b3084e9371d27d5e26f4f08334541127fb8765f35"
        in cookie
        and (
            "Expires=Thu, 01-Jan-1970 00:00:07 GMT" in cookie
            or "Expires=Thu, 01 Jan 1970 00:00:07 GMT" in cookie
        )
    ]


@pytest.mark.ckan_config("ckan.plugins", "lollipop")
@pytest.mark.ckan_config("app_instance_uuid", "b9fd6df7-46c0-402f-8739-65925dbc36ae")
@pytest.mark.ckan_config("ckanext.lollipop.cookie_name", "custard_creams")
@pytest.mark.ckan_config(
    "ckan.recaptcha.privatekey", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
)
@pytest.mark.usefixtures("with_plugins")
def test_lollipop_process_good_captcha(app, reset_db):
    data = {
        "return_to": tk.h.url_for("dataset.search"),
        "g-recaptcha-response": "thisWillAlwaysWork",
    }

    response = app.post(
        tk.h.url_for("lollipop.lollipop_process"),
        data=data,
        follow_redirects=False,
    )
    assert response.status_code == 302

    assert not (
        [
            cookie
            for cookie in [
                header[1] for header in response.headers if header[0] == "Set-Cookie"
            ]
            if "custard_creams=0b49850b093cfe6da565e20b3084e9371d27d5e26f4f08334541127fb8765f35"
            in cookie
            and (
                "Expires=Thu, 01-Jan-1970 00:00:07 GMT" in cookie
                or "Expires=Thu, 01 Jan 1970 00:00:07 GMT" in cookie
            )
        ]
    )


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
