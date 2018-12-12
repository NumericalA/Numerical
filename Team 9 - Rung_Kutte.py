from math import *


### Group 9
### Ahmed Maher
### Ibrahim Mahmoud
### Mohmamed Emad
### Reem Ashraf Salah
class Runge_kutte:
    def __init__(self,x0,y0,x,h,function,equation):
        self.x0=x0
        self.y0=y0
        self.h=h
        self.ya=self.y0
        self.function=function
        self.x=x    # set variable x in order to calculate exact value of y
        y= y0   # set variable x in order to calculate exact value of y
        self.ye=eval(equation) # y exact
        self.error=0
        self.k1 = 0.000000
        self.k2 = 0.000000
        self.k3 = 0.000000
        self.k4 = 0.000000

    def set(self):
        x = self.x0
        y = self.y0
        self.k1=eval(self.function)
        x += self.h/2.00000
        y += (self.h)*(self.k1)/2.000000
        self.k2 = eval(self.function)
        y = (self.y0) + (self.h)*(self.k2)/2.00000
        self.k3 = eval(self.function)
        x += (self.h)/2.00000000
        y = self.y0 + (self.k3 * self.h)
        self.k4 = eval(self.function)
    def calculate(self):
        if self.ye != 0:
            self.error = abs((self.ye - self.ya)/self.ye) * 100.0
        else:
            print("error calculating exact value")
    def solve(self):
        self.set()
        self.ya += (self.h /6.00000) * (self.k1 + 2.0000 * self.k2 + 2.0000 * self.k3 + self.k4)
        self.calculate()

def Runge_kutte_ODE(x0,y0,x,h,function,equation):
    r = Runge_kutte(x0,y0,x,h,function,equation)  # Make instance
    r.solve()  #solve the equation
    return r

func = input("input the function: ") # O.D.E
func2 = input(" input exact function: ") # Equation to Calculate the Exact Value
x0 = float (input("Enter x0: "))
y0 = float (input("Enter y0: "))
x = float (input("Enter x: "))
h = float (input("Enter h: "))
r = Runge_kutte_ODE(x0,y0,x,h,func,func2)
print("y = ",r.ya)
print("relative true error = ",r.error," % ")

#input number (6)
# string function       string equation       x0 y0 x and h
# output number (2)
# ya (y appromiate )    error (raltive true error)

#
# 2 testcases:
#     1- function
#         4*(exp(0.8*x))-0.5 * y
#     exact equation:
#         5* (exp(0.8*x))-0.25 * (y**2)
#     x0 = 0   y0 = 2   x=0   h = 0.5
#
#     2- function
#         x*y+(x**2)
#     exact equation:
#         (x**2)*y/2+(x**3)/3
# x0 = 0      y0 = 1      x = 0.1      h = 0.1