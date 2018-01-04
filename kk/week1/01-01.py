import sys
from utils import exit_if

exit_if(len(sys.argv) < 2, "You need to pass a string of numbers as an argument")
input_string = sys.argv[1]
exit_if(not input_string.isdigit(), "The input string must only contain numbers")

total = 0
for char in input_string:
    total += int(char)

print(total)
