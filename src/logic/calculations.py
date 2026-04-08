from datetime import datetime, timedelta
from enum import IntEnum

class RecordStatus(IntEnum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3

class ShiftCalculator:
    def __init__(self):
        self.night_start_hour = 19
        self.night_end_hour = 6
        self.legal_day_hours = 8
        self.is_holiday = 0

    def _get_night_window(self, start_dt, end_dt):
        n_start = start_dt.replace(hour=self.night_start_hour, minute=0, second=0, microsecond=0)
        n_end = end_dt.replace(hour=self.night_end_hour, minute=0, second=0, microsecond=0)
        return n_start, n_end

    def calculate_shift(self, actual_start, actual_end, scheduled_start, scheduled_end):
        """Manager: Orquesta todo el proceso"""
        total = self.calculate_total_duration(actual_start, actual_end)

        # 1. Es festivo o domingo?
        if self.is_holiday(actual_start):

            holiday_hours = total
            normal_overtime = 0
            night_hours = self.get_night_hours(actual_start, actual_end)
        else:
            holiday_hours = 0
            night = self.get_night_hours(actual_start, actual_end)
            normal_overtime = self.calculate_overtime(actual_start, actual_end, scheduled_start, scheduled_end)

        return {
            "total": total,
            "night": night,
            "overtime": normal_overtime,
            "holiday": holiday_hours,
            "status": RecordStatus.PENDING
        }

    def get_night_hours(self, start_dt, end_dt):
        n_start, n_end = self._get_night_window(start_dt, end_dt)
        overlap_start = max(start_dt, n_start)
        overlap_end = min(end_dt, n_end)
        
        if overlap_start < overlap_end:
            diff = overlap_end - overlap_start
            return diff.total_seconds() / 3600
        return 0

    def calculate_total_duration(self, start_dt, end_dt):
        if end_dt <= start_dt: return 0
        return (end_dt - start_dt).total_seconds() / 3600

    def calculate_overtime(scheduled_start, scheduled_end, actual_start, actual_end):
        if scheduled_end < scheduled_start:
            scheduled_end += timedelta(days=1)
        if actual_end < actual_start:
            actual_end += timedelta(days=1)
            
        diff = 0

        overlap_start = max(actual_start, scheduled_start)
        overlap_end = min(actual_end, scheduled_end)


        if overlap_end > overlap_start:
            if actual_start < scheduled_start:
                diff += (scheduled_start - actual_start).total_seconds() / 3600
            if actual_end > scheduled_end:
                diff += (actual_end - scheduled_end).total_seconds() / 3600
            return diff
        else:
            return 0
    
    def verify_schedule(self, scheduled_start, scheduled_end, actual_start, actual_end):
    # 1. Empezamos asumiendo que todo está bien
        report = {
            "is_compliant": True,
            "late_arrival_minutes": 0,
            "early_departure_minutes": 0
        }

        # 2. Verificamos llegada tarde
        if actual_start > scheduled_start:
            diff = actual_start - scheduled_start
            report["late_arrival_minutes"] = diff.total_seconds() / 60
            report["is_compliant"] = False

        # 3. Verificamos salida temprana
        if actual_end < scheduled_end:
            diff = scheduled_end - actual_end
            report["early_departure_minutes"] = diff.total_seconds() / 60
            report["is_compliant"] = False

        return report