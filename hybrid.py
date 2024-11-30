import numpy as np
import math
import os
import sys
inf = math.inf
eps = sys.float_info.epsilon
counter = 0

def sign(num):
    '''returns sign of a number'''
    if num >= 0:
        return '+'
    if num < 0:
        return '-'

def bisect(func, xl, xu, es=eps, maxit=1000000):
    """Uses bisection method to estimate a root of func(x).
    The method is iterated maxit (default = 20) times.
    input:
    func = name of the function
    x1 = lower guess
    xu = upper guess
    OUTPUT:
    xm = root estimate
    or
    error message if initial guess do not bracket solution """
    global counter
    xold = xl
    iter = 0
    counter = counter + 1
    if func(xl) * func(xu) > 0:
        print('solution not bracketed')
        return xl
    for i in range(maxit):
        iter = iter + 1
        xm = (xl + xu) / 2
        error = abs((xm - xold) / xm)
        if error < es:
            break
        if func(xm) * func(xl) > 0:
            xl = xm
            xold = xm
        else:
            xu = xm
            xold = xm
    return xm

def reg_fals(func, xl, xu, es=eps, maxit=10000):
    """finding point c using method of false position"""
    if func(xl) * func(xu) > 0:
        print('solution not bracketed')
        return xl
    xvals = []
    for i in range(maxit):
        xnew = xl - func(xl) * ((xu - xl) / (func(xu) - func(xl)))  # new x value, should get close to x value where f(x) is zero
        fxnew = func(xnew)  # should get super close to zero
        xvals.append(xnew)
        ea = abs((xnew - xl) / xnew)
        if ea < es:
            break
        elif func(xnew) <= 0:
            xl = xnew
        elif func(xnew) >= 0:
            xu = xnew
    c = xnew
    return c

def secant(fun, xold, xolder, es=eps, maxit=50):
    '''secant method '''
    error = 100
    iterations = 0
    while error >= es and iterations < maxit:
        iterations = iterations + 1
        xnew = xold - (fun(xold) * (xold - xolder)) / (fun(xold) - fun(xolder))
        error = abs((xnew - xold) / xnew)
        xolder = xold
        xold = xnew
    return (xnew, iterations)

def zero(a, b, f):
    global counter
    fun = f
    # find c
    c = reg_fals(fun, a, b, maxit=1)
    counter = counter + 1
    if c == a or c == b:
        return (c, counter)
    # perform secant using a, b, c, and d rules.
    if c == a:
        return (c, counter)
    elif c <= a or c >= b:  # special condition for c is line is really flat, do bisection and then start over.
        if c <= a:
            c = a + eps * abs(a)
            bisectres = bisect(fun, a, b, maxit=1)
        elif c >= b:
            c = b - eps * abs(b)
            bisectres = bisect(fun, a, b, maxit=1)
        if sign(bisectres) == sign(a):
            return zero(bisectres, b, fun)
        else:
            return zero(a, b, bisectres, fun)
    elif sign(fun(a)) == sign(fun(c)):  # if signs match for f(a) and f(c)
        secantit = secant(fun, a, c, maxit=1)
        counter = counter + 1
        d = secantit[0]
        iter_secant = secantit[1]
    elif sign(f(a)) != sign(f(c)):  # different sign
        secantit = secant(fun, b, c, maxit=1)
        counter = counter + 1
        d = secantit[0]
        iter_secant = secantit[1]
    else:
        return "something wrong, failed both cases"

    # Check if d falls outside of interval a, b
    if d < a or d > b:
        if d < a:
            bisectit = bisect(fun, d, c)
            return bisectit
        elif d > b:
            bisectit = bisect(fun, a, d)
            return bisectit

    elif abs(c - d) >= (1 / 2) * (b - a):
        bisect_it = bisect(fun, a, b, maxit=1)
        if sign(bisect_it) == sign(a):
            return zero(bisect_it, b, fun)
        else:
            return zero(a, b, bisect_it, fun)
    else:
        if d == c:
            return c, counter
        if d > c:
            if abs(a - b) > abs(d - c):
                bis = bisect(fun, c, d, maxit=1)
            else:
                bis = bisect(fun, a, b, maxit=1)
            if sign(bis) == d:
                result = zero(c, bis, fun)  # start over
                return result
            else:
                result = zero(bis, d, fun)  # start over
                return result
        elif c > d:
            if abs(a - b) > abs(c - d):
                bis = bisect(fun, d, c, maxit=1)
            else:
                bis = bisect(fun, a, b, maxit=1)
            if sign(bis) == sign(c):
                result = zero(d, bis, fun)  # start over
                return result
            else:
                result = zero(bis, c, fun)  # start over
                return result

# Test Functions
def fun(x):
    """function"""
    result = math.exp(-x) - x
    return result

def trigfun(x):
    """trig function"""
    result = x * math.cos(x) + math.sin(x)
    return result

# Main Code

# Running the tests
zeroedtrig = zero(2, 3, trigfun)
print(f'value of root for xcos(x) + sin(x) between bound [2, 3] is: {zeroedtrig[0]} \n Number of Iterations: {zeroedtrig[1]}')

zeroedtrig2 = zero(4, 5, trigfun)
if isinstance(zeroedtrig2, tuple):  # Check if result is valid
    print(f'value of root for xcos(x) + sin(x) between bound [4, 5]: {zeroedtrig2[0]} \n Number of Iterations: {zeroedtrig2[1] - zeroedtrig[1]}')
else:
    print("Error: " + zeroedtrig2)  # Handle the error message

zeroed2 = zero(0, 1, fun)
if isinstance(zeroed2, tuple):  # Check if result is valid
    print(f'value of root for e^(-x) - x between bound [0, 1]: {zeroed2[0]} \n Number of Iterations: {zeroed2[1] - zeroedtrig2[1]}')
else:
    print("Error: " + zeroed2)  # Handle the error message
