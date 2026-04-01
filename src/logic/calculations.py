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

    def _get_night_window(self, start_dt, end_dt):
        n_start = start_dt.replace(hour=self.night_start_hour, minute=0, second=0, microsecond=0)
        n_end = end_dt.replace(hour=self.night_end_hour, minute=0, second=0, microsecond=0)
        return n_start, n_end

    def calculate_shift(self, start_dt, end_dt):
        """Manager: Orquesta todo el proceso"""
        total = self.calculate_total_duration(start_dt, end_dt)
        night = self.get_night_hours(start_dt, end_dt)
        overtime = self.calculate_overtime(total)
        
        return {
            "total": total,
            "night": night,
            "overtime": overtime,
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

    def calculate_overtime(self, total_hours):
        return max(0, total_hours - self.legal_day_hours)