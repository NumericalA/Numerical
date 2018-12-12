# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 19:46:24 2018

@author: hagar
"""

# input up till now is 
#1-list of x points (4 points)
#2-list of y points (4 points)
#3-equation of the ode (string)
#4-The desired technique as a string
#5-The point to caluculate at 
#6-Approx Error with default 1 so we just do 5 itterations if not given

#output
#1-y
#2-ApproxError
from milnes import Milnes 
from adams import Adams
from adamsmoulton import AdamsMoulton

def PredictorCorrector(Xpoints,Ypoints,equation,x,technique,ApproxError=1):
    output=0
    error=0
    if technique=="Milne's":
        output=Milnes(Xpoints,Ypoints,equation,x,ApproxError) 
    elif technique=="AdamsBashforth":
        output=2
    elif technique=="AdamsMoulton":
        output , error =AdamsMoulton(Xpoints,Ypoints,equation,x,ApproxError)
    elif technique=="Adams":
        output, error = Adams(Xpoints,Ypoints,equation,x,ApproxError)
    return output ,error

        


xs=[-3,-2,-1,0]
ys=[-4.547302,-2.30616,-0.3929953,2]
x=1
itt=5
eq="4*exp(0.8*x) -0.5*y"
eq2="x*y+x**2"
approx=0.0005
out ,error =PredictorCorrector(xs,ys,eq,x,"Milne's",approx)
print (" Milne's      ",out,error)
out ,error =PredictorCorrector(xs,ys,eq,x,"Adams",approx)
print (" Adams        ",out,error)
out ,error =PredictorCorrector(xs,ys,eq,x,"AdamsMoulton",approx)
print (" AdamsMoulton ",out,error)