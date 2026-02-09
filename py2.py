sequence = input("Введите последовательность симоволов: ")

while not sequence:
    print("Последовательность не может быть пустой!")
    sequence = input("Введите последовательность симоволов: ")

letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
punctuatuion = set('.,!&;:-"\'()[]{}')

allowed = letters | punctuatuion

result = {char for char in sequence if char in allowed}
if not result:
    print("В последовательности нет ни одной буквы от A до Z или знака препинания.")
else:
    print("Множество подходящих символов: ", result)
    print("Количество подходящих символов: ", len(result))
