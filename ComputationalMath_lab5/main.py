import numpy as np
import matplotlib.pyplot as plt
import math


def print_delim(n):
    print("+%s+" % ("-"*n))


def print_menu():
    n = 40
    print_delim(n)
    print("|%s|" % "integration".center(n))
    print_delim(n)
    print("|%s|" % "Select function".center(n))
    print_delim(n)
    print("|%s|" % "1.   y' = x^3 + x + 3*y/x".center(n))
    print("|%s|" % "2.   y' = xsin(x) + y/x".center(n))
    print_delim(n)


def get_function(choice):
    choice = int(choice)
    match choice:
        case 1:
            return lambda x, y: x**3 + x + 3*y/x
        case 2:
            return lambda x, y: x*math.sin(x) + y/x


def get_solution_func(choice):
    choice = int(choice)
    match choice:
        case 1:
            return lambda x, x0, y0: x**4 - x**2 + 2*abs(x)**3 * ((y0 - x0**4 + x**2)/abs(x)**3)
        case 2:
            return lambda x, x0, y0: x*(y0/x0+math.cos(x0) - math.cos(x))


def get_number(message, a, b):
    while True:
        try:
            value = np.double(input(message))
            if (value < a or value > b):
                raise ValueError
            return value
        except ValueError:
            print("You must enter an integer in the range [", a, "; ", b, "]")


def EulerMethod(X, h, y0, func):
    Y = np.zeros(X.size)
    Y[0] = y0
    for i in range(1, Y.size, 1):
        Y[i] = Y[i-1] + h * func(X[i-1], Y[i-1])
    return Y


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

    print_menu()
    choice = get_number("\nenter function number: ", 1, 2)
    func = get_function(choice)
    x0 = get_number('\nEnter x0: ', -100, 100)
    y0 = get_number('Enter y0: ', -100, 100)
    right = get_number('\nEnter right boundary of the interval: ', x0+1, 100)
    h = get_number('\nEnter a step: ', 0.001,  (right-x0)/2)

    X = np.arange(x0, right+h, h)
    Y = EulerMethod(X, h, y0, func)

    X_after_inter = np.arange(x0, right, 0.01)
    Y_after_inter = np.arange(x0, right, 0.01)
    Y_solution = np.arange(x0, right, 0.01)

    solution_func = get_solution_func(choice)

    rasnost = get_rasnost(X, Y)
    for i in range(X_after_inter.size):
        Y_after_inter[i] = get_polynom(X, rasnost, X_after_inter[i])
        Y_solution[i] = solution_func(X_after_inter[i], x0, y0)

    plt.plot(X_after_inter, Y_after_inter, label="interpol")
    plt.plot(X_after_inter, Y_solution, label="analitic solution")
    plt.plot(X, Y, label="Euler method")
    plt.plot(X, Y, "ro")

    plt.legend()
    plt.grid(True)
    plt.show()


main()
