from odoo import api, fields, models

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'
    _uniq_name = models.Constraint(
        'unique (name)',
        'Type name already exists',
    )

    name = fields.Char('Property type', required=True)
    sequence = fields.Integer('Sequence', default=10)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')

    offer_count = fields.Integer(string='Offers', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)