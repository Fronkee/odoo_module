from odoo import models, api, fields


class HospitalManagement(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient    '

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    gender = fields.Selection([('female', 'Female'), ('male', 'Male')], tring='Gender', default='male')
