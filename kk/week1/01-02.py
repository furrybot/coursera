import sys
from utils import exit_if

exit_if(len(sys.argv) < 2, "You need to pass a number of steps as an argument")
steps_qty = sys.argv[1]
exit_if(not steps_qty.isdigit(), "The number of steps should be an integer number")
steps_qty = int(steps_qty)
exit_if(steps_qty == 0, "No staircase for you, smart ass")
exit_if(steps_qty > 200, "Just take an elevator")

for n in range(1, steps_qty + 1):
    print(' ' * (steps_qty - n) + '#' * n)
