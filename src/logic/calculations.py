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

    def is_holiday(self, dt):
        """Verifica si es domingo (6) o un festivo (por ahora solo domingos)"""
        return dt.weekday() == 6
    
    def _get_night_window(self, start_dt):
        """Define la ventana nocturna de 19:00 a 06:00 del día siguiente"""
        n_start = start_dt.replace(hour=self.night_start_hour, minute=0, second=0, microsecond=0)
        # La noche termina a las 6am del día siguiente
        n_end = n_start + timedelta(hours=11) 
        
        # Ajuste por si el turno empezó antes de las 6am
        if start_dt.hour < self.night_end_hour:
            n_start -= timedelta(days=1)
            n_end -= timedelta(days=1)
        return n_start, n_end


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

    def calculate_overtime(self, actual_start, actual_end, scheduled_start, scheduled_end):
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
    
    # --- ALL BACKGROUND METHODS ---^

    def calculate_shift(self, actual_start, actual_end, scheduled_start, scheduled_end):
        # 1. Corrección de medianoche (para que no de ceros)
        if actual_end < actual_start:
            actual_end += timedelta(days=1)
        if scheduled_end < scheduled_start:
            scheduled_end += timedelta(days=1)

        total_val = self.calculate_total_duration(actual_start, actual_end)
        
        # 2. Calculamos extras
        o_hours = self.calculate_overtime(actual_start, actual_end, scheduled_start, scheduled_end)

        n_hours = 0
        h_hours = 0

        if o_hours > 0:
        
            extra_start = scheduled_end
            extra_end = actual_end

            n_hours = self.get_night_hours(extra_start, extra_end)

        # 3. Solo el festivo es condicional
            if self.is_holiday(actual_start):
                h_hours = o_hours
                
        return {
            "total": total_val,
            "night": n_hours,
            "overtime": o_hours,
            "holiday": h_hours,
            "status": RecordStatus.PENDING
        }
    
    # --- MANAGER ---^  