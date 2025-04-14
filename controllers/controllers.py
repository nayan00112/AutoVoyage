# -*- coding: utf-8 -*-
# from odoo import http


# class Autovoyage(http.Controller):
#     @http.route('/autovoyage/autovoyage', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/autovoyage/autovoyage/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('autovoyage.listing', {
#             'root': '/autovoyage/autovoyage',
#             'objects': http.request.env['autovoyage.autovoyage'].search([]),
#         })

#     @http.route('/autovoyage/autovoyage/objects/<model("autovoyage.autovoyage"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('autovoyage.object', {
#             'object': obj
#         })

