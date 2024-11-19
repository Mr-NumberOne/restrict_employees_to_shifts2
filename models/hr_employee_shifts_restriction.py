from odoo import models, fields
class HrEmployeeLogout(models.Model):
    _inherit = "hr.employee"
    restrict_login_to_shifts = fields.Boolean(default=False)