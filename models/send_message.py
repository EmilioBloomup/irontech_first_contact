# -*- coding: utf-8 -*-
from odoo import api, fields, models

class LeadInspection(models.Model):
    _inherit = "insurance.lead"

    @api.depends('phase_id')
    def _set_requesting_inspection(self):
        for record in self:
            reminder_phase_id = self.env['insurance.lead.phase']._get_phases()['waiting_expertise'][0]
            if reminder_phase_id == record.phase_id.id:
                record.requesting_inspection = True
            else:
                record.requesting_inspection = False

    requesting_inspection = fields.Boolean(default="False", compute=_set_requesting_inspection, store=True)


    @api.model
    def _send_inspection_reminder(self):
        delay = self.env["ir.config_parameter"].sudo().get_param("irontech_first_contact.days_before_reminder")
        to_process = self.env['insurance.lead'].search([])
        if int(delay) > 0:
            for record in to_process:

                #check if reminder has already been sent
                if record.requesting_inspection:
                    #looking for id of phases requiring reminders
                    reminder_phase_id = self.env['insurance.lead.phase']._get_phases()['waiting_expertise'][0]

                    #get current phase days and configured delay
                    if record.phase_id.id == reminder_phase_id:
                        cur_phase_hist = self.env['insurance.phase.history'].search([('insurance_lead_id', '=', record.id), 
                                                ('phase_id.id', '=', reminder_phase_id)], order='create_date desc', limit=1)
                        if int(cur_phase_hist.days) >= int(delay):
                            #send stuff
                            if not record.user_id:
                                print("no one assigned to this phase, no message sent")
                            else:
                                temp_id = self.env["ir.config_parameter"].sudo().get_param("irontech_first_contact.inspection_reminder_template_id")
                                temp = self.env['mail.template'].search([('id', '=', temp_id)])
                                record.message_post_with_template(temp.id, composition_mode='mass_mail', partner_ids=[record.user_id.partner_id.id])
                                print("sent email to: ", record.user_id.partner_id.name)

                                temp_sms_id = self.env["ir.config_parameter"].sudo().get_param("irontech_first_contact.inspection_reminder_sms_template_id")
                                temp_sms = self.env['sms.template'].search([('id', '=', temp_sms_id)])
                                record._message_sms_with_template(temp_sms, partner_ids=[record.user_id.partner_id.id])
                                print("sent sms to: ", record.user_id.partner_id.name)


                            #reset to avoid sending message twice in the same phase
                            record.requesting_inspection = False

