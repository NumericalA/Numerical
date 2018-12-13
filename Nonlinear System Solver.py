#Team 6
##Inputs :
#    1. EquationsStrings: Array of equations' strings.
#    2. InitialValues: Initial values of the variables (default: ones).
#    3. StoppingError: The stopping approximate relative error (default: 0).
#Outputs:
#    1. Numpy array of the results values.
#    2. Numpy array of last approximate relative error.
#Notes
#    We assume variables' names (X0, X1, ...., Xn-1)
#Team 5

from sympy import Symbol, Matrix
from sympy.parsing.sympy_parser import parse_expr
from numpy import array

def subsMat(Mat, N, Symbols, Values):
    RMat = Mat
    for i in range(N):
        RMat = RMat.subs(Symbols[i],Values[i]).evalf()
    return RMat

def NonLinearSolver(EquationsStrings, InitialValues = -1, StoppingError = 0):
    NumberOfVariables = len(EquationsStrings)
    Symbols = Matrix([0] * NumberOfVariables)
    for i in range(NumberOfVariables):
        Symbols[i] = Symbol("X" + str(i))

    Equations = Matrix([0] * NumberOfVariables)
    for i in range(NumberOfVariables):
        Equations[i] = parse_expr(EquationsStrings[i])

    V = Matrix([1] * NumberOfVariables)
    if InitialValues != -1:
        for i in range(NumberOfVariables):
            V[i] = parse_expr(input("Enter The Initial Value For '" + str(Symbols[i]) + "': "))

    J = Matrix([[parse_expr("x")]*NumberOfVariables]*NumberOfVariables)
    for i in range(NumberOfVariables):
        J[:,i] = Equations[:,0].diff(Symbols[i])

    RError = [0] * NumberOfVariables
    for i in range(5):
        NewV = V - subsMat(J.inv(), NumberOfVariables, Symbols, V) * subsMat(Equations, NumberOfVariables, Symbols, V)
        numpyNewV = array(NewV)
        numpyV = array(V)
        if abs( numpyNewV.min() ) != 0:
            RError = abs( (numpyV - numpyNewV) / numpyNewV  )
            if max(RError) * 100 <= StoppingError:
                V = NewV
                break
        V = NewV
    return array(V), RError * 100