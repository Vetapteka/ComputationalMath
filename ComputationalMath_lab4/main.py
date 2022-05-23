import numpy as np
import math
import matplotlib.pyplot as plt


def print_delim(n):
    print("+%s+" % ("-"*n))


def print_menu():
    n = 40
    print_delim(n)
    print("|%s|" % "integration".center(n))
    print_delim(n)
    print("|%s|" % "Select function".center(n))
    print_delim(n)
    print("|%s|" % "1. x^5 + 7x^4 - 34x^2 + 2".center(n))
    print("|%s|" % "2.  sin(x) + x^4 ".center(n))
    print("|%s|" % "3. x^2 * cos(x) - 3x".center(n))
    print_delim(n)


def get_function(choice):
    choice = int(choice)
    match choice:
        case 1:
            return lambda x: x**5 + 7*x**4 - 34*x**2 + 2
        case 2:
            return lambda x: x* np.sin(x) + x**4
        case 3:
            return lambda x: np.cos(x)*x**2 - 3*x


def get_number(message, a, b):
    while True:
        try:
            value = np.double(input(message))
            if (value < a or value > b):
                raise ValueError
            return value
        except ValueError:
            print("You must enter an integer in the range [", a, "; ", b, "]")


# для функции возвращает набор разностей (х0) (х0, х1) (х0, х1, х2)
def get_rasnost(X, Y):
    count_points = X.size
    ans = np.zeros((int(count_points), int(count_points)))

    for i in range(count_points):
        ans[i][0] = Y[i]

    count_str = count_points - 1
    added_index = 0

    for i in range(1, count_points):
        added_index += 1
        for j in range(count_str):
            ans[j][i] = (ans[j+1][i-1] - ans[j][i-1]) / \
                (X[j+added_index]-X[j])
        count_str -= 1

    return ans[0]


def get_polynom(generated_x, rasnost, val):
    numder_points = rasnost.size
    x_arg = np.ones(numder_points)

    for i in range(1, numder_points):
        x_arg[i] = x_arg[i-1]*(val - generated_x[i-1])

    ans = rasnost[0]
    for i in range(1, numder_points):
        ans += rasnost[i]*(x_arg[i])

    return ans


def main():

    h = 0.1
    print_menu()
    choice = get_number("\nenter function number: ", 1, 3)
    func = get_function(choice)

    print("--------------------")
    print("Enter the interval:")
    left = get_number("\nleft: ", -100, 100)
    right = get_number("right: ", left, 100)

    # количество известных для нас точек
    count_points = int(get_number(
        "\nEnter number of points: ", 2, math.ceil((right-left+1)/h)))

    generated_x = np.linspace(left, right, count_points)

    y_for_generated_x = []
    for i in range(count_points):
        y_for_generated_x.append(func(generated_x[i]))

    

    rasnost = get_rasnost(generated_x, y_for_generated_x)

    X = np.arange(left, right + h, h)
    Y = np.arange(left, right + h, h)

    for i in range(X.size):
        Y[i] = get_polynom(generated_x, rasnost, X[i])

    plt.plot(X, func(X), label="y = f(x)")
    plt.plot(X, Y, label="interpolation")
    plt.plot(generated_x, y_for_generated_x, "ro")
    plt.grid(True)
    plt.legend()
    plt.show()


main()
