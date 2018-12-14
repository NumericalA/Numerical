
'''
5 inputs: 3 necessary , 2 optional
	X : the value to calculate the derivative at.
	table : contain 2 rows, the first for x values , and the second for y values
	errorOrder: the order of h (stopping criteria)
	f(optional): a string to contain the function, (default value "" , if she will insert a table not the function)
	h(optional): insert the max h if she will insert a function string (f), (not needed for table)

2 outputs: can ignore first output by _ , output = Rich( pla pla pla)
	- bool answer = true if there is no error, false if has error
	- string = "error", if not valid data inserted
	or float value contains the answer
'''

# answer is bool, if it false x will contain an error string , else if true x will contain the final answer
#answer , x=Rich(X = 1.6, table = [[0.8,1,1.2,1.4,1.6,1.8,2,2.2,2.4] , [1.3,1.7,2.3,3.2,4.7,6.2,8.1,9.2,9.8]],errorOrder = 6)
#answer , x= Rich(X = 0, table = [],errorOrder=16,f = "1/(1+x)",h = 0.1)

from sympy import*
from sympy.parsing.sympy_parser import parse_expr
import numpy as np 

def CD(x2,x1,h):
    return (x2-x1)/(2*h)

def Rich(X,table,errorOrder=6 , f="",h=-1):
    answer = False
    if(errorOrder%2):
        errorOrder += 1
    if(f!=""):
        x = Symbol("x")
        try:
            f = parse_expr(f , evaluate =False) 
            int(f.evalf(subs={x:1}))
        except:
           
           return  answer , "syntax error in the funciton "
        
       
        diffValues = [];
        arrOfHs = [h/(2**i) for i in range( int(errorOrder/2))]
        for i in arrOfHs:
            value = CD(f.evalf(subs={x:X+i}) , f.evalf(subs={x:X-i}),i)
            diffValues.append(value)
        diffValues = np.array(diffValues).astype(float)
        for i in range(len(diffValues)-1):
            diffValues =((4**(i+1))*diffValues[1:] - diffValues[:len(diffValues)-1])/(4**(i+1) -1)
            #print(diffValues)
        answer = True
        return answer , float("{0:.9f}".format(diffValues[-1]))      # get last element cause we beging with hmax so we want last element in column 
    else:
        table = np.array(table).astype(float)
        table = table[:,table[0,:].argsort()]
        TargetIndex = -1;
        for i in range(table.shape[1]):
            if(X == table[0,i]):
                TargetIndex = i;
        if(TargetIndex==-1):
            return  answer , "The element is not found in the table :("
        
        arrOfHs = []
        for i in range( TargetIndex+1 ,table.shape[1] ):
            temp = []
            h = table[0 , i] - X 
            NoStop = True
            while NoStop:
                if (float("{0:.9f}".format(X+h)) in table[0] )and (float("{0:.9f}".format(X-h)) in table[0]):
                    #temp.insert(0,float("{0:.9f}".format(h)))
                    temp.append(float("{0:.9f}".format(h)))
                    h=float("{0:.9f}".format(h))
                    h*=2
                else:
                    NoStop = False
            
            if(len(temp) > len(arrOfHs)):
                arrOfHs = temp.copy()
            
            if(len(arrOfHs)>=int(errorOrder/2)):
                break
        if(len(arrOfHs) == 0):
            return answer , "there is no x+h to computer the derivatives "
        
        if(len(arrOfHs) >int(errorOrder/2) ):
            arrOfHs = arrOfHs[0:int(errorOrder/2)]
        
       
        arrOfHs.reverse() # to make hmax first element so that same code works 
        #print(arrOfHs)
        diffValues = [];
        for i in arrOfHs:
            index1 = np.argmax(table[0] == float("{0:.9f}".format(X+i)))
            index2 = np.argmax(table[0] == float("{0:.9f}".format(X-i)))
            value = CD(table[1 , index1]  ,table[1 , index2] ,i)
            #print(X-i ,table[1 , index1] ,table[1 , index2] , value)
            diffValues.append(value)
        #print(diffValues)
        
        diffValues = np.array(diffValues).astype(float)
        for i in range(len(diffValues)-1):
            diffValues =((4**(i+1))*diffValues[1:] - diffValues[:len(diffValues)-1])/(4**(i+1) -1)
            #print(diffValues)
        answer = True
        return answer , float("{0:.9f}".format(diffValues[0]))
