from odoo import fields, models

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _uniq_name = models.Constraint(
        'unique (name)',
        'Type name already exists',
    )

    name = fields.Char('Property type', required=True)