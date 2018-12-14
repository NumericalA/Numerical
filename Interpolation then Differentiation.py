'''Number of Inputs (5) :
- X's of each point (X list)
- Y's of each point (Y list)
- Value of X you want the Derivative at
- Order of Approximation : Number of terms used in Approximation (Stopping Criteria)
- Approx.Error : Stop when error is less than Approx.Error(Stopping Criteria)

Number of Outputs (2):
- The result F'(X) (The Derivative at X)
- Approximation Error of the Derivative
'''

import numpy as np
import os.path
import sys

x = []
y = []


def newtonGeneral(workingList, workingListInv, value, order, ApproxError = 1e-8):
    # sort the array with respect to the minimum difference
    newWorkingList = []
    newWorkingListInv = []
    visited = [False] * (len(workingList))
    workingList.reverse()
    workingListInv.reverse()

    for i in range(len(workingList)):
        minimum = np.inf
        minimumValIdx = 0
        for j in range(len(workingList)):
            lastMin = minimum
            minimum = min(minimum, abs(value - workingList[j]))
            if visited[j]:
                minimum = lastMin
            else:
                if minimum < lastMin:
                    minimumValIdx = j

        visited[minimumValIdx] = True
        if len(newWorkingList) != len(workingList):
            newWorkingList += [workingList[minimumValIdx]]
            newWorkingListInv += [workingListInv[minimumValIdx]]

    dividedDifferenceTable = [newWorkingList, newWorkingListInv]

    for i in range(2, len(newWorkingList) + 1):
        dividedDifferenceTable.append(
            [
                (dividedDifferenceTable[i - 1][k + 1] - dividedDifferenceTable[i - 1][k]) /
                (newWorkingList[k + i - 1] - newWorkingList[k])
                for k in range(len(dividedDifferenceTable[i - 1]) - 1)
            ])

    error = 0
    done = False
    lastterm = -1
    derivative = 0
    for i in range(order):
        dividedDifferenceVal = dividedDifferenceTable[i+2][0]
        sum = 0
        for j in range(i+1):
            Diff = 1
            for k in range(i+1):
                if k != j:
                    Diff *= value - dividedDifferenceTable[0][k]
            sum += Diff
        derivative += sum * dividedDifferenceVal

        if lastterm != -1:
            appErr = abs(derivative - lastterm)/derivative
            appErr = abs(appErr)
            if appErr < ApproxError:
                error = appErr
                done = True
                break
        lastterm = derivative

    if (order < len(x) - 1) and (not done):
        dividedDifferenceVal = dividedDifferenceTable[order+2][0]
        sum = 0
        for j in range(order+1):
            Diff = 1
            for k in range(order+1):
                if k != j:
                    Diff *= value - dividedDifferenceTable[0][k]
            sum += Diff
        error += sum * dividedDifferenceVal

# --------------------Outputs-------------------------
    derivative = "{:.{n}f}".format(derivative, n=5)
    print("F`({0}) = {1}".format("x", derivative))
    error = "{:.{n}f}".format(error, n=5)
    error = abs(float(error))
    print("Error = {0} ".format(error))
# ----------------------------------------------------


def differentiate(value, isX, order, AppErr):
    global x, y
    if isX:
        workingList = x.copy()
        workingListInv = y.copy()
        notation = "x"
        notationInv = "y"
    else:
        workingList = y.copy()
        workingListInv = x.copy()
        notation = "y"
        notationInv = "x"

    newtonGeneral(workingList, workingListInv, value, order, AppErr)


def execute():

#---------Inputs----------------------------------
'''
    n = input("Enter number of points : ")
    print("Enter X's : ")
    for i in range(int(n)):
        val = input()
        x.append(float(val))
    print("Enter Y's : ")
    for i in range(int(n)):
        val = input()
        y.append(float(val))

    # Value of x to find Derivative at
    print("Enter Value of X you want Derivative at : ")
    value = input("Getting F`(x) at x = ")

    # Order of Approx. (number of terms used)
    print("Enter Order of Approximation ")
    order = input()

    # Order of Approx. (number of terms used)
    print("Approximation Error for Stopping Criteria ")
    Apperr = input()
'''
#--------------------------------------------------------------------

    if order >= n:
        raise ValueError("Order should be < number of points")

    differentiate(float(value), True, int(order), float(Apperr))


def main():
    execute()


if __name__ == '__main__':
    main()
