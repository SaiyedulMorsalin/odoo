# -*- coding: utf-8 -*-
# from odoo import http


# class BdcallingAttendance(http.Controller):
#     @http.route('/bdcalling_attendance/bdcalling_attendance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bdcalling_attendance/bdcalling_attendance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bdcalling_attendance.listing', {
#             'root': '/bdcalling_attendance/bdcalling_attendance',
#             'objects': http.request.env['bdcalling_attendance.bdcalling_attendance'].search([]),
#         })

#     @http.route('/bdcalling_attendance/bdcalling_attendance/objects/<model("bdcalling_attendance.bdcalling_attendance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bdcalling_attendance.object', {
#             'object': obj
#         })

