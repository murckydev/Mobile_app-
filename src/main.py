from datetime import datetime
from src.logic.calculations import ShiftCalculator

def get_datetime_input(prompt):
    while True:
        data = input(prompt)
        if data.lower() == 'q': return 'q'
        try:
            return datetime.strptime(data, "%Y-%m-%d %I:%M %p")
        except ValueError:
            print(" Formato inválido. Use: AAAA-MM-DD HH:MM AM/PM")

def main():
    calc = ShiftCalculator()
    print("SISTEMA MURCKY - CÁLCULO DE TURNOS")

    start = get_datetime_input("Entrada (AAAA-MM-DD HH:MM AM/PM) o 'q': ")
    if start == 'q': return
    
    end = get_datetime_input("Salida (AAAA-MM-DD HH:MM AM/PM) o 'q': ")
    if end == 'q': return

    report = calc.calculate_shift(start, end)

    print(f"\nRESULTADOS:")
    print(f"- Total: {report['total']:.2f} hrs")
    print(f"- Noche: {report['night']:.2f} hrs")
    print(f"- Extra: {report['overtime']:.2f} hrs")

if __name__ == "__main__":
    main()


