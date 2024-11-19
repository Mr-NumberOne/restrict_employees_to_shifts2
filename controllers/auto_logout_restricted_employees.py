# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import pytz

from colorama import Fore, Back, Style


class EmployeeLoginAccessController(http.Controller):
    @http.route('/hr/shift_restricted', auth='public', type='json')
    def logout_shift_restricted_employees(self):
        # ? Start checking if employee and restricted
        user_id = request.env.uid
        employee = request.env['hr.employee'].search([('user_id', '=', user_id)])
        if employee and employee.restrict_login_to_shifts:
            # ? start shift Handling
            current_datetime = datetime.now().astimezone(pytz.timezone('Asia/Aden'))
            day_of_the_week = self._map_day_to_integer(current_datetime.strftime('%A'))
            shifts = request.env['resource.calendar.attendance'].search(
                ['&',
                 ('calendar_id', '=', employee.resource_calendar_id.id),
                 ('dayofweek', '=', day_of_the_week),
                 ('day_period', '!=', 'lunch')])
            is_on_shift, minutes_remaining = self._check_if_in_shift(shifts, current_datetime)
            if is_on_shift:
                if 1 > minutes_remaining >= 0:
                    return 0.5   # to logout people with less than a minute
                else:
                    return minutes_remaining
            else:
                return 0.5  # log them out
        print(Style.RESET_ALL)

    @staticmethod
    def _map_day_to_integer(day_of_week):
        day_mapping = {
            'Monday': '0',
            'Tuesday': '1',
            'Wednesday': '2',
            'Thursday': '3',
            'Friday': '4',
            'Saturday': '5',
            'Sunday': '6'
        }
        return day_mapping.get(day_of_week, 'Invalid day')

    @staticmethod
    def _check_if_in_shift(shifts, current_datetime):
        flag = False
        minutes_remaining = 0
        def _time_to_float(c_dt):
            hours = c_dt.hour
            minutes = c_dt.minute
            tf = hours + minutes / 60.0
            return tf

        def _float_to_minutes(float_hours):
            total_minutes = float_hours * 60
            return round(total_minutes)

        time_float = _time_to_float(current_datetime)
        for shift in shifts:
            if shift.hour_from <= time_float <= shift.hour_to:
                flag = True
                minutes_remaining = _float_to_minutes(shift.hour_to - time_float)
                break

        return flag, minutes_remaining
