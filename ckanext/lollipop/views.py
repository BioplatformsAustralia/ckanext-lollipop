from flask import Blueprint
from flask.views import MethodView
from ckan.common import _, g
from ckan.lib.base import render, abort, request
from ckan.logic import get_action, ValidationError, NotFound, NotAuthorized
import ckan.logic as logic
import ckan.lib.captcha as captcha
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as dict_fns

from logging import getLogger

logger = getLogger(__name__)

lollipop = Blueprint("lollipop", __name__)

def lollipop_process():
    lollipop_status = 'bad'
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
    except captcha.CaptchaError:
        error_msg = _(u'Bad Captcha. Please try again.')
        h.flash_error(error_msg)
        # FIXME Need to clear the cookie
        return self.get(data_dict)

    # FIXME Need to set the cookie
    lollipop_status = 'good'

    return h.redirect_to(
        data_dict.get("return_to", "home.index"), lollipop_status=lollipop_status
   )

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
