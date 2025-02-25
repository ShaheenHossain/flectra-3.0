from flectra import models, fields, _
from flectra.tools import format_date


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_din5008_template_data = fields.Binary(compute='_compute_l10n_din5008_template_data')
    l10n_din5008_document_title = fields.Char(compute='_compute_l10n_din5008_document_title')
    l10n_din5008_addresses = fields.Binary(compute='_compute_l10n_din5008_addresses', exportable=False)

    def _compute_l10n_din5008_template_data(self):
        for record in self:
            record.l10n_din5008_template_data = data = []
            if record.name:
                data.append((_("Invoice No."), record.name))
            if record.invoice_date:
                data.append((_("Invoice Date"), format_date(self.env, record.invoice_date)))
            if record.invoice_date_due:
                data.append((_("Due Date"), format_date(self.env, record.invoice_date_due)))
            if record.delivery_date:
                data.append((_("Delivery Date"), format_date(self.env, record.delivery_date)))
            if record.invoice_origin:
                data.append((_("Source"), record.invoice_origin))
            if record.ref:
                data.append((_("Reference"), record.ref))

    def _compute_l10n_din5008_document_title(self):
        for record in self:
            record.l10n_din5008_document_title = ''
            if record.move_type == 'out_invoice':
                if record.state == 'posted':
                    record.l10n_din5008_document_title = _('Invoice')
                elif record.state == 'draft':
                    record.l10n_din5008_document_title = _('Draft Invoice')
                elif record.state == 'cancel':
                    record.l10n_din5008_document_title = _('Cancelled Invoice')
            elif record.move_type == 'out_refund':
                record.l10n_din5008_document_title = _('Credit Note')
            elif record.move_type == 'in_refund':
                record.l10n_din5008_document_title = _('Vendor Credit Note')
            elif record.move_type == 'in_invoice':
                record.l10n_din5008_document_title = _('Vendor Bill')

    def _compute_l10n_din5008_addresses(self):
        for record in self:
            record.l10n_din5008_addresses = data = []
            commercial_partner = record.partner_id.commercial_partner_id
            delivery_partner = record.partner_shipping_id
            invoice_partner = record.partner_id

            different_partner_count = len({partner.id for partner in [commercial_partner, delivery_partner, invoice_partner] if partner})
            # To avoid repetition in the address block.
            if different_partner_count <= 1:
                continue
            elif different_partner_count == 3:
                data.extend([(_("Shipping Address:"), delivery_partner), (_("Invoicing Address:"), invoice_partner)])
                continue
            elif commercial_partner == invoice_partner:
                data.append((_("Shipping Address:"), delivery_partner))
                continue
            elif commercial_partner == delivery_partner:
                data.append((_("Invoicing Address:"), invoice_partner))
                continue
            elif invoice_partner == delivery_partner:
                data.append((_("Invoicing and Shipping Address:"), invoice_partner))
                continue

    def check_field_access_rights(self, operation, field_names):
        field_names = super().check_field_access_rights(operation, field_names)
        return [field_name for field_name in field_names if field_name not in {
            'l10n_din5008_addresses',
        }]
