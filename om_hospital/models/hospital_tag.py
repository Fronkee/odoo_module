from odoo import fields, api, models


class HospitalTag(models.Model):
    _name = "hospital.tag"
    _description = "Hospital Tag"

    def default_get(self, fields_list):
        res = super(HospitalTag, self).default_get(fields_list)
        print('Context Tag -----------------------------', fields_list)
        return res

    name = fields.Char(string="Name", required=True, trim=False)
    active = fields.Boolean(string="Active", default=True, copy=False)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    # duplicate record for unique value
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + "(copy)"
        return super(HospitalTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique (name)', 'Name must be unique.'),
        ('check_sequence', 'check (sequence > 0)', 'Sequence must be greater than 0')
    ]
    # work _sql_constraints for unique_name, condition of sequence