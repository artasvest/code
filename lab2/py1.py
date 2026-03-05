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

def main():
    print("\n--- ВВОД ДАННЫХ ---")
    file1 = get_filename("Введите имя ПЕРВОГО файла (будет расширен): ")
    file2 = get_filename("Введите имя ВТОРОГО файла (источник строк): ")
    
    if not check_file_exists_and_not_empty(file1):
        print("Программа завершена.")
        return
    
    if not check_file_exists_and_not_empty(file2):
        print("Программа завершена.")
        return
    
    lines1 = read_file_lines(file1)
    lines2 = read_file_lines(file2)
    
    if not lines1 or not lines2:
        print("ОШИБКА: Не удалось прочитать содержимое файлов.")
        print("Программа завершена.")
        return
    
    print("\n--- ИСХОДНЫЕ ДАННЫЕ ---")
    display_file_content(file1, lines1)
    display_file_content(file2, lines2)
    
    print("\n--- ОБРАБОТКА ДАННЫХ ---")
    result_lines = []
    
    len1 = len(lines1)
    len2 = len(lines2)
    
    print(f"Длина первого файла: {len1} строк")
    print(f"Длина второго файла: {len2} строк")
    
    min_len = min(len1, len2)
    
    for i in range(min_len):
        combined = lines1[i] + " " + lines2[i]
        result_lines.append(combined)
        print(f"  Строка {i+1}: '{lines1[i]}' + '{lines2[i]}' -> '{combined}'")
    
    if len1 > len2:
        result_lines.extend(lines1[min_len:])
     
    
    elif len2 > len1:
        result_lines.extend(lines2[min_len:])
        
    
    print("\n--- РЕЗУЛЬТАТ ---")
    output_file = "result_combined.txt"
    if write_file_lines(output_file, result_lines):
        display_file_content(output_file, result_lines)
    
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