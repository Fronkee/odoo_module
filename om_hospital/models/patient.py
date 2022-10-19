from odoo import models, api, fields


class HospitalManagement(models.Model):
    _name = 'hospital.patient'
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = 'Hospital Patient    '

    name = fields.Char(string="Name")
    ref = fields.Char(string="Reference")
    age = fields.Integer(string="Age")
    gender = fields.Selection([('female', 'Female'), ('male', 'Male')], tring='Gender', default='male')
    active = fields.Boolean(string='Active', default=True)
