from odoo import models, fields

class CarBuyerPartnerExtension(models.Model):
    _inherit = 'res.partner'

    is_car_buyer = fields.Boolean(string="Is Car Buyer")
    preferred_car_brand_id = fields.Many2one("car.brand", string="Preferred Car Brand")