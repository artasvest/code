import os
import sys

def check_file_exists_and_not_empty(filename):
    if not os.path.exists(filename):
        print(f"ОШИБКА: Файл '{filename}' не существует!")
        return False
    
    if os.path.getsize(filename) == 0:
        print(f"ОШИБКА: Файл '{filename}' пуст!")
        return False
    
    return True

def read_file_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return [line.rstrip('\n') for line in lines]
    except Exception as e:
        print(f"ОШИБКА при чтении файла '{filename}': {e}")
        return []

def write_file_lines(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write(line + '\n')
        print(f"Результат успешно сохранен в файл '{filename}'")
        return True
    except Exception as e:
        print(f"ОШИБКА при записи в файл '{filename}': {e}")
        return False

def display_file_content(filename, lines):
    print(f"\nСодержимое файла '{filename}':")
    for i, line in enumerate(lines, 1):
        print(f"  {i}: {line}")

def get_filename(prompt):
    while True:
        filename = input(prompt).strip()
        
        if not filename:
            print("ОШИБКА: Имя файла не может быть пустым!")
            continue
        
        if not filename.endswith('.txt'):
            filename += '.txt'
            print(f"Добавлено расширение .txt: '{filename}'")
        
        return filename

def validate_numbers(lines):
    for i, line in enumerate(lines, 1):
        try:
            float(line)
        except ValueError:
            print(f"ОШИБКА: Строка {i} ('{line}') не является числом!")
            return False
    return True

def main():
    print("\n--- ВВОД ДАННЫХ ---")
    filename = get_filename("Введите имя файла с числами: ")
    
    if not check_file_exists_and_not_empty(filename):
        print("Программа завершена.")
        return
    
    lines = read_file_lines(filename)
    
    if not lines:
        print("ОШИБКА: Не удалось прочитать содержимое файла.")
        print("Программа завершена.")
        return
    
    print("\n--- ИСХОДНЫЕ ДАННЫЕ ---")
    display_file_content(filename, lines)
    
    print("\n--- ПРОВЕРКА ДАННЫХ ---")
    if not validate_numbers(lines):
        print("Файл содержит некорректные данные. Программа завершена.")
        return
    
    print("Все строки являются числами. Проверка пройдена!")
    
    print("\n--- ОБРАБОТКА ДАННЫХ ---")
    odd_lines = []   
    even_lines = []  
    
    for i, line in enumerate(lines, 1):
        if i % 2 == 1:
            odd_lines.append(line)
            print(f"  Строка {i}: '{line}' -> в файл с НЕЧЕТНЫМИ")
        else:           
            even_lines.append(line)
            print(f"  Строка {i}: '{line}' -> в файл с ЧЕТНЫМИ")
    
    print(f"\nВсего строк в исходном файле: {len(lines)}")
    print(f"Строк с НЕЧЕТНЫМИ номерами: {len(odd_lines)}")
    print(f"Строк с ЧЕТНЫМИ номерами: {len(even_lines)}")
    
    print("\n--- РЕЗУЛЬТАТ ---")
    
    
    odd_file = "odd_lines.txt"
    if write_file_lines(odd_file, odd_lines):
        display_file_content(odd_file, odd_lines)
    
    print()
    
    even_file = "even_lines.txt"
    if write_file_lines(even_file, even_lines):
        display_file_content(even_file, even_lines)
    
    print("\nПрограмма успешно завершена!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        sys.exit(1)