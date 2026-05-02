from odoo import models, fields

class CarFeature(models.Model):
    _name = "car.feature"
    _description = "Car Feature"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
