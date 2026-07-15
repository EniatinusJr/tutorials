from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float('Price')
    validity = fields.Integer('Validity (days)', default=7)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help='Status of the offer',
        copy=False,
    )

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_deadline',
        inverse='_inverse_validity')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            days = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - days).days