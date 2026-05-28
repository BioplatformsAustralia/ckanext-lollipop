from flask import Blueprint
from flask.views import MethodView
from ckan.common import _, g, config
from ckan.lib.base import render, abort, request
from ckan.logic import get_action, ValidationError, NotFound, NotAuthorized
import ckan.logic as logic
import ckan.lib.captcha as captcha
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as dict_fns

from logging import getLogger
from datetime import datetime, timedelta

logger = getLogger(__name__)

lollipop = Blueprint("lollipop", __name__)

def lollipop_process():
    cookie_name = config.get('ckanext.lollipop.cookie_name', 'ckanext-lollipop-yum')
    cookie_expiry = int(config.get('ckanext.lollipop.cookie_expiry', 7))
    cookie_value = "proceed with care"

    lollipop_status = 'bad'
    expiry = 0

    try:
        data_dict = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
        )

        files_dict = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.files)))
        )

        data_dict.update(files_dict)
    except dict_fns.DataError:
        base.abort(400, _(u'Integrity Error'))

    try:
        captcha.check_recaptcha(request)
        lollipop_status = 'good'
        expiry = datetime.now() + timedelta(days=cookie_expiry)
    except captcha.CaptchaError:
        error_msg = _(u'Bad Captcha. Please try again.')
        h.flash_error(error_msg)
        lollipop_status = 'bad'
        expiry = 0

    response =  h.redirect_to(
        data_dict.get("return_to", "home.index"), lollipop_status=lollipop_status
    )

    response.set_cookie(cookie_name, expires=expiry, value=cookie_value)

    return response

def lollipop_captcha_failed(self):
    return render("ckanext_lollipop/lollipop_captcha_failed.html", {})

lollipop.add_url_rule(
    rule="/captcha_process",
    view_func=lollipop_process,
    methods=["POST"],
)

lollipop.add_url_rule(
    rule="/captcha_failed",
    view_func=lollipop_captcha_failed,
)


def get_blueprints():
    return [lollipop]
