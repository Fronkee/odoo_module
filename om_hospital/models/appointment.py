from odoo import models, api, fields


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Hospital Appointment  '
    _rec_name = 'ref'

    patient_id = fields.Many2one('hospital.patient', strring="Patient")
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

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    # rainbow effect
    def test_btn(self):
        print("Class btn")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfully',
                'type': 'rainbow_man'
            }
        }

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action


class HospitalPharmacy(models.Model):
    _name = 'hospital.pharmacy.line'
    _description = 'Hospital Pharmacy'

    product_id = fields.Many2one('product.product', string="Product", required=1)
    price_unit = fields.Float(related='product_id.list_price', string="Sale Price", readonly=False)
    qty = fields.Integer(string="Quantity", default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
