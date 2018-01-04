import math

a = int(input('a: '))
b = int(input('b: '))
c = int(input('c: '))

d = b*b - 4*a*c

print('d = ', d)

if d < 0:
    print('sorry :(')
elif d == 0:
    x = int((-b + math.sqrt(d)) / 2 * a)
    print(x)
else:
    x1 = int((-b + math.sqrt(d)) / 2*a)
    x2 = int((-b - math.sqrt(d)) / 2*a)

    print(x1, x2)
