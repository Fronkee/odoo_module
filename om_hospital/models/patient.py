from datetime import date
from odoo import models, api, fields
from odoo.exceptions import ValidationError


class HospitalManagement(models.Model):
    _name = 'hospital.patient'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Hospital Patient'

    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="Reference")
    date_of_birth = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age", tracking=True, compute='_compute_age')
    gender = fields.Selection([('female', 'Female'), ('male', 'Male')], string='Gender', tracking=True)
    active = fields.Boolean(string='Active', default=True, invisible=1)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('hospital.tag', string="Patient Tag")

    @api.model
    def create(self, vals_list):
        print("Odoo....", vals_list)
        vals_list['ref'] = 'HERE001'
        return super(HospitalManagement, self).create(vals_list)

    def name_get(self):
        print("name get method")
        
    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            print(today)
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0
