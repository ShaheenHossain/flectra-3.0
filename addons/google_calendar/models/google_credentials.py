# -*- coding: utf-8 -*-
# Part of Flectra. See LICENSE file for full copyright and licensing details.

import logging
import requests
from datetime import timedelta

from flectra import fields, models, _
from flectra.exceptions import UserError
from flectra.addons.google_account.models.google_service import GOOGLE_TOKEN_ENDPOINT

_logger = logging.getLogger(__name__)

class GoogleCredentials(models.Model):
    """"Google Account of res_users"""

    _name = 'google.calendar.credentials'
    _description = 'Google Calendar Account Data'

    user_ids = fields.One2many('res.users', 'google_calendar_account_id', required=True)
    calendar_rtoken = fields.Char('Refresh Token', copy=False)
    calendar_token = fields.Char('User token', copy=False)
    calendar_token_validity = fields.Datetime('Token Validity', copy=False)
    calendar_sync_token = fields.Char('Next Sync Token', copy=False)

    calendar_cal_id = fields.Char('Calendar ID', copy=False, help='Last Calendar ID who has been synchronized. If it is changed, we remove all links between GoogleID and Flectra Google Internal ID')
    synchronization_stopped = fields.Boolean('Google Synchronization stopped', copy=False)

    def _set_auth_tokens(self, access_token, refresh_token, ttl):
        self.write({
            'calendar_rtoken': refresh_token,
            'calendar_token': access_token,
            'calendar_token_validity': fields.Datetime.now() + timedelta(seconds=ttl) if ttl else False,
        })

    def _google_calendar_authenticated(self):
        self.ensure_one()
        return bool(self.sudo().calendar_rtoken)

    def _is_google_calendar_valid(self):
        self.ensure_one()
        return self.calendar_token_validity and self.calendar_token_validity >= (fields.Datetime.now() + timedelta(minutes=1))

    def _refresh_google_calendar_token(self):
        # LUL TODO similar code exists in google_drive. Should be factorized in google_account
        self.ensure_one()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        client_id = get_param('google_calendar_client_id')
        client_secret = get_param('google_calendar_client_secret')

        if not client_id or not client_secret:
            raise UserError(_("The account for the Google Calendar service is not configured."))

        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            'refresh_token': self.calendar_rtoken,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
        }

        try:
            _dummy, response, _dummy = self.env['google.service']._do_request(GOOGLE_TOKEN_ENDPOINT, params=data, headers=headers, method='POST', preuri='')
            ttl = response.get('expires_in')
            self.write({
                'calendar_token': response.get('access_token'),
                'calendar_token_validity': fields.Datetime.now() + timedelta(seconds=ttl),
            })
        except requests.HTTPError as error:
            if error.response.status_code in (400, 401):  # invalid grant or invalid client
                # Delete refresh token and make sure it's commited
                self.env.cr.rollback()
                self._set_auth_tokens(False, False, 0)
                self.env.cr.commit()
            error_key = error.response.json().get("error", "nc")
            error_msg = _("An error occurred while generating the token. Your authorization code may be invalid or has already expired [%s]. "
                          "You should check your Client ID and secret on the Google APIs plateform or try to stop and restart your calendar synchronisation.",
                          error_key)
            raise UserError(error_msg)
