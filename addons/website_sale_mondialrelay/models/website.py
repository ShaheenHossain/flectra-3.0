# -*- coding: utf-8 -*-
# Part of Flectra. See LICENSE file for full copyright and licensing details.

from flectra import models


class WebsiteMondialRelay(models.Model):
    _inherit = 'website'

    def _prepare_sale_order_values(self, partner_sudo):
        values = super()._prepare_sale_order_values(partner_sudo)

        # never use Mondial Relay shipping address as default.
        shipping_address = self.env['res.partner'].browse(values['partner_shipping_id'])
        if shipping_address.id != values['partner_invoice_id'] and shipping_address.is_mondialrelay:
            values['partner_shipping_id'] = values['partner_invoice_id']
        return values
