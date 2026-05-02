from odoo import models, fields

class Brand(models.Model):
    _name = "car.brand"
    _description = "Car Brand"

    name = fields.Char(string="Name", required=True)
    country = fields.Char(string="Country of Origin")
    car_ids = fields.One2many("car.car", "brand_id", string="Cars")