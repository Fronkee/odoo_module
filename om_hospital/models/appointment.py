from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Hospital Appointment  '
    _rec_name = 'ref'

    patient_id = fields.Many2one('hospital.patient', strring="Patient", ondelete="cascade")  # restrict
    gender = fields.Selection(related='patient_id.gender',)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string="Reference", help="Reference from patient")
    age = fields.Integer(string="Age", related="patient_id.age")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'low'),
        ('1', 'normal'),
        ('2', 'high'),
        ('3', 'very high')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], default='draft', required=1)
    pharmacy_ids = fields.One2many('hospital.pharmacy.line', 'appointment_id', string="Pharmacy")
    hide_sale_price = fields.Boolean(string="Hide Sale Price", default=False)
    operation_id = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id")
    amount = fields.Monetary(string="Amount", )

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    # create serial number
    @api.model
    def create(self, vals_list):
        print("Vals is", vals_list)
        vals_list['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals_list)
        print('Serial number-----', res)

        sl_no = 0
        for line in res.pharmacy_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res

    # update serial number
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print("Write Serial ", res)
        sl_no = 0
        for line in self.pharmacy_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res

    def unlink(self):
        print("unlink method")
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_('Done state cannot Delete!'))
        return super(HospitalAppointment, self).unlink()

    # rainbow effect
    def test_btn(self):
        print("Class btn")
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.odoo.com'
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
            elif rec.state == 'cancel':
                print("State is", rec.state)
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Done State Successfully',
                'type': 'rainbow_man'
            }
        }

    def action_in_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            elif rec.state == 'in_consultation':
                progress = 40
            else:
                progress = 0
            rec.progress = progress

    # notification
    def action_notification(self):
        # msg = "Button Click Successful"
        # return{
        #     'type' : 'ir.actions.client',
        #     'tag' : 'display_notification',
        #     'params':{
        #         'message' : msg,
        #         'type' : 'warning', #type is color of bootstrap warn,danger,
        #         'sticky' : True,
        #     }
        # }      
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Click to open the patient record'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'sticky': True,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')]
                }
            }
        }

    # Send Email
    def action_send_mail(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        for rec in self:
            if rec.patient_id.email:
                email_values = {'subject': 'Test OM'}
                template.send_mail(rec.id, force_send=True, email_values=email_values)
            else:
                raise ValidationError(_(" Email does not exit! "))


class HospitalPharmacy(models.Model):
    _name = 'hospital.pharmacy.line'
    _description = 'Hospital Pharmacy'

    product_id = fields.Many2one('product.product', string="Product", required=1)
    price_unit = fields.Float(related='product_id.list_price', string="Sale Price", readonly=False)
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    currency_id = fields.Many2one('res.currency', string="Currency", related="appointment_id.currency_id")
    price_subtotal = fields.Monetary(string="Subtotal", compute="_compute_subtotal")
    sl_no = fields.Integer(string='SNO')

    @api.depends('price_unit', 'qty')
    def _compute_subtotal(self):
        # print("Subtotal-------------------------")
        for rec in self:
            # print(rec.qty)
            rec.price_subtotal = rec.price_unit * rec.qty
