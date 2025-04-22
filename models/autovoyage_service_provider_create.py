# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AutovoyageServiceProvidersCreate(models.Model):
    _name = 'autovoyage.createserviceprovider'
    _description = 'Service Providers'

    name = fields.Char(required=True)
    email = fields.Char(required=True)    
    join_date = fields.Date(string="Join Date", default=fields.Date.today)
    password = fields.Char(string="Password", required=True)
    user_id = fields.Many2one('res.users')

    @api.model_create_multi
    def create(self, vals_list):
        
        results = super().create(vals_list)

        for res in results:
            usr = self.env['res.users'].sudo().create({
                'name': res.name,
                'email': res.email,
                'login': res.email,
                'password': res.password,
                'groups_id': [(6, 0, [
                    self.env.ref('autovoyage.group_service_provider_user').id,
                    self.env.ref('base.group_user').id,
                ])],
            })
            res.user_id = usr
            usr.is_service_provider = True

        return results

    def write(self, vals):        
        res = super().write(vals)
        stud = self.env['res.users'].sudo().search([('id', '=', self.user_id.id)])
        if vals.get('email'):
            vals.update({
                'login': vals.get('email')
            })
        stud.sudo().write(vals)        

        return res
    
    def unlink(self):
        for record in self:
            if record.user_id:
                self.env['res.users'].search([('id', '=', record.user_id.id)]).unlink()
        return super().unlink()
