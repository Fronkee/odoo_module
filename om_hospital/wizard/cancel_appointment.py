import datetime
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields_list):
        # print(fields_list)
        res = super(CancelAppointmentWizard, self).default_get(fields_list)
        print("context...............", self.env.context.get('active_id'))
        res['cancel_date'] = datetime.date.today()
        res['appointment_id'] = self.env.context.get('active_id')
        res['reason'] = 'Testing'
        return res
    
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    # domain=['|', ('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))]
    reason = fields.Text(string="Reason", default="Test Default Function")
    cancel_date = fields.Date(string="Cancellation Date")

    def action_cancel_appointment(self):
        if self.appointment_id.booking_date == fields.date.today():
            raise ValidationError(_('Cancellation is not correct!'))
