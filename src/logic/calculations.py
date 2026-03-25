from enum import IntEnum
from datetime import datetime, timedelta

class RecordStatus(IntEnum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3

def calculate_duration(start_str, end_str):
    """
    Calcula la duración entre dos horas en formato HH:MM.
    Maneja automáticamente el cruce de medianoche.
    """
    fmt = "%H:%M"
    # Convertimos los strings a objetos de tiempo
    start = datetime.strptime(start_str, fmt)
    end = datetime.strptime(end_str, fmt)
    
    # Si la hora de fin es menor a la de inicio, 
    # asumimos que es el día siguiente.
    if end < start:
        end += timedelta(days=1)
    
    duration = end - start
    # Devolvemos el total en horas (float) para facilitar cálculos de nómina
    return duration.total_seconds() / 3600

def calculate_overtime(total_hours):
    extra_hours = 0
    if total_hours > 8:
        extra_hours = total_hours - 8
        normal_hours = 8
    else:
        normal_hours = total_hours

    return normal_hours, extra_hours

def split_night_hours(start_hour, end_hour):
    night_start = 21

    if end_hour < start_hour:
        actual_end = end_hour + 24
    else:
        actual_end = end_hour

    calculation_start = max(start_hour, night_start)

    night_hours = actual_end - calculation_start

    return max(0, night_hours)