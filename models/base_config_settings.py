from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    days_before_reminder = fields.Integer("Number of days after lead creation before sending a reminder to the assigned user", config_parameter="irontech_first_contact.days_before_reminder")
    inspection_reminder_template_id = fields.Many2one( string="Mail Template ID",
        comodel_name="mail.template", required=True, domain=[('model_id', '=', 'insurance.lead')], 
        config_parameter="irontech_first_contact.inspection_reminder_template_id")

    inspection_reminder_sms_template_id = fields.Many2one( string="SMS Template ID",
        comodel_name="sms.template", required=True, domain=[('model_id', '=', 'insurance.lead')], 
        config_parameter="irontech_first_contact.inspection_reminder_sms_template_id")