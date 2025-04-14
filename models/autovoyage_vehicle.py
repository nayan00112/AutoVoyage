# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AutovoyageVehicle(models.Model):
    _inherit = "product.template"
    
    owener_id = fields.Many2one('res.partner')
    vehicle_model = fields.Char(string="Vehicle Model")
    vehicle_buy_date = fields.Date(string="Vehicle Buy Date")
    vehicle_fule_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('lpg', 'LPG'),
    ], string="Fuel Type")
    vehicle_milage = fields.Float(string="Milage")
    # vehicle_maintenance_line=fields.One2many()
    is_vehicle = fields.Boolean(default=False)
    is_avaliable = fields.Boolean(default=False)
    
    per_day_cost = fields.Float()
    
    @api.constrains('vehicle_milage')
    def _check_vehicle_milage(self):
        for record in self:
            if record.vehicle_milage < 0:
                raise ValidationError("Vehicle milage must be a positive number.")

    @api.constrains('per_day_cost')
    def _check_per_day_cost(self):
        for record in self:
            if record.per_day_cost < 0:
                raise ValidationError("Per Day Cost must be a positive.")

