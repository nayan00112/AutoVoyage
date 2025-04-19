# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class AutovoyageService(models.Model):
    _name = 'autovoyage.service'
    
    name = fields.Char(string="Reference", readonly=True, copy=False, default='New')
    
    USER_REVIEW = [
        ('0', 'Normal'),
        ('1', 'Good'),
        ('2', 'Very Good'),
        ('3', 'Excellent')
    ]
    
    SERVICE_STATUS = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    service_consumer_id = fields.Many2one('res.users')
    service_provider_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    vehicle_ids = fields.Many2many('product.template')
    service_start_date = fields.Date()
    service_end_date = fields.Date()
    service_status = fields.Selection(SERVICE_STATUS, string="Service Status", compute="_compute_service_status", store=True)
    user_review = fields.Selection(USER_REVIEW)
    description = fields.Text()
    amount = fields.Float('Price', compute='_compute_ammount')
    
    @api.model
    def create(self, vals):
        if not self.env['res.users'].sudo().search([('id', '=', vals.get('service_provider_id', self.env.user.id))]).is_service_provider:
            raise ValidationError('Please select valid service provider.')
        
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('autovoyage.service') or '/'

        for record in self:
            print('=============-=-=---')
            print(record.service_provider_id)
            for vehicle in record.vehicle_ids:
                if record.service_status in ['completed', 'cancelled']:
                    vehicle.is_avaliable = False
                #  here i want to also check to which time interval vehicle is avaliable or not! and is avaliable become true after complete or cancled!
        return super().create(vals)
    
    @api.constrains('service_start_date', 'service_end_date')
    def _check_date_order(self):
        for record in self:
            if record.service_start_date and record.service_end_date:
                if record.service_start_date > record.service_end_date:
                    raise ValidationError("Service Start Date must be before End Date.")

    @api.depends('service_start_date', 'service_end_date')
    def _compute_service_status(self):
        today = date.today()
        for record in self:
            if record.service_start_date and record.service_end_date:
                if today < record.service_start_date:
                    record.service_status = 'upcoming'
                elif record.service_start_date <= today <= record.service_end_date:
                    record.service_status = 'active'
                elif today > record.service_end_date:
                    record.service_status = 'completed'
            else:
                record.service_status = 'upcoming'

    @api.onchange('service_provider_id')
    def _onchange_service_provider_id(self):        
        if self.service_provider_id:
            self.vehicle_ids = [(5, 0, 0)]  # Clear vehicle_ids instantly
            

    # @api.onchange('service_start_date', 'service_end_date', 'vehicle_ids')
    # def _check_is_this_vechile_avaliable(self):
    #     print(self.id)
    #     for record in self:    
    #         if record.service_start_date and record.service_end_date and record.vehicle_ids:
    #             exist_services = self.env['autovoyage.service'].search([('vehicle_ids', 'in', record.vehicle_ids.ids)])
    #             for es in exist_services:
                    
    #                 if (str(record.id).split('_')[1] != (str(es.id))):
    #                     print("es: ",es.id)
                       
    #                     # if (record.service_start_date > record.service_end_date):
                            
    #                     #     raise ValidationError("Service Start Date must be before End Date.----------------")
                        
    #                     override = not (es.service_start_date > record.service_end_date or es.service_end_date < record.service_start_date)
    #                     if override:
    #                         print(es.service_start_date, es.service_end_date)
    #                         print(record.service_start_date, record.service_end_date)
    #                         print('================', record.vehicle_ids.id)
    #                         vname = record.vehicle_ids.name 
    #                         record.vehicle_ids = [(3, record.vehicle_ids.id, 0)]
    #                         # (if this conditon true then latest changes rolback )
    #                         raise ValidationError("Vehicle "+  vname + " is already booked for given time period")
    #                     else:
    #                         print(es.service_start_date, es.service_end_date)
    #                         print(record.service_start_date, record.service_end_date)
    #                         print('---------------------------------')
    
    
    @api.onchange('service_start_date', 'service_end_date', 'vehicle_ids')
    def _check_is_this_vehicle_available(self):
        for record in self:
            if record.service_start_date and record.service_end_date and record.vehicle_ids:
                # Build a list of available vehicle IDs
                valid_vehicle_ids = []
                warning_msgs = []

                for vehicle in record.vehicle_ids:
                    overlapping_services = self.env['autovoyage.service'].search([
                        ('id', '!=', record.id or 0),
                        ('vehicle_ids', 'in', vehicle.ids),
                        ('service_start_date', '<=', record.service_end_date),
                        ('service_end_date', '>=', record.service_start_date),
                        ('service_status', 'in', ['active', 'upcoming'])
                    ])

                    if overlapping_services:
                        warning_msgs.append(f"- {vehicle.name} is already booked.")
                    else:
                        valid_vehicle_ids.append(vehicle.id)

                # Set only valid vehicles
                record.vehicle_ids = [(6, 0, valid_vehicle_ids)]  # Reset with only available vehicles

                # Show warning if any unavailable
                if warning_msgs:
                    return {
                        'warning': {
                            'title': "Unavailable Vehicles Removed",
                            'message': "Some vehicles were removed due to booking conflict:\n" + "\n".join(warning_msgs)
                        }
                    }

    @api.depends('service_start_date', 'service_end_date', 'vehicle_ids')
    def _compute_ammount(self):
        for record in self:
            if record.service_start_date and record.service_end_date and record.vehicle_ids:
                # Calculate the number of days
                delta = (record.service_end_date - record.service_start_date).days + 1  # Include the start date
                if delta < 0:
                    raise ValidationError("Service End Date must be after Service Start Date.")
                
                # Calculate the total cost based on per_day_cost of vehicles
                total_cost = sum(vehicle.per_day_cost for vehicle in record.vehicle_ids) * delta
                record.amount = total_cost
            else:
                record.amount = 0.0
        
    def confirm_service(self):
        for record in self:
            if record.service_status == 'cancelled':
                raise ValidationError('Can not generate sale order of "cancled" service state.')
            if not record.vehicle_ids:
                raise ValidationError("Please select at least one vehicle to confirm the service.")
            if not record.service_consumer_id:
                raise ValidationError("Please select a service consumer to confirm the service.")
            
            # Create a sale order
            sale_order = self.env['sale.order'].create({
                'partner_id': record.service_consumer_id.id,
                'date_order': fields.Datetime.now(),
                'origin': record.name,
            })
           
            order_lines_list = []
            for vehicle in record.vehicle_ids:
                product_variant = vehicle.product_variant_id
                if not product_variant:
                    raise ValidationError(f"Vehicle {vehicle.name} does not have a valid product variant.")

                order_lines_list.append((0, 0, {
                    'name': f"Service for {vehicle.name} ({record.service_start_date} to {record.service_end_date})",
                    'product_id': product_variant.id,
                    'product_uom_qty': 1,
                    'price_unit': vehicle.per_day_cost * ((record.service_end_date - record.service_start_date).days + 1),
                }))
            sale_order.order_line = order_lines_list

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': sale_order.id,
                'target': 'current',
            }
    def cancle_service(self):
        print(self.vehicle_ids.is_avaliable)
        self.service_status = "cancelled"
        # If service is cancle, then vehicle avaliable is true at this cancled
        # time period of service then, for creating other autovoyage services, 
        # when we looking for any vehicle avaliability in autovoyage services
        # then it must be check where then that autvoyage service's field status is
        # cancle or not, if cancle then ignore this as cancled services 
        # vehicles are avaliabled.
        
        print('cancle_service')
        
    def write(self, vals):
        if self.service_status in ('cancelled', 'completed'):
            raise ValidationError('Service State "completed" and "cancled" can not be modified!')
        super().write(vals)
    
    def unlink(self):
        if self.service_status in ('cancelled', 'completed'):
            raise ValidationError('Service State "completed" and "cancled" can not be delete.')
        super().unlink()
                