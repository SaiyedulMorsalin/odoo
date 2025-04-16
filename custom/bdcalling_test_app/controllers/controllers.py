# -*- coding: utf-8 -*-
# from odoo import http


# class BdcallingTestApp(http.Controller):
#     @http.route('/bdcalling_test_app/bdcalling_test_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bdcalling_test_app/bdcalling_test_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bdcalling_test_app.listing', {
#             'root': '/bdcalling_test_app/bdcalling_test_app',
#             'objects': http.request.env['bdcalling_test_app.bdcalling_test_app'].search([]),
#         })

#     @http.route('/bdcalling_test_app/bdcalling_test_app/objects/<model("bdcalling_test_app.bdcalling_test_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bdcalling_test_app.object', {
#             'object': obj
#         })

