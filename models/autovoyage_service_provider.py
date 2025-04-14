# -*- coding: utf-8 -*-

from odoo import models, fields

class AutovoyageServiceProviders(models.Model):
    _inherit = 'res.partner'
    
    joining_date = fields.Date()
    is_service_provider = fields.Boolean(default=False)
    vehicle_ids = fields.One2many('product.template', 'owener_id')