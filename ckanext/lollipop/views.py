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


class LollipopView(MethodView):
     def _prepare(self):
        context = {"user": g.user}

     def lollipop_process():
        lollipop_status = 'bad'
        try:
            data_dict = logic.clean_dict(
                dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
            )
            data_dict.update = logic.clean_dict(
                dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.files)))
            )
        except dictization_functions.DataError:
            base.abort(400, _(u'Integrity Error'))

        context[u'message'] = data_dict.get(u'log_message', u'')
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
            form_dict.get("return_to", "home.index"), lollipop_status=lollipop_status
       )

    def get(self):
        self._prepare()
        return render("ckanext_lollipop/lollipop_captcha_failed.html", {})

lollipop.add_url_rule(
    rule="/captcha_process",
    view_func=LollipopView.as_view(str('lollipop_process')),
)


def get_blueprints():
    return [lollipop]
