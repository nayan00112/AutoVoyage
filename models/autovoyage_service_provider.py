# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AutovoyageServiceProviders(models.Model):
    _inherit = 'res.users'
    
    joining_date = fields.Date()
    is_service_provider = fields.Boolean(default=False)
    vehicle_ids = fields.One2many('product.template', 'owener_id')
    
    @api.model_create_multi
    def create(self, vals_list):
        user = super().create(vals_list)
        if user.is_service_provider:
            user.groups_id = [(4, self.env.ref('autovoyage.group_service_provider_user').id)]
        return user
    
    def write(self, vals):
        res = super().write(vals)
        print('ok')
        for user in self:
            if vals.get('is_service_provider') is not None:
                group = self.env.ref('autovoyage.group_service_provider_user')
                if user.is_service_provider:
                    user.groups_id = [(4, group.id)]
                else:
                    user.groups_id = [(3, group.id)]
        return res