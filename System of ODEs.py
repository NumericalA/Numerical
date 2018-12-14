#Team 2 
#Name	    	Sec.    B.N.	Email
#Osama Nabih 	1	    10	    NabihThe4th@gmail.com
#Bassel Mostafa	1	    15	    bassel.mks97@gmail.com
#Omar Wagih	    2	    10	    o.wagih.ow@gmail.com
#Walid Ashraf 	2	    29	    WalidAshraf423@gmail.com

#Number of inputs 11
#Inputs 1 to 3
#array of functions of y', z', w' and they must be in this order
#Inputs 4 to 7
#array of initial values x,y,z,w
#Input 8
#step size
#Input 9
#error in percentage
#Input 10
#heunOrRunge (for heun pass 1, anything else is runge)
#Input 11
#number of iterations, which are by default 5.

#Number of outputs 2
#Output 1
#graph
#Output 2
#answer at last step


# coding: utf-8

# In[1]:


import numpy as np
from sympy.parsing.sympy_parser import (parse_expr,standard_transformations, implicit_multiplication_application)
from sympy import *


# In[45]:





# In[110]:


def solveSystemsHeun(Equations,initialArrays,h,error, numOfIterations = 5):
    Functions = []
    for i in range(len(Equations)):
        Functions.append(parse_expr(Equations[i],transformations=(standard_transformations +(implicit_multiplication_application,))))
    NextArrays = initialArrays 
    DummyArray = NextArrays
    c = initialArrays[0]
    numA = 0
    x = Symbol("x")
    y = Symbol("y")
    z = Symbol("z")
    w = Symbol("w")
    while(True and numA != numOfIterations):
        numA += 1
        OldArrays = NextArrays
        NextArrays = []
        YNots = []
        Ys = []
        YNots.append(OldArrays[0])
        for i in range(len(Functions)):
            YNots.append( round(OldArrays[i+1] + Functions[i].evalf(subs={x:OldArrays[0]
                                                                          ,y:OldArrays[1],z:OldArrays[2],w:OldArrays[3]})*h,4))
        while len(YNots) < 4:
            YNots.append(0)
        NextArrays.append(round(c+h,4))
        for i in range(len(Functions)):
            NextArrays.append(round(OldArrays[i+1] + (Functions[i].evalf(subs={x:OldArrays[0],y:OldArrays[1],z:OldArrays[2],w:OldArrays[3]})
                                                + Functions[i].evalf(subs={x:YNots[0],y:YNots[1],z:YNots[2],w:YNots[3]}))/2 * h,4))
        while len(NextArrays) < 4:
            NextArrays.append(0)
        c = round(c+h,4)
        fals = True
        for i in range(1,len(NextArrays)):
            if NextArrays[i] != 0:
                if abs(NextArrays[i]-DummyArray[i])/NextArrays[i] * 100 > error:
                    fals = False
        if fals == True:
            break;
    return NextArrays;
def solveSystems(Equations,initialArrays, h, error, numOfIterations = 5):
    Functions = []
    for i in range(len(Equations)):
        Functions.append(parse_expr(Equations[i],transformations=(standard_transformations +(implicit_multiplication_application,))))
    NextArrays = initialArrays 
    DummyArray = NextArrays
    c = h
    numA = 0
    x = Symbol("x")
    y = Symbol("y")
    z = Symbol("z")
    w = Symbol("w")
    while(True and numA != numOfIterations):
        numA += 1
        DummyArray = NextArrays
        OldArrays = NextArrays
        NextArrays = []
        K1 = []
        K2 = [] 
        K3 = []
        K4 = []
        K1.append(0)
        for i in range(len(Functions)):
            K1.append(round(Functions[i].evalf(subs={x:DummyArray[0],y:DummyArray[1],z:DummyArray[2], w:DummyArray[3]}),4))
        while len(K1) < 4:
            K1.append(0)
        K2.append(0)
        for i in range(len(Functions)):
            K2.append(round(Functions[i].evalf(subs={x:DummyArray[0]+ (h/2),y:DummyArray[1]+(K1[1]*h/2)
                                                     ,z:DummyArray[2]+(K1[2]*h/2), w:DummyArray[3]+(K1[3]*h/2)}),4))
        while len(K2) < 4:
            K2.append(0)
        K3.append(0)
        for i in range(len(Functions)):
            K3.append(round(Functions[i].evalf(subs={x:DummyArray[0]+ (h/2),y:DummyArray[1]+(K2[1]*h/2)
                                                     ,z:DummyArray[2]+(K2[2]*h/2),w:DummyArray[3]+(K2[3]*h/2)}),4))
        while len(K3) < 4:
            K3.append(0)
        K4.append(0)
        for i in range(len(Functions)):
            K4.append(round(Functions[i].evalf(subs={x:DummyArray[0]+ (h),y:DummyArray[1]+(K3[1]*h)
                                                     ,z:DummyArray[2]+(K3[2]*h),w:DummyArray[3]+(K3[3]*h)}),4))
        while len(K4) < 4:
            K4.append(0)
        for i in range(len(DummyArray)):
            NextArrays.append(round(DummyArray[i] + h/6 * (K1[i] + 2*(K2[i]+K3[i]) + K4[i]),4))
        NextArrays[0] += h
        fals = True
        NextArrays = np.round(NextArrays,4)
        for i in range(1,len(NextArrays)):
            if NextArrays[i] != 0:
                if abs(NextArrays[i]-DummyArray[i])/NextArrays[i] * 100 > error:
                    fals = False
        if fals == True:
            return NextArrays;
    return NextArrays;


# In[114]:


def SolveODE(Equations,InitialValues,h,error,HeunOrRunge,numOfIterations=5):
    Initial = len(InitialValues)
    while len(InitialValues) < 4:
        InitialValues.append(0)
    if HeunOrRunge == 1:
        return solveSystemsHeun(Equations,InitialValues,h,error,numOfIterations)[0:Initial]
    else:
        return solveSystems(Equations,InitialValues,h,error,numOfIterations)[0:Initial]
print(SolveODE(["z","6+y-5*x*z"],[1,1,-1],0.2,0.001,1,1))
print(SolveODE(["z","6+y-5*x*z"],[1,1,-1],0.2,0.001,2,1))

