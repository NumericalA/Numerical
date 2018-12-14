# Team 1
# Ahmad Khaled          - S. 01 BN. 03
# Zeinab Rabie          - S. 01 BN. 26
# Sara Maher            - S. 02 BN. 28
# Abdelrahman Mohamed   - S. 02 BN. 03
# Trapezoidal, Simpson 1/3 and Simpson 3/8 Integration.
import numpy as np
import sympy
import types
from sympy.utilities.lambdify import lambdify, implemented_function


# returns a table [x, y] from f(x), a, b, n
def get_table(f, a, b, n):
    h = (b - a) / n
    x = np.arange(a, b, h)
    if (x.size < n + 1):
        x = np.append(x, b)
    if (callable(f)):
        fx = f(x)
    else:
        fx = np.array(f)
    if (fx.size != n + 1):
        raise ValueError("Error in Table Dimensions! x.shape != fx.shape")
    return x, fx


# get a lambda function from user input
def get_function():
    func = input("Enter a function of x: ")
    f = sympy.sympify(func)
    x = sympy.symbols('x')
    fx = lambdify(x, f)
    return fx


# parameters:
# f: either a table (with f[i] = f(x_i), the x_i are n samples between a, b) or a function.
# a: start of interval.
# b: end of interval.
# n: no. of samples points.
def trapezoidal(f, a, b, n):
    h = (b - a) / n
    x, fx = get_table(f, a, b, n)
    second_der = np.gradient(np.gradient(fx))
    error = - np.power((b - a), 3) * np.max(second_der) / (12 * n * n)  # Very approximate!
    fx[1:n] = fx[1:n] * 2
    I = np.sum(fx) * h / 2
    return I, np.abs(error)


# parameters:
# f: either a table (with f[i] = f(x_i), the x_i are n samples between a, b) or a function.
# a: start of interval.
# b: end of interval.
# n: no. of samples points.
def simpson_3_8(f, a, b, n=3):
    if n != 3:
        raise ValueError("Can only apply Sympson's 3/8 rule to n=3.")
    h = (b - a) / n
    x, fx = get_table(f, a, b, n)
    ans = (3.0 * h / 8) * (fx[0] + 3 * (fx[1] + fx[2]) + fx[3])
    f4_intg = np.gradient(np.gradient(np.gradient(fx)))
    err = abs((-3 * (h**5) / 80) * (2 * np.max(f4_intg)))
    return ans, err


# Calculate error using difference table
def simpson_1_3_error(table, n, a, b):
    delta_f_4 = 0
    v = n - 3  # number of delta_f_4 that i can calc according to num of points=>(n + 1) - 5 +1
    for i in range(0, v):
        delta_f_4 += table[i + 4] - 4 * table[i + 3] + 6 * table[i + 2] - 4 * table[i + 1] + table[i]
    delta_f_4 /= 5  # taking average
    E = (b - a) * delta_f_4 / 180
    return E


# Calculate error with direct differentiation
def simpson1_3_error2(y, a, b, h):
    x = Symbol('x')
    z = diff(y, x, 4)
    g = lambdify(x, z, 'numpy')
    delta_f_4 = g(a)
    E = (b - a) * (h ** 4) * delta_f_4 / 180
    return E


# parameters:
# f: either a table (with f[i] = f(x_i), the x_i are n samples between a, b) or a function.
# a: start of interval.
# b: end of interval.
# n: no. of samples points.
def simpson_1_3(f, a, b, n):
    h = (b - a) / n
    x, table = get_table(f, a, b, n)
    I = table[0] + table[n]
    odds = (k for k in range(1, n) if k % 2)
    for i in odds:
        I += (table[i] * 4)  # table[i][1] => f(xi) corresponding to xi
    evens = (k for k in range(2, n) if k % 2 == 0)
    for i in evens:
        I += (table[i] * 2)
    I *= h / 3
    error = simpson_1_3_error(table, n, a, b)
    return I, error


def test_integrals():
    def g(x):
        return 0.2 + 25 * x - 200 * x * x + 675 * np.power(x, 3) - 900 * np.power(x, 4) + 400 * np.power(x, 5)
    print(trapezoidal(g, 0, 1, 5))
    print(simpson_1_3(g, 0, 1, 5))
    print(simpson_3_8(g, 0, 1, 3))
    f = np.array([1, 2, 3, 4])
    print(trapezoidal(f, 0, 1, 3))
    print(simpson_3_8(f, 0, 1, 3))
    f = get_function()
    print(trapezoidal(f, 0, 1, 3))
    print(simpson_3_8(f, 0, 1, 3))
    print(simpson_1_3(f, 0, 1, 3))


test_integrals()
