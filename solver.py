# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:44:14 2024

@author: alsip
"""
import numpy as np
from sympy import symbols,diff,exp,sin,pi,Function
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

#fonctions


def solver(data):
    #Pour les tracer
    Results=[]
    #pour les boucles
    t=0
    #Constante de la matrice
    alpha = 1 +3*data.Deff*data.unsurdx**2*data.dt
    beta = -2*data.Deff*data.unsurdx**2*data.dt
    delta = -1*data.Deff*data.unsurdx**2*data.dt
    
    #Initialisation
    gamma0=np.zeros((5,1))
    gamma0[4][0]=data.Ce
    Results.append(gamma0)
    
    unit=np.ones((5,1))
    #Configuration de A cas constant
    
    A=np.zeros((5,5))
    A[4][4]=1
    A[0][0]=-3
    A[0][1]=4
    A[0][2]=-1
    
    for i in range (1,4):
        A[i][i-1]=beta
        A[i][i]=alpha
        A[i][i+1]=delta
        
    invA=np.linalg.inv(A)
    
    #Cas constante
    if data.const == True:
        while t<data.itermax:
            t+=1
            gamma0=np.dot(invA,gamma0)-data.S*data.dt*np.dot(invA,unit)
            Results.append(gamma0)
    
    #Cas non constante
    if data.const != True:
        invA=np.linalg.inv(A-data.k*data.dt*np.eye(5))
        while t<data.itermax:
            gamma0=np.dot(invA,gamma0)
            Results.append(gamma0)
        

    return Results