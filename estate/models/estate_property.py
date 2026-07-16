from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char('Property Titel', required=True)
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From', copy=False, default=lambda self: self._default_date_availability())
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')],
        help="Orientation of the Garden area.")
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        help="Status of the Property.",
        required=True,
        copy=False,
        default="new"
    )

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    employee_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', readonly=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(
        'Total Area (sqm)',
        compute='_compute_total_area')
    best_price = fields.Float(
        'Best Offer',
        compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def set_status_sold(self):
        for record in self:
            if 'cancelled' in record.mapped('state'):
                raise UserError('Canceled properties cannot be sold')
            else:
                record.state = 'sold'
        return True

    def set_status_cancel(self):
        for record in self:
            if 'sold' in record.mapped('state'):
                raise UserError('Sold properties cannot be cancelled')
            else:
                record.state = 'cancelled'
        return True
