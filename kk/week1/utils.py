# It's like an assert, but softer
def exit_if(condition, message):
    if condition:
        print(message)
        exit()


def quad_equation(a, b, c):
    def common_root(x):
        return (-b + x) / (2 * a)
    d = b ** 2 - 4 * a * c
    if d > 0:
        sqrt = (b ** 2 - 4 * a * c) ** 0.5
        return common_root(sqrt), common_root(-sqrt)
    elif d == 0:
        return - b / (2 * a)
    else:
        return None
