import sys
import math as math

if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    delta = (b**2) - (4*a*c)
    solution1 = (-b-math.sqrt(delta))/(2*a)
    solution2 = (-b+math.sqrt(delta))/(2*a)
    print(int(solution1))
    print(int(solution2))