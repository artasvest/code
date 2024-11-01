def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_valid_input(prompt):
    while True:
        value = input(prompt)
        if is_number(value):
            return float(value)
        else:
            print("Пожалуйста, введите число!")


x = get_valid_input("Введите число x: ")
e = get_valid_input("Введите число e: ")

if x == 0 or x == 1:
    print("x не может быть равен 0 или 1")
elif e <= 0 or e >= 1:
    print("e должно быть больше нуля и меньше единицы")
else:
    elem = 0
    summa = 0
    previous_sum = 0 
    
    for step in range(1, 101):
        elem = 1 / x**step
        summa += elem
        
        if abs(summa - previous_sum) < e:
            break
        
        previous_sum = summa
    
    print(f"Сумма ряда с точностью e = {e}: {summa}")