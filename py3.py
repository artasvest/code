print("Введите элементы множеств через пробел: ")
A_input = input("Множество А: ").strip()
B_input = input("Множество B: ").strip()
C_input = input("Множество C: ").strip()
if not A_input or not B_input or not C_input:
    print("Все множества должны содержать элементы!")
    exit()

A = set(A_input.split())
B = set(B_input.split())
C = set(C_input.split())

print(f"\nA = {A}")
print(f"B = {B}")
print(f"C = {C}")

if not (B.issubset(A) and A.issubset(C)):
    print("Ошибка: не выполнется условие B вл A вл С")
else:
    X = (C - A) | B
    print("Множество X: ", X)