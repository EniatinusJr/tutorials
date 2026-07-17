from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offered price must be a positive number',
    )

    price = fields.Float('Price')
    validity = fields.Integer('Validity (days)', default=7)
    state = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help='Status of the offer',
        copy=False,
    )

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", string="Property Type", store=True)

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

    def action_accept(self):
        for record in self:
            if 'accepted' in record:
                raise UserError('One offer has already been accepted')
            record.state = 'accepted'
            self.env['estate.property'].search([('name','=', record.property_id.name)], limit=1).selling_price = record.price
            self.env['estate.property'].search([('name','=', record.property_id.name)], limit=1).buyer_id = record.partner_id.id
            self.env['estate.property'].search([('name','=', record.property_id.name)], limit=1).state = 'offer accepted'
        return True

    def action_reject(self):
        for record in self:
            record.state = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")

            if property_id and price is not None:
                prop = self.env["estate.property"].browse(property_id)
                if prop.offer_ids:
                    max_offer = max(prop.offer_ids.mapped("price"))
                    if float_compare(price, max_offer, precision_rounding=0.01) <= 0:
                        raise UserError(
                            "The offer must be higher than %.2f" % max_offer
                        )

                prop.state = "offer received"
        return super().create(vals)