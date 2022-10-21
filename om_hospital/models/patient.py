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

    # create sequence with sequence_data.xml
    @api.model
    def create(self, vals_list):
        print("odooooo-------------------------------------------------------", vals_list)
        print('...................', self.env['ir.sequence'])
        vals_list['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalManagement, self).create(vals_list)

    # can update data,
    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
            print("We are going to go", vals)
            return super(HospitalManagement, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    def name_get(self):
        # patient_list = []
        # for rec in self:
        #     name = f'{rec.ref}  {rec.name}'
        #     patient_list.append((rec.id, name))
        # return patient_list
    # single line method
        return [(rec.id, "%s:%s" % (rec.ref, rec.name)) for rec in self]
