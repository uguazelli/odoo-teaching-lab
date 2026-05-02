from odoo import models, fields

class CarBuyer(models.Model):
    _name = 'car.buyer'
    _description = 'Car Buyer'

    name = fields.Char(required=True)
    max_budget = fields.Float(string="Max Budget")