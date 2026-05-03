from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Car(models.Model):
    _name = "car.car"
    _description = "Car"

    name = fields.Char(string="Name")
    full_name = fields.Char(string="Full Name", compute="_compute_full_name")
    model = fields.Char(string="Model")
    year = fields.Integer(string="Year")
    color = fields.Char(string="Color")
    price = fields.Float(string="Price")
    description = fields.Text(string="Description")
    available = fields.Boolean(string="Available", default=True)

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ], string="Status", default="draft"
    )

    feature_ids = fields.Many2many("car.feature", string="Features")
    buyer_id = fields.Many2one("car.buyer", string="Buyer")
    brand_id = fields.Many2one("car.brand", string="Brand")
    brand_country = fields.Char( string="Brand Country", related="brand_id.country", readonly=True )


##### Constraints #####
### name: unique constraint name, can be any string but should be unique across the model
### rule: name must be unique
### message: message i want to display
    _sql_constraints = [
        (
            "unique_car_name",
            "unique(name)",
            "Car name must be unique.",
        ),
        (
            "check_car_price_positive",
            "CHECK(price >= 0)",
            "Price cannot be negative.",
        ),
        (
            "check_car_year_valid",
            "CHECK(year IS NULL OR year >= 1886)",
            "Year must be 1886 or later.",
        ),
    ]


#### Business logic methods ####

    def sell_car(self):
        for record in self:
            record.available = False
            record.status = "sold"

    def set_status_draft(self):
        for record in self:
            record.status = "draft"

    def set_status_available(self):
        for record in self:
            record.status = "available"

    def set_status_reserved(self):
        for record in self:
            record.status = "reserved"

    def set_status_sold(self):
        for record in self:
            record.status = "sold"
            record.available = False

    def set_status_cancelled(self):
        for record in self:
            record.status = "cancelled"


# Computed fields, onchange methods, and constraints
    @api.depends("brand_id", "model", "year")
    def _compute_full_name(self):
        for record in self:
            brand_name = record.brand_id.name or ""
            model_name = record.model or ""
            year = record.year or ""
            record.full_name = f"{brand_name} {model_name} ({year})".strip()


# Onchange method to update brand_country when brand_id changes
    @api.onchange("brand_id")
    def _onchange_brand_id(self):
        if self.brand_id:
            self.brand_country = self.brand_id.country
        else:
            self.brand_country = "No country selected"


# Constrains method to validate price, year, and availability
    @api.constrains("price", "year", "available")
    def _check_price_and_year(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Price cannot be negative.")

            if record.year and record.year < 1886:
                raise ValidationError("Year must be 1886 or later.")

            if record.year and record.year > fields.Date.today().year:
                raise ValidationError("Year cannot be in the future.")

            if not record.available and record.price <= 0:
                raise ValidationError("Price must be greater than zero for sold cars.")
