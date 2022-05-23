import math
import string
from numpy import array, double, zeros
import scipy
from sympy import *
from array import *

import numpy as np


def print_delim(n):
    print("+%s+" % ("-"*n))


def print_menu_equation():
    n = 40
    print_delim(n)
    print("|%s|" % "nonlinear equations".center(n))
    print_delim(n)
    print("|%s|" % "Select function".center(n))
    print_delim(n)
    print("|%s|" % "1. sin(x)".center(n))
    print("|%s|" % "2. ln(x)".center(n))
    print("|%s|" % "3. x^3 + 4x - 3".center(n))
    print_delim(n)


def print_menu_system():
    n = 40
    print_delim(n)
    print("|%s|" % "system nonlinear equations".center(n))
    print_delim(n)
    print("|%s|" % "Select system".center(n))
    print_delim(n)
    a = int(n/2)
    print("|%s|%s|" % ("4.".center(a), "5.".center(a-1)))
    print_delim(n)
    print("|%s|%s|" % ("10x + x*y^3 = 9".center(a), "sin(x) + y^3 = 1".center(a-1)))
    print("|%s|%s|" % ("x*y + x*y*y = 6".center(a), "x^2 + y^2 = 8".center(a-1)))
    print_delim(n)


def get_number(message, a, b):
    while True:
        try:
            value = double(input(message))
            if (value < a or value > b):
                raise ValueError
            return value
        except ValueError:
            print("You must enter an integer in the range [", a, "; ", b, "]")


def get_function(choice):
    choice = int(choice)
    match choice:
        case 1:
            return math.sin
        case 2:
            return math.log2
        case 3:
            return lambda x: x*x*x + 4*x - 3
        case 4:
            x, y = symbols('x, y')
            return ('10*x+x*y*y*y-9', 'x*y + x*y*y - 6')
        case 5:
            x, y = symbols('x, y')
            return('2*x*x*x-y*y-1', 'x*y*y*y-y-4')


def check_interval(foo, a, b):
    return foo(a)*foo(b) < 0


def bisection_method(foo, a, b, accuracy):

    if(not check_interval(foo, a, b)):
        raise ValueError
    accuracy = int(-math.log10(accuracy))
    while(True):
        mid = (a+b)/2
        if(round(foo(mid), accuracy) == 0):
            return mid
        if (check_interval(foo, a, mid)):
            b = mid
        else:
            a = mid


def tangent_method(foo, a, b, accuracy):
    from scipy.misc import derivative
    h = 0

    if (derivative(foo, b, 1.0, 2) > 0):
        x = b
    elif (derivative(foo, a, 1.0, 2) > 0):
        x = a
    else:
        raise ValueError

    while(True):
        x -= h
        h = foo(x)/derivative(foo, x)

        if(x < a or x > b):
            raise ValueError            

        if (abs(h) < accuracy):
            return x


def newton_method(foo_vector, x0, x1, accuracy):

    len = 2
    s = (len, len)

    x_vector = [x0, x1]
    h = []

    # матрица производных для якобиана
    dx_matrix = [[], []]
    jac = np.zeros(s)

    x, y = symbols('x, y')
    symb = (x, y)

    for i in range(len):
        for j in range(len):
            dx_matrix[i].append(
                lambdify(symb, sympify(diff(foo_vector[i], symb[j]))))

    while (True):
        x_prev = x_vector.copy()
        fx_vector = []

        for i in range(len):
            # посчитали значения f(x)
            fx_vector.append(lambdify(symb, sympify(foo_vector[i]))(
                x_vector[0], x_vector[1]))
            for j in range(len):
                # посчитали значение матрицы якоби
                jac[i][j] = dx_matrix[i][j](
                    x_vector[0], x_vector[1])

        if (np.linalg.det(jac) == 0):
            raise ValueError

        x_vector -= 0.1*(np.dot(np.linalg.inv(jac), (fx_vector)))

        dx = x_vector - x_prev
        Dx =  max(abs(dx[0]), abs(dx[1]))

        if(Dx < accuracy):
            return x_vector


def main():
    try:
        print_menu_equation()
        foo = get_function(get_number("\nenter function number: ", 1, 3))
        left = get_number("\nenter left border: ", -100, 100)
        right = get_number("enter right border: ", left, 100)
        accuracy = get_number("\nenter the accuracy: ",  0.000001, 0.1)

        print("\nbisection method answer: ",
                bisection_method(foo, left, right, accuracy))
        print("tangent_method answer: ", tangent_method(
            foo, left, right, accuracy))

        print_menu_system()
        foo_vector = get_function(get_number(
            "\nenter function number: ", 4, 5))
        x0 = get_number("\nenter x0: ", -100, 100)
        y0 = get_number("enter y0: ", -100, 100)
        accuracy = get_number("\nenter the accuracy: ",  0.000001, 0.1)

        answer = newton_method(foo_vector, x0, y0, accuracy)

        print("\nnewton method answer: ")
        print("x = %f" % answer[0])
        print("y = %f" % answer[1])

    except ValueError:
        print("invalid interval: no solution or metod does not support this interval")


main()
