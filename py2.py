def numlen(num):
    if len(str(num)) > 5:
        num = float(str(num)[:-1])
    return num

print("°C: ", end =' ')
fc = 15
f = 15
c = 15
while c < 30:
    c+= 1.5
    if c == 30:
        print(c)
    else:
        print(c, end=' ')
print("°F: ", end = ' ')

while fc < 30:
    fc+= 1.5
    f = fc*1.8+32
    if fc == 30:
        print(numlen(f))
    else:
        print(numlen(f), end=' ')