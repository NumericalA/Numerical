import numpy as np

def interpolateNewton(x,y,order=5,x0 = None, appError = 1e-8,numDigits = 4):
    """
    6 inputs: 2 lists necessary and 4 has default:
    list (or numpy array) :x :the input x values for all points
    list (or numpy array) :y :the input y values for all points (length of y should equal length of x)
    integer :order :number of itertations before the stoping (by default 5) 
    float :x0 :the required x to get the value of the function (by default None)
    float :appError :approximate error to stop evaluating (by default 10^(-8))
    integer :numDigits :number of digits after floating point (by default 4) 

    3 outputs:
    string :sout :the function writen in string (e.g 0.2x + 0.4(x-1) * (x-2) ... )
    if given x0:
        float :sumOut :the value of the function at x0
    if given x0 and error can be determined (number of points more than the order):
        float :error :the value of the approximate error at x0
    """
    x = np.round(np.array(x,dtype=np.float64),numDigits)
    y = np.round(np.array(y,dtype=np.float64),numDigits)

    givenX = True
    if len(x) != len(y):
        raise ValueError("Length of X doesn't equals length of Y")

    if order > len(y):
        raise ValueError('Order is more than number of the point')
    
    if x0 == None:
        x0 = 0
        givenX = False
    elif x0 > np.max(x) or x0 < np.min(x):
        raise ValueError('Requierd x is out of the given x range')
    else:
        diffX = x - x0
        diffIndx = diffX.argsort()
        x = x[diffIndx]
        y = y[diffIndx]

    fout = np.zeros((len(y),len(y)),dtype=np.float64)
    fout[:,0] = y

    for j in range(1,len(y)):
        for i in range(len(y)-j):
            fout[i][j] = ( fout[i+1][j-1] - fout[i][j-1] ) / ( x[i+j] - x[i] )

    sout = '{1:.{0}f} '.format(numDigits,y[0])
    sumOut = y[0]
    for i in range(1,order):
        termout = ' + {1:.{0}f}'.format(numDigits,fout[0][i])
        term = fout[0][i]
        for j in range(i):
            termout += ' * ( x - {1:.{0}f} )'.format(numDigits,x[j])
            term *= (x0 - x[j])
        if (givenX and term < appError):
            return sout,sumOut,term
        
        sout += termout 
        sumOut += term

    if givenX:
        if order < len(y):
            error = fout[0][order]
            for j in range(order):
                error *= (x0 - x[j])
            return sout,sumOut,error
        else:
            return sout,sumOut
    return sout


def interpolationLagrange(x,y,x0 = None,numDigits = 4):
    """
    4 inputs: 2 lists necessary and 2 has default:
    list (or numpy array) :x :the input x values for all points
    list (or numpy array) :y :the input y values for all points (length of y should equal length of x)
    float :x0 :the required x to get the value of the function (by default None)
    integer :numDigits :number of digits after floating point (by default 4) 

    2 outputs:
    string :sout :the function writen in string (e.g 0.2x + 0.4(x-1) * (x-2) ... )
    if given x0:
        float :sumOut :the value of the function at x0
    """

    x = np.round(np.array(x,dtype=np.float64),numDigits)
    y = np.round(np.array(y,dtype=np.float64),numDigits)
    givenX = True

    if len(x) != len(y):
        raise ValueError("Length of X doesn't equals length of Y")
    
    if x0 == None:
        x0 = 0
        givenX = False
    elif x0 > np.max(x) or x0 < np.min(x):
        raise ValueError('Requierd x is out of the given x range')


    sout = ''
    sumOut = 0
    for i in range(len(y)):
        product = y[i]
        upS = ''
        down = y[i]
        for j in range(len(y)):
            if i != j:
                product *= (x0 - x[j])/(x[i] - x[j])
                upS += '( X - {1:.{0}f} )'.format(numDigits,x[j])
                down /= (x[i] - x[j])
        sout += ' + {0} * {2:.{1}f}'.format(upS,numDigits,down)
        sumOut += product 
    sout = sout[3:]

    if givenX:
            return sout,sumOut
    return sout
