from datetime import date
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalManagement(models.Model):
    _name = 'hospital.patient'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Hospital Patient'
    _order = 'id desc'

    name = fields.Char(string="Name", tracking=True)
    ref = fields.Char(string="Reference")
    date_of_birth = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age", compute="_compute_age", inverse="_inverse_compute_age", search="_search_age",
                         tracking=True)
    gender = fields.Selection([('female', 'Female'), ('male', 'Male')], string='Gender', tracking=True)
    active = fields.Boolean(string='Active', default=True, invisible=1)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('hospital.tag', string="Patient Tag")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count", store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment IDS")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status")
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Brithday", compute="_compute_is_birthday")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    _sql_constraints = [
        ('unique_ref', 'unique (ref)', 'Reference Number Must Be Unique!')
    ]
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('Bron Date must be last than Current Date'))

    # create sequence with sequence_data.xml
    @api.model
    def create(self, vals_list):
        print("odooooo-------------------------------------------------------", vals_list)
        print('...................', self.env['ir.sequence'])
        vals_list['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalManagement, self).create(vals_list)

    # can update data,
    # def write(self, vals):
    #     if not self.ref and not vals.get('ref'):
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
    #         print("We are going to go", vals)
    #         return super(HospitalManagement, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            print("today is --------------------", today)
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
                print("Age is ----------------------", rec.age)
            else:
                rec.age = 1

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            print("Reverse age----------------------------------------------")
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
            # does not work inverse function for age

    # compute age cannot search controlpanel view, use _search function can find
    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You Cannot delete a patient with appointment"))

    def action_test(self):
        print('click me')
        return

    def _compute_is_birthday(self):
        for rec in self:
            is_birth = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    print(f'month is {rec.date_of_birth.month}')
                    is_birth = True
                    print(is_birth)
            rec.is_birthday = is_birth

    def name_get(self):
        # patient_list = []
        # for rec in self:
        #     name = f'{rec.ref}  {rec.name}'
        #     patient_list.append((rec.id, name))
        # return patient_list
        # single line method
        return [(rec.id, "%s:%s" % (rec.ref, rec.name)) for rec in self]
