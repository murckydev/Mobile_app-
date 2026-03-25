from src.logic.calculations import calculate_overtime

def main():
    # Todo mi flujo de usuario vive aquí, todo esta encapsulado
    user_input = input("Enter total hours worked: ")
    total = float(user_input) 
    normal, extra = calculate_overtime(total)
    print(f"Normal Hours: {normal}, Overtime: {extra}")

if __name__ == "__main__":
    # Solo se ejecuta si corres "python src/main.py"
    main()



