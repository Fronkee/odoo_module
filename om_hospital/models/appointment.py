from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Hospital Appointment  '
    _rec_name = 'ref'

    patient_id = fields.Many2one('hospital.patient', strring="Patient", ondelete="cascade")  # restrict
    gender = fields.Selection(related='patient_id.gender', readonly=False)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string="Reference", help="Reference from patient")
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([('0', 'low'), ('1', 'normal'), ('2', 'high'), ('3', 'very high')], string="Priority")
    state = fields.Selection([('draft', 'Draft'), ('in_consultation', 'Consultation'), ('done', 'Done'),
                              ('cancel', 'Cancel')], default='draft', required=1)
    pharmacy_ids = fields.One2many('hospital.pharmacy.line', 'appointment_id', string="Pharmacy")
    hide_sale_price = fields.Boolean(string="Hide Sale Price", default=False)
    operation_id = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related="company_id.currency_id")

    # amount = fields.Monetary(string="Amount")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        print(self.pharmacy_ids.qty)
        self.ref = self.patient_id.ref

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


class HospitalPharmacy(models.Model):
    _name = 'hospital.pharmacy.line'
    _description = 'Hospital Pharmacy'

    product_id = fields.Many2one('product.product', string="Product", required=1)
    price_unit = fields.Float(related='product_id.list_price', string="Sale Price", readonly=False)
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    currency_id = fields.Many2one('res.currency', string="Currency", related="appointment_id.currency_id")
    price_subtotal = fields.Monetary(string="Subtotal", compute="_compute_subtotal", store = True)
    amount = fields.Monetary(string="Amount", onchange="_onchange_amount")

    @api.depends('price_unit', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty

    @api.onchange('price_subtotal')
    def _onchange_amount(self):
        self.env.cr.execute(""" SELECT price_subtotal FROM hospital_pharmacy_line WHERE appointment_id=24""")
        results = self.env.cr.dictfetchall()
        print(results)
        for res in results:
            print(res['price_subtotal'])
