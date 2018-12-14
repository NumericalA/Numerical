
# coding: utf-8

# In[55]:


import numpy as np

#Calculating Permutation of A list. used to convert a matrix into a diagonally dominant one.
#by manipulating the order of the rows.
def permutation(lst): 
  
    if len(lst) == 0: 
        return [] 
  
    if len(lst) == 1: 
        return [lst] 
  
    l = [] 
    for i in range(len(lst)): 
        m = lst[i]
        remLst = lst[:i]+lst[i+1:]
        for p in permutation(remLst): 
               l.append([m] + p) 
    return l

#Checks if abs(A[i,i])> sum(Abs(A[i,j!=i])).
def CheckDiagDominant(mat):
    # Assuming a square matrix
    flag = True
    for i in range(mat.shape[0]):
        x = 2*np.abs(mat[i,i])
        y = np.sum(np.abs(mat[i,:]))
        if(x<=y):
            flag = False
            break
    return flag

#uses CheckDiagDominant and Permutation to get A diagonally dominant matrix.
def MakeItDiagDominant(mat):
    m,n = mat.shape
    if(m != n):
        print("Error : Not A Square Matrix.")
        return mat
    lst = []
    for i in range(n):
        lst.append(i)
    
    per = permutation(lst)
    flag = True
    
    w = len(per)
    temp = np.empty([n,m])
    for i in range(w):
        for j in range(n):
            temp[j] = mat[per[i][j]]
        if(CheckDiagDominant(temp)):
            return temp
            flag = False
            break
        if (not (flag)):
            break
    return mat


# In[61]:


# solving a linear system of equations using gauss seidel.
# mat : the coeffecients matrix.
# vec : the result vector.
# init : initial solution.
#epsilon : stopping criteria.
def SolveGaussSeidel(mat,vec,init,epsilon):
    error = np.zeros([mat.shape[0],1])
    print(error.shape)
    prev = np.copy(init)
    ddmat = MakeItDiagDominant(mat)
    #TODO : Add the Relation.
    # the Relation is R[i] = (v[i] - sigma(R[j]*A[j,j]))/A[i,i]
    # where A is the coeffecients matrix, v is the result vector and R is the solution vector
    maxError =  1000
    n = 5 
    while(n>0 and maxError > epsilon):
        for i in range(mat.shape[0]):
            x = vec[i]
            for j in range(mat.shape[1]):
                x -= (init[j]*ddmat[i,j])
            x+= init[i]*ddmat[i,i]
            x /= ddmat[i,i]
            init[i] = x
            error[i] = abs((init[i]-prev[i])/init[i])
            n -=1
        maxError = max(error)
        prev = init
    return init,maxError

# solving a linear system of equations using successive over relaxation.
# mat : the coeffecients matrix.
# vec : the result vector.
#init : initial solution.
#omega : relaxation factor.
#epsilon : stopping criteria.
def SolveSOR(mat,vec,init,omega,epsilon):
    error = np.zeros(mat.shape[0])
    print(error.shape)
    prev = np.copy(init)

    ddmat = MakeItDiagDominant(mat)
    
    n = 5
    maxError = 10000
    #TODO : Add the Relation.
    # the Relation is R[i] = (v[i] - sigma(R[j]*A[j,j]))/A[i,i]
    # where A is the coeffecients matrix, v is the result vector and R is the solution vector
    while(n>0 and maxError > epsilon):
        for i in range(mat.shape[0]):
            x = vec[i]
            for j in range(mat.shape[1]):
                x -= (init[j]*ddmat[i,j])
            x+= init[i]*ddmat[i,i]
            x*= omega
           
            x /= ddmat[i,i]
            x += (1-omega)*init[i]
            
            init[i] = x
            error[i] = abs((init[i]-prev[i])/init[i])
            n -=1
        maxError = max(error)
        prev = init   
    return init,maxError





# In[64]:


#TESTING.
mat = np.array([[9,2,1],[1,7,3],[1,1,8]])
vec = np.array([12,11,11])

epsilon = 0.1
init= np.array([1.2,1.2,1.2])
result,error= SolveSOR(mat,vec,init,1.0,epsilon)
print(result)
print(error)

