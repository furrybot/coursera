import sys

def count_sum_numbers(digit_string):
    sum = 0
    for letter in digit_string:
        sum += int(letter)
    return sum

if __name__ == "__main__":
    digit_string = sys.argv[1]
    print(count_sum_numbers(digit_string))