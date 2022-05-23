import numpy as np
import math

from sympy import Symbol, diff, lambdify, sympify


def print_delim(n):
    print("+%s+" % ("-"*n))


def print_menu():
    n = 40
    print_delim(n)
    print("|%s|" % "integration".center(n))
    print_delim(n)
    print("|%s|" % "Select function".center(n))
    print_delim(n)
    print("|%s|" % "1. sin(3*x/2)+1/2".center(n))
    print("|%s|" % "2. sin(x)/x".center(n))
    print("|%s|" % "3. 1/x".center(n))
    print_delim(n)


def get_number(message, a, b):
    while True:
        try:
            value = np.double(input(message))
            if (value < a or value > b):
                raise ValueError
            return value
        except ValueError:
            print("You must enter an integer in the range [", a, "; ", b, "]")


def get_function(choice):
    choice = int(choice)
    match choice:
        case 1:
            return 'sin(3*x/2)+1/2'
        case 2:
            return 'sin(x)/x'
        case 3:
            return '1/x'


def get_discontinuity(choice):
    choice = int(choice)
    match choice:
        case 1:
            return []
        case 2:
            return [0]
        case 3:
            return [0]


def root_exist(foo, a, b):
    return foo(a)*foo(b) < 0


def bisection_method(foo, a, b, accuracy):

    if(not root_exist(foo, a, b)):
        return a
    accuracy = int(-math.log10(accuracy))
    while(True):
        mid = (a+b)/2
        if(round(foo(mid), accuracy) == 0):
            return mid
        if (root_exist(foo, a, mid)):
            b = mid
        else:
            a = mid


def get_n(func, left, right, accuracy):
    x = Symbol('x')
    # четвертая производная
    dif = sympify(diff(func, x))
    dif = sympify(diff(dif, x))
    dif = sympify(diff(dif, x))
    dif = sympify(diff(dif, x))
    if(sympify(dif) == sympify('0')):
        return 10
    dif_lambda = lambdify(x, dif)

    # проверяем на концах отрезка
    max_in_interval = max(abs(dif_lambda(left)), abs(dif_lambda(right)))

    # ищем экстремумы
    # для этого производная = 0 ищем корни
    dif_5 = sympify(diff(dif, x))
    dif_5_lambda = lambdify(x, dif_5)

    root = bisection_method(dif_5_lambda, left, right, accuracy)
    max_in_interval = max(max_in_interval, dif_lambda(root))

    n = math.ceil((max_in_interval*(right-left)**5/2880.0/accuracy)**0.25)
    return n


def method_Simpson(func, left, right, accuracy):
    n = get_n(func, left, right, accuracy)
    h = (right - left)/2/n
    x = Symbol('x')
    func_lambda = lambdify(x, sympify(func))
    answer = func_lambda(left) + func_lambda(left+2*n*h)

    for i in range(1, 2*n):
        xi = left+i*h
        if(i % 2 == 0):
            answer += 2*func_lambda(xi)
        else:
            answer += 4*func_lambda(xi)
    return answer * (h/3.0)


def get_solution(func, discontinuity, left, right, accuracy):
    count = len(discontinuity)
    sum = 0
    
    while(count):
        count -= 1
        point = discontinuity[count]
        if(point == right):
            right -=accuracy;
        if(point == left):
            left +=accuracy;
        if(point < right and point > left):
            sum += method_Simpson(func, point + accuracy, right, accuracy)
            right = point-accuracy

    sum += method_Simpson(func, left, right, accuracy)
    return sum


def main():
    print_menu()
    choice = get_number("\nenter function number: ", 1, 3)
    func = get_function(choice)
    discontinuity = get_discontinuity(choice)

    print("\nenter interval")
    left = get_number("\nleft: ", -100, 100)
    right = get_number("right: ", -100, 100)
    accuracy = get_number("enter accuracy: ",  0.000001, 0.1)

    print("result: ", get_solution(func, discontinuity, left, right, accuracy))

main()
