from odoo import fields, api, models


class HospitalTag(models.Model):
    _name = "hospital.tag"
    _description = "Hospital Tag"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active")
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
