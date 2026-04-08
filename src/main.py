from datetime import datetime, timedelta
from src.logic.calculations import ShiftCalculator


def request_hour(message, base_date):
    while True:
        hour_str = input(f"{message} (ej: 08:00 AM): ").strip().upper()

        if "AM" in hour_str and " AM" not in hour_str:
            hour_str = hour_str.replace("AM", " AM")
        if "PM" in hour_str and " PM" not in hour_str:
            hour_str = hour_str.replace("PM", " PM")
        try:
            full_string = f"{base_date} {hour_str}"
            return datetime.strptime(full_string, "%Y-%m-%d %I:%M %p")
        except ValueError:
            print("Formato incorrecto. Intenta de nuevo usando HH:MM AM/PM")

if __name__ == "__main__":
    manager = ShiftCalculator()
    while True:
        print("\n--- REGISTRO DE NUEVO TURNO ---")
        base_date = input("Fecha (YYYY-MM-DD) o escribe 'salir': ").strip()
        
        if base_date.lower() == 'salir':
            break

        try:
            print("\n--- Horario PROGRAMADO (Lo que debía hacer) ---")
            scheduled_start = request_hour("Entrada programada", base_date)
            scheduled_end = request_hour("Salida programada", base_date)

            print("\n--- Horario REAL (Lo que en verdad hizo) ---")
            actual_start = request_hour("Entrada real", base_date)
            actual_end = request_hour("Salida real", base_date)

                # 3. Llamar al Manager (el cerebro)
                # Asegúrate de que tu Manager ya acepte los 4 parámetros
            results = manager.calculate_shift(scheduled_start, scheduled_end, actual_start, actual_end)

                # 4. Mostrar los resultados de la hoja física
            print("\n" + "="*30)
            print("REPORTE DE LA JORNADA")
            print(f"Total Horas: {results['total']:.2f}")
            print(f"Horas Extras: {results['overtime']:.2f}")
            print(f"Horas Nocturnas: {results['night']:.2f}")
            print(f"Horas Festivas: {results['holiday']:.2f}")
            print("="*30)
            print("\nCálculo completado.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


