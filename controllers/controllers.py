from odoo import http
from odoo.http import request
# from psycopg2 import Binary
# from odoo.addons.web.controllers.main import Binary

class AutovoyageController(http.Controller):
    
    @http.route('/autovoyage/get_vehicles', type='json', auth='public')
    def get_vehicles(self):
        vehicles = request.env['product.template'].sudo().search([('is_vehicle', '=', True)])
        vehicle_data = []
        for vehicle in vehicles:
            vehicle_data.append({
                'id': vehicle.id,
                'name': vehicle.name,
                'vehicle_model': vehicle.vehicle_model,
                'service_provider': vehicle.owener_id.name,
                'vehicle_fule_type': vehicle.vehicle_fule_type,
                'per_day_cost': vehicle.per_day_cost,
                'image_url': f'/web/image/product.template/{vehicle.id}/image_256',
            })
        return vehicle_data
    
    # @http.route('/autovoyage/vehicle_image/<int:vehicle_id>', type='http', auth='public', website=True)
    # def vehicle_image(self, vehicle_id):
    #     return Binary().content_image(
    #         model='product.template',
    #         id=vehicle_id,
    #         field='image_256',
    #         filename_field='name',
    #     )
        
    @http.route('/autovoyage/book_vehicle/<int:vehicle_id>', type='http', auth='user', website=True)
    def book_vehicle(self, vehicle_id):
        vehicle = request.env['product.template'].sudo().browse(vehicle_id)
        vehicle_details = {
            'id': vehicle.id,
            'name':vehicle.name,
            'vehicle_model': vehicle.vehicle_model,
            'vehicle_number': vehicle.vehicle_number,
            'vehicle_fule_type': vehicle.vehicle_fule_type,
            'vehicle_milage': vehicle.vehicle_milage,
            'per_day_cost': vehicle.per_day_cost,
            'service_provider': vehicle.owener_id.name,
        }
        return request.render("autovoyage.book_vehicle_template", vehicle_details)
    
    @http.route('/autovoyage/confirm_booking', type='http', auth='user', website=True, csrf=False)
    def confirm_booking(self, vehicle_id, start_date, end_date, notes=None, **kwargs):
        vehicle = request.env['product.template'].sudo().browse(int(vehicle_id))
        # Check if the vehicle is available for the given time period
        overlapping_services = request.env['autovoyage.service'].sudo().search([
            ('vehicle_ids', 'in', vehicle.id),
            ('service_start_date', '<=', end_date),
            ('service_end_date', '>=', start_date),
            ('service_status', 'in', ['active', 'upcoming'])
        ])

        if overlapping_services:
            return request.render("autovoyage.vehicle_unavailable_template", {
                'vehicle_name': vehicle.name,
                'start_date': start_date,
                'end_date': end_date,
            })
        
        # Create a booking record (or handle booking logic here)        
        booking = request.env['autovoyage.service'].sudo().create({
            'name': f"Booking for {vehicle.name}",
            'service_consumer_id': request.env.user.id,
            'service_provider_id': vehicle.owener_id.id,
            'service_start_date': start_date,
            'service_end_date': end_date,
            'vehicle_ids': [(6, 0, [vehicle.id])],
            'description': notes,
        })

        return request.redirect('/autovoyage/booking_success')
    
    @http.route('/autovoyage/booking_success', type='http', auth='user', website=True)
    def booking_success(self, **kwargs):
        return request.render("autovoyage.booking_success_template")