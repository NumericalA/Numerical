# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 22:30:09 2018

@author: hagar
"""

# input up till now is 
#1-list of x points (
    #adams bashforth: min: 2 points max: 5 points
    #adams moulton: 3 points 
    #adams: 4 points
    #milines: 4 points)
#2-list of y points (same as x)
#3-equation of the ode (string)
#4-The desired technique as a string {"Milne's","AdamsBashforth","AdamsMoulton","Adams"}
#5-list of x points to caluculate at 
#6-Approx Error ( we just do 5 itterations if it is large)

#output
#1-list of calculated ys
#2-list of Approx Error for each y
#3-Final approx error 

#function to call 
#PredictorCorrector(Xpoints,Ypoints,equation,technique,xs,ApproxError)

import matplotlib.pyplot as plt
from math import *
import numpy as np

class Point:
    def __init__(self,x,y,f):
        self.x=x
        self.y=y
        self.f=f
    
def GetF(x,y,equation):
    #should add all kind of functions that can be entered ,, cos ..... etc
    f=eval(equation,{'__builtins__': None},
    {'x': x,'y':y,'cos':cos,'sin':sin,'tan':tan,'acos':acos,'asin':asin,
     'atan':atan,'exp':exp,'pow':pow, 'sqrt': sqrt,'log10':log10,'log':log, #ln
     'fabs':fabs,'radians':radians,'degrees':degrees,'cosh':cosh,'acosh':acosh,
     'sinh':sinh,'asinh':asinh,'tanh':tanh,'atanh':atanh,'pi':pi,'e':e})
    return f
        
def MilnesPredictor(i,points,h):
    yp= points[i-4].y+h*(4/3)*(2*points[i-1].f -points[i-2].f + 2*points[i-3].f)
    return yp

def MilnesCorrector(i,points,h):
    yc= points[i-2].y + (h/3)*(points[i-2].f +4*points[i-1].f+ points[i].f )
    return yc
          
def Milnes (xpoints,ypoints,equation,evalxs,approxerror):
    itterations=5
    points=[]
    for i in range (len(xpoints)):
        points.append(Point(xpoints[i],ypoints[i],GetF(xpoints[i],ypoints[i],equation)))
    
    evalYs=[]
    approxErrors=[]
    for k in range (len(evalxs)):
        points.append(Point(evalxs[k],0,0))
        myNum = len(points)-1
        h= points[1].x-points[0].x
        points[myNum].y= MilnesPredictor(myNum,points,h)
        points[myNum].f=GetF(points[myNum].x , points[myNum].y ,equation)
        yPrev =points[myNum].y
        myApproxError=100
        i=0
        while i<itterations and myApproxError > approxerror:
            points[myNum].y=MilnesCorrector(myNum,points,h)
            myApproxError = abs((points[myNum].y-yPrev)/points[myNum].y)
#            print(k," ycorrected",points[myNum].y,"yPrev",yPrev,"Error",myApproxError)
            yPrev=points[myNum].y
            points[myNum].f=GetF(points[myNum].x , points[myNum].y ,equation)
            i+=1
        evalYs.append(points[myNum].y)
        approxErrors.append(myApproxError)
    return evalYs,approxErrors,max(approxErrors)


#assume x after the last point in table ##Error
def AdamsBashforth(xpoints,ypoints,equation,xs,error):
    points=[] #contains all given points
    f=[] #all calculated f(x,y)
    y0 = 0
    yCorrect = 0
    yPredict = 0
    iterations = 5
    #result
    evalYs=[] 
    approxErrors=[]
    #Table: 1st row: f, 2nd row: delta f ...
    matrix= np.zeros((5,6))

    #calculate f for the given points
    for i in range (len(xpoints)):
        tempF = GetF(xpoints[i],ypoints[i],equation)
        points.append(Point(xpoints[i],ypoints[i],tempF))
        f.append(tempF)
    for i in range (6-len(f)):
        f.append(0)

    #step
    h = abs(points[1].x-points[0].x)

    for l in range (0,len(xs)):
        #Fill the table with intial values 
        matrix[0] = f
        for j in range (1,len(xpoints)):
            for k in range (0,len(xpoints)-j):
                matrix[j][k] = matrix[j-1][k+1]-matrix[j-1][k]

        for i in range (iterations):
            yPrevious = yCorrect
            if i == 0:
                y0 = points[-1].y
                yPredict = y0+h*(points[-1].f+0.5*matrix[1][len(xpoints)-2]+(float(5)/12)*matrix[2][len(xpoints)-3]+ (float(3)/8)*matrix[3][len(xpoints)-4]+ (float(251)/720)*matrix[4][len(xpoints)-5])
                yPrevious = yPredict
                #put f(x,y) in the table
                matrix[0][len(xpoints)] = GetF(xs[l],yPredict,equation)
                
            #calculate all new values in the table
            for j in range (0,len(xpoints)-1):
                    matrix[j+1][len(xpoints)-j-1] = matrix[j][len(xpoints)-j]-matrix[j][len(xpoints)-j-1]

            yCorrect = y0+h*(matrix[0][len(xpoints)]-0.5*matrix[1][len(xpoints)-1]-(float(1)/12)*matrix[2][len(xpoints)-2]-(float(1)/24)*matrix[3][len(xpoints)-3]-(float(19)/720)*matrix[4][len(xpoints)-4])
            #check stopping criteria
            if (abs((yCorrect-yPrevious)/yCorrect*1.0))*100.0 <= error:
                break
            matrix[0][len(xpoints)] = GetF(xs[l],yCorrect,equation)
        #put calculated values in table
        xpoints.append(xs[l])
        ypoints.append(yCorrect)
        if len(xpoints) > 5:
            xpoints.pop(0)
            ypoints.pop(0)
            f.pop(0)
            f.append(GetF(xs[l],yCorrect,equation))
        else: 
            f[len(xpoints)-1]=(GetF(xs[l],yCorrect,equation))
        evalYs.append(yCorrect)
        approxErrors.append((abs((yCorrect-yPrevious)/yCorrect*1.0))*100.0)
    return evalYs,approxErrors,max(approxErrors)

def AdamsMoulton(xpoints,ypoints,equation,xvalues,stopping_criteria):
    h=xpoints[1]-xpoints[0]
    f=[]
    x=[]
    y=[]
    answers=[]
    errors=[]
    k=len(xpoints)
    for i in range(k):
        value=GetF(xpoints[i],ypoints[i],equation)
        f.append(value)
        x.append(xpoints[i])
        y.append(ypoints[i])

    for xval in xvalues:
        n=len(f)
        i=n-1
        predictor=y[i]+(h/12)*(23*f[i]-16*f[i-1]+5*f[i-2])
        corrector=predictor
        iteration=5
        approximate_error=100
        while ( iteration > 0 and approximate_error > stopping_criteria):
            prev_corrector=corrector
            corrector=y[i]+(h/12)*(5*corrector+8*f[i]-f[i-1])
            approximate_error=abs( (corrector- prev_corrector) / corrector )*100
            iteration-=1
        value=GetF(xval,corrector,equation) 
        f.append(value)
        x.append(xval)
        y.append(corrector)
        answers.append(corrector)
        errors.append(approximate_error)
    return answers , errors  , max(errors)  

def Adams(xpoints,ypoints,equation,xvalues,stopping_criteria):
    h=xpoints[1]-xpoints[0]
    f=[]
    x=[]
    y=[]
    answers=[]
    errors=[]
    k=len(xpoints)
    for i in range(k):
        value=GetF(xpoints[i],ypoints[i],equation)
        f.append(value)
        x.append(xpoints[i])
        y.append(ypoints[i])
            
    for xval in xvalues:
        n=len(f)
        i=n-1
        predictor=y[i]+(h/24)*(55*f[i]-59*f[i-1]+37*f[i-2]-9*f[i-3])
        corrector=predictor
        iteration=5
        approximate_error=100
        while ( iteration > 0 and approximate_error > stopping_criteria):
            prev_corrector=corrector
            corrector=y[i]+(h/24)*(9*corrector+19*f[i]-5*f[i-1]+f[i-2])
            approximate_error=abs( (corrector- prev_corrector) / corrector )*100
            iteration-=1
        value=GetF(xval,corrector,equation) 
        f.append(value)
        x.append(xval)
        y.append(corrector)
        answers.append(corrector)
        errors.append(approximate_error)
    return answers , errors , max(errors)  

def PredictorCorrector(Xpoints,Ypoints,equation,technique,xs,ApproxError):
    ys=[]
    errors=[]
    finalerror=0
    if technique=="Milne's":
        ys,errors,finalerror=Milnes(Xpoints,Ypoints,equation,xs,ApproxError) 
    elif technique=="AdamsBashforth":
        ys,errors,finalerror=AdamsBashforth(Xpoints,Ypoints,equation,xs,ApproxError)
    elif technique=="AdamsMoulton":
        ys , errors,finalerror =AdamsMoulton(Xpoints,Ypoints,equation,xs,ApproxError)
    elif technique=="Adams":
        ys, errors, finalerror = Adams(Xpoints,Ypoints,equation,xs,ApproxError)
    finalX=Xpoints+xs
    finalY=Ypoints+ys
    plt.plot(finalX,finalY)
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.title('The ODE')
    plt.show()

    return ys ,errors,finalerror

#xs=[-3,-2,-1,0]
#ys=[-4.547302,-2.30616,-0.3929953,2]
#x=[1]
#eq="4*exp(0.8*x) -0.5*y"
#xs=[-0.1,0,0.1,0.2]
#ys=[1.0047,1,1.0053,1.0229]
#x=[0.3,0.4]
#eq="x*y+x**2"
#xs=[-0.1,0,0.1,0.2]
#ys=[1.0047,1,1.0053,1.0229]
#x=0.3
#eq="x*y+x**2"
#approx=0.00000000005
#out ,errors,error =PredictorCorrector(xs,ys,eq,"Milne's",x,approx)
#print (" Milne's      ",out,errors,error)
#out ,errors,error =PredictorCorrector(xs,ys,eq,"Adams",x,approx)
#print (" Adams        ",out,errors,error)
#out ,errors,error = PredictorCorrector(xs,ys,eq,"AdamsMoulton",x,approx)
#print (" AdamsMoulton       ",out,errors,error)
#out ,errors,error = PredictorCorrector(xs,ys,eq,"AdamsBashforth",x,approx)
#print (" AdamsBashforth       ",out,errors,error)