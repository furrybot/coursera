import sys

def get_stairs(num_steps):
    return [" "*(num_steps - x) + "#"*x for x in range(1,num_steps + 1)]

if __name__ == "__main__":
    num_steps = sys.argv[1]
    stairs = get_stairs(int(num_steps))
    for line in stairs:
        print(line)