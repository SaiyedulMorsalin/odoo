# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, datetime, time, timedelta
import pytz


class SsVentureHrAttendance(models.Model):
    _name = 'ss.venture.hr.attendance'
    _description = 'SS Venture HR Attendance'






class DailyAttendance(models.Model):
    _name = 'attendance.daily'
    _description = 'Daily Attendance'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    first_check_in = fields.Datetime(string='Check In')
    last_check_out = fields.Datetime(string='Check Out')
    worked_hours = fields.Float(string="Valid Worked Hours")
    emp_att_late = fields.Char(default='')

    def generate_daily_attendance(self):
        print("____________Daily Attendance Created__________")
        today = fields.Date.today()
        employees = self.env['hr.employee'].search([])
        print(today)

        for emp in employees:
            # Get today's datetime range
            start_datetime = datetime.combine(today, datetime.min.time())
            end_datetime = datetime.combine(today + timedelta(days=1), datetime.min.time())
            print('start_datetime',start_datetime)
            print('end_datetime',end_datetime)
            # Get today's attendance records for employee
            today_attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', emp.id),
                ('check_in', '>=', start_datetime),
                ('check_in', '<', end_datetime),
            ], order='check_in asc')
            print('today_attendance',today_attendances.check_in)
            if not today_attendances:
                today_attendances.unlink()
                continue  # No check-ins today

            # Calculate values
            first_check_in = today_attendances[0].check_in
            last_check_out = today_attendances[-1].check_out
            emp_first_check_in = first_check_in + timedelta(hours=6)
            print('first_Check_In',emp_first_check_in)

            worked_hours = sum(today_attendances.mapped('worked_hours'))

            # Find existing summary
            existing_summary = self.search([
                ('employee_id', '=', emp.id),
                ('first_check_in', '>=', start_datetime),
                ('first_check_in', '<', end_datetime)
            ], limit=1)
            print('existing summary',existing_summary)
            if existing_summary:
                # Update the existing record
                existing_summary.write({
                    'first_check_in': first_check_in,
                    'last_check_out': last_check_out,
                    'worked_hours': worked_hours,
                })
            else:
                # Create new summary
                self.create({
                    'employee_id': emp.id,
                    'first_check_in': first_check_in,
                    'last_check_out': last_check_out,
                    'worked_hours': worked_hours,
                })


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
            print('first_check out', first_check_in)
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

                        print("Searching for late attendance:")
                        print(f"Employee: {employee.id}, Check-in time: {first_check_in}, Start hour: {start_hour}")
                        print(f"Query: {datetime.combine(today, time(start_hour.hour, 14, 59))}")

                        late_attendance = self.env['hr.attendance'].sudo().search([
                            ('employee_id', '=', employee.id),
                            ('first_check_in', '>', datetime.combine(today, time(start_hour.hour, 14, 59))),
                            ('emp_att_late', '=', '')
                        ], limit=1)
                        print('Late check in',late_attendance.first_check_in)
                        late_attendance.update({'emp_att_late':'Late'})
                        print(f"Late Attendance found: {late_attendance.check_in}")




        return res




