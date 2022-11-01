import datetime
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


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
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        print("cancel day--------------------", cancel_day)
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        print('allow date-------------------------', allowed_date)
        if allowed_date < date.today():
            print(f"Al date{allowed_date} and today {date.today()}------------------------------------------")
            raise ValidationError(_('Cancellation is not correct!'))

        self.appointment_id.state = 'cancel'
        query = """select id,patient_id from hospital_appointment where id=%s""" % self.appointment_id.id
        # self.env.cr.execute(query)
        self._cr.execute(query)
        patients = self.env.cr.dictfetchall()
        print('Patients -------------->', patients)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'cancel.appointment.wizard',
        #     'target': 'new',
        #     'res_id': self.id
        # }
