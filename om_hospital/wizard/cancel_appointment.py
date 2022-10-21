import datetime
from odoo import fields, api, models


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields_list):
        # print(fields_list)
        res = super(CancelAppointmentWizard, self).default_get(fields_list)
        print("Coming From Default Get Function", res)
        res['cancel_date'] = datetime.date.today()
        return res
    
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    reason = fields.Text(string="Reason", default="Test Default Function")
    cancel_date = fields.Date(string="Cancellation Date")

    def action_cancel_appointment(self):
        pass
