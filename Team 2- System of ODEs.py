#Team 2 
#Name	    	Sec.    B.N.	Email
#Osama Nabih 	1	    10	    NabihThe4th@gmail.com
#Bassel Mostafa	1	    15	    bassel.mks97@gmail.com
#Omar Wagih	    2	    10	    o.wagih.ow@gmail.com
#Walid Ashraf 	2	    29	    WalidAshraf423@gmail.com

# Inputs are string array of functions of y', z', w' and they must be in this order, array of initial values x,y,z,w, step size, error in percentage,
# heunOrRunge (for heun pass 1, anything else is runge), number of iterations which are by default 5.
# Output is a array of numbers at the last step, and a matplotlib graph

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sympy.parsing.sympy_parser import (parse_expr,standard_transformations, implicit_multiplication_application)
from sympy import *


# In[49]:


def solveSystemsHeun(Equations,initialArrays,h,error, numOfIterations = 5):
    Functions = []
    for i in range(len(Equations)):
        Functions.append(parse_expr(Equations[i],transformations=(standard_transformations +(implicit_multiplication_application,))))
    NextArrays = initialArrays 
    DummyArray = NextArrays
    AllOutputs = []
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
        AllOutputs.append(NextArrays)
        fals = True
        for i in range(1,len(NextArrays)):
            if NextArrays[i] != 0:
                if abs(NextArrays[i]-DummyArray[i])/NextArrays[i] * 100 > error:
                    fals = False
        if fals == True:
            break;
    return np.array(AllOutputs);
def solveSystems(Equations,initialArrays, h, error, numOfIterations = 5):
    Functions = []
    AllOutputs = []
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
        AllOutputs.append(NextArrays)
        for i in range(1,len(NextArrays)):
            if NextArrays[i] != 0:
                if abs(NextArrays[i]-DummyArray[i])/NextArrays[i] * 100 > error:
                    fals = False
        if fals == True:
            break;
    return np.array(AllOutputs);


# In[56]:


def SolveODE(Equations,InitialValues,h,error,HeunOrRunge,numOfIterations=5):
    Initial = len(InitialValues)
    Answer = []
    colors = ['mo','ro','go']
    while len(InitialValues) < 4:
        InitialValues.append(0)
    if HeunOrRunge == 1:
        Answer = solveSystemsHeun(Equations,InitialValues,h,error,numOfIterations)[:,0:Initial]
    else:
        Answer = solveSystems(Equations,InitialValues,h,error,numOfIterations)[:,0:Initial]
    for i in Answer:
        for j in range(1,len(i)):
            plt.plot(i[0], i[j],colors[j-1])
    plt.xlabel('X')
    redPatch = mpatches.Patch(color='red', label='Z values')
    magentaPatch = mpatches.Patch(color='magenta', label='Y values')
    greenPatch = mpatches.Patch(color='green', label='W values')
    plt.legend(handles=[magentaPatch,redPatch,greenPatch][0:Initial-1])
    return Answer[-1]
