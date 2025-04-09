# -*- coding: utf-8 -*-
# from odoo import http


# class LateHrAttendanceSAndSVentureLtd(http.Controller):
#     @http.route('/late_hr_attendance_s_and_s_venture_ltd/late_hr_attendance_s_and_s_venture_ltd', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/late_hr_attendance_s_and_s_venture_ltd/late_hr_attendance_s_and_s_venture_ltd/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('late_hr_attendance_s_and_s_venture_ltd.listing', {
#             'root': '/late_hr_attendance_s_and_s_venture_ltd/late_hr_attendance_s_and_s_venture_ltd',
#             'objects': http.request.env['late_hr_attendance_s_and_s_venture_ltd.late_hr_attendance_s_and_s_venture_ltd'].search([]),
#         })

#     @http.route('/late_hr_attendance_s_and_s_venture_ltd/late_hr_attendance_s_and_s_venture_ltd/objects/<model("late_hr_attendance_s_and_s_venture_ltd.late_hr_attendance_s_and_s_venture_ltd"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('late_hr_attendance_s_and_s_venture_ltd.object', {
#             'object': obj
#         })

