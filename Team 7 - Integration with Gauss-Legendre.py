''' 
* no. of inputs: 4
    - 1 string (f) [the function which will be integrated]
    - 3 numbers
        - n [count of points in Gauss formula which may have value of 2 or 3 only]
        - 2 limits of integration which may have values from -1e9 (negative infinity) to 1e9 (infinity)         
* no. of outputs: 1 [Value of Integration]
'''

'''
Team members:
1- Omar Mohammed Mohammed 
2- Walid Mohammed
3- Yahia Ali
'''

from math import *

def solve(symF, polyorder, a, b, flag = 0):
    xs = None
    Ws = None
    if polyorder == 2:
        xs = [-0.57735027, 0.57735027]
        Ws = [1,1]
    elif polyorder == 3:
        Ws = [0.55555556, 0.88888889, 0.55555556]
        xs = [-0.77459667,0,0.77459667]
    if not xs or not Ws:
        print("Error! Inappropriate number of points for gauss formula!")
        return "error"
    ans = 0.0
    for i in range (len(Ws)):
        expr = ((a+b) * 0.5) + ((b-a) * 0.5 * xs[i])
        ans += (b-a)*0.5*Ws[i]*calculate(symF, expr, flag)
    return ans

def calculate(f, n, flag):
    if flag:
        x = 1/n
        return eval(f) * (-1/(n*n))
    else:
        x = n
        return eval(f)

def Integration_GaussLegendre(f, n, a, b):
    f = str(f)  # you should make type casting if you enter sympy string
    sign = 1
    if a > b: 
        a, b = b, a
        sign = -1
    if a == -1e9: # negative infinity
        if b == 0:
            ans = solve(f, n, 0, -1, flag = 1) + solve(f, n, -1, 0)
        elif b == 1e9:
            ans = solve(f, n, 0, 1, flag = 1) + solve(f, n, 1, 0, flag = 1)
        else:
            ans = solve(f, n, 0, 1/b, flag = 1)
    elif a == 0:
        if b == 1e9:
            ans = solve(f, n, 0, 1) + solve(f, n, 1, 0, flag = 1)
        else:
            ans = solve(f, n, a, b)
    else:
        if b == 1e9:  # infinity
            ans = solve(f, n, 1/a, 0, flag = 1)
        else:
            ans = solve(f, n, a, b)
    return ans * sign

'''
A test case:

equation = "1/(x**2 + 4)"  
n = 2
a = 2
b = 1e9
print (Integration_GaussLegendre(equation, n, a, b))
'''