# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AutovoyageCustomVehicle(models.Model):
    _name = "autovoyage.vehicle.custom"
    _description = "Custom Vehicle Registration"

    name = fields.Char(required=True)
    owener_id = fields.Many2one('res.users')
    vehicle_model = fields.Char(string="Vehicle Model")
    vehicle_number = fields.Char(string="Vehicle number")
    vehicle_buy_date = fields.Date(string="Vehicle Buy Date")
    vehicle_fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('lpg', 'LPG'),
    ], string="Fuel Type")
    vehicle_milage = fields.Float(string="Milage")
    per_day_cost = fields.Float()
    is_available = fields.Boolean(default=True)
    product_template_id = fields.Many2one('product.template', string="Linked Product", readonly=True)
    user_id = fields.Many2one("res.users",default = lambda self: self.env.user)
    
    @api.model
    def create(self, vals):
        record = super().create(vals)        
        if not record.owener_id.id:
            record.owener_id = record.user_id
        if not record.owener_id.is_service_provider:
            raise ValidationError('This owner id is not service provider!')        
        record.user_id = record.owener_id
        product = self.env['product.template'].sudo().create({
            'name': record.name,
            'owener_id': record.owener_id.id,
            'vehicle_model': record.vehicle_model,
            'vehicle_number': record.vehicle_number,
            'vehicle_buy_date': record.vehicle_buy_date,
            'vehicle_fule_type': record.vehicle_fuel_type,
            'vehicle_milage': record.vehicle_milage,
            'per_day_cost': record.per_day_cost,
            'is_vehicle': True,
            'is_avaliable': record.is_available,
        })
        record.product_template_id = product.id
        return record

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.product_template_id:
                product_vals = {}
                if 'name' in vals:
                    product_vals['name'] = vals['name']
                if 'owener_id' in vals:
                    product_vals['owener_id'] = vals.get('owner_id', record.user_id)
                if 'vehicle_model' in vals:
                    product_vals['vehicle_model'] = vals['vehicle_model']
                if 'vehicle_number' in vals:
                    product_vals['vehicle_number'] = vals['vehicle_number']
                if 'vehicle_buy_date' in vals:
                    product_vals['vehicle_buy_date'] = vals['vehicle_buy_date']
                if 'vehicle_fuel_type' in vals:
                    product_vals['vehicle_fule_type'] = vals['vehicle_fuel_type']
                if 'vehicle_milage' in vals:
                    product_vals['vehicle_milage'] = vals['vehicle_milage']
                if 'per_day_cost' in vals:
                    product_vals['per_day_cost'] = vals['per_day_cost']
                if 'is_available' in vals:
                    product_vals['is_avaliable'] = vals['is_available']
                
                record.product_template_id.sudo().write(product_vals)
        return res

    def unlink(self):
        for record in self:
            if record.product_template_id:
                record.product_template_id.sudo().unlink()
        return super().unlink()
