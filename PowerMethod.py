import numpy as np


def powerMethod(A, initial=None, epsilon=None, numberOfIterations=100, minEigen=False):
    """
    A function to calculate largest eigen value and eigen vector of a matrix, and approximate relative error

    Args: 
            A (numpy array): Matrix to get eigen value/vector (size n*n)
            initial (numpy array): Vector used as initial guess of eigen vector (size 1*n)
            epsilon (float): Stopping criteria at which eigen value is considered converged
            numberOfIterations (int): Number of iterations untill stopping
            minEigen (boolean): Calculate smallest eigen value or largest

    Returns:
            eigenValue (numpy float)
            eigenVector (numpy array)
            error (numpy float)
    Raises:
            TypeError
            ValueError

    """

    ##Validate input##

    # negative number of iterations
    if numberOfIterations <= 0:
        raise ValueError("Number of iterations should be positive")

    # invalid type of matrix A
    if not isinstance(A, np.ndarray):
        raise TypeError("A should be of type numpy.ndarray")

    # invalid type of vector initial
    if (initial is not None) and (not isinstance(A, np.ndarray)):
        raise TypeError("initial should be of type numpy.ndarray")

    # check initial is 1d array
    if (initial is not None) and (initial.ndim != 1):
        raise TypeError("initial should be 1D array")

    # number of iterations is not integer
    if not isinstance(numberOfIterations, int):
        raise TypeError("Number of iterations should be integer")

    #matrix is not square
    if A.shape[0] != A.shape[1]:
        raise TypeError("Matrix should be square")

    # check size of initial vector
    if (initial is not None) and (initial.shape[0] != A.shape[1]):
        raise TypeError("Length of initial vector should match size of matrix")

    ##Calculate eigen pair##

    # dimension of matrix
    n = A.shape[0]

    if minEigen:
        try:
            A = np.linalg.inv(A)
        except:
            #Matrix is not invertible
            raise TypeError("Matrix should be invertible")

    if initial is None:
        # initial guess for eigen vector
        x = np.random.rand(n)
    else:
        x = initial.copy()
        x = x.astype(np.float32)

    # Relative approximate error between each iteration
    error = None
    # Eigen value calculated at previous iteration
    prevEigen = None

    # iterate to get eigen value/eigen vector
    # Stops after numberOfIterations or after error is less than epsilon
    # whichever comes first
    for i in range(numberOfIterations):
        x = np.dot(A, x)
        eigenValue = x[np.argmax(np.abs(x))]
        # If there isn't any left eigen values
        if eigenValue == 0:
            break
        x /= eigenValue
        if prevEigen is not None:

            # I believe it should be relative error, not relative approximate error
            # but doctor asked us to do it as relative approximate error, so I did it
            #error = abs(eigenValue-prevEigen)
            error = np.abs((eigenValue-prevEigen)/eigenValue)

            if (epsilon is not None) and (error <= epsilon):
                break
        prevEigen = eigenValue

    if(minEigen and eigenValue != 0):
        eigenValue = 1/eigenValue

    # Eigen Value, Eigen Vector, Relative approximate error
    return eigenValue, x, error

####################################################################################################################

def deflate(A, initial=None, epsilon=None, numberOfIterations=100, minEigen=False):
    """
    A function to calculate second largest eigen value and eigen vector of a matrix, and approximate relative error

    Args: 
            A (numpy array): Matrix to get eigen value/vector (size n*n)
            initial (numpy array): Vector used as initial guess of eigen vector (size 1*n)
            epsilon (float): Stopping criteria at which eigen value is considered converged
            numberOfIterations (int): Number of iterations untill stopping
            minEigen (boolean): Calculate smallest eigen value or largest

    Returns:
            deflatedMat (numpy array)
            eigenValue (numpy float)
            eigenVector (numpy array)
            error (numpy float)
    Raises:
            TypeError
            ValueError

    """
    
    #get largest eigen value for A
    eigenValue, eigenVector, error = powerMethod(A, initial, epsilon, numberOfIterations, minEigen)

    norm = np.linalg.norm(eigenVector)

    if(norm != 0):
        eigenVectorNormalized = eigenVector/norm
    else:
        eigenVectorNormalized = eigenVector

    if minEigen:
        try:
            A = np.linalg.inv(A)
        except:
            #Matrix is not invertible
            raise TypeError("Matrix should be invertible")

    # get deflated matrix (B = A - lambda.x*.x*T), where x* is normalized eigen vector
    deflatedMat = A-eigenValue*np.outer(eigenVectorNormalized, eigenVectorNormalized.T)

    # get largest eigen value for deflated matrix
    eigenValue, eigenVector, error = powerMethod(deflatedMat, initial, epsilon, numberOfIterations)

    if minEigen and eigenValue != 0:
        eigenValue = 1/eigenValue

    return deflatedMat, eigenValue, eigenVector, error