steps_amount = int(input('Enter number of steps: '))
space_char, hash_char = ' ', '#'
loop_step = 0

while loop_step < steps_amount:
    loop_step += 1
    result = space_char * (steps_amount - loop_step)
    result += hash_char * loop_step
    print(result)
