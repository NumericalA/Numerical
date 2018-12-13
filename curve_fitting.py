import numpy as np
def curve_fitting(x,y,degree=1):
    """
    calculates the coefficients to fit (x, y) using a polynomial
    of the specified degree
    :param x the input data points
    :param y the output data points
    :return the coefficients of the polynomial that best fits (x, y)
    """
    x=np.array(x)
    y=np.array(y)
    #x=x[:degree+1]
    #y=y[:degree+1]
    if(degree > x.shape[0]):
        print("inputs values not enough for degree")
        return 0
    powers=np.ones([x.shape[0],degree+1])
    help_vectors=np.array([range(0,degree+1)])
    powers=(powers*help_vectors).T
    x=x**powers

    y=np.dot(x,y)
    #invx=np.linalg.inv(np.dot(x,x.T))
    #coeff=np.dot(invx,y)
    coeff = np.linalg.solve(np.dot(x,x.T), y)
    return coeff

# some tests
def fun(x):
    return x ** 3 + 3 * x * x - 24 * x + 2

def fun1(x):
    return x ** 4 + x ** 3 + x ** 2 + x  ** 1 +6565656

x=[1,2,3,4,5]
y=[1 + 3,8 + 3,27 + 3,64 + 3,125 + 3]
print(curve_fitting(x,y,degree=9))

x = list(range(100))
y = list(map(fun, x))
print(curve_fitting(x,y,degree=4))

x = list(range(100))
y = list(map(fun1, x))
print(curve_fitting(x,y,degree=4))
