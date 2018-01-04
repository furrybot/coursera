digit_string = input('Enter number to sum: ')
result = 0

for digit in digit_string:
    result += int(digit)

print(result)