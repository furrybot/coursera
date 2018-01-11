import sys
from utils import exit_if, quad_equation

exit_if(len(sys.argv) < 4, "You need to pass a, b, c")

a = b = c = 0
try:
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])
except ValueError:
    exit_if(True, "Numbers only please")

result = quad_equation(a, b, c)
if result is None:
    print("No real solutions")
elif isinstance(result, tuple):
    for x in result:
        print(round(x))
elif isinstance(result, float):
    print(round(result))
else:
    print("I have no idea what I'm doing")
