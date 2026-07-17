from odoo import fields, models

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'
    _uniq_name = models.Constraint(
        'unique (name)',
        'Tag name already exists',
    )

    name = fields.Char('Property tag', required=True)
    color= fields.Integer('Color index')