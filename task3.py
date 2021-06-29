import csv
import numpy as np 
from matplotlib import pyplot

var = 100
P_ = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]], dtype = float)
I4 = np.identity(4)
t = 1

#R = np.array([[10,0,0,0],[0,10,0,0],[0,0,20,0], [0,0,0,20]], dtype = float)
R = np.array([[0.001,0,0,0],[0,0.001,0,0],[0,0,0.001,0],[0,0,0,0.001]],dtype=float)

A = np.array([[1,0,t,0],[0,1,0,t],[0,0,1,0],[0,0,0,1]], dtype = int)


Xpts_ = []
Xpts = []
Ypts = []
Ypts_ = []



with open('kalmann.txt') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    c = 0
    for row in csvReader:
        if c <= 1:
            if c==1:
                X_ = np.array([[row[0]], [row[1]], [row[2]], [row[3]]], dtype = float)
            else:
                X_ = np.array([[row[0]], [row[1]]], dtype = float)
            c = c+1
            Xpts.append(X_[0][0])
            Xpts_.append(X_[0][0])
            Ypts.append(X_[1][0])
            Ypts_.append(X_[1][0])
            
        else:
            X = np.array([[row[0]], [row[1]], [row[2]], [row[3]]], dtype = float)
            Xpts.append(X[0][0])
            Ypts.append(X[1][0])
            Xest = A@(X_)
            if c==2:
                P_[0][0] = abs(Xpts[0] - Xpts[1])
                P_[1][1] = abs(Ypts[0] - Ypts[1])
                P_[2][2] = abs(X_[2][0])
                P_[3][3] = abs(X_[3][0])
            P = (A@P_)@A.transpose()
            J = P + R
            K = []
            for i in range(4):  #evaluating the kalmann gain
                K.append([])
                for j in range(4):
                    if i != j:
                        K[i].append(0)
                    else:
                        K[i].append(P[i][i]/J[i][i])
            K = np.asarray(K)
            P_ = (I4 - K)@P  #calculate new P
            M = K@(X - Xest)
            X_ = Xest + M  #update estimation
            Xpts_.append(X_[0][0]) 
            Ypts_.append(X_[1][0])
            c = c+1



pyplot.plot(Xpts_,Ypts_, 'g')
pyplot.plot(Xpts,Ypts,'r' )
pyplot.legend(["Predicted path", "Measured path"])
pyplot.show()


