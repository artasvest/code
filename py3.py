def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_valid_float_input(prompt):
    while True:
        value = input(prompt)
        if is_number(value):
            return float(value)
        else:
            print("Пожалуйста, введите число!")

def get_valid_int_input(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
        else:
            print("Пожалуйста, введите целое положительное число!")

A = get_valid_float_input("Введите число A: ")
N = get_valid_int_input("Введите число N: ")

if N <= 0:
    print("N должно быть больше чем 0")
else:
    print("Все целые степени числа A от 1 до N:")
    for i in range(1, N + 1):
        print(round((A ** i),15))