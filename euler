import numpy as np
import matplotlib.pyplot as plt
from sympy import integrate,Symbol
from math import *

dict_to_list = lambda some_dict:[ some_dict[key] for key in sorted(some_dict.keys())]
round_list = lambda some_list,digits : [round(elem,digits) for elem in some_list]
euler = lambda y,vars,h,eq : y + eval(eq,globals(),vars.copy())*h

def integrator(x,ys,h,xend,eqs):
    while(1):
        if(xend -x <h):
            h = xend -x
        new_ys = ys.copy()
        for i in range(len(eqs)):
            variables = ys.copy();variables['x'] =x #use the prev x not the curr one
            new_y = euler(ys['y{0}'.format(i)],variables,h,eqs[i])
            new_ys['y{0}'.format(i)] = new_y
        ys.update(new_ys) 
        x=x+h    
        if(x>= xend):
            return x

def test_equations(eqs,variables):
    variables['x']=1
    try:
        for eq in eqs:
            eval(eq,globals(),variables)
    except:
        print("wrong equations or intial variables")
        exit()


def read_input():
    n = int(input("Enter number of equations: "))
    print("Enter equations as python format ex: -2*x**3 + exp(x)-20*x + 8.5")
    print("Note That y0 is the name of variable 2 equations ex:\n 1-> dy0/dx = 3*x*y1 + 2*y0\n 2-> dy1/dx = x + y1 + y0\n")
    eqs = [input("eq{0}: dy{0}/dx = ".format(i)) for i in range(n)]
    print("\nIntial values for variables")
    ys = {} # Intial values for variables
    for i in range(n):
        try:
            ys['y{0}'.format(i)] = float(input("y{0}_intial = ".format(i)))
        except: pass
    test_equations(eqs,ys.copy()) # testing input of equations
    xi = float(input("x_initial = "))
    xf = float(input("x_final = "))
    dx = float(input("calculation step size h = "))
    xout = input("show output every step (for default = h press Enter) = ")
    xout = float(xout) if xout != '' else dx
    intial_conditions=ys.copy();intial_conditions['x']=xi
    return eqs,ys,xi,xf,dx,xout

def plot_points(points):
    legends = []
    for i in range(len(points[0])-1):
        plt.scatter(points[:,0],points[:,i+1])
        legends.append('y'+str(i))
    plt.legend(legends, loc='upper left')
    plt.show()


def main():
    #TODO replace read_input with argument variables or with gui
    eqs,ysi,xi,xf,h,xout = read_input() # i for initial and f for final and out for output_interval
    result_table = [xi] + dict_to_list(ysi)
    points = []
    points.append(round_list([xi] + [ ysi['y'+str(j)] for j in range(len(eqs))],5))
    while(1):
        xend = xi + xout
        if(xend > xf):
            xend = xf
        xi = integrator(xi,ysi,h,xend,eqs) # ysi dictionary is passed by ref
        new_row = round_list( [xi] + dict_to_list(ysi),5)
        points.append(new_row)
        if(xi>=xf):
            break

    points=np.array(points)
    print(points)
    plot_points(points)
        
if __name__ == "__main__":
    main()

'''
Test Case one equation
1
-2*x**3+12*x**2-20*x+8.5
1
0
4
.5
'''
'''
Test Case two equation
2
-.5*y0
4-.3*y1-.1*y0
4
6
0
2
.5
'''
