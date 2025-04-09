# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, datetime, time, timedelta
import pytz


class SsVentureHrAttendance(models.Model):
    _name = 'ss.venture.hr.attendance'
    _description = 'SS Venture HR Attendance'


def get_local_datetime(self, your_date_or_datetime_info):
    user_tz = self.env.user.tz or 'UTC'
    local = pytz.timezone(user_tz)
    dt_utc = pytz.utc.localize(datetime.strptime(your_date_or_datetime_info, "%Y-%m-%d %H:%M:%S"))
    dt_local = dt_utc.astimezone(local)
    return dt_local.strftime("%d/%m/%Y %H:%M:%S")


def float_to_time(hours_float):
    hours, remainder = divmod(hours_float, 1)
    minutes = int(remainder * 60)
    return time(int(hours), minutes)


def float_to_datetime(hours_float, date_str):
    """
    Convert a float (e.g. 9.5) and date string (e.g. '2025-04-06') to a datetime object.
    """
    hours, remainder = divmod(hours_float, 1)
    minutes = int(remainder * 60)
    base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    dt = datetime.combine(base_date, time(int(hours), minutes))
    return dt


class InheritHRAttendance(models.Model):
    _inherit = 'hr.attendance'

    emp_att_late = fields.Char(default='')
    first_check_in = fields.Datetime(string='First Check In', default=None)
    last_check_out = fields.Datetime(string='Last Check Out', default=None)
    dt = fields.Datetime.now() + timedelta(hours=6)

    def create(self, values):
        res = super(InheritHRAttendance, self).create(values)

        # Handle single or multiple attendance records
        for attendance in res:
            employee = attendance.employee_id
            all_first_check_in_list = []
            work_schedule = employee.resource_calendar_id.attendance_ids if employee.resource_calendar_id else []
            emp_first_check_in_today = None
            emp_first_check_in_date = None
            todays_start_working_hour = None

            last_check_out = None
            emp_last_check_out_time = None
            emp_last_check_out_date = None
            today = date.today()

            today_weekofday = str(today.weekday())

            for day in work_schedule:
                if today_weekofday == day.dayofweek:
                    todays_start_working_hour = day.hour_from

            attendance_list = employee.attendance_ids
            first_check_in = None


            for att in attendance_list:
                if att.check_in and att.check_in.date() == today:
                    if first_check_in is None or att.check_in < first_check_in:
                        first_check_in = att.check_in+timedelta(hours=6)
                        emp_first_check_in_today = first_check_in.time()
                        emp_first_check_in_date = att.check_in

            print('first_check out',first_check_in)
            print('first_check out', first_check_in.hour)
            for att in attendance_list:
                if att.check_out and att.check_out.date() == today:
                    if last_check_out is None or att.check_out > last_check_out:
                        last_check_out = att.check_out
                        emp_last_check_out_time = att.check_out.time()
                        emp_last_check_out_date = att.check_out

            print('Last check-out today:', emp_last_check_out_date)

            if emp_first_check_in_date:
                attendance.first_check_in = emp_first_check_in_date
                all_first_check_in_list.append(emp_first_check_in_date)

            if emp_last_check_out_date:
                attendance.last_check_out=emp_last_check_out_date

            print('Start Working Hours',todays_start_working_hour)
            if todays_start_working_hour and emp_first_check_in_today:
                start_hour = float_to_time(todays_start_working_hour)

                if start_hour < emp_first_check_in_today:

                    print("start hour",start_hour,'first check in time',emp_first_check_in_today)
                    # Mark as late if check-in is after start hour
                    if employee:
                        # Search for today's attendance (you can adjust the domain as needed)
                        attendance = self.env['hr.attendance'].sudo().search([
                            ('employee_id', '=', employee.id),
                            ('first_check_in', '>', datetime.combine(today, time(start_hour.hour, 14, 59))),
                            ('emp_att_late', '=', '')
                        ], limit=1)

                        if attendance:
                            print("COunt Late")
                            attendance.write({'emp_att_late': 'Late'})

                    # late_attendance = self.env['hr.attendance'].sudo().search([
                    #     ('employee_id', '=', employee.id),
                    #     ('first_check_in', '>', datetime.combine(today, start_hour))
                    # ], limit=1)
                    # print(datetime.combine(today, start_hour))
                    # if late_attendance:
                    #     print("late dict", late_attendance)
                    #     late_attendance.write({'emp_att_late': 'Late'})

        return res
