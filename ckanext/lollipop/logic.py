import ckan.plugins.toolkit as tk
from ckan.common import _, g, config
from ckan import logic
from ckan.lib.base import request
from ckan.logic import NotFound
from ckanext.lollipop.util import cookie_filling

import ckan.lib.helpers as h
import ckan.lib.captcha as captcha

from logging import getLogger

logger = getLogger(__name__)

CONFIG_LOLLIPOP_COOKIE = "ckanext.lollipop.cookie_name"

def _cookie_valid():
    cookie_name = config.get('ckanext.lollipop.cookie_name', 'ckanext-lollipop-yum')

    if cookie_name in request.cookies:
        if request.cookies.get(cookie_name) == cookie_filling():
            return True

    return False


def lollipop_set(response, expiry=None):
    cookie_name = config.get('ckanext.lollipop.cookie_name', 'ckanext-lollipop-yum')
    cookie_value = cookie_filling()

    if expiry is not None:
        cookie_expiry = int(config.get('ckanext.lollipop.cookie_expiry', 7))
    else:
        cookie_expiry = expiry

    response.set_cookie(cookie_name, expires=cookie_expiry, value=cookie_value)

    return True

def lollipop_update(response):
    return lollipop_set(response)

def lollipop_clear(response):
    return lollipop_set(response, expiry=0)

def lollipop_process(context, data_dict):
    """Process the submitted CAPTCHA form

    :rtype: string
    """

    lollipop_status = None

    try:
        captcha.check_recaptcha(request)
        lollipop_status = 'good'
    except captcha.CaptchaError:
        lollipop_status = 'bad'

    return lollipop_status


def lollipop_required():
    """Return true if the page requires a CAPTCHA to be completed to access

    :rtype: bool
    """

    # exclude rejected CAPTCHA instructions
    if request.path.startswith(tk.url_for("lollipop.lollipop_captcha_failed")):
        return False

    # exclude processing CAPTCHA
    if request.path.startswith(tk.url_for("lollipop.lollipop_process")):
        return False

    # exclude if have a valid cookie from ckanext-lollipop
    if _cookie_valid():
        return False

    return True
