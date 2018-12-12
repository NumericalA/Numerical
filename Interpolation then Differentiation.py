import numpy as np
import os.path
import sys

x = []
y = []


def newtonGeneral(workingList, workingListInv, value):
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

    polynomialSum = newWorkingListInv[0]
    for i in range(2, len(dividedDifferenceTable)):
        polynomialSum += (dividedDifferenceTable[i][0]) * np.prod(
            np.array([value - newWorkingList[k] for k in range(0, i - 1)])
        )

    return polynomialSum


def differentiate(value, p, isX):
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

    h = 0.00000001

    # Second Formula for Central Difference O(h^4)
    derivative = (8*newtonGeneral(workingList, workingListInv, value + h) -
                  newtonGeneral(workingList, workingListInv, value + 2*h) -
                  8*newtonGeneral(workingList, workingListInv, value - h) +
                  newtonGeneral(workingList, workingListInv, value - 2*h)) / (12 * h)

    # Final answer
    derivative = "{:.{n}f}".format(derivative, n = p)
    print("F`({0}) = {1}".format(notation, derivative))


def execute():

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

    print("Enter number of decimal places")
    per = input()

    differentiate(float(value), int(per), True)


def main():
    execute()


if __name__ == '__main__':
    main()
