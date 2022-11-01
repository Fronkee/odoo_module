from odoo import api, fields, models


class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    DEFAULT_ENV_VARIABLES = """# Available variable 
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object
    # - self : Current Object \n\n\n"""

    model_id = fields.Many2one('ir.model', string="Model")
    code = fields.Text(string="Code", default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string="Result")

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
                self.result = model
            else:
                model = self
                print(model)
                self.result = model
        except Exception as e:
            print("coming from exception")
            self.result = str(e)
