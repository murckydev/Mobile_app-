from src.logic.calculations import calculate_overtime

def main():
    while True:
        user_input = input("Enter total hours worked (or 'q' to quit): ")
        
        if user_input.lower() == 'q':
            return # El usuario decidió salir
            
        try:
            total = float(user_input)
            break

        except ValueError:
            print("Error: Please enter a valid number.")

    # Aquí sigue el resto del programa...
    normal, extra = calculate_overtime(total)
    print(f"Normal: {normal}, Extra: {extra}")

if __name__ == "__main__":
    # Solo se ejecuta si corres "python src/main.py"
    main()



