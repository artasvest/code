import random
import time
from copy import deepcopy
from tabulate import tabulate


# ─────────────────────────────────────────────
#  АЛГОРИТМЫ СОРТИРОВКИ
# ─────────────────────────────────────────────

def insertion_sort(arr):
    """Прямое включение"""
    a = arr[:]
    iterations = comparisons = swaps = 0

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        iterations += 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key

    return a, iterations, comparisons, swaps

def selection_sort(arr):
    """Прямой выбор"""
    a = arr[:]
    n = len(a)
    iterations = comparisons = swaps = 0

    for i in range(n - 1):
        min_idx = i
        iterations += 1
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return a, iterations, comparisons, swaps


def bubble_sort(arr):
    """Прямой обмен (пузырёк)"""
    a = arr[:]
    n = len(a)
    iterations = comparisons = swaps = 0

    for i in range(n - 1):
        iterations += 1
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1

    return a, iterations, comparisons, swaps


def quick_sort(arr):
    """Быстрая сортировка Хоара — обёртка с подсчётом метрик"""
    a = arr[:]
    metrics = {"iterations": 0, "comparisons": 0, "swaps": 0}

    def _quick(a, low, high):
        if low < high:
            metrics["iterations"] += 1
            pivot = a[low]  # опорный элемент — первый
            i = low + 1
            j = high

            while True:
                while i <= high:
                    metrics["comparisons"] += 1
                    if a[i] <= pivot:
                        i += 1
                    else:
                        break
                while j > low:
                    metrics["comparisons"] += 1
                    if a[j] >= pivot:
                        j -= 1
                    else:
                        break
                if i >= j:
                    break
                a[i], a[j] = a[j], a[i]
                metrics["swaps"] += 1

            a[low], a[j] = a[j], a[low]
            if low != j:
                metrics["swaps"] += 1

            _quick(a, low, j - 1)
            _quick(a, j + 1, high)

    import sys
    sys.setrecursionlimit(100000)
    _quick(a, 0, len(a) - 1)
    return a, metrics["iterations"], metrics["comparisons"], metrics["swaps"]


# ─────────────────────────────────────────────
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

SORT_METHODS = {
    "Включение": insertion_sort,
    "Выбор": selection_sort,
    "Обмен": bubble_sort,
    "Хоар": quick_sort,
}


def measure(sort_fn, arr):
    """Запускает сортировку и замеряет время."""
    start = time.perf_counter()
    _, iters, comps, swps = sort_fn(arr)
    elapsed = time.perf_counter() - start
    return iters, comps, swps, elapsed


def make_partially_sorted(n, sorted_fraction):
    """
    Создаёт частично упорядоченный массив:
    первые sorted_fraction*N элементов отсортированы,
    остальные перемешаны.
    """
    full = sorted(random.randint(-10000, 10000) for _ in range(n))
    split = int(n * sorted_fraction)
    tail = full[split:]
    random.shuffle(tail)
    return full[:split] + tail


def get_array_states(n):
    """Возвращает словарь: тип → массив для заданного N."""
    base = [random.randint(-10000, 10000) for _ in range(n)]
    return {
        "Random":    base[:],
        "Sorted":    sorted(base),
        "Reversed":  sorted(base, reverse=True),
        "25%":       make_partially_sorted(n, 0.25),
        "50%":       make_partially_sorted(n, 0.50),
        "75%":       make_partially_sorted(n, 0.75),
    }


def input_int(prompt, min_val=1, max_val=None):
    """Ввод целого числа с проверкой."""
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"  Введите число >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"  Введите число <= {max_val}")
                continue
            return val
        except ValueError:
            print("  Ошибка: введите целое число.")


# ─────────────────────────────────────────────
#  ПУНКТ 1 — зависимость от размера массива
# ─────────────────────────────────────────────

def part1():
    print("\n" + "=" * 60)
    print("  ЧАСТЬ 1. Зависимость от размера массива")
    print("=" * 60)

    sizes = [20, 500, 1000, 3000, 5000, 10000]

    # Для каждого метода своя таблица
    for method_name, sort_fn in SORT_METHODS.items():
        print(f"\n--- Метод: {method_name} ---")
        rows = []
        for n in sizes:
            arr = [random.randint(-10000, 10000) for _ in range(n)]
            iters, comps, swps, t = measure(sort_fn, arr)
            rows.append([n, iters, comps, swps, f"{t:.6f}"])

        print(tabulate(
            rows,
            headers=["Размер", "Итерации", "Сравнения", "Перестановки", "Время (с)"],
            tablefmt="grid"
        ))


# ─────────────────────────────────────────────
#  ПУНКТ 2 — влияние начальной упорядоченности
# ─────────────────────────────────────────────

def part2():
    print("\n" + "=" * 60)
    print("  ЧАСТЬ 2. Влияние начальной упорядоченности")
    print("=" * 60)

    n = input_int("\nВведите размер массива N: ", min_val=2, max_val=100000)
    states = get_array_states(n)

    # Таблица: строки — типы, столбцы — методы
    # На пересечении: перестановки / время
    headers = ["Тип"] + [f"{m}\nПерест. / Время(с)" for m in SORT_METHODS]
    rows = []

    for state_name, arr in states.items():
        row = [state_name]
        for sort_fn in SORT_METHODS.values():
            _, _, swps, t = measure(sort_fn, arr[:])
            row.append(f"{swps} / {t:.6f}")
        rows.append(row)

    print(f"\nN = {n}\n")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


# ─────────────────────────────────────────────
#  ПУНКТ 3 — выводы
# ─────────────────────────────────────────────

def part3():
    print("\n" + "=" * 60)
    print("  ЧАСТЬ 3. Выводы")
    print("=" * 60)
    print("""
  Теоретическая сложность:
  ┌─────────────────┬────────────┬────────────┐
  │ Метод           │ В среднем  │ Худший     │
  ├─────────────────┼────────────┼────────────┤
  │ Прямое включение│  O(n²)     │  O(n²)     │
  │ Прямой выбор    │  O(n²)     │  O(n²)     │
  │ Прямой обмен    │  O(n²)     │  O(n²)     │
  │ Быстрая (Хоар)  │  O(n log n)│  O(n²)     │
  └─────────────────┴────────────┴────────────┘

  Что показывает практика:

  1. На случайных данных быстрая сортировка (Хоар) значительно
     опережает остальные — особенно заметно на массивах от 1000
     элементов, что соответствует теории O(n log n).

  2. Прямое включение работает лучше всего на почти отсортированных
     данных (25%, 50%, 75%, Sorted) — внутренний цикл почти не
     выполняется, приближаясь к O(n).

  3. Прямой выбор всегда делает ровно n*(n-1)/2 сравнений — не
     зависит от исходного порядка. Перестановок мало, но сравнений
     всегда много.

  4. Прямой обмен (пузырёк) — наихудший на обратно отсортированных
     данных: максимальное число и сравнений, и перестановок.

  5. На уже отсортированном массиве быстрая сортировка с опорным
     элементом = первый может деградировать до O(n²). В реальности
     используют случайный pivot или median-of-3.

  Итог: для общего случая — Хоар лучший. Для почти
  отсортированных данных — прямое включение конкурентоспособно.
""")


# ─────────────────────────────────────────────
#  ПУНКТ 4 — вариант: массив a1..a15,
#  сортировка по возрастанию |x| прямым включением
# ─────────────────────────────────────────────

def insertion_sort_abs(arr):
    """Прямое включение по абсолютному значению."""
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and abs(a[j]) > abs(key):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def part4():
    print("\n" + "=" * 60)
    print("  ЧАСТЬ 4. Вариант: сортировка по |x|, прямое включение")
    print("=" * 60)
    print("\nМассив из 15 элементов. Можно ввести вручную или сгенерировать.")

    choice = input("  [1] Ввести вручную  [2] Сгенерировать случайно: ").strip()

    if choice == "1":
        arr = []
        print("  Вводите числа по одному (всего 15):")
        for i in range(1, 16):
            val = input_int(f"  a[{i}]: ", min_val=-10**9, max_val=10**9)
            arr.append(val)
    else:
        arr = [random.randint(-100, 100) for _ in range(15)]
        print(f"  Сгенерирован массив: {arr}")

    sorted_arr = insertion_sort_abs(arr)

    print(f"\n  Исходный:       {arr}")
    print(f"  По возр. |x|:   {sorted_arr}")
    print(f"\n  Проверка (|x|): {[abs(x) for x in sorted_arr]}")


# ─────────────────────────────────────────────
#  ГЛАВНОЕ МЕНЮ
# ─────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════════════╗")
    print("║   Лабораторная работа: Сортировки    ║")
    print("╚══════════════════════════════════════╝")

    while True:
        print("\n  Выберите раздел:")
        print("  [1] Часть 1 — зависимость от размера массива")
        print("  [2] Часть 2 — влияние начальной упорядоченности")
        print("  [3] Часть 3 — выводы")
        print("  [4] Часть 4 — вариант (|x|, прямое включение)")
        print("  [0] Выход")

        choice = input("\n  Ваш выбор: ").strip()

        if choice == "1":
            part1()
        elif choice == "2":
            part2()
        elif choice == "3":
            part3()
        elif choice == "4":
            part4()
        elif choice == "0":
            print("\n  Выход. Пока!\n")
            break
        else:
            print("  Введите число от 0 до 4.")


if __name__ == "__main__":
    main()
